# 13 — Equipment

> Complete equipment system: 10 slots, 11 quality tiers, refinement, advancement, resonance, suit sets, treasure boxes, loadout presets, and appearance system.

---

## 10 Equipment Slots

| Slot | Name | Has Figure | Sprite Key |
|------|------|-----------|-----------|
| 1 | Weapon | Yes | zjm_ui_wuqi |
| 2 | Shoulder Guard | Yes | zjm_ui_goushi |
| 3 | Helmet | Yes | zjm_ui_mianshi |
| 4 | Shoulder Pad | Yes | zjm_ui_hujian |
| 5 | Armor | Yes | zjm_ui_kaijia |
| 6 | Bracers | No | zjm_ui_bijia |
| 7 | Gloves | No | zjm_ui_shoutao |
| 8 | Belt | No | zjm_ui_yaodai |
| 9 | Greaves | No | zjm_ui_hutui |
| 10 | Boots | No | zjm_ui_xiezi |

---

## Quality Tiers (11 Total)

| Value | Name | Color |
|-------|------|-------|
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

## ConfigEquipment (Line 229175, 20 Fields)

| Field | Description |
|-------|-------------|
| id | Unique equipment config ID |
| name | Equipment name (string_ref) |
| level | Equipment tier/level requirement |
| part | Equipment slot (1-10) |
| quality | Quality tier (1-11) |
| number | Internal number identifier |
| advanced | Advanced attribute group ID (-> ConfigEquipment_attr.group_id) |
| multiple | Optional multiplier array |
| suitId | Suit set ID (0 = no suit; -> ConfigEquipment_suit) |
| icon | Icon resource ID |
| atlas | Atlas resource ID |
| job | Job type restriction (0 = any job) |
| wearable | Job type that can wear (0 = all; matches ConfigJobs.type) |
| gradeRange | Optional grade range for variation |
| preAttr | Optional pre-defined attribute array |
| is_precious | 1 if confirmation required before selling |
| drop_condition | Drop condition string |
| unlock_level | Player level required |
| preview | Preview flag |
| is_hide | Hidden from normal UI |

**No XOR encoding** — ConfigEquipment has `usesConfigKey: false`.

---

## Attribute System

### Base Attributes

Each equipment has up to 4 base stats: `[{k: attr_id, v: value}, ...]`
```
Base attribute IDs: [1002 (HP), 1001 (ATK), 1024 (DEF), 1003]
```

### Random Attributes

Up to 2 percentage-based bonuses per equipment (`rand_attr`):
```
Display: value * 100 / 10000 = percentage (e.g., 500 = 5%)
```

### ConfigEquipment_attr (Line 228846)

| Field | Description |
|-------|-------------|
| id | Unique attr config ID |
| group_id | Attribute group (matches ConfigEquipment.advanced) |
| attr_id | Actual attribute ID (-> ConfigAttribute) |
| type | Attribute type classification |
| pro | Probability weight for random selection |
| value | Value range array |

### Display Order (Line 234508)
```
Equipment detail attribute IDs:
[1002, 1001, 1024, 1003, 1004, 1016, 1017, 1023, 1008, 1012, 1037, 4001, 4005]
```

---

## Equipment Level System

### ConfigEquipment_level (Line 228960, keyed by [part, level])

| Field | Description |
|-------|-------------|
| part | Equipment slot |
| level | Enhancement level |
| basic | Stat multiplier |
| price | Enhancement cost `[[item_id, amount], ...]` |

### Drop Level Weights (Line 234610)
```
[[-2, 500], [-1, 1500], [0, 6000], [1, 1500], [2, 500]]
```
60% chance of base level, 15% +/-1, 5% +/-2.

---

## Refinement System

Per-slot leveling. Each of the 10 equipment slots has its own refinement level.

### ConfigEquipment_refinement (Line 229012)

| Field | Description |
|-------|-------------|
| id | Refinement level |
| attar | Attribute multipliers `[[attr_id, multiplier], ...]` |
| cost | Cost `[[item_id, amount], ...]` |

### Formula (Line 279920)
```
refinement_bonus = Math.round(base_attr_value * multiplier / 10000)
```

**Cost Items:** Item 1333 (Refining Stone), Item 1334

### Operations
- **Single refine:** `equip.equip_refine_c2s` type=1 — lowest-level slot
- **Batch refine:** `equip.equip_refine_c2s` type=2 — all at lowest level

---

## Advancement System

Stage-based system affecting ALL equipment slots collectively.

### ConfigEquipment_advancement (Line 228788)

| Field | Description |
|-------|-------------|
| id | Stage number |
| attr | Global bonuses `[[attr_id, value], ...]` |
| cost | Advance cost |
| limit | Max refinement level at this stage |
| power | Combat power |

### Trigger Condition (Line 281355)
All 10 slot refinement levels must equal current stage's `limit`.
```javascript
var p = r == s && s == a.limit;
// r = max refinement level, s = min refinement level, a = current advancement config
```

### Battle Attributes by Stage

| Stage | Pierce (1068) | Ign Pierce (1069) | Block (1071) | Ign Block (1072) | Inspire (1074) | Ign Inspire (1075) | Suppress (1077) | Ign Suppress (1078) |
|-------|------|------|------|------|------|------|------|------|
| 1 | +100 | +100 | — | — | — | — | — | — |
| 2 | — | — | +100 | +100 | — | — | — | — |
| 6 | — | — | — | — | +100 | +100 | — | — |
| 36 | +6,240 | +6,240 | +6,240 | +6,240 | +6,240 | +6,240 | +6,240 | +6,240 |

### Displayed Attribute IDs (Line 237573)
```
[1068, 1069, 1071, 1072, 1074, 1075, 1077, 1078]
```

---

## Resonance System

Milestone rewards tied to advancement stages.

### ConfigEquipment_resonance (Line 229060)

| Field | Description |
|-------|-------------|
| id | Milestone ID |
| attr | Cumulative bonuses `[[attr_id, value], ...]` |
| current_attr | Bonus at this specific milestone |
| stage | Required advancement stage |
| power | Combat power |

### Key Values

| Milestone | Stage | Final DMG Bonus (1081) | Final DMG RES (1082) |
|-----------|-------|----------------------|---------------------|
| 1 | 1 | +200 | — |
| 18 | 18 | **+3,800** | **+3,800** |

### Claim Logic (Line 281589)
```javascript
IS(g).refineInfo.stage < t.data.stage || IS(v).send_equip_refine_resonate_c2s()
```
Condition: `refineInfo.stage >= resonance.stage`

Red point notification appears when any unclaimed resonance milestone has `stage <= current advancement stage`.

---

## Suit Set System

### ConfigEquipment_suit (Line 229118, keyed by [suit_id, num])

| Field | Description |
|-------|-------------|
| suit_id | Set ID |
| num | Pieces required |
| effect | Effects granted |
| desc | Bonus description |
| name | Tier name |

### Counting Logic (Line 280544)
```
For each equipped item:
    if configEquipment(config_id).suitId == target_suit_id:
        count++
```

Active bonuses shown in gold (#FDF9B8), inactive in gray (#908474).

---

## Treasure Box System

### Operations

| Protocol | Description |
|----------|-------------|
| equip_box_open_c2s | Open single box |
| equip_box_open_all_c2s | Open multiple `{num, quality}` |
| equip_box_lv_c2s | Level up box |

### Auto-Open Thresholds (Line 234632)
```
[[1,1], [8,2], [12,4], [16,6], [20,8], [24,10], [28,20]]
```
At box level X, can auto-open Y at a time.

### Guarantee / Pity (ConfigEquipment_guarantee, Line 228908)

| Field | Description |
|-------|-------------|
| num | Opens trigger threshold |
| quality | Minimum guaranteed quality tier |
| level | Minimum guaranteed level |
| part | Optional restriction on which parts |

After N opens without high-quality drop -> guaranteed minimum quality.

---

## Equipment Tabs (Loadout Presets)

Players can save multiple equipment loadouts (Line 279348):

| Protocol | Description |
|----------|-------------|
| equip_tab_info_c2s | Get tab info |
| equip_choose_tab_c2s | Switch to a tab |
| equip_change_tab_name_c2s | Rename a tab |

---

## Figure / Appearance System (Line 187466)

Equipment slots 1-3 affect the character's visual appearance:
```
skin_slots: [1, 2, 3]
```

| Slot | Visual |
|------|--------|
| 1 | Weapon appearance |
| 2 | Ornaments/shoulder appearance |
| 3 | Face/helmet appearance |
| 4 | Fate (special modes only) |
| 5 | Wing |

---

## Network Protocol

Prefix: `equip` (Line 279245)

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

## Stat Contribution Pipeline

```
Step 1: Base Attributes     — equipment's base_attr (up to 4)
Step 2: Random Attributes   — equipment's rand_attr (up to 2, percentage)
Step 3: Refinement Bonus    — round(base_value * refinement_attar / 10000)
Step 4: Advancement Bonus   — global bonuses from current stage
Step 5: Resonance Bonus     — cumulative from all claimed milestones
Step 6: Suit Set Bonus      — effects when enough pieces equipped
```

---

## Dependencies

- ConfigJobs — Equipment `wearable` field matches `ConfigJobs.type`
- ConfigAttribute — All attribute IDs referenced throughout
- Combat formulas — Equipment stats feed into all damage calculations
