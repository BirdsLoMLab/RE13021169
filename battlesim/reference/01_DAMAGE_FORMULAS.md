# 01 — Damage Formulas

> Complete damage calculation pipeline. Every formula extracted from `game_script.js`.

## FixMath Rounding (Used Everywhere)

```
round(x)    = Math.round(x * 10000) / 10000   // 4-decimal precision
roundInt(x) = Math.round(x)                    // integer rounding
clamp(v, min, max) = Math.max(min, Math.min(max, v))
```

All combat math uses deterministic FixMath — no floating-point drift.

---

## Master Damage Pipeline (`addDamage`)

Called once per frame for each unit. Processes all health events in order:

### HP Recovery (Every Frame)
```
recoveryAmount = roundInt(round(maxHP * (hp_recovery - ignore_hp_recovery)) * treatDecay)
if recoveryAmount > 0:
    apply REDUCE_HEAL buffs
    currenHp = min(currenHp + recoveryAmount, maxHP)
    fire HP_Heal effect triggers
```
- `treatDecay` = 0.30 in PvP (hp_recovery_correct/10000), 1.0 in PvE

### Damage Types (HealthType Enum)

| Category | Types |
|----------|-------|
| **Damage** (full pipeline) | Hurt(1), Hurt_Crit(2), Hurt_Ret(3), Hurt_Share_Damage(13/14), Hurt_Double(15/16), Real_Damage(20), Hurt_Bleed(19/23), Hurt_Counter(21/22), SpiritToPlayer(31) |
| **Heal** | Treat(4), Treat_Crit(5), Skill_Hpsteal(11), Act_Hpsteal(12) |
| **Display only** | Miss(6), Armor(28), Armor_def(29), Inspire(27), Suppress(26) |
| **Spirit** | SpiritToSpirit(30) — direct HP reduction |

### Damage Pipeline Steps

```
Step 1: PvP Reduction    → damage = max(roundInt(damage / injuryReduce), 1)
Step 2: Season PvE Bonus → if seasonPveDamAdd > 0 && teamId==1: damage *= (1 + seasonPveDamAdd)
Step 3: Shield Absorb    → for each SHIELD buff: damage -= shield.onShieldAction(damage)
Step 4: Block Absorb     → for each BLOCK buff:  damage -= block.onShieldAction(damage)
Step 5: HP Reduction     → currenHp = roundInt(currenHp - damage)
Step 6: Death Prevention → TIME_REVERSAL → REMAKE_HP → IMMUNE_DEATH (checked in order)
Step 7: Record Damage    → RECORD_DAMAGE buffs log cumulative damage
Step 8: HP Change Triggers → HP_CHANGE_TRIGER and TOTAL_DAMAGE_TRIGGER buffs fire
```

### Heal Pipeline
```
Step 1: Treat Decay    → healAmount = roundInt(healAmount * treatDecay)
Step 2: Heal Reduction → apply REDUCE_HEAL buffs
Step 3: HP Addition    → currenHp = min(roundInt(currenHp + healAmount), maxHP)
```

---

## Base Damage Formula

Used by all damage calculations:
```
baseDmg = max(roundInt(ATK - DEF * (1 + DEF_COE)), 1)
```
- `ATK` = attacker.att (1001)
- `DEF` = defender.def (1024)
- `DEF_COE` = defender.def_coe (1060) — defense coefficient, increases DEF effectiveness

---

## Normal Attack Damage (`normalHurt`)

```
Player:
  resistance = calArmorAndBlock(defender, attacker, att_resist, key=att_resist)
  dmg = roundInt(baseDmg * round(att_dam * round(1 - resistance)))
  dmg = calHurt(dmg, defender, attacker)
  if crit: dmg = roundInt(dmg * max(1.5, round(crit_dam / crit_def)))
  dmg = max(1, dmg)

Pal:
  ATK = parent.att (inherits player ATK)
  pal_mult = round(partner_dam * parent.partner_dam_extra)
  resistance = calSuppressAndInspire(defender, attacker, partner_resist, key=partner_resist)
  dmg = roundInt(baseDmg * round(pal_mult * round(1 - resistance)))
  dmg = calHurt(dmg, defender, attacker)
  if crit: dmg = roundInt(dmg * max(1.5, round(crit_dam / crit_def)))
  dmg = max(1, dmg)
```

| Attribute | ID | Role |
|-----------|------|------|
| att | 1001 | Attack power |
| att_dam | 1039 | Basic ATK multiplier |
| partner_dam | 1040 | Pal damage multiplier |
| partner_dam_extra | 1047 | Pal damage extra multiplier |
| att_resist | 1018 | Basic ATK resistance |
| partner_resist | 1020 | Pal resistance |
| crit_dam | 1005 | Crit damage multiplier |
| crit_def | 1006 | Crit damage reduction (floor 0.5) |

---

## Combo (Double Hit) Damage (`normalDoubleHurt`)

```
Player:
  resistance = calArmorAndBlock(defender.double_hit_def)
  dmg = roundInt(roundInt(baseDmg * double_hit_dam) * round(1 - resistance))

Pal:
  pal_mult = round(partner_dam * parent.partner_dam_extra)
  pal_resist = calSuppressAndInspire(defender.partner_resist)
  x = roundInt(roundInt(baseDmg * pal_mult) * round(1 - pal_resist))
  dmg = roundInt(roundInt(x) * double_hit_dam)

Gun (Cannon):
  cannon_resist = defender.season_cannon_att_def
  combo_resist = calArmorAndBlock(defender.double_hit_def)
  y = roundInt(roundInt(baseDmg * partner_dam) * round(1 - cannon_resist))
  dmg = roundInt(roundInt(y) * double_hit_dam) * round(1 - combo_resist)
```
Then: `dmg = calHurt → crit multiplier → max(1, dmg)`

| Attribute | ID | Role |
|-----------|------|------|
| double_hit_dam | 1032 | Combo damage multiplier |
| double_hit_def | 1034 | Combo damage resistance |

---

## Counter Attack Damage (`normalCounterHurt`)

```
resistance = calArmorAndBlock(defender.counter_def) if usePierceResist else counter_def
dmg = roundInt(roundInt(baseDmg * counter_dam) * round(1 - resistance))
dmg = calHurt → crit multiplier → max(1, dmg)
```

| Attribute | ID | Role |
|-----------|------|------|
| counter_dam | 1033 | Counter damage multiplier |
| counter_def | 1035 | Counter damage resistance |

---

## Skill Damage (`SkillHurt`)

```
resistance = defender.skill_resist
if usePierceResist:
    resistance = calArmorAndBlock(defender, attacker, skill_resist, key=double_hit_def)
    NOTE: Uses double_hit_def as attribute key for up_limit lookup (quirk/bug)
dmg = roundInt(roundInt(baseDmg * skill_dam_extra) * round(1 - resistance))
dmg = calHurt → crit multiplier → max(1, dmg)
```

| Attribute | ID | Role |
|-----------|------|------|
| skill_dam_extra | 1045 | Skill damage multiplier |
| skill_resist | 1019 | Skill damage resistance |
| skill_crit_rate | 1037 | Skill crit rate (separate check) |
| skill_crit_dam | 1038 | Skill crit damage |

---

## Spirit Damage (`spiritNormalHit`)

Two modes:

### Spirit vs Spirit
```
dmg = round(ATK * (spirit_dam_add - spirit_dam_def + 1) * (1 - spirit_dam_def_final))
```

### Spirit vs Player
```
config = configSpirit_level.getDataByKeys(spirit_id, spirit_level)
A = config.att_dam  // array of [key, value] coefficients
  // Keys: 1=normalDoubleHurt, 2=normalCounterHurt, 3=normalHurt, 4=SkillHurt

combo_dmg   = round(normalDoubleHurt(parent, defender, 1, false)  * A[1] / 10000)
counter_dmg = round(normalCounterHurt(parent, defender, 1, false) * A[2] / 10000)
basic_dmg   = round(normalHurt(parent, defender, 1, false)        * A[3] / 10000)
skill_dmg   = round(SkillHurt(parent, defender, 1, false)         * A[4] / 10000)
dmg = round(combo_dmg + counter_dmg + basic_dmg + skill_dmg)
```
Note: Uses parent (player) as attacker, crit_flag=1 (no crit), usePierceResist=false.

| Attribute | ID | Role |
|-----------|------|------|
| spirit_dam_add | 6001 | Spirit damage bonus |
| spirit_dam_def | 6002 | Spirit damage resistance |
| spirit_dam_def_final | 6003 | Spirit final damage resist |
| spirit_hp | 6004 | Spirit HP |
| spirit_att | 6005 | Spirit ATK |

---

## Damage Resistance Layer (`calHurt`)

Applied by all damage formulas after base damage:
```
dmg = roundInt(dmg * round(1 + pve_dam))                         // PvE bonus
dmg = roundInt(roundInt(dmg * round(1 - resist)) * round(1 - pve_resist))  // resistances
dmg = max(1, dmg)
```

| Attribute | ID | Role |
|-----------|------|------|
| resist | 1021 | General damage resistance |
| pve_dam | 1057 | PvE damage bonus |
| pve_resist | 1058 | PvE damage resistance |

---

## Pierce/Block Layer (`calArmorAndBlock`)

Random roll — pierce and block are **mutually exclusive per hit**:
```
ranges = [0, 0, 10000]
if armor_penetration > ignore_armor_penetration:
    ranges[0] = roundInt(10000 * armor_penetration_rate)     // Pierce probability
if block > ignore_block:
    ranges[1] = ranges[0] + roundInt(10000 * block_rate)     // Block probability (stacked after pierce)

rand = randomInt(0, 10000)
if rand <= ranges[0]:       // PIERCE
    resistance = round(resistance - min(0.5, (armor_penetration - ignore_armor_penetration) / 10000))
else if rand <= ranges[1]:  // BLOCK
    resistance = round(resistance + min(0.5, (block - ignore_block) / 10000))
// else: no change

// Apply attribute up_limit cap
if config.up_limit != 0:
    cap = (config.num_type == 2) ? round(up_limit / 10000) : up_limit
    resistance = min(resistance, cap)
```
- Pierce/block amounts are **capped at ±0.5 (50%)**

| Attribute | ID | Role |
|-----------|------|------|
| armor_penetration_rate | 1067 | Pierce trigger rate |
| armor_penetration | 1068 | Pierce amount |
| ignore_armor_penetration | 1069 | Ignore pierce |
| block_rate | 1070 | Block trigger rate |
| block | 1071 | Block amount |
| ignore_block | 1072 | Ignore block |

---

## Inspire/Suppress Layer (`calSuppressAndInspire`)

Same structure as Pierce/Block, used for **pal/cannon damage**:
```
if partner_inspire > ignore_partner_inspire:
    ranges[0] = roundInt(10000 * partner_suppress_rate)   // NOTE: cross-referenced attribute!
if partner_suppress > ignore_partner_suppress:
    ranges[1] = ranges[0] + roundInt(10000 * partner_inspire_rate)  // Also cross-referenced!

INSPIRE:  resistance -= min(0.5, (partner_inspire - ignore_partner_inspire) / 10000)
SUPPRESS: resistance += min(0.5, (partner_suppress - ignore_partner_suppress) / 10000)
```

**Quirk**: Inspire condition uses `partner_inspire` but probability uses `partner_suppress_rate`. Suppress condition uses `partner_suppress` but probability uses `partner_inspire_rate`. The attribute names are swapped.

| Attribute | ID | Role |
|-----------|------|------|
| partner_inspire_rate | 1073 | Inspire trigger rate |
| partner_inspire | 1074 | Inspire amount |
| ignore_partner_inspire | 1075 | Ignore inspire |
| partner_suppress_rate | 1076 | Suppress trigger rate |
| partner_suppress | 1077 | Suppress amount |
| ignore_partner_suppress | 1078 | Ignore suppress |

---

## Hit/Miss/Crit Check (`checkHit`)

Weighted random roll across three outcomes:
```
accuracy = attacker.hit
evasion = ignoreMiss ? 0 : defender.miss

raw_miss = max(round(evasion - accuracy), 0)
corrected_miss = round(pow(round(100 * raw_miss), round(miss_correct / 10000)) / 100)
// miss_correct = 9000 → exponent 0.9 → compresses high miss rates

if PvP: final_miss = min(corrected_miss, round(battle_up_limit[0][1] / 10000))
// battle_up_limit[0] = [1008, 8000] → miss cap = 80%

ranges[Miss]   = roundInt(10000 * final_miss)
ranges[Normal] = ranges[Miss] + roundInt(round(1 - final_miss) * round(1 - effective_crit) * 10000)
ranges[Crit]   = ranges[Normal] + roundInt(round(1 - final_miss) * effective_crit * 10000)

effective_crit = max(crit_rate - ignore_crit_rate, 0)

rand = randomInt(0, 10000)
return Miss(0), Normal(1), or Crit(2)
```

---

## Skill Crit Check (`checkSkillCirt`)

Separate from normal crit. Only checks crit (no miss):
```
probability = roundInt(10000 * skill_crit_rate)
if probability <= 0: return false
return randomInt(0, 10000) < probability    // strict < (not <=)
```

---

## Combo Trigger Check (`checkDoubleAct`)

```
probability = roundInt(10000 * max(round(double_hit - ignore_double_hit), 0))
if probability <= 0: return false
return randomInt(0, 10000) <= probability
```

---

## Counter Trigger Check (`checkCounterAct`)

```
probability = roundInt(10000 * max(round(counter - ignore_counter), 0))
if probability <= 0: return false
return randomInt(0, 10000) <= probability
```

---

## Stun (Vertigo) Check (`checkDizz`)

```
base = max(0, round(vertigo - vertigo_def))
if base <= 0: return false
corrected = round(pow(round(100 * base), round(vertigo_correct / 10000)) / 100)
// vertigo_correct = 9000 → exponent 0.9 (same curve as miss)
probability = roundInt(10000 * corrected)
return randomInt(0, 10000) <= probability
```

---

## Launch/Knockup Check (`checkThrowHit`)

```
probability = roundInt(10000 * round(suspend - suspend_def))
if probability <= 0: return false
return randomInt(0, 10000) <= probability
```

Variant: `checkCounterThrowHit` uses `counter_suspend` instead of `suspend`.

---

## HP Steal (Lifesteal)

### Normal Attack HP Steal
```
rate = max(0, roundInt(att_hpsteal - att_hpsteal_def))
heal = roundInt(damage * rate)
```

### Skill HP Steal
```
rate = max(0, round(skill_hpsteal - skill_hpsteal_def))
heal = roundInt(damage * rate)
```

### Percentage HP Steal (maxHP-based)
Trigger check:
```
rate = roundInt(max(0, 10000 * round(hpsteal_rate - hpsteal_res)))
triggers if randomInt(0, 10000) <= rate
```
Heal amount:
```
heal = roundInt(maxHP * round(hpsteal_amount * max(0, round(1 - ignore_hpsteal))))
```

| Attribute | ID | Role |
|-----------|------|------|
| att_hpsteal | 1014 | Normal ATK lifesteal rate |
| att_hpsteal_def | 1027 | Normal ATK lifesteal defense |
| skill_hpsteal | 1015 | Skill lifesteal rate |
| skill_hpsteal_def | 1028 | Skill lifesteal defense |
| hpsteal_rate | 1053 | % HP steal trigger rate |
| hpsteal_amount | 1054 | % HP steal amount |
| hpsteal_res | 1055 | % HP steal resistance |
| ignore_hpsteal | 1056 | Ignore % HP steal |

---

## Total Damage Bonus/Resistance

Applied as a final multiplier layer:
```
total_dam_multiplier = max(total_damage_add_down_limit/10000, round(1 + total_dam_add - total_dam_def))
// total_damage_add_down_limit = 2000 → floor at 0.20 (20%)
// Prevents total DMG resistance from reducing damage below 20%
```

| Attribute | ID | Role |
|-----------|------|------|
| total_dam_add | 1081 | Total damage bonus |
| total_dam_def | 1082 | Total damage resistance |

---

## Critical Damage Multiplier

Used in all damage formulas when crit triggers:
```
crit_multiplier = max(1.5, round(crit_dam / max(0.5, crit_def)))
```
- Minimum crit multiplier is **1.5x** (150%)
- `crit_def` floors at **0.5** — even maximum crit defense can't reduce crit below 1.5x
- For skills: uses `skill_crit_dam (1038)` instead of `crit_dam (1005)`

---

## Death Prevention Chain

Checked in priority order when HP ≤ 0:

| Priority | Buff Type | Effect |
|----------|-----------|--------|
| 1 | TIME_REVERSAL | Checks if HP dropped below threshold; reverses time if so |
| 2 | REMAKE_HP | Restores HP when it drops too low |
| 3 | IMMUNE_DEATH | Prevents death entirely (currenHp = max(currenHp, 1)) |

Only one triggers per death event.
