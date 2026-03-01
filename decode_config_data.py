#!/usr/bin/env python3
"""
decode_config_data.py — Decode binary config tables from bundle-firstload-res.

Reads the config/datas binary blob (12MB+) from a game capture and decodes
all 908 config tables into named-field JSON files.

Pipeline per table:
  1. XOR decrypt: byte = 255 & ~(32 ^ byte)
  2. Zlib decompress
  3. Parse records: count(4B BE) + [str_len(2B BE) + JSON_string] × count
  4. Map positional arrays to named fields using schemas
  5. De-XOR protected numeric fields: value ^ CONFIG_KEY(24455)

Usage:
  python3 decode_config_data.py uploads/20260228
  python3 decode_config_data.py uploads/20260228 --output data/tables
"""

import argparse
import glob
import json
import os
import struct
import sys
import zlib

CONFIG_KEY = 24455


def find_config_binary(base_path):
    """Locate the config/datas .bin file inside a capture directory."""
    # Standard path inside bundle-firstload-res
    patterns = [
        os.path.join(base_path, "**", "bundle-firstload-res", "native", "**", "*.bin"),
        os.path.join(base_path, "native", "c8", "*.bin"),
        os.path.join(base_path, "**", "*.8e8a4.bin"),
    ]
    for pattern in patterns:
        matches = glob.glob(pattern, recursive=True)
        if matches:
            return matches[0]
    return None


def find_proto_json(base_path):
    """Locate the config/proto JSON asset inside a capture directory."""
    patterns = [
        os.path.join(base_path, "**", "bundle-firstload-res", "import", "38", "*.json"),
        os.path.join(base_path, "import", "38", "*.json"),
        os.path.join(base_path, "**", "*.ceb0d.json"),
    ]
    for pattern in patterns:
        matches = glob.glob(pattern, recursive=True)
        for m in matches:
            size = os.path.getsize(m)
            if size > 100000:  # Proto JSON is ~500KB
                return m
    return None


def parse_filepack(data):
    """Parse the FilePack binary format into table name → raw data mapping."""
    version = struct.unpack(">H", data[0:2])[0]
    table_count = struct.unpack(">H", data[2:4])[0]

    tables = {}
    pos = 4
    for _ in range(table_count):
        name_len = struct.unpack(">H", data[pos : pos + 2])[0]
        pos += 2
        name = data[pos : pos + name_len].decode("utf-8")
        pos += name_len
        data_len = struct.unpack(">I", data[pos : pos + 4])[0]
        pos += 4
        tables[name] = data[pos : pos + data_len]
        pos += data_len

    return version, tables


def decrypt_and_decompress(raw_data):
    """XOR decrypt and zlib decompress a table's raw data."""
    buf = bytearray(raw_data)
    for j in range(len(buf)):
        buf[j] = 255 & ~(32 ^ buf[j])
    return zlib.decompress(bytes(buf))


def parse_records(decompressed):
    """Parse decompressed data into list of JSON-parsed records."""
    pos = 0
    count = struct.unpack(">I", decompressed[pos : pos + 4])[0]
    pos += 4
    records = []
    for _ in range(count):
        str_len = struct.unpack(">H", decompressed[pos : pos + 2])[0]
        pos += 2
        s = decompressed[pos : pos + str_len].decode("utf-8")
        pos += str_len
        records.append(json.loads(s))
    return records


def load_schema(schema_dir, table_name):
    """Load the schema for a table, trying Config{Name} naming convention."""
    candidates = [
        f"Config{table_name}.json",
        f"Config{table_name.lower()}.json",
        f"Config{table_name.replace('_', '')}.json",
    ]
    for candidate in candidates:
        path = os.path.join(schema_dir, candidate)
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
    return None


def apply_schema(records, schema):
    """Map positional arrays to named-field dicts using schema, de-XOR protected fields."""
    fields = schema.get("fields", [])
    if not fields:
        return records

    named_records = []
    for record in records:
        if not isinstance(record, list):
            named_records.append(record)
            continue

        obj = {}
        for i, field in enumerate(fields):
            if i < len(record):
                val = record[i]
                # De-XOR protected numeric fields
                if field.get("xor") and isinstance(val, (int, float)) and not isinstance(val, bool):
                    val = int(val) ^ CONFIG_KEY
                obj[field["name"]] = val

        # Include any extra positional values beyond schema
        if len(record) > len(fields):
            obj["_extra"] = record[len(fields) :]

        named_records.append(obj)

    return named_records


def extract_proto_schema(proto_path):
    """Extract the protobuf schema from the Cocos Creator JSON asset."""
    with open(proto_path) as f:
        data = json.load(f)
    # Element [5][0][2] contains the proto JSON definition
    return data[5][0][2]


def main():
    parser = argparse.ArgumentParser(description="Decode binary config tables from game capture")
    parser.add_argument("input_path", help="Path to capture directory (e.g., uploads/20260228)")
    parser.add_argument("--output", default="data/tables", help="Output directory for decoded tables (default: data/tables)")
    parser.add_argument("--schema-dir", default="data/schemas", help="Directory with Config*.json schema files")
    parser.add_argument("--proto-output", default="data/proto_schema.json", help="Output path for proto schema")
    args = parser.parse_args()

    # Find the config binary
    bin_path = find_config_binary(args.input_path)
    if not bin_path:
        print(f"ERROR: Could not find config/datas binary in {args.input_path}")
        sys.exit(1)
    print(f"Config binary: {bin_path} ({os.path.getsize(bin_path):,} bytes)")

    # Read and parse FilePack
    with open(bin_path, "rb") as f:
        data = f.read()

    version, raw_tables = parse_filepack(data)
    print(f"FilePack v{version}: {len(raw_tables)} tables")

    # Load schemas
    schema_dir = os.path.abspath(args.schema_dir)
    schema_count = 0

    # Create output directory
    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    # Decode all tables
    index = {}
    success = 0
    errors = 0
    total_records = 0

    for table_name in sorted(raw_tables.keys()):
        try:
            decompressed = decrypt_and_decompress(raw_tables[table_name])
            records = parse_records(decompressed)

            # Try to apply schema
            schema = load_schema(schema_dir, table_name)
            if schema:
                named_records = apply_schema(records, schema)
                schema_count += 1
            else:
                named_records = records

            # Write output
            out_path = os.path.join(output_dir, f"{table_name}.json")
            with open(out_path, "w") as f:
                json.dump(named_records, f, ensure_ascii=False, separators=(",", ":"))

            index[table_name] = {
                "records": len(records),
                "raw_bytes": len(raw_tables[table_name]),
                "has_schema": schema is not None,
            }
            total_records += len(records)
            success += 1

        except Exception as e:
            print(f"  ERROR decoding {table_name}: {e}")
            errors += 1

    # Write index
    index_path = os.path.join(output_dir, "_index.json")
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"\nDecoded {success}/{success + errors} tables ({total_records:,} total records)")
    print(f"Schema-mapped: {schema_count} tables")
    print(f"Output: {output_dir}/")

    # Extract proto schema
    proto_path = find_proto_json(args.input_path)
    if proto_path:
        proto_schema = extract_proto_schema(proto_path)
        proto_output = os.path.abspath(args.proto_output)
        os.makedirs(os.path.dirname(proto_output), exist_ok=True)
        with open(proto_output, "w") as f:
            json.dump(proto_schema, f, indent=2, ensure_ascii=False)
        ns_count = len(proto_schema.get("nested", {}))
        print(f"Proto schema: {ns_count} namespaces → {proto_output}")
    else:
        print("WARNING: Proto JSON not found")


if __name__ == "__main__":
    main()
