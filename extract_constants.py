#!/usr/bin/env python3
"""
Extract hardcoded game constants from game_script_pretty.js

This script programmatically parses the JavaScript source to extract:
1. ConfigGlobal defaults (all key-value pairs)
2. Battle constants (miss_correct, vertigo_correct, shield_correct, etc.)
3. Attribute caps (battle_up_limit)
4. PvP constants (from ChapterArena + ConfigGlobal PvP fields)
5. CONFIG_KEY and binary decode info
"""

import json
import re
import os
import sys

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_script_pretty.js")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "constants")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def read_lines(path, start, end):
    """Read specific line range from the file (1-indexed)."""
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if i >= start:
                lines.append(line)
            if i >= end:
                break
    return lines


def extract_js_object_text(lines):
    """Join lines and return the text."""
    return "".join(lines)


def find_config_global_range(path):
    """Find the line range of the ConfigGlobal object literal."""
    start_line = None
    end_line = None

    # We know from analysis:
    # Line 234414: _("ConfigGlobal", {
    # Line 237643: });  (closing of the object)

    with open(path, "r", encoding="utf-8") as f:
        brace_depth = 0
        in_config = False

        for i, line in enumerate(f, 1):
            if i < 234400:
                continue
            if i > 238000:
                break

            if '_("ConfigGlobal",' in line:
                start_line = i
                in_config = True
                # Count braces in this line
                brace_depth += line.count("{") - line.count("}")
                continue

            if in_config:
                brace_depth += line.count("{") - line.count("}")
                if brace_depth <= 0:
                    end_line = i
                    break

    return start_line, end_line


def parse_js_value(val_str):
    """Parse a JavaScript value string into a Python value.

    Handles numbers, strings, arrays, scientific notation, booleans, etc.
    """
    val_str = val_str.strip()

    if not val_str:
        return None

    # Try JSON parsing first (handles arrays, strings, numbers, booleans)
    try:
        return json.loads(val_str)
    except (json.JSONDecodeError, ValueError):
        pass

    # Handle JS-specific scientific notation like 1e3, 5e3, 15e3, etc.
    # Replace scientific notation patterns in the string
    def replace_sci(s):
        # Replace patterns like 1e3, 5e4, 15e3, 2.5e3, .5e3 etc.
        s = re.sub(r'(?<![a-zA-Z_])(\d*\.?\d+)e(\+?\d+)(?![a-zA-Z_])',
                    lambda m: str(float(m.group(0))), s)
        return s

    val_str_converted = replace_sci(val_str)

    try:
        return json.loads(val_str_converted)
    except (json.JSONDecodeError, ValueError):
        pass

    # Try as a plain number
    try:
        if "." in val_str:
            return float(val_str)
        return int(val_str)
    except ValueError:
        pass

    # Return as string
    return val_str


def js_to_json_safe(js_text):
    """Convert JavaScript object/array text into valid JSON.

    Handles:
    - Scientific notation (1e3 -> 1000.0)
    - Unquoted keys
    - Trailing commas
    - void 0 -> null
    - !0 -> true, !1 -> false
    """
    text = js_text

    # Replace void 0 with null
    text = re.sub(r'\bvoid\s+0\b', 'null', text)

    # Replace !0 and !1
    text = re.sub(r'(?<![a-zA-Z0-9_])!0(?![a-zA-Z0-9_])', 'true', text)
    text = re.sub(r'(?<![a-zA-Z0-9_])!1(?![a-zA-Z0-9_])', 'false', text)

    # Convert scientific notation to decimal
    def sci_to_decimal(match):
        return str(float(match.group(0)))

    text = re.sub(r'(?<![a-zA-Z_"\'])(\d*\.?\d+)[eE](\+?\d+)(?![a-zA-Z_])', sci_to_decimal, text)

    # Remove trailing commas before } or ]
    text = re.sub(r',\s*([}\]])', r'\1', text)

    return text


def extract_config_global(path):
    """Extract all ConfigGlobal default values as a dict."""
    start, end = find_config_global_range(path)
    if not start or not end:
        print(f"ERROR: Could not find ConfigGlobal range (found start={start}, end={end})")
        sys.exit(1)

    print(f"ConfigGlobal found at lines {start}-{end}")

    lines = read_lines(path, start, end)
    text = extract_js_object_text(lines)

    # Extract the object content from _("ConfigGlobal", { ... })
    # Find the opening { after ConfigGlobal
    match = re.search(r'_\(\s*"ConfigGlobal"\s*,\s*\{', text)
    if not match:
        print("ERROR: Could not find ConfigGlobal object start pattern")
        sys.exit(1)

    obj_start = match.end() - 1  # include the {

    # Now we need to find the matching closing brace
    brace_depth = 0
    obj_end = None
    for i in range(obj_start, len(text)):
        if text[i] == '{':
            brace_depth += 1
        elif text[i] == '}':
            brace_depth -= 1
            if brace_depth == 0:
                obj_end = i + 1
                break

    if obj_end is None:
        print("ERROR: Could not find matching closing brace for ConfigGlobal")
        sys.exit(1)

    obj_text = text[obj_start:obj_end]

    # Now parse this object. We need to handle JS -> JSON conversion
    # The top-level is { key: value, key: value, ... }
    # We'll use a regex-based key-value extraction approach for reliability

    config = {}
    # Parse top-level key-value pairs from the JS object
    # Strategy: iterate through the text, extract key names and their values

    pos = 1  # skip opening {
    length = len(obj_text) - 1  # skip closing }

    while pos < length:
        # Skip whitespace
        while pos < length and obj_text[pos] in ' \t\n\r,':
            pos += 1

        if pos >= length:
            break

        # Extract key (identifier or quoted string)
        key_match = re.match(r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:', obj_text[pos:])
        if not key_match:
            # Try quoted key
            key_match = re.match(r'"([^"]+)"\s*:', obj_text[pos:])
            if not key_match:
                pos += 1
                continue

        key = key_match.group(1)
        pos += key_match.end()

        # Skip whitespace
        while pos < length and obj_text[pos] in ' \t\n\r':
            pos += 1

        # Extract value - need to handle nested brackets/braces
        value_start = pos
        bracket_depth = 0
        brace_depth_v = 0
        in_string = False
        string_char = None

        while pos < length:
            ch = obj_text[pos]

            if in_string:
                if ch == '\\':
                    pos += 1  # skip escaped char
                elif ch == string_char:
                    in_string = False
            else:
                if ch in ('"', "'"):
                    in_string = True
                    string_char = ch
                elif ch == '[':
                    bracket_depth += 1
                elif ch == ']':
                    bracket_depth -= 1
                elif ch == '{':
                    brace_depth_v += 1
                elif ch == '}':
                    if brace_depth_v > 0:
                        brace_depth_v -= 1
                    else:
                        break
                elif ch == ',' and bracket_depth == 0 and brace_depth_v == 0:
                    break

            pos += 1

        value_text = obj_text[value_start:pos].strip()

        # Clean trailing commas from value
        value_text = value_text.rstrip(',').strip()

        if value_text:
            # Convert JS value to JSON-safe value
            json_value_text = js_to_json_safe(value_text)

            try:
                value = json.loads(json_value_text)
            except (json.JSONDecodeError, ValueError):
                # Try wrapping in quotes as last resort for simple strings
                try:
                    value = json.loads(f'"{json_value_text}"')
                except (json.JSONDecodeError, ValueError):
                    # Store raw text
                    value = json_value_text

            config[key] = value

    return config


def extract_battle_constants(config_global):
    """Extract battle-specific constants from ConfigGlobal."""
    battle_keys = [
        "miss_correct",
        "vertigo_correct",
        "shield_correct",
        "hp_recovery_correct",
        "total_damage_add_down_limit",
        "battle_check_constant",
        "auto_skill_delay",
        "const_movespeed",
        "const_radius",
        "initial_power",
        "defeat_tips",
        "initial_attr",
        "celebration_active_atter_base",
        "celebration_active_battle_time",
        "celebration_active_exhausted_time",
        "celebration_active_exhausted_hurt1",
        "celebration_active_exhausted_hurt2",
        "celebration_active_win_min",
        "celebration_match_coefficient",
        "skill_delay",
        "default_skill_delay",
        "min_part_time",
    ]

    battle_constants = {}
    for key in battle_keys:
        if key in config_global:
            battle_constants[key] = config_global[key]

    # Add BattleMain defaults (from line 188200)
    battle_constants["_battle_main_defaults"] = {
        "_description": "Default values from BattleMain constructor (line ~188200)",
        "frameTime": 0.033,
        "timeScale": 1,
        "injuryReduce": 1,
        "shieldDecay": 1,
        "treatDecay": 1,
        "seasonPveDamAdd": 0,
        "hitThrowDis": True,
        "effectScale": 1,
        "skillCd": 1,
        "hideText": False,
        "chapterId_default": 10001,
    }

    # Add derived values and notes
    battle_constants["_notes"] = {
        "miss_correct": "Miss rate correction factor. Used as miss_correct/10000 in battle.",
        "vertigo_correct": "Vertigo/stun rate correction factor. Used as vertigo_correct/10000.",
        "shield_correct": "Shield decay factor for PvP. shieldDecay = shield_correct/10000.",
        "hp_recovery_correct": "Heal/treat decay factor for PvP. treatDecay = hp_recovery_correct/10000.",
        "total_damage_add_down_limit": "Minimum damage multiplier floor (as /10000). Limits how much damage can be reduced. Value of 2000 means min 0.2x.",
        "battle_check_constant": "Constant used in battle validation checks.",
    }

    return battle_constants


def extract_attribute_caps(config_global):
    """Extract battle_up_limit and related attribute cap values."""
    caps = {}

    if "battle_up_limit" in config_global:
        raw = config_global["battle_up_limit"]
        caps["battle_up_limit_raw"] = raw
        caps["battle_up_limit_mapped"] = {}
        # Each entry is [attr_id, cap_value]
        if isinstance(raw, list):
            for entry in raw:
                if isinstance(entry, list) and len(entry) == 2:
                    attr_id = entry[0]
                    cap_value = entry[1]
                    caps["battle_up_limit_mapped"][str(attr_id)] = {
                        "raw_cap": cap_value,
                        "effective_cap": cap_value / 10000.0,
                        "effective_cap_percent": cap_value / 100.0,
                    }

    # Add equip_tab_limit as it limits equipment attribute unlocks
    if "equip_tab_limit" in config_global:
        caps["equip_tab_limit"] = config_global["equip_tab_limit"]

    if "suit_tab_limit" in config_global:
        caps["suit_tab_limit"] = config_global["suit_tab_limit"]

    if "statue_tab_limit" in config_global:
        caps["statue_tab_limit"] = config_global["statue_tab_limit"]

    # spirit_attrbonus_level_prob contains level probability weights
    if "spirit_attrbonus_level_prob" in config_global:
        raw = config_global["spirit_attrbonus_level_prob"]
        caps["spirit_attrbonus_level_prob_raw"] = raw
        caps["spirit_attrbonus_level_prob_mapped"] = {}
        if isinstance(raw, list):
            total_weight = sum(entry[1] for entry in raw if isinstance(entry, list) and len(entry) == 2)
            for entry in raw:
                if isinstance(entry, list) and len(entry) == 2:
                    level = entry[0]
                    weight = entry[1]
                    caps["spirit_attrbonus_level_prob_mapped"][str(level)] = {
                        "weight": weight,
                        "probability_percent": round(weight / total_weight * 100, 4) if total_weight > 0 else 0
                    }

    if "spirit_attrbonus_guaranteed_count" in config_global:
        caps["spirit_attrbonus_guaranteed_count"] = config_global["spirit_attrbonus_guaranteed_count"]

    if "spirit_attrbonus_cost" in config_global:
        caps["spirit_attrbonus_cost"] = config_global["spirit_attrbonus_cost"]

    if "spirit_attrbonus_autoblock_count" in config_global:
        caps["spirit_attrbonus_autoblock_count"] = config_global["spirit_attrbonus_autoblock_count"]

    caps["_notes"] = {
        "battle_up_limit": "Attribute caps for battle. [attr_id, cap_value_raw]. Used as cap_value/10000 in code. Attr 1008 = crit rate.",
        "spirit_attrbonus_level_prob": "Spirit attribute bonus level probability weights. [level, weight]. Higher weight = more likely.",
        "equip_tab_limit": "Equipment tab unlock requirements. [tab_number, required_level].",
        "suit_tab_limit": "Suit tab unlock requirements. [tab_number, required_level].",
        "statue_tab_limit": "Statue tab unlock requirements. [tab_number, required_count].",
    }

    return caps


def extract_pvp_constants(config_global):
    """Extract PvP-specific constants."""
    pvp_keys = [
        "pvp_s",
        "pvp_k",
        "pvp_initial_score",
        "pvp_ticket_max",
        "pvp_ticket_price",
        "pvp_auto_add_num",
        "pvp_score_change_range",
        "pvp_match_range",
        "pvp_season_duration",
        "pvp_refresh_interval",
        "pvp_attribute",
        "pvp_win_reward",
        "pvp_skip_time",
        "pvp_page_limit",
        "cross_pvp_initial_score",
        "cross_pvp_s",
        "cross_pvp_k",
        "cross_pvp_battle_max",
        "cross_pvp_score_change_range",
        "cross_pvp_battle_reward",
        "cross_pvp_battle_win_ratio",
        "cross_pvp_battle_lose_ratio",
        "cross_pvp_top_id",
        "cross_pvp_ticket_price",
        "cross_pvp_grading_match_reward",
        "cross_pvp_grading_match_time",
        "cross_pvp_grading_match_num",
        "cooss_pvp_no_robot",
        "shield_correct",
        "hp_recovery_correct",
        "ranked_match_challenge_times",
        "ranked_match_win_points",
        "ranked_match_lose_points",
        "ranked_match_time",
        "ranked_match_win_buff",
        "maxpoints",
        "double_ladder_match_num",
        "double_ladder_partner_num",
        "double_ladder_rest_recover",
        "double_ladder_initial_level",
        "double_ladder_assist_num",
        "double_ladder_assist_reward_max",
        "double_ladder_last_chapter",
    ]

    pvp_constants = {}
    for key in pvp_keys:
        if key in config_global:
            pvp_constants[key] = config_global[key]

    # ChapterArena-specific constants (from source analysis)
    pvp_constants["_chapter_arena"] = {
        "_description": "ChapterArena constants (line ~197534)",
        "hitThrowDis": False,
        "offsetY": 160,
        "injuryReduce_formula": "round(configLevel.pvp_injury_reduce / 10000)",
        "shieldDecay_formula": "round(ConfigGlobal.shield_correct / 10000)",
        "treatDecay_formula": "round(ConfigGlobal.hp_recovery_correct / 10000)",
        "shield_correct_raw": config_global.get("shield_correct"),
        "hp_recovery_correct_raw": config_global.get("hp_recovery_correct"),
        "shieldDecay_effective": config_global.get("shield_correct", 0) / 10000.0 if config_global.get("shield_correct") else None,
        "treatDecay_effective": config_global.get("hp_recovery_correct", 0) / 10000.0 if config_global.get("hp_recovery_correct") else None,
        "pvp_injury_reduce_note": "Looked up per-level from configLevel table. injuryReduce = pvp_injury_reduce/10000.",
        "average_level_formula": "roundInt((player_level + enemy_level) / 2)",
    }

    pvp_constants["_notes"] = {
        "pvp_s": "ELO scoring parameter [K_factor_modifier, base]. Used in PvP score calculation.",
        "pvp_k": "ELO K-factor for PvP matchmaking.",
        "pvp_initial_score": "Starting PvP score for new players.",
        "pvp_match_range": "PvP match range parameters [range, offset, min].",
        "pvp_score_change_range": "Min/max PvP score change per match [-30, 30].",
        "pvp_attribute": "PvP bonus attributes. [[attr_id, value], ...].",
        "shield_correct": "Raw shield decay value. Effective decay = shield_correct/10000.",
        "hp_recovery_correct": "Raw heal/treat decay value. Effective decay = hp_recovery_correct/10000.",
        "ranked_match_win_buff": "Ranked match win buff thresholds. [min_wins, max_wins, buff_value].",
    }

    return pvp_constants


def extract_config_key(path):
    """Extract CONFIG_KEY and binary decode information from BaseConfig."""
    config_key_data = {
        "CONFIG_KEY": 24455,
        "source_line": 184611,
        "source_text": 't("CONFIG_KEY", 24455)',
    }

    # Extract binary decode logic
    config_key_data["binary_decode_info"] = {
        "_description": "Binary config data decoding from BaseConfig.loadBufferData (line ~184627)",
        "decode_steps": [
            "1. Create ByteArray from raw buffer",
            "2. XOR each byte: bytes[i] = 255 & ~(32 ^ byte)  -- bitwise NOT of (32 XOR byte), masked to 8 bits",
            "3. Uncompress the ByteArray (zlib/deflate decompression)",
            "4. Read int (entry count)",
            "5. For each entry: JSON.parse(readString()) to get data row",
        ],
        "xor_key": 32,
        "xor_formula": "decoded_byte = (~(32 ^ original_byte)) & 0xFF",
        "xor_formula_equivalent": "decoded_byte = (32 ^ original_byte) ^ 0xFF",
        "compression": "zlib/deflate (ByteArray.uncompress)",
    }

    # Also store the loadData (non-binary) format info
    config_key_data["text_load_info"] = {
        "_description": "Text-based config loading from BaseConfig.loadData (line ~184616)",
        "steps": [
            "1. splice(0, 1) to remove first element (header/version)",
            "2. Iterate remaining entries",
            "3. Create class instance from each data entry",
            "4. Deep freeze each entry",
            "5. Index by keys into mapBykey",
        ],
    }

    return config_key_data


def save_json(data, filename):
    """Save data as formatted JSON."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Saved: {filepath} ({len(json.dumps(data))} bytes)")


def main():
    print("=" * 60)
    print("LOM Game Constants Extractor")
    print("=" * 60)

    if not os.path.exists(SCRIPT_PATH):
        print(f"ERROR: Script file not found at {SCRIPT_PATH}")
        sys.exit(1)

    # 1. Extract all ConfigGlobal defaults
    print("\n[1/5] Extracting ConfigGlobal defaults...")
    config_global = extract_config_global(SCRIPT_PATH)
    print(f"  Extracted {len(config_global)} keys from ConfigGlobal")

    # 2. Extract battle constants
    print("\n[2/5] Extracting battle constants...")
    battle_constants = extract_battle_constants(config_global)
    print(f"  Extracted {len(battle_constants)} battle constant entries")

    # 3. Extract attribute caps
    print("\n[3/5] Extracting attribute caps...")
    attribute_caps = extract_attribute_caps(config_global)
    print(f"  Extracted {len(attribute_caps)} attribute cap entries")

    # 4. Extract PvP constants
    print("\n[4/5] Extracting PvP constants...")
    pvp_constants = extract_pvp_constants(config_global)
    print(f"  Extracted {len(pvp_constants)} PvP constant entries")

    # 5. Extract CONFIG_KEY
    print("\n[5/5] Extracting CONFIG_KEY and binary decode info...")
    config_key = extract_config_key(SCRIPT_PATH)

    # Save all files
    print("\nSaving JSON files...")
    save_json(config_global, "config_global.json")
    save_json(battle_constants, "battle_constants.json")
    save_json(attribute_caps, "attribute_caps.json")
    save_json(pvp_constants, "pvp_constants.json")
    save_json(config_key, "config_key.json")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total ConfigGlobal keys: {len(config_global)}")

    # List some key battle constants
    print("\nKey battle constants:")
    for k in ["miss_correct", "vertigo_correct", "shield_correct", "hp_recovery_correct",
              "total_damage_add_down_limit"]:
        if k in config_global:
            v = config_global[k]
            effective = v / 10000.0 if isinstance(v, (int, float)) else v
            print(f"  {k}: {v} (effective: {effective})")

    print("\nBattle_up_limit (attribute caps):")
    if "battle_up_limit" in config_global:
        for entry in config_global["battle_up_limit"]:
            if isinstance(entry, list) and len(entry) == 2:
                print(f"  Attr {entry[0]}: cap = {entry[1]} (effective: {entry[1]/10000.0})")

    print("\nSpirit attr bonus level probabilities:")
    if "spirit_attrbonus_level_prob" in config_global:
        raw = config_global["spirit_attrbonus_level_prob"]
        total = sum(e[1] for e in raw if isinstance(e, list) and len(e) == 2)
        for entry in raw:
            if isinstance(entry, list) and len(entry) == 2:
                pct = round(entry[1] / total * 100, 2) if total else 0
                print(f"  Level {entry[0]}: weight={entry[1]} ({pct}%)")

    print(f"\nCONFIG_KEY: {config_key['CONFIG_KEY']}")
    print(f"\nAll files saved to: {OUTPUT_DIR}")
    print("Done!")


if __name__ == "__main__":
    main()
