# 06 — Pals and Pets

> 322 pets, 55 races, deploy effects, damage formulas, and the talent system.

---

## Battle Loading

Pals are loaded as separate units that **inherit the parent player's ATK**.

### Inherited Attributes from Player

| Attribute | ID | Inherited |
|-----------|------|-----------|
| att | 1001 | Yes — Pal uses PARENT's ATK |
| hp | 1002 | Yes — Pal uses PARENT's HP |
| partner_dam_extra | 1047 | Yes — Pal damage scaling |
| skill_dam_extra | 1045 | Server only |
| skill_crit_rate | 1037 | Server only |
| skill_crit_dam | 1038 | Server only |
| boss_dam | 1046 | Server only |

### Attribute Calculation (getPetFactAttrValue)
```
final = base + pet_bonus(petId, attrId) + global_bonus(0, attrId)

For each group_attr in attribute_group(attrId):
    group_sum = pet_bonus(petId, group_attr) + global_bonus(0, group_attr)
    multiplier = round(round(group_sum / 10000) + 1)
    final = roundInt(final * multiplier)
```

---

## Pal Damage Formulas

### Basic Attack (normalHurt for Partner type)
```
base_raw   = max(roundInt(PARENT_ATK - DEF * (1 + DEF_COE)), 1)
pal_mult   = round(PARTNER_DAM * PARTNER_DAM_EXTRA)
resistance = calSuppressAndInspire(target, parent, PARTNER_RESIST)
pal_dmg    = roundInt(base_raw * round(pal_mult * round(1 - resistance)))
pal_dmg    = calHurt(pal_dmg, target, pal)
if CRIT:
    pal_dmg = roundInt(pal_dmg * max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF))))
result     = max(1, pal_dmg)
```

### Combo Attack (normalDoubleHurt for Partner type)
```
pal_base  = roundInt(max(roundInt(PARENT_ATK - DEF*(1+DEF_COE)), 1) * pal_mult)
            * round(1 - resistance)
pal_combo = roundInt(roundInt(pal_base) * DOUBLE_HIT_DAM)
```
Combo multiplier applied AFTER pal damage, not combined with partner_dam.

### HP-Based Damage Clamping for Pals
```
att_dam modified: att_dam * partner_dam * partner_dam_extra
Clamp limits for pal HP% skills: [0.8, 2000] (min 80% base, max 2000× base)
```

---

## Key Attributes

| Attribute | ID | Owner | Description |
|-----------|------|-------|-------------|
| partner_dam | 1040 | Pal | Base damage multiplier (from ConfigPetlevel) |
| partner_dam_extra | 1047 | Player | Additional pal damage multiplier |
| partner_resist | 1020 | Target | Resistance to pal damage (**cap ~80%**) |
| partner_inspire | 1074 | Attacker | Inspire bonus (reduces resist) |
| partner_suppress | 1077 | Target | Suppress (increases resist) |

---

## ConfigPet Schema (12 fields)

| Field | Description |
|-------|-------------|
| id | Pet ID |
| name | Localized name |
| icon | Icon asset |
| desc | Description |
| quality | Rarity tier (3-8) |
| type | Race type array |
| unitId | Unit config ID |
| talent | Talent slots `[[talent_group, talent_tier], ...]` |
| power | Combat power |
| if_activity | Activity-gated |
| if_season | Season-gated |
| open_time | Availability window |

---

## ConfigPetlevel (64 Combat Stats)

Each pet level defines 64 XOR-encoded combat fields including:
```
partner_dam, def, hp, att_range, detection_range, att_speed,
crit_rate, crit_dam, crit_def, boss_dam, double_hit, hit, miss,
speed, vertigo, suspend, target_num, double_hit_dam,
skill_dam_extra, power_recovery, att_hpsteal, skill_hpsteal,
skill_crit_rate, skill_crit_dam, hp_recovery, counter, att_resist,
skill_resist, partner_resist, resist, suspend_def, vertigo_def,
att_hpsteal_def, skill_hpsteal_def, vertigo_times, vertigo_res,
counter_dam, double_hit_def, counter_def, counter_suspend,
ignore_double_hit, ignore_counter, boss_def, hpsteal_rate,
hpsteal_amount, ignore_hpsteal, hpsteal_res, pve_dam, pve_resist,
shield_time_extra, shield_hp_extra, skillbuff_time_all, control_res,
total_dam_add, total_dam_def
```

---

## Pet Races (55 Total)

| ID | Race | ID | Race | ID | Race |
|----|------|----|------|----|------|
| 1 | Cat | 2 | Specter | 3 | Snow Sprite |
| 4 | Cactus | 5 | Chicken | 6 | Sprite |
| 7 | Panda | 8 | Snail | 9 | Deer |
| 10 | Turtle | 11 | Octopus | 12 | Dog |
| 13 | Lizard | 14 | Dragon | 15 | Fox |
| 16 | Banana | 17 | Toothpaste | 18 | Mecha Dragon |
| 19 | Bear | 20 | Pig | 21 | Mouse |
| 22 | Bird | 23 | Eggplant | 24 | Rabbit |
| 25 | Alpaca | 26 | Snake | 1003 | Pepe |
| 1004 | Spritefox | 1005 | Hellflame Feather | 1008 | Puppy Fervor |
| 1080 | Skeleton Minion | 1081 | Camel | 1082 | Blackeye |
| 1098 | Vermillion Bird | 1099 | B.Duck | 3001-3005 | Named Pals |

---

## Quality Distribution

| Quality | Name | Count | Power Range |
|---------|------|-------|-------------|
| 3 | Blue | ~50 | 5,500 |
| 4 | Purple | ~50 | 6,000 |
| 5 | Gold | ~50 | 7,000 |
| 6 | Orange | ~60 | 8,000 |
| 7 | Red | ~60 | 9,000 |
| 8 | Pink | ~50 | 9,500 |

---

## Talent System

### ConfigPet_talent (9 fields)
| Field | Description |
|-------|-------------|
| id | Talent ID |
| all_star | Total star level required |
| name | Talent name |
| effect_des | Effect description |
| desc_parm1 | Description params |
| effect | Stat bonus array |
| power_des | Power description |
| desc_parm2 | Power params |
| power | Power bonus |

Talents unlock at star thresholds. Each pet's `talent` field defines available talent slots as `[[talent_group, talent_tier], ...]`.

---

## Proficiency System

### ConfigPet_proficiency (indexed by [id, level])
| Field | Description |
|-------|-------------|
| id | Proficiency type ID |
| level | Proficiency level |
| exp | EXP required |
| addexp | Additional EXP |
| extra_star | Bonus stars granted |
| own_attrs | Attribute bonuses |
| power | Power contribution |

Proficiency bonuses feed into `getPetFactAttrValue()` as group multiplier data.

---

## Pet Skill Loading

Pet skills use type `PARTNER_SKILL = 4` and are stored in a separate `petPassiveSkillList` on the player unit:
```javascript
if (skill.type == PARTNER_SKILL) {
    unit.petPassiveSkillList.push(skill)
}
```

---

## PvP Pal Mechanics Summary

- Pal resistance (1020) caps at **80%** — cannot fully negate pal damage
- Pal damage uses PARENT's ATK (not pal's own ATK)
- Inspire/Suppress uses the same mechanic as Pierce/Block but for pal damage
- Pal damage is affected by Total DMG Bonus/RES (1081/1082)
- Pal damage is divided by injuryReduce in PvP like all other damage
