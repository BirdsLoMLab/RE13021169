# 17 — Path to Divinity

> Talent tree with affix nodes, quality-tiered rolls, and per-attribute caps.

---

## Overview

Path to Divinity is a talent tree where players invest in nodes along branching trunks. Each node grants an **affix** — a random attribute bonus — with quality tiers and level-scaling probabilities. Per-attribute upper limits prevent unbounded stacking.

---

## Trunk Structure (ConfigPath_to_divinity, 4 fields)

| Field | Description |
|-------|-------------|
| trunk_id | Trunk/branch ID |
| name | Display name |
| tree_id | Parent tree (multiple trunks form one tree) |
| sensor_node_list | Ordered list of node IDs |

---

## Node Definitions (ConfigPath_sensor_node, 5 fields)

| Field | Description |
|-------|-------------|
| node_id | Unique ID |
| trunk_id | FK to trunk |
| trunk_number | Position index (sequential) |
| affix_group | Affix group rolled on activation |
| desc | Description |

### Activation Flow
1. Select node in sequence (trunk_number order)
2. Roll affix from node's affix_group
3. Quality determined by player level (ConfigPath_affix_levelpro)
4. Affix attribute bonus added to player stats

---

## Affix System (ConfigPath_affix, 6 fields)

| Field | Description |
|-------|-------------|
| affix_id | Unique ID |
| affix_group | Group (referenced by node) |
| quality | Rarity tier |
| attr_id | AttribDefine ID |
| value | Value range [min, max] |
| power_rate | Power contribution |

### Rolling Process
1. Filter affixes by node's affix_group
2. Select quality by level probability (ConfigPath_affix_levelpro)
3. Pick affix of that quality
4. Roll value within range

---

## Quality Probability (ConfigPath_affix_levelpro, 3 fields)

| Field | Description |
|-------|-------------|
| id | Level threshold ID |
| total_number | Probability denominator |
| pro_quality | Distribution `[[quality, probability], ...]` |

Higher player levels shift probability toward higher-quality affixes.

---

## Attribute Caps (ConfigPath_upper_limit, 6 fields)

| Field | Description |
|-------|-------------|
| trunk_id | FK to trunk |
| attr_id | Attribute ID |
| upper_limit | Maximum value from this trunk |
| show_type | Display format |
| unique | Non-stackable flag |
| sort | Display order |

### Cap Enforcement
Each attribute has a **per-trunk cap**. When total affix bonuses reach `upper_limit`, no further bonuses of that type are gained. Encourages diversified builds.

---

## Combat Relevance

- Uses standard AttribDefine IDs (1001=ATK, 1002=HP, etc.)
- Bonuses are additive in MetaAttrib calculation
- Cap system is **unique to Path** — most other systems have no per-system caps
- Common affixes: ATK, HP, DEF, crit_rate, crit_dam

### Connections
- **Rings** reference Path trunks via `path1`/`path2`
- Path bonuses stack with all other attribute sources
