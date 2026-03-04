# 13 — Equipment

> Advancement, resonance, refinement, suits, and the 10-slot equipment system.

---

## 10 Equipment Slots

| Slot | Name | Has Figure |
|------|------|-----------|
| 1 | Weapon | Yes |
| 2 | Shoulder Guard | Yes |
| 3 | Helmet | Yes |
| 4 | Shoulder Pad | Yes |
| 5 | Armor | Yes |
| 6 | Bracers | No |
| 7 | Gloves | No |
| 8 | Belt | No |
| 9 | Greaves | No |
| 10 | Boots | No |

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

## Base Attributes

Each equipment has up to 4 base stats: `[{k: attr_id, v: value}, ...]`
```
Base attribute IDs: [1002 (HP), 1001 (ATK), 1024 (DEF), 1003]
```

### Random Attributes
Up to 2 percentage-based bonuses per equipment (`rand_attr`):
```
Display: value * 100 / 10000 = percentage (e.g., 500 = 5%)
```

---

## Refinement System

Per-slot leveling. Each of the 10 equipment slots has its own refinement level.

### ConfigEquipment_refinement
| Field | Description |
|-------|-------------|
| id | Refinement level |
| attar | Attribute multipliers `[[attr_id, multiplier], ...]` |
| cost | Cost `[[item_id, amount], ...]` |

### Formula
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

### ConfigEquipment_advancement
| Field | Description |
|-------|-------------|
| id | Stage number |
| attr | Global bonuses `[[attr_id, value], ...]` |
| cost | Advance cost |
| limit | Max refinement level at this stage |
| power | Combat power |

### Trigger Condition
All 10 slot refinement levels must equal current stage's `limit`.

### Battle Attributes by Stage

| Stage | Pierce (1068) | Ign Pierce (1069) | Block (1071) | Ign Block (1072) | Inspire (1074) | Ign Inspire (1075) | Suppress (1077) | Ign Suppress (1078) |
|-------|------|------|------|------|------|------|------|------|
| 1 | +100 | +100 | — | — | — | — | — | — |
| 2 | — | — | +100 | +100 | — | — | — | — |
| 6 | — | — | — | — | +100 | +100 | — | — |
| 36 | +6,240 | +6,240 | +6,240 | +6,240 | +6,240 | +6,240 | +6,240 | +6,240 |

---

## Resonance System

Milestone rewards tied to advancement stages.

### ConfigEquipment_resonance
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

---

## Suit Set System

### ConfigEquipment_suit (keyed by [suit_id, num])
| Field | Description |
|-------|-------------|
| suit_id | Set ID |
| num | Pieces required |
| effect | Effects granted |
| desc | Bonus description |
| name | Tier name |

### Counting Logic
```
For each equipped item:
    if configEquipment(config_id).suitId == target_suit_id:
        count++
```

Active bonuses shown in gold (#FDF9B8), inactive in gray (#908474).

---

## Equipment Level System

### ConfigEquipment_level (keyed by [part, level])
| Field | Description |
|-------|-------------|
| part | Equipment slot |
| level | Enhancement level |
| basic | Stat multiplier |
| price | Enhancement cost |

### Drop Level Weights
```
[-2, 500], [-1, 1500], [0, 6000], [1, 1500], [2, 500]
```
60% chance of base level, 15% ±1, 5% ±2.

---

## Treasure Box System

| Protocol | Description |
|----------|-------------|
| equip_box_open_c2s | Open single box |
| equip_box_open_all_c2s | Open multiple `{num, quality}` |
| equip_box_lv_c2s | Level up box |

### Auto-Open Thresholds
```
[1,1], [8,2], [12,4], [16,6], [20,8], [24,10], [28,20]
```
At box level X, can auto-open Y at a time.

### Guarantee/Pity
After N opens without high-quality drop → guaranteed minimum quality.

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
