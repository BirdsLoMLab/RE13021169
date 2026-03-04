# PvP Battle Simulation Bible — Master Index

> **Purpose**: Single source of truth for every combat-relevant system in the game.
> Any future agent can build a full PvP simulation from this folder alone.

## How to Use This Reference

1. **Each file is self-contained** — it includes all data, formulas, and context needed for that system.
2. **Attribute IDs** (e.g., `1001`=ATT, `1002`=HP) are consistent across all files. See `03_ATTRIBUTES.md` for the complete mapping.
3. **Rates/percentages** are stored as raw integers divided by 10,000 unless noted otherwise (e.g., `9000` = 90.00%).
4. **FixMath** rounding is used everywhere in combat: `round(x) = Math.round(x * 10000) / 10000`, `roundInt(x) = Math.round(x)`. See `01_DAMAGE_FORMULAS.md`.
5. **Schema tables** referenced (e.g., `ConfigFly`, `ConfigAngel_star`) correspond to decoded binary config tables. Schema definitions live in `data/schemas/`.
6. **XOR-protected fields** in config tables use `value ^ 24455` to decode. The decoder script is `decode_config_data.py`.

## File Index

| # | File | Contents |
|---|------|----------|
| 00 | `00_INDEX.md` | This file — master index and conventions |
| 01 | `01_DAMAGE_FORMULAS.md` | Complete damage pipeline, all 15 combat formulas, FixMath |
| 02 | `02_PVP_CONSTANTS.md` | 220-level PvP injury reduce table, shield/heal decay, ELO |
| 03 | `03_ATTRIBUTES.md` | All 89+ combat attributes with IDs, keys, initial values, caps |
| 04 | `04_CLASSES.md` | All 8 T5 classes: passives, actives, ownEffect arrays |
| 05 | `05_ACTIVE_SKILLS.md` | All 38 active skills (IDs 0–37) with parameters |
| 06 | `06_PALS_AND_PETS.md` | Pet/pal system: 322 pets, 55 races, deploy effects, damage |
| 07 | `07_AVIANS.md` | ConfigFly system: types, entries, advance levels, affixes |
| 08 | `08_TALENTS.md` | 6 final talents + 7 leveled talents |
| 09 | `09_RELICS.md` | All 5 relics with combat effects |
| 10 | `10_BUFFS_AND_STATUS.md` | 46 buff group types, mutex rules, bleed, shields, death prevention |
| 11 | `11_MOUNT_SKINS.md` | 21+ mount skin combat skills |
| 12 | `12_ARTIFACT_SKINS_AND_GEMS.md` | 19+ artifact skin skills + 7 gem sets |
| 13 | `13_EQUIPMENT.md` | Advancement, resonance, refinement, suits |
| 14 | `14_SPIRITS.md` | 20 spirits + spirit damage formula + affixes |
| 15 | `15_ANGELS.md` | Formation, battle skills, star progression, energy pool |
| 16 | `16_FATE_CARDS.md` | Attribute bonuses + fusion passive skills |
| 17 | `17_PATH_TO_DIVINITY.md` | Affix/talent tree with per-attribute caps |
| 18 | `18_RINGS_AND_BADGES.md` | Ring skills, Path trunk links, badge levels |
| 19 | `19_BACK_DECORATIONS.md` | Back talent trees with attrs/skills per class |
| 20 | `20_SPECIAL_MECHANICS.md` | 0.98 exponent, clones, speed cascade, animation exploit |

## Key Constants Quick Reference

| Constant | Raw Value | Effective | Source |
|----------|-----------|-----------|--------|
| `CONFIG_KEY` | 24455 | XOR key for protected fields | `config_key.json` |
| `miss_correct` | 9000 | 0.90 (90%) | `battle_constants.json` |
| `vertigo_correct` | 9000 | 0.90 (90%) | `battle_constants.json` |
| `shield_correct` | 4000 | 0.40 (40% decay in PvP) | `battle_constants.json` |
| `hp_recovery_correct` | 3000 | 0.30 (30% decay in PvP) | `battle_constants.json` |
| `total_damage_add_down_limit` | 2000 | 0.20 (min damage multiplier) | `battle_constants.json` |
| `pvp_k` | 30 | ELO K-factor | `pvp_constants.json` |
| `pvp_initial_score` | 1000 | Starting ELO | `pvp_constants.json` |
| `crit_rate cap (battle)` | 8000 | 0.80 (80% max crit) | `attribute_caps.json` |
| `frameTime` | 0.033 | ~30 FPS simulation tick | `battle_constants.json` |

## Data Source Hierarchy

When data conflicts, trust sources in this order:
1. `game_script.js` (18MB) — the actual client code; final authority
2. `data/formulas/` — extracted formulas from game_script.js
3. `data/schemas/` — config table field definitions from game_script.js
4. `data/enums/` — enumeration values from game_script.js
5. `data/constants/` — extracted constants from game_script.js
6. `reverse-engineered/*.md` — analysis documents (interpreted, may have errors)
7. `battlesim/battlesim_old_ref-only.html` — old simulator (subset of data)

## Notation Conventions

- **`/10000`** — Raw values are divided by 10,000 to get effective rates/percentages
- **`^ CONFIG_KEY`** — XOR with 24455 to decode protected numeric fields
- **`round()`** — `Math.round(x * 10000) / 10000` (FixMath precision)
- **`roundInt()`** — `Math.round(x)` (integer rounding)
- **`clamp(v, min, max)`** — `Math.max(min, Math.min(max, v))`
- **`[attr_id, value]`** — Attribute pair format used throughout config tables
- **Schema field `[N]`** — Positional index in config data array (0-based)

## Binary Config Decoding

The game's ~908 config tables are packed in a binary blob:
1. **XOR decrypt**: `byte = 255 & ~(32 ^ byte)` for each byte
2. **Zlib decompress**: standard zlib inflation
3. **FilePack parse**: `version(2B BE) + count(2B BE) + [name_len(2B) + name + data_len(4B) + data] × count`
4. **Record parse**: `count(4B BE) + [str_len(2B BE) + JSON_string] × count`
5. **Schema map**: positional array → named fields using `data/schemas/Config*.json`
6. **Field de-XOR**: fields with `"xor": true` → `value ^ 24455`

Decoder script: `decode_config_data.py`
