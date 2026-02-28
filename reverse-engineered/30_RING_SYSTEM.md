# 30 — Ring System

## Overview

The Ring system provides **equippable rings** that grant attribute bonuses and base skills. Rings have quality tiers, level-based progression, and connect to the Path to Divinity system through `path1`/`path2` trunk references. Leveling rings requires both EXP and material goods.

---

## Config Tables

| Table | Source Line | Main Key | Fields | Description |
|-------|-----------|----------|--------|-------------|
| ConfigRing | 255436 | id | 7 | Ring definitions: name, path trunk references, icons, quality |
| ConfigRing_level | 255367 | level | 7 | Per-level progression: costs, attribute bonuses, base skills, power |

---

## A. Ring Definition (ConfigRing)

| Field | Type | Description |
|-------|------|-------------|
| id | number | Unique ring ID |
| name | string_ref | Ring display name |
| path1 | number | First Path to Divinity trunk reference |
| path2 | number | Second Path to Divinity trunk reference |
| icon1 | number | Primary icon asset |
| icon2 | number | Secondary icon asset |
| quality | number | Rarity tier |

### Path Connection
Each ring references **two Path to Divinity trunks** (`path1` and `path2`). This creates a thematic link between rings and specific talent tree branches, suggesting that rings may enhance or synergize with specific path builds.

---

## B. Level Progression (ConfigRing_level)

| Field | Type | Description |
|-------|------|-------------|
| level | number | Ring level |
| expend_exp | number | EXP cost to reach this level |
| expend_goods | array? | Material costs: `[[goodsId, count], ...]` |
| attr | array? | Attribute bonuses at this level: `[[attrId, value], ...]` |
| base_skill | array? | Base skills unlocked/enhanced at this level |
| unlock | number | Prerequisite (e.g., required player level or rank) |
| power | number | Combat power contribution |

### Leveling Flow
1. Player accumulates ring EXP and materials
2. When `expend_exp` and `expend_goods` requirements are met, level up
3. New `attr` bonuses replace previous level's bonuses
4. New `base_skill` entries may unlock or enhance ring abilities
5. `power` contribution increases

---

## C. Combat Relevance

### Attribute Bonuses
Ring `attr` values follow the standard format `[[attrId, value], ...]`:
- Use AttribDefine IDs (1001=att, 1002=hp, 1024=def, etc.)
- Applied additively during stat assembly
- Scale with ring level

### Base Skills
The `base_skill` field adds passive or active skills from the ring:
- Skills reference ConfigSkill IDs
- These follow the standard skill execution pipeline
- Higher ring levels may enhance existing skills or unlock new ones

### Dual-Path Synergy
The `path1`/`path2` references suggest rings are designed to complement specific Path to Divinity builds. While the exact synergy mechanics depend on runtime data, the structural link implies:
- Rings may boost the effectiveness of path affix bonuses
- Certain ring + path combinations may unlock set bonuses
- Ring quality tiers may gate access to higher-tier path trunks

---

## D. Relationship to Other Systems

| System | Connection |
|--------|-----------|
| Path to Divinity | `path1`/`path2` trunk references |
| Equipment | Rings occupy a separate slot from main equipment |
| Stat Assembly | `attr` values feed into MetaAttrib calculation |
| Skill System | `base_skill` entries use standard ConfigSkill framework |
