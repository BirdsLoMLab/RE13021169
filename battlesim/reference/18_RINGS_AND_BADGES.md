# 18 — Rings and Badges

> Ring skills, Path trunk links, badge level progression.

---

## Ring System

### ConfigRing (7 fields)

| Field | Description |
|-------|-------------|
| id | Ring ID |
| name | Display name |
| path1 | First Path to Divinity trunk reference |
| path2 | Second Path to Divinity trunk reference |
| icon1/icon2 | Icon assets |
| quality | Rarity tier |

### Path Connection
Each ring references **two Path to Divinity trunks**. This creates thematic links between rings and talent tree branches, suggesting rings enhance/synergize with specific path builds.

---

## Ring Level Progression (ConfigRing_level, 7 fields)

| Field | Description |
|-------|-------------|
| level | Ring level |
| expend_exp | EXP cost |
| expend_goods | Material costs `[[goodsId, count], ...]` |
| attr | Attribute bonuses `[[attrId, value], ...]` |
| base_skill | Skills unlocked/enhanced |
| unlock | Prerequisite (player level/rank) |
| power | Combat power |

### Leveling Flow
1. Accumulate EXP + materials
2. Meet expend_exp and expend_goods requirements → level up
3. New attr replaces previous level's bonuses
4. New base_skill may unlock ring abilities
5. Power contribution increases

---

## Combat Relevance

### Attribute Bonuses
- Standard `[[attrId, value], ...]` format
- AttribDefine IDs (1001=ATK, 1002=HP, etc.)
- Applied additively during stat assembly
- Scale with ring level

### Base Skills
- `base_skill` adds passive/active skills from the ring
- Skills reference ConfigSkill IDs
- Standard skill execution pipeline
- Higher levels may enhance or unlock new skills

---

## Badge System

### Overview
- Single badge type: **Lightkeeper** (ID 9001)
- 25 levels
- Grants **Global Basic ATK DMG (attribute 2023)**

### Level Progression

| Level | Global Basic ATK DMG (2023) |
|-------|-----------------------------|
| 1 | 400 |
| 2 | 700 |
| 3 | 1,000 |
| 4 | 1,400 |
| 5 | 1,800 |
| 6 | 2,100 |
| 7 | 2,400 |
| 8 | 2,800 |
| 9 | 3,100 |
| 10 | 3,500 |
| 11 | 3,800 |
| 12 | 4,100 |
| 13 | 4,500 |
| 14 | 4,800 |
| 15 | 5,200 |
| 16 | 5,500 |
| 17 | 5,800 |
| 18 | 6,200 |
| 19 | 6,500 |
| 20 | 6,900 |
| 21 | 7,200 |
| 22 | 7,500 |
| 23 | 7,900 |
| 24 | 8,200 |
| **25** | **8,600** |

---

## Statue System (Related)

The Statue system is a stat-boosting system with rerollable attribute slots.

### ConfigStatue_attr (6 fields)
| Field | Description |
|-------|-------------|
| id | Entry ID |
| product | Statue type |
| attr_id | AttribDefine ID |
| pro | Probability weight |
| value | Range [min, max] |
| power_rate | Power per value |

### ConfigStatue_level (4 fields)
- Level → quality probability → higher quality distribution
- `pro_quality` = `[[quality, probability], ...]`

### Reroll Mechanics
1. Lock desirable attributes
2. Cost scales with lock count (ConfigStatue_spend)
3. Unlocked slots rerolled from attribute pool
4. Locked slots retained

### Key Difference from Path to Divinity
| Aspect | Statue | Path |
|--------|--------|------|
| Structure | Flat slots | Branching tree |
| Rolling | Rerollable with locks | Permanent |
| Caps | No per-system caps | Per-trunk caps |
