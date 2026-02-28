# LOM Master Formula Reference

**Source:** `game_script_pretty.js` (457,538 lines)
**Date:** 2026-02-28
**Status:** Reverse-engineered from code — authoritative reference

---

## Table of Contents
1. [Math Primitives](#1-math-primitives)
2. [Attribute System](#2-attribute-system)
3. [Damage Formulas](#3-damage-formulas)
4. [Critical Hit System](#4-critical-hit-system)
5. [PvP System](#5-pvp-system)
6. [HP-Based Damage](#6-hp-based-damage)
7. [Bleed Damage](#7-bleed-damage)
8. [Shield System](#8-shield-system)
9. [Pierce / Block](#9-pierce--block)
10. [Pal Inspire / Suppress](#10-pal-inspire--suppress)
11. [Stun & Control](#11-stun--control)
12. [Ignore Mechanics](#12-ignore-mechanics)
13. [Buff Damage Modifiers](#13-buff-damage-modifiers)
14. [Damage Application Pipeline](#14-damage-application-pipeline)
15. [Config Constants](#15-config-constants)
16. [Key Discrepancies vs Community Docs](#16-key-discrepancies)

---

## 1. Math Primitives

### FixMath.round(x) — Line 292606
```
round(x) = (x > 0 ? floor(10000 × x + 0.5) : ceil(10000 × x - 0.5)) / 10000
```
Rounds to 4 decimal places. Used throughout all formulas.

### FixMath.roundInt(x) — Line 292608
```
roundInt(x) = floor(round(x))
```
Rounds to 4 decimals, then floors to integer.

**CRITICAL:** The game applies roundInt at EVERY multiplication step. Simulators MUST replicate this to match game values exactly.

---

## 2. Attribute System

### MetaAttrib Value Formula (Line 349642)
```
value = roundInt(roundInt(baseValue + _addValue) × _time + _addExtraValue)
if (up_limit ≠ 0): value = min(value, up_limit)
if (num_type = 2): value = round(value / 10000)   // percentage display
```

**Components:**
- `baseValue` — from server (set during stat assembly)
- `_addValue` — flat bonuses from buffs/effects (stacks additively)
- `_time` — multiplicative modifier (starts at 1.0, `addMultiples(x)` → `_time += x`, `multiple(x)` → `_time *= x`)
- `_addExtraValue` — post-multiplier flat bonus

**Anti-cheat:** `_checkValue = baseValue XOR 32`, verified via `checkCheat()`

### Key Attribute IDs (AttribDefine, Line 349634)

| ID | Name | Description |
|----|------|-------------|
| 1001 | att | Attack |
| 1002 | hp | Hit Points |
| 1003 | att_speed | Attack Speed |
| 1004 | crit_rate | Critical Rate |
| 1005 | crit_dam | Critical Damage |
| 1006 | crit_def | Critical Defense (min 0.5) |
| 1007 | hit | Accuracy |
| 1008 | miss | Evasion |
| 1016 | double_hit | Combo Rate |
| 1017 | counter | Counter Rate |
| 1018 | att_resist | Basic ATK Resistance |
| 1019 | skill_resist | Skill Resistance |
| 1020 | partner_resist | Pal Resistance |
| 1021 | resist | DMG Resistance |
| 1024 | def | Defense |
| 1032 | double_hit_dam | Combo Damage Multiplier |
| 1033 | counter_dam | Counter Damage Multiplier |
| 1034 | double_hit_def | Combo Resistance |
| 1035 | counter_def | Counter Resistance |
| 1037 | skill_crit_rate | Skill Crit Rate |
| 1038 | skill_crit_dam | Skill Crit Damage |
| 1039 | att_dam | Basic ATK Multiplier |
| 1040 | partner_dam | Pal Damage Multiplier |
| 1043 | active_skilldamage_par | Skill Damage Factor |
| 1045 | skill_dam_extra | Skill Damage Extra |
| 1046 | boss_dam | Boss Damage Bonus |
| 1047 | partner_dam_extra | Pal Damage Extra |
| 1048 | ignore_double_hit | Ignore Combo Rate |
| 1049 | ignore_counter | Ignore Counter Rate |
| 1051 | shield_hp_extra | Shield HP Bonus |
| 1057 | pve_dam | PvE Damage Bonus |
| 1058 | pve_resist | PvE Resistance |
| 1060 | def_coe | Defense Coefficient |
| 1065 | ignore_crit_rate | Ignore Crit Rate |
| 1066 | ignore_hp_recovery | Ignore Heal |
| 1067 | armor_penetration_rate | Armor Pen Rate |
| 1068 | armor_penetration | Armor Pen Value |
| 1071 | block | Block Value |
| 1081 | total_dam_add | Total DMG Bonus |
| 1082 | total_dam_def | Total DMG Resistance |

---

## 3. Damage Formulas

### 3.1 Base Damage (Common to All Types)
```
effective_def = roundInt(DEF × (1 + DEF_COE))
base_raw = max(roundInt(ATK - effective_def), 1)
```
**Note:** `DEF_COE` (1060) applies to ALL damage types. Community docs miss this.

### 3.2 Basic ATK (normalHurt) — Line 322756
```
resistance = calArmorAndBlock(target, attacker, ATT_RESIST, att_resist_id)
damage = roundInt(base_raw × round(ATT_DAM × round(1 - resistance)))
damage = calHurt(damage, target, attacker)
if CRIT: damage = roundInt(damage × max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF))))
result = max(1, damage)
```

### 3.3 Combo/Double Hit (normalDoubleHurt) — Line 322839
```
resistance = calArmorAndBlock(target, attacker, DOUBLE_HIT_DEF, double_hit_def_id)
damage = roundInt(base_raw × DOUBLE_HIT_DAM) × round(1 - resistance)
damage = roundInt(damage)
damage = calHurt(damage, target, attacker)
if CRIT: damage = roundInt(damage × max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF))))
result = max(1, damage)
```

### 3.4 Counter (normalCounterHurt) — Line 322869
```
resistance = calArmorAndBlock(target, attacker, COUNTER_DEF, counter_def_id)
damage = roundInt(base_raw × COUNTER_DAM) × round(1 - resistance)
damage = roundInt(damage)
damage = calHurt(damage, target, attacker)
if CRIT: damage = roundInt(damage × max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF))))
result = max(1, damage)
```

### 3.5 Skill (SkillHurt) — Line 322967
```
resistance = calArmorAndBlock(target, attacker, SKILL_RESIST, double_hit_def_id)
damage = roundInt(base_raw × SKILL_DAM_EXTRA) × round(1 - resistance)
damage = roundInt(damage)
damage = calHurt(damage, target, attacker)
if CRIT: damage = roundInt(damage × max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF))))
result = max(1, damage)
```

### 3.6 Pal Basic ATK — Line 322765
```
ATK = PARENT.ATK     (uses parent player's ATK)
pal_mult = round(PARTNER_DAM × PARENT.PARTNER_DAM_EXTRA)
resistance = calSuppressAndInspire(target, parent, PARTNER_RESIST)
damage = roundInt(base_raw × round(pal_mult × round(1 - resistance)))
damage = calHurt(damage, target, attacker)
if CRIT: same as normal crit
result = max(1, damage)
```

### 3.7 calHurt (DMG Resistance) — Line 322831
```
calHurt(damage, target, attacker):
    damage = roundInt(damage × round(1 + PVE_DAM))
    damage = roundInt(roundInt(damage × round(1 - RESIST)) × round(1 - PVE_RESIST))
    return max(1, damage)
```
Where `RESIST` = attribute 1021 (DMG Resistance).

---

## 4. Critical Hit System

### 4.1 Normal Crit (checkHit) — Line 322896
```
effective_crit = max(CRIT_RATE - IGNORE_CRIT_RATE, 0)
raw_evasion = max(round(MISS - HIT), 0)
corrected_evasion = round((100 × raw_evasion)^0.9 / 100)
In PvP: final_evasion = min(corrected_evasion, 0.80)
In PvE: final_evasion = corrected_evasion

P(miss) = final_evasion
P(normal) = (1 - evasion) × (1 - effective_crit)
P(crit) = (1 - evasion) × effective_crit
```

### 4.2 Crit Damage Multiplier
```
crit_mult = max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF)))
crit_damage = roundInt(base_damage × crit_mult)
```

### 4.3 Skill Crit (checkSkillCirt) — Line 322956
```
probability = roundInt(10000 × SKILL_CRIT_RATE)
triggers if random(0, 10000) < probability

skill_crit_damage = roundInt(Math.pow(roundInt(damage × round(1 + SKILL_CRIT_DAM)), 0.98))
```
**NOTE:** The 0.98 exponent is on the PRODUCT `(damage × (1+SCRIT))`, not on `(1+SCRIT)` alone.

---

## 5. PvP System

### 5.1 PvP Factor Calculation — Line 197543
```
1v1:  avg_level = roundInt((player1_level + player2_level) / 2)
Team: avg_level = roundInt(sum_all_levels / player_count)
injuryReduce = round(configLevel[avg_level].pvp_injury_reduce / 10000)
```

### 5.2 PvP Damage Reduction — Line 449285
```
final_damage = max(roundInt(pre_pvp_damage / injuryReduce), 1)
```

### 5.3 PvP Shield Decay — Line 195201
```
shieldDecay = round(shield_correct / 10000) = 0.4 (default)
shield_hp = roundInt(base_shield × shieldDecay)  [when _isDec == 0]
```

### 5.4 PvP Heal Decay — Line 449335
```
treatDecay = round(hp_recovery_correct / 10000) = 0.3 (default)
heal = roundInt(base_heal × treatDecay)
```

---

## 6. HP-Based Damage

### Formula (BuffSkillValue._calHpHurt) — Line 195792
```
hp_dmg = roundInt(hp_value × skillPercent)
hp_dmg = roundInt(hp_dmg × injuryReduce)       [multiply UP]
if _limit exists:
    base_atk = roundInt(max(roundInt(ATK - DEF×(1+DEF_COE)), 1) × ATT_DAM)
    min_dmg = roundInt(base_atk × _limit[0])
    max_dmg = roundInt(base_atk × _limit[1])
    hp_dmg = clamp(hp_dmg, min_dmg, max_dmg)
healthTarget(target, hp_dmg, Hurt)
→ In healthTarget: hp_dmg = round(hp_dmg × max(1 + total_dam_add - total_dam_def, 0.20))
→ At Unit.addDamage: final = max(roundInt(hp_dmg / injuryReduce), 1)  [divide DOWN]
```

**Total DMG Bonus/RES DOES affect HP-based damage** — `Hurt` is in `NeedAddDamHurtList`.

---

## 7. Bleed Damage

### 8 Bleed Types (BuffBleed) — Line 192770

| Type | Formula |
|------|---------|
| 0 | (ATK-DEF_eff) × ATT_DAM × calHurt → can GIANT_SLAYER |
| 1 | current_HP × skillPar × injuryReduce |
| 2 | (ATK-DEF_eff) × SKILL_DAM_EXTRA × skillPar × (1-SKILL_RESIST) → can skill crit (×0.98 exp) |
| 3 | (ATK-DEF_eff) × ATT_DAM × (1-ATT_RESIST) × calHurt → can normal crit |
| 4 | (ATK-DEF_eff) × DOUBLE_HIT_DAM × (1-DOUBLE_HIT_DEF) × calHurt → can normal crit |
| 5 | (ATK-DEF_eff) × COUNTER_DAM × (1-COUNTER_DEF) × calHurt → can normal crit |
| 6 | max_HP × skillPar × injuryReduce |
| 10 | target/caster attribute × skillPar × injuryReduce |

---

## 8. Shield System

### Shield Creation (BuffShield) — Line 195180
```
shield_hp = roundInt(base × skillPar)
shield_hp = roundInt(shield_hp × round(1 + SHIELD_HP_EXTRA))
if _isDec == 0: shield_hp = roundInt(shield_hp × shieldDecay)
```

### Shield Absorption — Line 195235
```
absorbed = min(shield_remaining, incoming_damage)
damage_through = incoming_damage - absorbed
```
- Multiple shields iterate sequentially
- Damage overflows past depleted shields
- Shield check occurs AFTER PvP reduction

---

## 9. Pierce / Block

### calArmorAndBlock — Line 322773
```
Can pen?   → armor_penetration > ignore_armor_penetration
Can block? → block > ignore_block

Mutually exclusive random check (pen has priority)

If PIERCE: resistance -= min(0.5, (pen - ignore_pen) / 10000)
If BLOCK:  resistance += min(0.5, (block - ignore_block) / 10000)
Final: capped by attribute's up_limit config
```

---

## 10. Pal Inspire / Suppress

### calSuppressAndInspire — Line 322802
```
Identical structure to Pierce/Block but for Pal damage:

If SUPPRESS: pal_resist -= min(0.5, (inspire - ignore_inspire) / 10000)
If INSPIRE:  pal_resist += min(0.5, (suppress - ignore_suppress) / 10000)
```

---

## 11. Stun & Control

### Stun Check (checkDizz) — Line 322947
```
effective_stun = max(0, round(VERTIGO - VERTIGO_DEF))
corrected = round((100 × effective_stun)^0.9 / 100)
probability = roundInt(10000 × corrected)
triggers if random(0, 10000) <= probability
```

### Stun Duration — Line 430036
```
duration = round(VERTIGO_TIMES × round(1 - VERTIGO_RES))
```

### Knockup Check (checkThrowHit) — Line 322933
```
effective = round(SUSPEND - SUSPEND_DEF)
probability = roundInt(10000 × effective)
triggers if random(0, 10000) <= probability
```
Note: Knockup does NOT use the 0.9 power correction.

---

## 12. Ignore Mechanics

**ALL ignores are SUBTRACTIVE:**
```
effective_rate = max(rate - ignore_rate, 0)
```

| Mechanic | Rate Attrib | Ignore Attrib |
|----------|------------|---------------|
| Crit | crit_rate (1004) | ignore_crit_rate (1065) |
| Combo | double_hit (1016) | ignore_double_hit (1048) |
| Counter | counter (1017) | ignore_counter (1049) |
| Armor Pen | armor_penetration (1068) | ignore_armor_penetration (1069) |
| Block | block (1071) | ignore_block (1072) |
| Pal Inspire | partner_inspire (1074) | ignore_partner_inspire (1075) |
| Pal Suppress | partner_suppress (1077) | ignore_partner_suppress (1078) |
| HP Steal | hpsteal_rate (1053) | hpsteal_res (1055) |

---

## 13. Buff Damage Modifiers

### BuffExtraDamage (EXTRA_DAMAGE) — Line 193978
Applied multiplicatively after base damage:
```
Type 0: damage × (1 + skillPar)                    [flat %]
Type 1: damage × (1 + (maxHP - currentHP)/maxHP × skillPar)  [HP loss %]
Type 2: same as 1 but with CURRENT_HP buff correction
```

### BuffGiantSlayer (GIANT_SLAYER) — Line 194158
HP-difference-based damage bonus:
```
if target_HP > caster_HP:
    hp_diff = ceil(round((target_HP - caster_HP) / caster_HP × 100))
    bonus = round(hp_diff × extraDam)
    bonus = min(bonus, maxForBoss_or_maxForUnit)
    damage = round(damage × (1 + bonus / 10000))
```

### BuffSkillFragileAdd (FRAGILE_EFFECT) — Line 195457
ADDITIVE flat damage:
```
Type 0: bonus = roundInt(attacker_attribute × skillPar)
Type 1: bonus = roundInt(target_currentHP × skillPar)
damage += bonus
```

---

## 14. Damage Application Pipeline

### Complete Order

#### In healthTarget() (game_script.js line 7229):
```
0. Total DMG Bonus/Res (if healthType in NeedAddDamHurtList && attacker != target):
   damage = round(damage × max(1 + total_dam_add - total_dam_def, 0.20))
```

#### In Unit.addDamage (Line 449270):
```
1. runningToPart check → skip if transitioning
2. PvP reduction: damage = max(roundInt(damage / injuryReduce), 1)
3. Season PvE bonus (team 1 only)
4. Shield absorption (iterates all shields)
5. Block absorption
6. HP -= remaining damage
7. Death prevention checks (Time Reversal → Remake HP → Immune Death)
8. If immuneDeath: HP = max(HP, 1)
9. Total damage accumulation
10. HP change triggers
11. Death if HP <= 0
```

### For Healing Types
```
1. Heal decay: heal = roundInt(heal × treatDecay)
2. REDUCE_HEAL buff modifications
3. HP += heal, capped at maxHP
```

---

## 15. Config Constants

### Battle Global Defaults (Line 235658+)
| Constant | Value | Divided by 1e4 | Meaning |
|----------|-------|----------------|---------|
| miss_correct | 9000 | 0.9 | Evasion power exponent |
| vertigo_correct | 9000 | 0.9 | Stun power exponent |
| shield_correct | 4000 | 0.4 | PvP shield decay |
| hp_recovery_correct | 3000 | 0.3 | PvP heal decay |
| battle_up_limit | [[1008, 8000]] | 0.8 | PvP evasion cap (80%) |
| total_damage_add_down_limit | 2000 | 0.2 | Total DMG floor (20%) |

### ConfigLevel Schema (Line 243004)
| Index | Field | Description |
|-------|-------|-------------|
| 0 | level | Level number |
| 3 | pvp_injury_reduce | PvP factor (÷10000) |

---

## 16. Key Discrepancies vs Community Docs

| # | Issue | Community Says | Code Shows |
|---|-------|---------------|------------|
| 1 | **DEF_COE** | Not mentioned | DEF × (1 + def_coe) in ALL formulas |
| 2 | **Skill Crit Exponent** | `Skill × (1+SCRIT)^0.98` | `(Skill × (1+SCRIT))^0.98` |
| 3 | **Total DMG Scope** | Final layer on all damage | CONFIRMED — universal via healthTarget() |
| 4 | **Total DMG Floor** | Unknown | 0.20 (20%) |
| 5 | **Pal ATK Source** | Unclear | Uses PARENT player's ATK |
| 6 | **Shield/Heal Decay** | Unknown specifics | Global: 40% / 30% (level-independent) |
| 7 | **Basic ATK resist** | Separate multiplier | Combined with att_dam in one round step |
| 8 | **Pierce/Block** | Direct damage mod | Modifies resistance value |
| 9 | **Evasion** | Not detailed | Power curve (^0.9), 80% PvP cap |
| 10 | **Rounding** | Not mentioned | 10+ roundInt ops per calculation |

---

## 17. Stat Assembly Pipeline (setPlayerList, Line 187356)

### Assembly Order
```
1. Look up job figure → ConfigJobs → model → ConfigUnit
2. setPlayerAttrib: Load all module=1 attributes, set baseValue from server attr_list
   - PvE filter: if chapterType.pve == 0, force pve_dam/pve_resist to 0
3. setPlayerEquip: Process equipment figure (weapon, ornaments, face, fate, wing)
4. Parse attr_obj_list → group 1 (pet attribs) + group 2 (skill attribs)
5. setPlayerPets: Initialize pal units with stat inheritance
6. setPlayerSkill: Load active skills sorted by position
7. Process ext data: HP percentage, absolute HP, buffs, avian, spirit, angel skills
8. setPlayerSpirit: Set spirit data
9. setPlayerPassiveSkill: Load passives with chapter type filtering + angel enhancements
```

### Pet Attribute Scaling (getPetFactAttrValue, Line 187495)
```
base = petLevel[attr.key]
additive = base + petAttrById(petId, attrId) + petAttrById(0, attrId)
for each groupAttr in configAttribute.group(attrId):
    groupBonus = petAttrById(petId, groupAttr.id) + petAttrById(0, groupAttr.id)
    multiplier = round(round(groupBonus / 10000) + 1)
    result = roundInt(result × multiplier)
```
Group bonuses are percentage-based (÷10000) and multiply sequentially.

### Pal Stat Inheritance
Pals inherit from parent player: `hp, att, partner_dam_extra, skill_dam_extra, skill_crit_rate, skill_crit_dam, boss_dam`

---

## 18. Life Steal System (HurtUtil, Line 322999)

### HP Steal Check (hpStealCheck)
```
rate = max(0, HPSTEAL_RATE - IGNORE_HPSTEAL)
triggers if randomInt(0, 10000) < roundInt(10000 × rate)
```

### HP Steal Calculation (hpStealCal)
```
heal = roundInt(damage × max(0, attribId_hpsteal - target_hpsteal_def))
heal += roundInt(damage × HPSTEAL_AMOUNT)
heal -= roundInt(damage × target_HPSTEAL_RES)
heal = max(0, heal)
```

### BuffVampire Life Steal (Line 196745)
```
totalDmgMult = round(round(1 + total_dam_add) / round(1 + total_dam_def))
totalDmgMult = max(round(total_damage_add_down_limit / 10000), totalDmgMult)  // floor at 0.20
heal = roundInt(damage × totalDmgMult × skillPar × treatDecay)
hp_cap = roundInt(maxHP × param3)
heal = min(heal, hp_cap)
```

---

## 19. Spirit Combat (spiritNormalHit, Line 323010)

### Spirit vs Spirit
```
damage = roundInt(spirit_ATT × round(round(1 + spirit_dam_add) - spirit_dam_def))
damage = roundInt(damage × round(1 - spirit_dam_def_final))
```

### Spirit vs Normal Unit
```
Scales parent player's normalHurt, doubleHurt, counterHurt, or skillDamage
by the ratio of spirit's att_dam to parent's att_dam
```

---

## 20. Data Architecture

### Config System (BaseConfig, Line 184594)
```
711 Config modules define data table schemas
Row data loaded from server via:
  loadData(json)       → parse JSON arrays
  loadBufferData(buf)  → bytes[i] = 255 & ~(32 ^ bytes[i]) → decompress → parse JSON
CONFIG_KEY = 24455     → used for XOR obfuscation: this._data[N] ^ CONFIG_KEY
```

### Probability System
All probability checks use `randomInt(0, 10000)`:
```
triggers if randomInt(0, 10000) < roundInt(10000 × rate)
```
Rates are stored as decimals (e.g., 0.5 = 50%). The 10000-point system gives 0.01% granularity.

---

*End of Master Formula Reference*
*All formulas verified against game_script_pretty.js*
*Line numbers reference the beautified file*
*Data files: data/schemas/ (711), data/enums/ (96), data/constants/ (5), data/formulas/ (25+)*
