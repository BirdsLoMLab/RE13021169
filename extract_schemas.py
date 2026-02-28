#!/usr/bin/env python3
"""
LOM Config Schema Extractor
Parses game_script_pretty.js to extract all Config module schemas.

Each Config module defines a class with getter properties that map array indices
to named fields. This script extracts those mappings along with type information.
"""

import re
import json
import os
import sys

GAME_SCRIPT = "game_script_pretty.js"
OUTPUT_DIR = "data/schemas"

# CONFIG_KEY used for XOR deobfuscation
CONFIG_KEY = 24455


def extract_config_blocks(content):
    """Find all System.register blocks for Config*.ts modules."""
    # Match the start of each Config module registration
    pattern = re.compile(
        r'System\.register\("chunks:///_virtual/(Config[A-Za-z_0-9]+)\.ts".*?\n\}\)\);',
        re.DOTALL
    )
    blocks = []
    for match in pattern.finditer(content):
        config_name = match.group(1)
        block_text = match.group(0)
        start_pos = match.start()
        # Calculate line number
        line_num = content[:start_pos].count('\n') + 1
        blocks.append({
            'name': config_name,
            'text': block_text,
            'line': line_num,
        })
    return blocks


def extract_fields(block_text, config_name):
    """Extract field definitions from a Config block."""
    fields = []

    # Pattern for field getter: key: "field_name" followed by return this._data[N]
    # Handle multiple patterns:
    # 1. Simple: return this._data[N]
    # 2. XOR: return this._data[N] ^ a  (where a = CONFIG_KEY)
    # 3. BigNumber: return BigNumber(this._data[N]).toNumber()
    # 4. String: return GetStrFromConfig(this._data[N])
    # 5. Optional: return null != (t = this._data[N]) ? t : LNIL

    # Find all key-getter pairs
    key_pattern = re.compile(
        r'key:\s*"([a-zA-Z_][a-zA-Z0-9_]*)".*?'
        r'get:\s*function\(\)\s*\{(.*?)\}',
        re.DOTALL
    )

    for match in key_pattern.finditer(block_text):
        field_name = match.group(1)
        getter_body = match.group(2).strip()

        field_info = {
            'name': field_name,
            'index': None,
            'type': 'raw',
            'xor': False,
            'optional': False,
        }

        # Extract array index
        idx_match = re.search(r'this\._data\[(\d+)\]', getter_body)
        if idx_match:
            field_info['index'] = int(idx_match.group(1))
        else:
            continue  # Skip if no _data access

        # Detect type
        if 'GetStrFromConfig' in getter_body:
            field_info['type'] = 'string_ref'
        elif 'BigNumber' in getter_body:
            field_info['type'] = 'bignum'
        elif re.search(r'\^\s*[a-z](?:\s*\)|\s*$|\s*\n)', getter_body):
            field_info['type'] = 'xor_number'
            field_info['xor'] = True
        elif 'LNIL' in getter_body:
            field_info['type'] = 'optional_array'
            field_info['optional'] = True
        elif 'null !=' in getter_body and 'LNIL' not in getter_body:
            field_info['type'] = 'optional'
            field_info['optional'] = True
        else:
            field_info['type'] = 'number'

        fields.append(field_info)

    return fields


def extract_table_metadata(block_text):
    """Extract table name, mainKey, and indexed keys."""
    metadata = {
        'tableName': None,
        'mainKey': None,
        'indexedKeys': {},
    }

    # Extract table name: this.name = "TableName"  or  n.name = "TableName"
    name_match = re.search(r'\.name\s*=\s*"([^"]+)"', block_text)
    if name_match:
        metadata['tableName'] = name_match.group(1)

    # Extract mainKey: this.mainKey = "fieldName"  or  n.mainKey = "fieldName"
    mainkey_match = re.search(r'\.mainKey\s*=\s*"([^"]+)"', block_text)
    if mainkey_match:
        metadata['mainKey'] = mainkey_match.group(1)

    # Extract indexed keys: n.keys = ((e = {}).id = 0, e.module = 4, e.group = 5, e), n
    # Match everything between (( and the final single-letter var before ))
    keys_match = re.search(r'\.keys\s*=\s*\(\((.+?),\s*\w+\)', block_text)
    if keys_match:
        keys_str = keys_match.group(1)
        # Parse key-value pairs: t.fieldName = N
        for kv_match in re.finditer(r'\.(\w+)\s*=\s*(\d+)', keys_str):
            metadata['indexedKeys'][kv_match.group(1)] = int(kv_match.group(2))

    return metadata


def detect_config_key_usage(block_text):
    """Check if this config module imports CONFIG_KEY."""
    return 'CONFIG_KEY' in block_text


def process_config_block(block):
    """Process a single Config block into a schema definition."""
    fields = extract_fields(block['text'], block['name'])
    metadata = extract_table_metadata(block['text'])
    uses_config_key = detect_config_key_usage(block['text'])

    schema = {
        'className': block['name'],
        'tableName': metadata['tableName'],
        'sourceLine': block['line'],
        'mainKey': metadata['mainKey'],
        'indexedKeys': metadata['indexedKeys'],
        'usesConfigKey': uses_config_key,
        'fieldCount': len(fields),
        'fields': fields,
    }

    return schema


def main():
    print(f"Reading {GAME_SCRIPT}...")
    with open(GAME_SCRIPT, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Extracting Config module blocks...")
    blocks = extract_config_blocks(content)
    print(f"Found {len(blocks)} Config modules")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    index = []
    schemas = {}

    for block in blocks:
        schema = process_config_block(block)

        # Save individual schema file
        filename = f"{block['name']}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2)

        schemas[block['name']] = schema
        index.append({
            'className': block['name'],
            'tableName': schema['tableName'],
            'sourceLine': schema['sourceLine'],
            'mainKey': schema['mainKey'],
            'fieldCount': schema['fieldCount'],
            'usesConfigKey': schema['usesConfigKey'],
        })

    # Save master index
    index_path = os.path.join(OUTPUT_DIR, '_index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump({
            'totalConfigs': len(index),
            'configKey': CONFIG_KEY,
            'sourceFile': GAME_SCRIPT,
            'configs': sorted(index, key=lambda x: x['className']),
        }, f, indent=2)

    print(f"\nExtracted {len(index)} schemas to {OUTPUT_DIR}/")
    print(f"Master index: {index_path}")

    # Print summary statistics
    xor_count = sum(1 for s in schemas.values() if s['usesConfigKey'])
    total_fields = sum(s['fieldCount'] for s in schemas.values())
    print(f"Total fields across all schemas: {total_fields}")
    print(f"Schemas using CONFIG_KEY XOR: {xor_count}")

    return schemas


if __name__ == '__main__':
    main()
