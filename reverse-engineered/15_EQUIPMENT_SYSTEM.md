# 15 — Equipment System

## Code Locations
**Config Module:** ConfigEquipment.ts
**Lines:** 229175+ in `game_script_pretty.js`
**UI/Logic Lines:** 279245-281600+ in `game_script_pretty.js`

**Related Data:** `data/systems/equipment_system.json`

---

## Overview

The equipment system manages gear items worn by the player across 10 body slots. Equipment provides base attributes, random attributes, and participates in suit set bonuses. Sub-systems include refinement (per-slot level ups), advancement (stage-based group upgrades), resonance (milestone rewards), and a treasure box opening system with quality guarantees.

---

## A. Equipment Slots

**Source:** `game_script_pretty.js` line 281238

Players have 10 equipment slots identified by the `part` field in ConfigEquipment:

| Slot ID | Name | Sprite Key |
|---------|------|-----------|
| 1 | Weapon | zjm_ui_wuqi |
| 2 | Shoulder Guard | zjm_ui_goushi |
| 3 | Helmet | zjm_ui_mianshi |
| 4 | Shoulder Pad | zjm_ui_hujian |
| 5 | Armor | zjm_ui_kaijia |
| 6 | Bracers | zjm_ui_bijia |
| 7 | Gloves | zjm_ui_shoutao |
| 8 | Belt | zjm_ui_yaodai |
| 9 | Greaves | zjm_ui_hutui |
| 10 | Boots | zjm_ui_xiezi |

Slot IDs correspond to `ConfigEquipment.part` and `location` values in the player's `equip_list`.

---

## B. Equipment Config

**Config:** ConfigEquipment (line 229175), main key: `id`

| Field | Description |
|-------|-------------|
| id | Unique equipment config ID |
| name | Equipment name (string_ref) |
| level | Equipment tier/level requirement |
| part | Equipment slot (1-10) |
| quality | Quality tier (1=WHITE through 11=FOREVER) |
| number | Internal number identifier |
| advanced | Advanced attribute group ID (references ConfigEquipment_attr.group_id) |
| multiple | Optional multiplier array |
| suitId | Suit set ID (0 = no suit; references ConfigEquipment_suit) |
| icon | Icon resource ID |
| atlas | Atlas resource ID |
| job | Job type restriction (0 = any job) |
| wearable | Job type that can wear this equipment (0 = all classes; matches ConfigJobs.type) |
| gradeRange | Optional grade range for variation |
| preAttr | Optional pre-defined attribute array |
| is_precious | 1 if confirmation required before selling |
| drop_condition | Drop condition string |
| unlock_level | Player level required to use |
| preview | Preview flag |
| is_hide | Hidden from normal UI flag |

---

## C. Quality Tiers

**Source:** `game_script_pretty.js` line 279699

| Value | Name | Typical Color |
|-------|------|--------------|
| 1 | WHITE | White |
| 2 | GREEN | Green |
| 3 | BLUE | Blue |
| 4 | PURPLE | Purple |
| 5 | GOLD | Gold |
| 6 | ORANGE | Orange |
| 7 | RED | Red |
| 8 | PINK | Pink |
| 9 | MULTICOLOR | Rainbow |
| 10 | GILT | Gilt |
| 11 | FOREVER | Eternal |

---

## D. Attribute System

### Base Attributes

**Source:** `game_script_pretty.js` line 234505

Each equipment has up to 4 base stats stored as `[{k: attr_id, v: value}, ...]`:

```
Base attribute IDs: [1002 (HP), 1001 (ATK), 1024 (DEF), 1003]
```

Display order is sorted by the `attrToIndex` mapping at line 280036.

### Random Attributes

**Source:** `game_script_pretty.js` line 112173

Each equipment can have up to 2 random attributes (`rand_attr`). These are percentage-based bonuses:

```javascript
// Line 112173: Display random attributes
for (var v = t.rand_attr || [], _ = 0; _ < 2; _++) {
    // ...
    txtValue.string = d.formatStr('%s%', 100 * r / 1e4)  // value/10000 * 100
}
```

**Display formula:** `value * 100 / 10000 = percentage` (e.g., 500 = 5%)

### Equipment Attribute Config

**Config:** ConfigEquipment_attr (line 228846)

| Field | Description |
|-------|-------------|
| id | Unique attr config ID |
| group_id | Attribute group (matches ConfigEquipment.advanced) |
| attr_id | Actual attribute ID (references ConfigAttribute) |
| type | Attribute type classification |
| pro | Probability weight for random selection |
| value | Value range array for the attribute |

### Display Order

**Source:** `game_script_pretty.js` line 234508

```
Equipment detail attribute IDs:
[1002, 1001, 1024, 1003, 1004, 1016, 1017, 1023, 1008, 1012, 1037, 4001, 4005]
```

---

## E. Equipment Level System

**Config:** ConfigEquipment_level (line 228960), indexed by `[part, level]`

| Field | Description |
|-------|-------------|
| part | Equipment slot ID |
| level | Enhancement level |
| basic | Basic stat multiplier at this level |
| price | Cost to enhance: `[[item_id, amount], ...]` |

### Level Drop Weights

**Source:** `game_script_pretty.js` line 234610

```javascript
[[-2, 500], [-1, 1500], [0, 6000], [1, 1500], [2, 500]]
```

When equipment drops, its level is offset from a base level using these weights:
- Offset -2: weight 500 (5%)
- Offset -1: weight 1500 (15%)
- Offset 0: weight 6000 (60%, most common)
- Offset +1: weight 1500 (15%)
- Offset +2: weight 500 (5%)

---

## F. Suit Set System

**Config:** ConfigEquipment_suit (line 229118), indexed by `[suit_id, num]`

| Field | Description |
|-------|-------------|
| suit_id | Suit set ID (matches ConfigEquipment.suitId) |
| num | Number of pieces required for this bonus tier |
| effect | Array of effects granted by this tier |
| desc | Bonus description |
| name | Bonus tier name |

### Counting Logic

**Source:** `game_script_pretty.js` line 280544

```javascript
getEquipWearCountBySuitId:
    for each equipped item:
        if configEquipment.getDataByKey(equip.config_id).suitId == target_suit_id:
            count += 1
```

Display: Shows as `BonusName (currentCount/requiredCount): description`
- Active: color `#FDF9B8`
- Inactive: color `#908474`

---

## G. Refinement System

**Config:** ConfigEquipment_refinement (line 229012)

Refinement is a per-slot leveling system. Each of the 10 equipment slots has its own refinement level. Refinement adds percentage-based multipliers to base attributes.

| Field | Description |
|-------|-------------|
| id | Refinement level |
| attar | Attribute multipliers: `[[attr_id, multiplier_value], ...]` |
| cost | Refinement cost: `[[item_id, amount], ...]` |

### Refinement Bonus Formula

**Source:** `game_script_pretty.js` line 279920

```javascript
var h = Math.round(i * d[1] / 1e4)
```

```
refinement_bonus = Math.round(base_attr_value * refinement_multiplier / 10000)
```

Where:
- `i` = base_attr value (the equipment's base attribute for matching attr_id)
- `d[1]` = refinement multiplier from ConfigEquipment_refinement.attar entry
- `h` = resulting refinement bonus

### Operations

**Source:** `game_script_pretty.js` line 279390

- **Single refine:** `equip.equip_refine_c2s` with `type=1` -- refines one level for the lowest-level slot
- **Batch refine:** `equip.equip_refine_c2s` with `type=2` -- refines multiple slots at once (all at lowest level)

**Cost items:**
- Item 1333: Primary refinement material (Refining Stone)
- Item 1334: Secondary refinement material

---

## H. Advancement System

**Config:** ConfigEquipment_advancement (line 228788)

Advancement is a stage-based system that applies to ALL equipment slots collectively. When all slots reach the refinement limit for the current stage, the player can advance to the next stage.

| Field | Description |
|-------|-------------|
| id | Advancement stage number |
| attr | Global attribute bonuses: `[[attr_id, value], ...]` |
| cost | Advance cost: `[[item_id, amount], ...]` |
| limit | Maximum refinement level at this stage |
| power | Combat power value |

### Advancement Trigger

**Source:** `game_script_pretty.js` line 281355

```javascript
var p = r == s && s == a.limit;
// r = max refinement level, s = min refinement level, a = current advancement config
```

All 10 slot refinement levels must equal the current stage's `limit` to trigger advancement.

### Advancement Attribute Display

**Source:** `game_script_pretty.js` line 237573

```
Displayed attribute IDs: [1068, 1069, 1071, 1072, 1074, 1075, 1077, 1078]
```

### Protocol

```
equip.equip_refine_stage_c2s
```

---

## I. Resonance System

**Config:** ConfigEquipment_resonance (line 229060)

Resonance is a milestone reward system tied to advancement stages. When the player reaches a certain advancement stage, they can claim resonance rewards.

| Field | Description |
|-------|-------------|
| id | Resonance milestone ID (sequential) |
| attr | Cumulative attribute bonuses: `[[attr_id, value], ...]` |
| current_attr | Specific attribute bonus at this resonance level (displayed individually) |
| stage | Required advancement stage to unlock |
| power | Combat power value |

### Claim Logic

**Source:** `game_script_pretty.js` line 281589

```javascript
IS(g).refineInfo.stage < t.data.stage || IS(v).send_equip_refine_resonate_c2s()
```

Condition: `refineInfo.stage >= resonance.stage`

### Red Point Logic

**Source:** `game_script_pretty.js` line 279638

Red point notification appears when any unclaimed resonance milestone has `stage <= current advancement stage`.

---

## J. Guarantee / Pity System

**Config:** ConfigEquipment_guarantee (line 228908)

| Field | Description |
|-------|-------------|
| num | Number of opens trigger threshold |
| quality | Minimum guaranteed quality tier |
| level | Minimum guaranteed level |
| part | Optional restriction on which parts are guaranteed |

After a certain number of treasure box opens without a high-quality drop, the system guarantees one.

---

## K. Treasure Box System

**Source:** `game_script_pretty.js` line 279286

Equipment is obtained by opening treasure boxes with consumable items.

### Operations

| Protocol | Description |
|----------|-------------|
| equip.equip_box_open_c2s | Open single box |
| equip.equip_box_open_all_c2s | Open multiple boxes `{num, quality}` |
| equip.equip_box_lv_c2s | Level up the box |

### Auto-Open Batch Thresholds

**Source:** `game_script_pretty.js` line 234632

```
[[1, 1], [8, 2], [12, 4], [16, 6], [20, 8], [24, 10], [28, 20]]
```

Format: `[box_level, batch_size]` -- at box level X, can auto-open Y at a time.

---

## L. Stat Contribution Pipeline

Equipment stats flow into the player's total attributes through 6 steps:

```
Step 1: Base Attributes     -- equipment's base_attr (up to 4) added directly
Step 2: Random Attributes   -- equipment's rand_attr (up to 2) as percentage bonuses
Step 3: Refinement Bonus    -- bonus = round(base_value * refinement_attar / 10000)
Step 4: Advancement Bonus   -- global attribute bonuses from current advancement stage
Step 5: Resonance Bonus     -- cumulative bonuses from all claimed resonance milestones
Step 6: Suit Set Bonus      -- set bonus effects when enough pieces are equipped
```

**Source:** `game_script_pretty.js` line 199068

```javascript
setPlayerAttrib:
    for each attribute in module=1:
        getRoleAttrById(attr_id) sets the base value
```

Note: `getRoleAttrById` aggregates all attribute sources on the server side; the client reads final values.

---

## M. Equipment Tabs (Loadout Presets)

**Source:** `game_script_pretty.js` line 279348

Players can save multiple equipment loadouts:

| Protocol | Description |
|----------|-------------|
| equip.equip_tab_info_c2s | Get tab info |
| equip.equip_choose_tab_c2s | Switch to a tab |
| equip.equip_change_tab_name_c2s | Rename a tab |

---

## N. Figure / Appearance System

**Source:** `game_script_pretty.js` lines 187466, 234511

Equipment slots 1 (weapon), 2 (shoulder), and 3 (helmet) affect the character's visual appearance:

```javascript
skin_slots: [1, 2, 3]
```

Visual mapping:
- Slot 1: Weapon appearance
- Slot 2: Ornaments/shoulder appearance
- Slot 3: Face/helmet appearance
- Slot 4: Fate (special modes only)
- Slot 5: Wing

---

## O. Network Protocol

**Source:** `game_script_pretty.js` line 279245, prefix: `equip`

| Protocol | Description |
|----------|-------------|
| equip_info_c2s/s2c | Get full equipment list |
| equip_wear_c2s | Equip an item |
| equip_change_s2c | Equipment list change notification |
| equip_shop_c2s/s2c | Sell equipment |
| equip_box_info_c2s/s2c | Get treasure box info |
| equip_box_open_c2s/s2c | Open single box |
| equip_box_open_all_c2s/s2c | Open multiple boxes |
| equip_refine_info_c2s/s2c | Get refinement info |
| equip_refine_c2s/s2c | Refine equipment (type 1=single, 2=batch) |
| equip_refine_stage_c2s/s2c | Advance to next stage |
| equip_refine_resonate_c2s/s2c | Claim resonance milestone |
| equip_filter_info_c2s/s2c | Get equipment filter settings |
| equip_filter_attr_c2s | Set equipment filter attribute |

---

## Dependencies

- **ConfigJobs** -- Equipment `wearable` field matches `ConfigJobs.type`
- **ConfigAttribute** -- All attribute IDs referenced in base_attr, rand_attr, refinement, advancement, resonance
- **14_CLASS_JOB_SYSTEM.md** -- Job type determines equipment eligibility
- **01_BASIC_DAMAGE_CALCULATION.md** -- Equipment stats feed into combat formulas
