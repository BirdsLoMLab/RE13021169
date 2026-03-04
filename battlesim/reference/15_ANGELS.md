# 15 — Angels (Guardian Spirits)

> Formation, battle skills, star progression, and energy pool.

---

## Overview

Angels ("Guardian Spirits") are companion units that boost stats, contribute battle skills, and provide passive development effects. They're organized into a typed formation with an energy budget system.

---

## Formation System

### ConfigAngel_array
| Field | Description |
|-------|-------------|
| type | Formation type |
| pos | Slot position (1-based) |
| pos_type | Angel type allowed in this slot |

### Two Formation Groups

**Main Slots (1-3):** Contribute battle skills directly
- Slot 1: Primary slot with Skill 1
- Slots 2-3: Use Skill 2 from ConfigAngel_skill

**Development Slots (1-4):** Provide passive development bonuses

### Energy Pool
All angel skills share a single energy pool:
```
all_cost1 = sum of battle_skill1_cost + battle_skill2_cost for main slots
all_cost2 = sum of develop_cost for development slots
Display: cost + "/" + maxBudget
```

---

## ConfigAngel (9 fields)

| Field | Description |
|-------|-------------|
| id | Angel identifier |
| name | Localized name |
| quality | Rarity tier (1-5) |
| type | Type class (formation slot matching) |
| desc | Description |
| image/image2/image3 | Portrait assets |
| open_time | Availability window |

---

## ConfigAngel_star (16 fields, keyed by [id, star])

| Field | Description |
|-------|-------------|
| id | Angel ID |
| star | Star level |
| expend | Upgrade cost `[[itemId, count], ...]` |
| frame | UI frame asset |
| attr | Stat bonuses `[[attrId, value], ...]` |
| skill1_type | Skill 1 category (1=active, 2=passive, 3=aura) |
| battle_skill1 | Skill 1 `[[skillId, skillLevel]]` → ConfigSkill_level |
| battle_skill1_cost | Energy cost |
| skill2_type | Skill 2 category |
| battle_skill2 | Skill 2 ID → ConfigAngel_skill |
| battle_skill2_cost | Energy cost |
| develop_effect | Development passive data |
| develop_desc | Development description |
| develop_desc_num | Description parameters |
| develop_cost | Development energy cost |
| power | Combat power |

---

## Skill System

### Skill Slot 1
- References standard ConfigSkill + ConfigSkill_level
- Lookup: `configSkill_level.getDataByKeys("id", skillId, "level", skillLevel)`
- `skill1_type` determines visual badge (1/2/3)

### Skill Slot 2
- References ConfigAngel_skill directly
- Lookup: `configAngel_skill.getDataByKey(battle_skill2)`

### ConfigAngel_skill (6 fields)
| Field | Description |
|-------|-------------|
| id | Skill ID |
| skill_name | Localized name |
| skill_effect | Effect IDs triggered |
| skillPar | Damage coefficients |
| skill_dec | Description template |
| desc_parm | Description parameters |

---

## Gacha / Draw System

### Permanent Banners (ConfigAngel_draw, 11 fields)
| Field | Description |
|-------|-------------|
| id | Banner ID |
| type | Banner type |
| cost/cost2 | Single/multi pull costs |
| prob | Quality tier probabilities |
| must | Pity thresholds |

### Limited-Time Banners (ConfigAngel_draw_time_limit, 18 fields)
Adds rate-up mechanics:
- `is_up` — rate-up active flag
- `prob_up` — rate-up probabilities
- `up_reward` — featured angel rewards
- `special_rewards_times` — special reward trigger count

---

## Combat Integration

1. **Skill 1** enters standard skill execution pipeline
2. **Skill 2** triggers via ConfigAngel_skill.skill_effect chain
3. **Development effects** apply as passive modifiers
4. **Star attrs** added to player's combat attributes

---

## Dependencies

- ConfigSkill / ConfigSkill_level — Skill 1 references
- ConfigSkilleffcet — Effect chain execution
- ConfigBuff — Buffs from angel skills
- AttribDefine — Attribute IDs for stat bonuses
