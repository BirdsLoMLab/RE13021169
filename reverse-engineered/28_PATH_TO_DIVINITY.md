# 28 — Path to Divinity System

## Overview

Path to Divinity is a **talent tree / affix system** where players invest in nodes along branching trunks. Each node grants an **affix** — a specific attribute bonus — with quality tiers and level-scaling probabilities. The system has per-attribute upper limits to prevent unbounded stacking.

---

## Config Tables

| Table | Source Line | Main Key | Fields | Description |
|-------|-----------|----------|--------|-------------|
| ConfigPath_to_divinity | 251523 | trunk_id | 4 | Trunk (branch) definitions with sensor node lists |
| ConfigPath_sensor_node | 251467 | node_id | 5 | Individual nodes: trunk assignment, position, affix group, description |
| ConfigPath_affix | 251405 | affix_id | 6 | Affix definitions: group, quality, attribute ID, value range, power |
| ConfigPath_affix_levelpro | 251358 | id | 3 | Level-based quality probability scaling |
| ConfigPath_upper_limit | 251575 | trunk_id + attr_id | 6 | Per-trunk, per-attribute caps |

---

## A. Trunk Structure (ConfigPath_to_divinity)

| Field | Type | Description |
|-------|------|-------------|
| trunk_id | number | Trunk/branch identifier |
| name | string_ref | Trunk display name |
| tree_id | number | Parent tree ID (multiple trunks form one tree) |
| sensor_node_list | array? | Ordered list of node IDs in this trunk |

Each tree consists of multiple **trunks** (branches), and each trunk contains a sequence of **sensor nodes**. Players unlock nodes in order along a trunk.

---

## B. Node Definitions (ConfigPath_sensor_node)

| Field | Type | Description |
|-------|------|-------------|
| node_id | number | Unique node identifier |
| trunk_id | number | FK to ConfigPath_to_divinity |
| trunk_number | number | Position index within the trunk (sequential) |
| affix_group | number | Affix group rolled when this node is activated |
| desc | string_ref | Node description text |

### Node Activation Flow
1. Player selects a node in sequence (`trunk_number` order)
2. System rolls an affix from the node's `affix_group`
3. Quality of the rolled affix depends on player level (see `ConfigPath_affix_levelpro`)
4. The affix's attribute bonus is added to the player's stats

---

## C. Affix System (ConfigPath_affix)

| Field | Type | Description |
|-------|------|-------------|
| affix_id | number | Unique affix identifier |
| affix_group | number | Group ID (referenced by node's `affix_group`) |
| quality | number | Rarity tier of this affix variant |
| attr_id | number | AttribDefine ID (1001=att, 1002=hp, etc.) |
| value | array? | Value range for the attribute bonus |
| power_rate | number | Combat power contribution rate |

### Affix Rolling
When a node is activated, the system:
1. Filters all affixes matching the node's `affix_group`
2. Selects quality based on player level probabilities (`ConfigPath_affix_levelpro`)
3. Picks an affix of that quality from the group
4. Rolls the attribute value within the `value` range

---

## D. Quality Probability Scaling (ConfigPath_affix_levelpro)

| Field | Type | Description |
|-------|------|-------------|
| id | number | Level threshold ID |
| total_number | number | Total probability weight |
| pro_quality | array? | Quality distribution: `[[quality, probability], ...]` |

Higher player levels shift the probability distribution toward higher-quality affixes. The `total_number` serves as the denominator for probability calculation.

---

## E. Attribute Caps (ConfigPath_upper_limit)

| Field | Type | Description |
|-------|------|-------------|
| trunk_id | number | FK to trunk |
| attr_id | number | AttribDefine attribute ID |
| upper_limit | number | Maximum value for this attribute from this trunk |
| show_type | number | Display formatting type |
| unique | number | Whether this limit applies uniquely (non-stackable) |
| sort | number | Display sort order |

### Cap Enforcement
Each attribute has a **per-trunk cap**. When a player's total affix bonuses for a given attribute in a trunk reach `upper_limit`, no further bonuses of that type are gained. This prevents infinite scaling of any single stat.

---

## F. Combat Relevance

Path to Divinity feeds into combat through **direct attribute modification**:
- Affix values use standard AttribDefine IDs (same as all other systems)
- Bonuses are additive and contribute to the MetaAttrib calculation
- The `upper_limit` system creates diminishing returns, encouraging diversified builds
- Common combat-relevant affixes: att (1001), hp (1002), def (1024), crit_rate (1004), crit_dam (1005)

### Relationship to Other Systems
- **Rings** (`30_RING_SYSTEM.md`) reference Path trunk IDs via `path1`/`path2`
- Path bonuses stack with all other attribute sources (equipment, pets, fates, etc.)
- The cap system (`upper_limit`) is unique to Path — most other systems have no per-system caps
