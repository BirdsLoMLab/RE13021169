# 05 — Active Skills

> All active skills with IDs, parameters, and the skill effect system.

---

## Skill System Architecture

### ConfigSkill Schema (14 fields)
| Field | Description |
|-------|-------------|
| id | Skill ID |
| name | Localized name |
| type | 1=Active, 2=Passive_Add, 3=Passive_Effect, 4=Partner_Skill, 5=Fly_Skill |
| priority | Execution priority |
| desc | Description |
| cd | Cooldown (seconds) |
| cost | Energy cost |
| par | Base skill parameter (damage %) |
| effect | Effect IDs triggered by this skill |
| release_time | Cast time |
| is_show | UI visibility |
| icon | Icon asset |
| ownEffect | Owner stat modifications [[attrId, value], ...] |
| level_up_desc | Level-up description |

### ConfigSkill_level Schema (8 fields)
| Field | Description |
|-------|-------------|
| id | Skill ID |
| level | Skill level |
| cd | Cooldown at this level |
| cost | Energy cost at this level |
| par | Damage parameter at this level |
| desc_parm | Description format parameters |
| ownEffect | Stat mods at this level |
| effect | Effects at this level |

---

## T5 Active Skills (8 Total)

All T5 actives have the same base damage scaling at lv220: **~15157-15166% AoE DMG**.

| ID | Skill Name | Class | Unique Effect |
|----|-----------|-------|---------------|
| 1053 | Blades Reunion | Martial Sage | -40% Counter DMG RES; each counter deals +1% target current HP |
| 1054 | Shattering Axe | Warbringer | -40% Counter DMG RES; gain 0.15 DEF per ATK + 0.75 ATK per DEF for 8s |
| 1055 | Piercing Boneforge | Sacred Hunter | -40% Combo DMG RES; block energy regen on 6 skills for 4s |
| 1056 | Sun Pursuit | Plume Monarch | -40% Combo DMG RES; ignore enemy evasion for 10s |
| 1057 | Crane's Whisper | Prophet | -20% Skill DMG RES; break enemy shields instantly for 10s |
| 1058 | Galaxy Dive | Darklord | -20% Skill DMG RES; +50% Skill Crit DMG for 10s |
| 1066 | Tamer of Beasts | Beastmaster | -20% Pal DMG RES; pals ignore evasion for 10s |
| 1067 | Wilting Souls | Supreme Spirit | -20% Pal DMG RES; pals 40% chance +1% target HP for 8s |

---

## Skill Effect System

### EffectTriggerType Enum (15 Types)

| ID | Name | When Triggered |
|----|------|----------------|
| 0 | Active | Manually activated |
| 1 | Start | Battle start |
| 2 | Passive | Always active |
| 4 | Counter | On counter attack |
| 5 | HP_Hurt | When HP damaged |
| 6 | HP_Heal | When HP healed |
| 7 | Kill | On kill |
| 8 | Dead | On death |
| 9 | Crit | On critical hit |
| 10 | Dodge | On dodge |
| 11 | Double | On combo trigger |
| 12 | Normal | On normal attack |
| 13 | Stun | On stun trigger |
| 14 | Shield | On shield break |
| 16 | GetDodge | When dodged by target |

### ConfigSkilleffcet Schema (16 fields)

| Field | Description |
|-------|-------------|
| id | Effect ID |
| trigger_type | EffectTriggerType |
| trigger_probability | Trigger chance (/10000) |
| trigger_parm | Trigger parameters |
| effect_id | Buff IDs to apply |
| effect_duration | Buff durations |
| effect_target | Target selection |
| effect_par | Effect parameters (skillPar override) |
| bullet_num | Number of projectiles |
| parse_skill | Secondary skill to trigger |
| parse_probability | Secondary trigger chance |
| parse_target | Secondary target |
| parse_parm | Secondary parameters |
| delay_time | Delay before effect triggers |
| T1045 | Flag: if true, skip skill_dam_extra modifier |
| is_share_damage | Flag: if true, damage is shared type |

### Effect Chain Flow
```
1. Skill activates → effect[] array lists ConfigSkilleffcet IDs
2. Each effect checks trigger_type and trigger_probability
3. On trigger: applies buff(effect_id) with duration(effect_duration) to target(effect_target)
4. If parse_skill != 0: chain into another skill (recursive)
5. If parse_probability check passes: apply parse effects
```

---

## Passive Skill IDs by Class

### Warriors (Shared Lv30-40)
| ID | Level | Effect |
|----|-------|--------|
| 2001 | Lv30 | Counter +30%, Counter Mult +30% |
| 2005 | Lv40 | DEF +30% |

### Martial Sage Exclusive
| ID | Level | Effect |
|----|-------|--------|
| 2008 | Lv50 | DMG RES +15% |
| 2033 | Lv70 | 8% Max HP regen every 5s |
| 2022 | Lv100 | Shield = 8% max HP every 10s |

### Warbringer Exclusive
| ID | Level | Effect |
|----|-------|--------|
| 2020 | Lv50 | Counter DMG +140% |
| 2123 | Lv70 | 20% AoE counter on hit |
| 2028 | Lv100 | Per 10% HP lost → ATK +3% |

### Archers (Shared Lv30-40)
| ID | Level | Effect |
|----|-------|--------|
| 2003 | Lv30 | Combo +30% |
| 2007 | Lv40 | ATK SPD +15%, Hit +10% |

### Sacred Hunter Exclusive
| ID | Level | Effect |
|----|-------|--------|
| 2021 | Lv50 | Crit DMG +20% |
| 2126 | Lv70 | Basic ATK deals +1% target current HP |
| 2031 | Lv100 | After crit → ATK +40% for 1s |

### Plume Monarch Exclusive
| ID | Level | Effect |
|----|-------|--------|
| 2013 | Lv50 | Combo DMG +140% |
| 2118 | Lv70 | +3 extra combo bullets |
| 2032 | Lv100 | +2 extra basic attack bullets |

### Mages (Shared Lv30-40)
| ID | Level | Effect |
|----|-------|--------|
| 2002 | Lv30 | Skill Crit +15% |
| 2004 | Lv40 | ATK +12% |

### Prophet Exclusive
| ID | Level | Effect |
|----|-------|--------|
| 2016 | Lv50 | Energy Regen +20% |
| 2124 | Lv70 | Prolong skills +40%, DMG +10% |
| 2029 | Lv100 | Per stun → skill CD -0.3s |

### Darklord Exclusive
| ID | Level | Effect |
|----|-------|--------|
| 2017 | Lv50 | Skill Crit DMG +50%, Skill Crit +15% |
| 2125 | Lv70 | 20% extra true DMG on skills |
| 2030 | Lv100 | Per 10% HP lost → Skill DMG +3% |

### Beast (Shared Lv30-40)
| ID | Level | Effect |
|----|-------|--------|
| 2101 | Lv30 | +1 Pal slot |
| 2102 | Lv40 | Pal SPD +10%, Hit +10% |

### Beastmaster Exclusive
| ID | Level | Effect |
|----|-------|--------|
| 2103 | Lv50 | Pal Crit +25%, Crit DMG +20% |
| 2114 | Lv70 | Pal DMG Mult +20% |
| 2105 | Lv100 | Per 10% HP lost → Pal DMG +3% |

### Supreme Spirit Exclusive
| ID | Level | Effect |
|----|-------|--------|
| 2106 | Lv50 | Deploy Effects +20% |
| 2117 | Lv70 | Race-based bonus (first 2 pals) |
| 2108 | Lv100 | Race-count-based bonus |

---

## Skill Damage Pipeline (BuffSkillValue)

11 calculation types (`calType`):

| Type | Name | Formula |
|------|------|---------|
| 0 | Attribute | Uses param3 attribute directly |
| 1 | ATK-DEF | `max(roundInt(ATK - DEF*(1+DEF_COE)), 1)` |
| 2 | HP Difference | Target max HP - current HP |
| 3 | Current HP | `current_HP * skillPar` |
| 4 | Max HP | `max_HP * skillPar` |
| 5 | Partner Damage | Pal-specific calculation |
| 6 | Fixed Value | `skillPar` directly |
| 7 | Attribute Ratio | Attribute value * skillPar |
| 8 | ATK Only | `ATK * skillPar` |
| 9 | DEF Only | `DEF * skillPar` |
| 10 | Combined | Multi-attribute formula |

### Post-Calculation Chain
```
1. Base damage from calType
2. × skillPar × active_skilldamage_par
3. + SKILL_DAMAGE_ADD flat bonus
4. × skill_dam_extra (unless T1045 flag)
5. Skill crit check → × (1 + skill_crit_dam) → pow(0.98)
6. Normal crit check (if UseCrit) → × max(1.5, crit_dam / max(0.5, crit_def))
7. × boss_dam
8. × RECORD_DAMAGE bonus
9. × (1 - skill_resist) resistance
10. calHurt (DMG RES, PvE)
11. EXTRA_DAMAGE → GIANT_SLAYER
12. healthTarget (Total DMG, shields, HP)
```
