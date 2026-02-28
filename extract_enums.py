#!/usr/bin/env python3
"""
Extract ALL enum definitions from the LOM game script (game_script_pretty.js)
and save them as individual JSON files in data/enums/.

Handles multiple patterns:
  A) IIFE pattern: function(e){ e[e.X=N]="X"; ... }(VAR || (VAR = e("EnumName", {})))
  B) Direct object export: e("EnumName", { Key: Value, Key2: Value2, ... })
  C) UnitConfig constants: d.KEY = VALUE (string and numeric)
  D) AttribDefine (same as pattern A but in MetaAttrib.ts block)
"""

import re
import json
import os
from collections import OrderedDict

SCRIPT_PATH = "/home/user/RE13021169/game_script_pretty.js"
OUTPUT_DIR = "/home/user/RE13021169/data/enums/"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_enum(name, values, source_line):
    """Save an enum as a JSON file with forward and reverse maps."""
    # Build the reverse map (value -> name)
    reverse_map = {}
    for k, v in values.items():
        str_v = str(v)
        # If multiple names map to the same value, keep the first one
        # (or overwrite - both are valid, we keep last to match JS behavior)
        reverse_map[str_v] = k

    data = {
        "name": name,
        "sourceLine": source_line,
        "values": values,
        "reverseMap": reverse_map,
    }

    filename = os.path.join(OUTPUT_DIR, f"{name}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Saved {filename} ({len(values)} entries)")
    return filename


def extract_iife_enum_values(block_text):
    """
    Extract values from an IIFE enum block like:
      e[e.Born = 0] = "Born", e[e.Idle = 1] = "Idle"
    Returns OrderedDict of {name: value}
    """
    values = OrderedDict()
    # Match e[e.NAME = VALUE] = "NAME"
    pattern = r'e\[e\.(\w+)\s*=\s*(-?\d+)\]\s*=\s*"(\w+)"'
    for m in re.finditer(pattern, block_text):
        name = m.group(1)
        val = int(m.group(2))
        values[name] = val
    return values


def extract_object_literal_values(block_text):
    """
    Extract values from an object literal like:
      { Key: 0, Key2: 1, ... }
    Returns OrderedDict of {name: value}
    """
    values = OrderedDict()
    # Match Key: NumericValue patterns
    pattern = r'(\w+)\s*:\s*(-?\d+)'
    for m in re.finditer(pattern, block_text):
        name = m.group(1)
        val = int(m.group(2))
        values[name] = val
    return values


def find_matching_brace(text, start):
    """Find the position of the matching closing brace for the opening brace at 'start'."""
    depth = 0
    i = start
    while i < len(text):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def find_matching_paren(text, start):
    """Find the position of the matching closing paren for the opening paren at 'start'."""
    depth = 0
    i = start
    while i < len(text):
        if text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def get_line_number(text, pos):
    """Get 1-based line number for a character position."""
    return text[:pos].count('\n') + 1


def main():
    print(f"Reading {SCRIPT_PATH}...")
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Also read as lines for line-number lookups
    lines = content.split('\n')

    all_enums = {}  # name -> (values, source_line)

    # =========================================================================
    # PATTERN A: IIFE enum pattern
    # function(e){ e[e.X=N]="X"; ... }(VAR || (VAR = e("EnumName", {})))
    # =========================================================================
    print("\n--- Pattern A: IIFE enum blocks ---")

    # Find all occurrences of: e("EnumName", {})
    # These appear at the end of IIFE blocks
    # Pattern: }(VAR || (VAR = e("EnumName", {})))
    iife_pattern = re.compile(
        r'\}\s*\(\s*\w+\s*\|\|\s*\(\s*\w+\s*=\s*e\(\s*"(\w+)"\s*,\s*\{?\s*\}?\s*\)\s*\)\s*\)'
    )

    for m in iife_pattern.finditer(content):
        enum_name = m.group(1)
        end_pos = m.end()

        # Walk backwards from the closing } to find the function(e){ start
        brace_close_pos = m.start()  # This is approximately at the }

        # Find the function body: search backwards for "function(e)" or "function (e)"
        # We need to find the function block that contains e[e.X = N] patterns
        search_start = max(0, brace_close_pos - 5000)
        preceding = content[search_start:brace_close_pos + 1]

        # Find the last "function(e)" or "function (e)" before the closing
        func_matches = list(re.finditer(r'function\s*\(\s*e\s*\)\s*\{', preceding))
        if func_matches:
            last_func = func_matches[-1]
            func_body_start = search_start + last_func.end()
            # The body extends to the closing brace
            func_body = content[func_body_start:brace_close_pos]

            values = extract_iife_enum_values(func_body)
            if values:
                line_num = get_line_number(content, m.start())
                all_enums[enum_name] = (dict(values), line_num)
                print(f"  Found IIFE enum: {enum_name} with {len(values)} values (line {line_num})")

    # =========================================================================
    # PATTERN B: Direct object literal exports
    # e("EnumName", { Key: Value, ... })  OR  var X = e("EnumName", { Key: Value, ... })
    # =========================================================================
    print("\n--- Pattern B: Direct object literal exports ---")

    # Find e("EnumName", { ... })
    obj_export_pattern = re.compile(r'e\(\s*"(\w+)"\s*,\s*\{')

    for m in obj_export_pattern.finditer(content):
        enum_name = m.group(1)
        brace_start = m.end() - 1  # Position of the opening {
        brace_end = find_matching_brace(content, brace_start)
        if brace_end == -1:
            continue

        obj_text = content[brace_start:brace_end + 1]

        # Skip if this is an empty {} (used in IIFE pattern)
        if obj_text.strip() == '{}':
            continue

        # Skip if this is not an enum-like object (contains functions, complex nesting, etc.)
        # Enum objects should mainly have Key: NumericValue pairs
        values = extract_object_literal_values(obj_text)

        if values and len(values) >= 1:
            # Verify it's actually an enum (all values should be numbers)
            # Already guaranteed by the regex
            line_num = get_line_number(content, m.start())

            # Don't overwrite IIFE enums which are more accurate
            if enum_name not in all_enums:
                all_enums[enum_name] = (dict(values), line_num)
                print(f"  Found object export enum: {enum_name} with {len(values)} values (line {line_num})")
            else:
                # Merge: IIFE values take precedence, but object literal may have initial values
                existing_vals, existing_line = all_enums[enum_name]
                for k, v in values.items():
                    if k not in existing_vals:
                        existing_vals[k] = v
                all_enums[enum_name] = (existing_vals, existing_line)
                if len(values) > 0:
                    print(f"  Merged object literal values into IIFE enum: {enum_name}")

    # =========================================================================
    # PATTERN C: Inline assignment pattern for non-IIFE enums
    # e("EnumName", ((VAR = {}).key = val, VAR.key2 = val2, VAR))
    # or e("BindType", ((_ = {}).bp_lead = 1, _.bp_bottom = 2, ...))
    # =========================================================================
    print("\n--- Pattern C: Inline assignment pattern ---")

    # Pattern: e("EnumName", ((_ = {}).key = val, ... , _))
    inline_pattern = re.compile(r'e\(\s*"(\w+)"\s*,\s*\(\s*\(\s*(\w+)\s*=\s*\{\s*\}\s*\)')

    for m in inline_pattern.finditer(content):
        enum_name = m.group(1)
        var_name = m.group(2)

        # Find the enclosing e(...) call
        paren_start_pos = content.rfind('e(', max(0, m.start() - 5), m.start() + 3)
        if paren_start_pos == -1:
            paren_start_pos = m.start()

        # Find the matching closing paren
        # We need to find from the 'e('
        first_paren = content.index('(', paren_start_pos)
        paren_end = find_matching_paren(content, first_paren)
        if paren_end == -1:
            continue

        block_text = content[m.start():paren_end + 1]

        # Extract VAR.key = value patterns
        # Also handle the first entry which appears as {}).key = val
        values = OrderedDict()
        # Match both {}).key = val and VAR.key = val
        assign_pattern = re.compile(
            r'(?:' + re.escape(var_name) + r'|\})\s*\)\s*\.(\w+)\s*=\s*(-?\d+)'
            r'|' + re.escape(var_name) + r'\.(\w+)\s*=\s*(-?\d+)'
        )
        for am in assign_pattern.finditer(block_text):
            if am.group(1) is not None:
                key = am.group(1)
                val = int(am.group(2))
            else:
                key = am.group(3)
                val = int(am.group(4))
            values[key] = val

        if values and enum_name not in all_enums:
            line_num = get_line_number(content, m.start())
            all_enums[enum_name] = (dict(values), line_num)
            print(f"  Found inline assignment enum: {enum_name} with {len(values)} values (line {line_num})")

    # =========================================================================
    # PATTERN D: UnitConfig constants
    # d.KEY = VALUE (where d is the UnitConfig export)
    # =========================================================================
    print("\n--- Pattern D: UnitConfig constants ---")

    # Find the UnitConfig definition
    unitconfig_match = re.search(r'e\(\s*"UnitConfig"\s*,', content)
    if unitconfig_match:
        # Read the block around it
        uc_start = unitconfig_match.start()
        uc_line = get_line_number(content, uc_start)

        # Find the line containing UnitConfig definition
        line_start = content.rfind('\n', 0, uc_start) + 1
        # Read forward to find all d.KEY = VALUE assignments
        # They typically appear on the same or next few lines
        search_end = min(len(content), uc_start + 3000)
        uc_block = content[line_start:search_end]

        # First, figure out what variable name is used for UnitConfig
        # Pattern: var d = e("UnitConfig", ...)  or  e("UnitConfig", ...)
        var_match = re.search(r'(\w+)\s*=\s*e\(\s*"UnitConfig"', uc_block)
        if var_match:
            uc_var = var_match.group(1)

            # Now extract all assignments: d.KEY = VALUE or d.KEY = "STRING"
            values_str = OrderedDict()
            values_num = OrderedDict()

            assign_pat = re.compile(re.escape(uc_var) + r'\.(\w+)\s*=\s*("([^"]+)"|(-?\d+))')
            for am in assign_pat.finditer(uc_block):
                key = am.group(1)
                if am.group(3) is not None:
                    # String value
                    values_str[key] = am.group(3)
                elif am.group(4) is not None:
                    # Numeric value
                    values_num[key] = int(am.group(4))

            # Save UnitConfig with all values (strings and numbers)
            all_values = OrderedDict()
            for k, v in values_str.items():
                all_values[k] = v
            for k, v in values_num.items():
                all_values[k] = v

            if all_values:
                all_enums["UnitConfig"] = (dict(all_values), uc_line)
                print(f"  Found UnitConfig with {len(all_values)} constants (line {uc_line})")

    # =========================================================================
    # PATTERN E: Broader search for any e[e.X = N] = "X" blocks with named exports
    # that might have been missed. Also look in other System.register blocks.
    # =========================================================================
    print("\n--- Pattern E: Broader IIFE search (non-named, local enums) ---")

    # Find all function(e){ e[e.X = N] = "X" } blocks that are NOT captured above
    # These might be unnamed/local enums in other files
    # We look for function(t){ t[t.X = N] = "X" } as well (different parameter names)

    for param_name in ['e', 't', 'i', 'n']:
        p = re.escape(param_name)
        # Find function(X){ X[X.Name = val] = "Name" patterns
        func_pattern = re.compile(
            r'function\s*\(\s*' + p + r'\s*\)\s*\{([^}]*' + p + r'\[' + p + r'\.\w+\s*=\s*-?\d+\][^}]*)\}'
        )
        for fm in func_pattern.finditer(content):
            body = fm.group(1)
            # Extract the enum name from the trailing: (VAR || (VAR = e("NAME", {})))
            # or (VAR || (VAR = {}))  -- unnamed
            after_brace = content[fm.end():fm.end() + 200]
            name_match = re.search(r'\(\s*\w+\s*=\s*\w+\(\s*"(\w+)"', after_brace)

            if name_match:
                ename = name_match.group(1)
                if ename in all_enums:
                    continue  # Already captured
            else:
                # Try to find unnamed enum: (VAR || (VAR = {}))
                # These are local enums, skip unless we can find a name
                continue

            # Extract values
            val_pattern = re.compile(p + r'\[' + p + r'\.(\w+)\s*=\s*(-?\d+)\]\s*=\s*"(\w+)"')
            values = OrderedDict()
            for vm in val_pattern.finditer(body):
                values[vm.group(1)] = int(vm.group(2))

            if values and ename not in all_enums:
                line_num = get_line_number(content, fm.start())
                all_enums[ename] = (dict(values), line_num)
                print(f"  Found additional enum: {ename} with {len(values)} values (line {line_num})")

    # =========================================================================
    # PATTERN F: Search for more e("NAME", {key:val}) patterns with arrays
    # like e("NeedAddDamHurtList", [...]) - skip arrays but note them
    # Also search for e("EnumName", VAR) where VAR was previously assigned
    # =========================================================================
    print("\n--- Pattern F: Additional named exports ---")

    # Already handled via Pattern B. Let's check for any we missed.
    named_export_pattern = re.compile(r'e\(\s*"(\w+)"\s*,')
    seen_names = set(all_enums.keys())

    for m in named_export_pattern.finditer(content):
        ename = m.group(1)
        if ename in seen_names:
            continue
        seen_names.add(ename)

        # Look at what follows
        after = content[m.end():m.end() + 500]

        # Skip arrays
        if after.lstrip().startswith('['):
            continue

        # Skip function definitions and class exports
        if after.lstrip().startswith('function') or after.lstrip().startswith('void 0'):
            continue

        # Skip string values
        first_char = after.lstrip()[0] if after.lstrip() else ''
        if first_char == '"' or first_char == "'":
            continue

        # Check if it's an object literal with numeric values
        if after.lstrip().startswith('{'):
            brace_start = m.end() + after.index('{')
            brace_end = find_matching_brace(content, brace_start)
            if brace_end != -1:
                obj_text = content[brace_start:brace_end + 1]
                # Only process small objects (likely enums)
                if len(obj_text) < 5000:
                    values = extract_object_literal_values(obj_text)
                    if values and len(values) >= 2:
                        line_num = get_line_number(content, m.start())
                        all_enums[ename] = (dict(values), line_num)
                        print(f"  Found additional named export enum: {ename} with {len(values)} values (line {line_num})")

    # =========================================================================
    # Now scan specifically the EnumDefine block and MetaAttrib block areas
    # to make sure we haven't missed anything
    # =========================================================================
    print("\n--- Verifying coverage of EnumDefine block ---")

    expected_enums = [
        "StateType", "HealthType", "DmgType", "RunMode", "RunState",
        "UnityType", "PathState", "TargetFilter", "TargetSelectFilter",
        "HitType", "AttackType", "SpBuffState", "StateTrigerType",
        "BuffGroupType", "SkillType", "EffectTriggerType", "BattleFlag",
        "BindType", "AIEvent", "RecordSource", "UnitConfig", "AttribDefine"
    ]

    for ename in expected_enums:
        if ename in all_enums:
            vals = all_enums[ename][0]
            print(f"  OK: {ename} ({len(vals)} values)")
        else:
            print(f"  MISSING: {ename}")

    # =========================================================================
    # Save all enums to JSON files
    # =========================================================================
    print(f"\n--- Saving {len(all_enums)} enums ---")

    saved_files = []
    for name, (values, source_line) in sorted(all_enums.items()):
        f = save_enum(name, values, source_line)
        saved_files.append(f)

    print(f"\nDone! Saved {len(saved_files)} enum files to {OUTPUT_DIR}")

    # Print summary
    print("\n=== SUMMARY ===")
    for name in sorted(all_enums.keys()):
        vals, line = all_enums[name]
        print(f"  {name}: {len(vals)} values (line {line})")


if __name__ == "__main__":
    main()
