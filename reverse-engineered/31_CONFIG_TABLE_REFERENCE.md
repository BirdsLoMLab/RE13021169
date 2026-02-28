# 31 — Config Table Reference

## Overview

The LOM game client uses **711 config tables** totaling **4,807 fields** to define all game content. Tables are loaded from server data at runtime using `BaseConfig.loadData()` (JSON) or `loadBufferData()` (binary XOR-encoded). All schemas have been extracted to `data/schemas/`.

---

## Data Format

### Field Types
| Type | Description |
|------|-------------|
| `number` | Plain integer |
| `string_ref` | Language string reference ID (resolved via GetStrFromConfig) |
| `bignum` | Large number (for HP/ATT/DEF exceeding normal int range) |
| `xor_number` | XOR-obfuscated integer (decoded with config key) |
| `optional_array` | Nullable JSON array field |

### XOR Obfuscation
- **CONFIG_KEY = 24455** (line ~184611)
- Decode: `realValue = rawValue ^ 24455`
- Binary data decode: `bytes[i] = 255 & ~(32 ^ bytes[i])` → decompress → parse JSON
- Only **5 tables** use XOR fields (anti-tamper on combat-critical stats)

---

## XOR-Obfuscated Tables

| Table | Fields | XOR Fields | Description |
|-------|--------|------------|-------------|
| **Unit** | 97 | 77 | All combat stat fields for units |
| **MainUnit** | 90 | 70 | Player character stat fields |
| **Petlevel** | 64 | 56 | Pet per-level combat stats |
| **Skill** | 28 | 4 | autoDis, initialPower, maxPower, powerRecovery |
| **Reversion_war_chess** | 14 | 2 | initialCd, maxCd |

---

## Category Summary

| Category | Tables | Fields | Description |
|----------|--------|--------|-------------|
| Minigame | 88 | 595 | All embedded minigames (88 distinct modes) |
| Chapter / Stage | 67 | 788 | Battle stage definitions across all modes |
| Misc / Uncategorized | 105 | 615 | Fly system (16), Jobs (2), World Boss (4), Statue (4), Wartoken (3), etc. |
| Activity / Event | 47 | 298 | Seasonal events, holidays, login bonuses |
| Season / Battlepass | 45 | 290 | Seasonal modes, ships, battlepass |
| UI / Guide / System | 36 | 191 | Client config, guides, function unlock |
| PvP / Arena | 31 | 223 | Cross-server PvP, arenas, guild brawl |
| Farm / Housing | 29 | 207 | Backyard, farm, parking lot, trees |
| Language | 24 | 62 | 10 languages + UI strings |
| Equipment / Artifact / Relic | 22 | 162 | Gear, artifacts, gems, relics |
| Angel / Spirit / Fate | 21 | 158 | Companions, spirits, fate cards |
| Quest / Task | 20 | 136 | Achievements, daily/main tasks |
| Shop / Mall | 19 | 175 | IAP, shops, privilege cards |
| Gacha / Draw | 18 | 124 | Pull/draw systems |
| Unit / Combat Core | 16 | 317 | Units, attributes, buffs, bullets |
| Guild / Social | 16 | 93 | Guild system, GvE modes |
| Adventure | 14 | 106 | Adventure space exploration |
| Mining | 13 | 66 | Mining minigame |
| Rogue | 12 | 85 | Roguelike mode |
| Marry / Romance | 10 | 84 | Marriage, rings, favorability |
| Mount | 9 | 82 | Mount definitions, skins, gacha |
| Escort | 9 | 55 | Caravan escort mode |
| Merge | 7 | 43 | Merge puzzle minigame |
| Pet / Companion | 6 | 97 | Pet definitions, leveling, talents |
| Fish / Fishing | 6 | 54 | Fishing system |
| Treasure | 6 | 54 | Treasure hunt/skins |
| Skill / Buff / Effect | 5 | 66 | Skills, effects, buffs |
| Dragon Map | 4 | 34 | World map events |
| Tower | 3 | 22 | Tower defense mode |
| Ads | 3 | 21 | Ad monetization |
| **TOTAL** | **711** | **4,807** | |

---

## Combat-Critical Tables (Detailed)

### Unit / Combat Core

| Table | Line | Key | Fields | Description |
|-------|------|-----|--------|-------------|
| Attribute | 219864 | id | 12 | Attribute definitions (89 IDs: 1001-1082, 6001-6007) |
| Unit | 267178 | id | 97 | All unit combat stats (77 XOR fields) |
| MainUnit | 244973 | id | 90 | Player character stats (70 XOR fields) |
| UnitType | 267115 | id | 7 | Per-type constants (suspend_time, vertigo_time) |
| UnitModel | 267007 | id | 34 | Visual/animation configuration |
| Buff | 222479 | id | 16 | Buff definitions (action, params, mutex) |
| Specil_buff | 262195 | id | 8 | Special CC/status effects |
| Bullet | 222363 | id | 8 | Projectile definitions |
| Level | 242991 | level | 5 | Level config (pvp_injury_reduce, power_par) |
| Monster | 248178 | id | 4 | Monster type mappings |
| Monster_buff_chapter | 248120 | id | 6 | Monster buff assignments per chapter |

### Skill / Effect

| Table | Line | Key | Fields | Description |
|-------|------|-----|--------|-------------|
| Skill | 261531 | id | 28 | Skill definitions (4 XOR fields) |
| Skill_level | 261387 | id+level | 11 | Per-level damage coefficients |
| Skill_pos | 261479 | id | 4 | Skill slot unlock conditions |
| Skilleffcet | 261711 | id | 18 | Skill effect definitions |

### Equipment / Artifact

| Table | Line | Key | Fields | Description |
|-------|------|-----|--------|-------------|
| Equipment | 229175 | id | 20 | Equipment base definitions |
| Equipment_attr | 229064 | id | 6 | Equipment attribute bonuses |
| Equipment_level | 229130 | id | 4 | Equipment level scaling |
| Artifact | 218298 | id | 16 | Artifact definitions |
| Artifact_level | 218150 | id | 7 | Artifact level scaling |
| Relic | 254905 | id | 12 | Relic definitions |

### Pet / Companion

| Table | Line | Key | Fields | Description |
|-------|------|-----|--------|-------------|
| Pet | 252193 | id | 12 | Pet definitions |
| Petlevel | 252287 | id+level | 64 | Pet per-level stats (56 XOR fields) |
| Petrace | 252643 | id | 2 | Pet race types |
| Pet_talent | 252111 | id+all_star | 9 | Pet talent effects |
| Pet_proficiency | 252044 | id+level | 7 | Pet proficiency progression |

### Spirit / Angel

| Table | Line | Key | Fields | Description |
|-------|------|-----|--------|-------------|
| Spirit | 262760 | id | 14 | Spirit definitions |
| Spirit_level | 262620 | id+level | 10 | Spirit level scaling |
| Spirit_affix_group | 262486 | id | 4 | Spirit affix groups |
| Angel | 218577 | id | 9 | Angel/hero definitions |
| Angel_skill | 218461 | id | 6 | Angel skill enhancements |
| Angel_star | 218380 | id+star | 16 | Angel star-level progression |

### Class / Job

| Table | Line | Key | Fields | Description |
|-------|------|-----|--------|-------------|
| Jobs | 239943 | id | 28 | Class/job definitions |
| Jobs_wakeup | 239885 | id | 5 | Job awakening system |

### Mount

| Table | Line | Key | Fields | Description |
|-------|------|-----|--------|-------------|
| Mount | 248453 | id | 24 | Mount definitions |
| Mount_level | 248363 | id+level | 10 | Mount level scaling |
| Mount_ability | 248247 | id | 4 | Mount abilities |

### Progression / Enhancement

| Table | Line | Key | Fields | Description |
|-------|------|-----|--------|-------------|
| Fate | 231972 | fate_id | 7 | Fate card definitions |
| Fate_level | 231902 | fate_id+level | 7 | Fate leveling |
| Path_to_divinity | 251523 | trunk_id | 4 | Path trunk definitions |
| Path_affix | 251405 | affix_id | 6 | Path affix bonuses |
| Statue_attr | 263229 | id | 6 | Statue attribute pool |
| Statue_level | 263291 | level | 4 | Statue level progression |
| Ring | 255436 | id | 7 | Ring definitions |
| Ring_level | 255367 | level | 7 | Ring level progression |

### PvP / Season

| Table | Line | Key | Fields | Description |
|-------|------|-----|--------|-------------|
| Chapter_type | 224043 | id | 16 | Chapter type definitions (PvP modes) |
| Season_ship | 259623 | id | 9 | Ship definitions |
| Season_equipment | 259150 | id | 11 | Season equipment |
| Global | 235650 | key | 3 | 744 global constants |

---

## Largest Tables by Field Count

| Rank | Table | Fields | XOR | Description |
|------|-------|--------|-----|-------------|
| 1 | Unit | 97 | 77 | Unit combat stats |
| 2 | MainUnit | 90 | 70 | Player character stats |
| 3 | Petlevel | 64 | 56 | Pet level stats |
| 4 | Pay_mall | 43 | — | IAP store definitions |
| 5 | UnitModel | 34 | — | Unit visual config |
| 6 | Jobs | 28 | — | Class/job definitions |
| 7 | Skill | 28 | 4 | Skill definitions |
| 8 | League_gve_chapter_monster | 27 | — | GvE monster config |
| 9 | Chapter | 24 | — | Main chapter definitions |
| 10 | Mount | 24 | — | Mount definitions |

---

## Schema File Format

Each schema file in `data/schemas/` contains:

```json
{
  "className": "ConfigUnit",
  "tableName": "Unit",
  "sourceLine": 267178,
  "mainKey": "id",
  "indexedKeys": { "id": 0 },
  "usesConfigKey": true,
  "fieldCount": 97,
  "fields": [
    {
      "name": "id",
      "index": 0,
      "type": "number",
      "xor": false,
      "optional": false
    },
    ...
  ]
}
```

---

## Data Directory

```
data/schemas/
├── _index.json          # Master index of all 711 tables
├── ConfigUnit.json      # Individual schema files
├── ConfigSkill.json
├── ...
└── (711 files total)
```

The `_index.json` contains a compact listing of all tables with className, tableName, sourceLine, mainKey, fieldCount, and usesConfigKey for quick lookup without reading individual files.
