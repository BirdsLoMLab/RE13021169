# 07 — Avians (Spirit Birds / FlyPet)

> ConfigFly system: types, entries, advance levels, skills, breeding, and affixes.

---

## Overview

Avians ("FlyPet" in code, "Spirit Bird" in-game) are flying companions providing passive skills and stat bonuses. Unlike pals, avians use their **own unit config stats** (not inherited from player).

---

## Battle Loading

### setPlayerFlyPet
```javascript
var config = configFly.getDataByKey(flyPetId);
var unitConfig = configUnit.getDataByKey(config.unitid);
// Attributes loaded from unit config directly
for (attr in combatAttributes) {
    unit.attribs[attr.id].baseValue = unitConfig[attr.key];
}
unit.idleIndex = 8;  // Fixed position 8
```

### Key Differences from Pets

| Aspect | Pet/Pal | Avian/FlyPet |
|--------|---------|--------------|
| ATK source | Inherits PARENT's ATK | Own unit config stats |
| HP source | Inherits PARENT's HP | Own unit config stats |
| partner_dam_extra | Inherits from parent | Not used |
| Position | pet_pos + 1 (variable) | Fixed at 8 |
| Attribute calc | getPetFactAttrValue() | Direct from unit config |
| Skill type | PARTNER_SKILL (4) | FLY_SKILL (5) |

---

## ConfigFly Schema (15 fields)

| Field | Description |
|-------|-------------|
| id | Avian ID |
| name | Localized name |
| type | Avian type classification |
| icon | Icon asset |
| quality | Rarity tier |
| hybrid_type | Breeding type |
| unitid | Unit config ID (determines base stats) |
| attr | Attribute bonuses |
| home_weight | Nest placement weights |
| entry_weight | Entry generation weights |
| open_time | Availability window |
| fly_special | Special ability ID (0 = none) |
| fly_tips | Tips/hints |
| scale | Model scale |
| position | Position offset |

---

## Leveling System

### ConfigFly_level (6 fields, keyed by [id, level])

| Field | Description |
|-------|-------------|
| id | Avian type ID |
| level | Level number |
| expend | Currency cost |
| if_advance | Advance gate flag (blocks leveling until advance) |
| attr | Attribute bonuses at this level `[[attrId, value], ...]` |
| power | Combat power |

At certain levels, `if_advance != 0` requires advancing before further leveling.

---

## Advance System

### ConfigFly_advance (7 fields, keyed by [id, advance_level])

| Field | Description |
|-------|-------------|
| id | Avian type ID |
| advance_level | Advance tier |
| expend | Material cost array |
| attr | Attribute bonuses `[[attrId, value], ...]` |
| fly_skill | Skills unlocked at this advance `[[skillId, level], ...]` |
| entry_level | Maximum entry level allowed |
| power | Combat power |

Advancing provides attributes, unlocks skills, and raises the cap on entry levels.

---

## Entry System (Sub-Stats / Affixes)

### ConfigFly_entry (12 fields, keyed by [id, level])

| Field | Description |
|-------|-------------|
| id | Entry ID |
| level | Entry level |
| name | Entry name |
| quality | Quality tier |
| passive_skill | Passive skill array (combat buffs) |
| special_effect | Special effect array |
| home_effect | Non-combat nest effect |
| belong_talent | Talent group assignment |
| desc | Description |
| desc_parm | Description parameters |
| power | Combat power |
| conflict_entry | Incompatible entry IDs |

### Entry Mechanics
- Each avian has multiple entry slots
- Entry count determined at hatching via `entry_num_weight`
- Max entry level gated by advance level (`ConfigFly_advance.entry_level`)
- Entries with `conflict_entry` arrays cannot coexist
- Entries can be rerolled via `ConfigFly_remake_cost`

---

## Hatching System

### ConfigFly_egg (6 fields)

| Field | Description |
|-------|-------------|
| id | Egg ID |
| name | Egg name |
| path | Model path |
| quality | Egg quality |
| fly_weight | Weighted probability for avian species `[[flyId, weight], ...]` |
| entry_num_weight | Weighted probability for entry count `[[count, weight], ...]` |

Higher quality eggs have better weights for rarer avians and more entries.

---

## Breeding / Hybridization

### ConfigFly_hybrid (4 fields, keyed by [id1, id2])

| Field | Description |
|-------|-------------|
| id1 | First parent avian ID |
| id2 | Second parent avian ID |
| template_id | Hybrid template reference |
| fly_weight | Offspring probability `[[flyId, weight], ...]` |

Two avians combine as parents. Offspring species determined by weighted random from `fly_weight`.

### Related Tables
- **ConfigFly_hybird_template** — Breeding result templates
- **ConfigFly_hybrid_time** — Breeding duration (per attempt count)
- **ConfigFly_cd** — Cooldown timers between breeding

---

## Evolution System

### ConfigFly_evolution_pro (keyed by [id, times])
- Evolution progression tracking per attempt count
- `pro` field determines probability

### ConfigFly_evolution_rate (keyed by id)
- `rate` array defines success rates for evolution stages

---

## Achievement System

### ConfigFly_achievement (9 fields)
| Field | Description |
|-------|-------------|
| id | Achievement ID |
| group | Achievement group |
| name/desc | Localized text |
| condition | Unlock conditions |
| reward | Rewards |
| next_id | Next achievement in chain |

### ConfigFly_total_achievement (5 fields)
- Milestone achievements based on total collection progress
- `num` field = required count

---

## Skill Loading

Avian skills use type `FLY_SKILL = 5` and stored separately:
```javascript
if (skill.type == FLY_SKILL) {
    unit.flyPetPassiveSkillList.push(skill)
}
```

### fly_special
Some avians have a `fly_special` value granting a special activatable ability, shown with a dedicated icon in the UI.

---

## Live Swap During Battle

Avians can be swapped mid-battle:
1. Remove existing FlyPet units
2. Unload old passive skills (`unloadFlyPetPassiveSkill`)
3. Load new avian via `setPlayerFlyPet`
4. Add new units to battle
5. Reposition units
