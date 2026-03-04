# 02 — PvP Constants

> PvP damage reduction, shield/heal decay, ELO system, and all battle modifiers.

---

## PvP Injury Reduce (Damage Divisor)

The most important PvP constant. Divides **all** damage in PvP by a level-dependent value.

### Formula
```
avg_level = roundInt((player1_level + player2_level) / 2)
injuryReduce = round(configLevel.getDataByKey(avg_level).pvp_injury_reduce / 10000)
final_damage = max(roundInt(base_damage / injuryReduce), 1)
```

### Values by Level

| Level | injuryReduce | Effective Damage |
|-------|-------------|-----------------|
| 1-7 | 1.0× | 100% |
| 10 | 1.4× | 71% |
| 20 | 3.5× | 29% |
| 30 | 5.8× | 17% |
| 50 | 11.0× | 9% |
| 80 | 27.6× | 3.6% |
| 100 | 56.9× | 1.8% |
| 120 | 117.3× | 0.85% |
| 150 | 280.6× | 0.36% |
| 180 | 471.7× | 0.21% |
| 220 | 754.0× | 0.13% |

**Source:** ConfigLevel table, field `pvp_injury_reduce` (schema index 3).
Looked up per-battle using average level of both combatants.

---

## Shield & Heal Decay (Global Constants)

These are NOT per-level — they're global constants applied uniformly in all PvP.

| Constant | Raw Value | Effective | Formula |
|----------|-----------|-----------|---------|
| `shield_correct` | 4000 | 0.40 (40%) | `shieldDecay = round(shield_correct / 10000)` |
| `hp_recovery_correct` | 3000 | 0.30 (30%) | `treatDecay = round(hp_recovery_correct / 10000)` |

### Shield Decay
```
shield_hp = roundInt(base_shield_hp * shieldDecay)    // if _isDec == 0
```
- Shields in PvP are **40%** of their PvE value
- Some shields skip decay if `_isDec != 0` (rare, specific buff configurations)

### Heal Decay
```
healAmount = roundInt(healAmount * treatDecay)
hp_recovery_per_frame = round(maxHP * (hp_recovery - ignore_hp_recovery) * treatDecay)
```
- ALL healing in PvP is **30%** of PvE value
- HP recovery, skill heals, and treat-type heals all affected
- Life steal uses a different path: `max(roundInt(healAmount / injuryReduce), 1)`

### Asymmetry Note
DEFER_DAMAGE (buff 50019) has **no decay modifier** — it absorbs raw damage at full value, making it more efficient than both shields and healing in PvP.

---

## Battle Defaults

| Parameter | PvP Value | PvE Value | Description |
|-----------|-----------|-----------|-------------|
| `injuryReduce` | per-level table | 1.0 | Damage divisor |
| `shieldDecay` | 0.40 | 1.0 | Shield HP multiplier |
| `treatDecay` | 0.30 | 1.0 | Healing multiplier |
| `frameTime` | 0.033 | 0.033 | ~30 FPS tick rate |
| `timeScale` | 1 | 1 | Simulation speed |
| `hitThrowDis` | false (arena) | true | Knockback enabled |
| `seasonPveDamAdd` | 0 | varies | Seasonal PvE bonus |
| `skillCd` | 1 | 1 | Skill cooldown multiplier |

---

## Total Damage Bonus / Resistance

The **final universal multiplier** applied to ALL 13 damage types.

### Formula
```
multiplier = max(round(1 + total_dam_add - total_dam_def), total_damage_add_down_limit / 10000)
damage = round(damage * multiplier)
```

| Constant | Raw | Effective | Meaning |
|----------|-----|-----------|---------|
| `total_damage_add_down_limit` | 2000 | 0.20 | Minimum damage multiplier floor |

### Applied To (All 13 Types)
| HealthType | ID | Name |
|------------|-----|------|
| 1 | Hurt | Normal hit |
| 2 | Hurt_Crit | Normal crit |
| 3 | Hurt_Ret | Reflect damage |
| 13 | Hurt_Share_Damage | Share damage |
| 14 | Hurt_Share_Damage_Crit | Share damage crit |
| 15 | Hurt_Double | Combo hit |
| 16 | Hurt_Double_Crit | Combo crit |
| 19 | Hurt_Bleed | Bleed tick |
| 20 | Real_Damage | True damage |
| 21 | Hurt_Counter | Counter hit |
| 22 | Hurt_Counter_Crit | Counter crit |
| 23 | Hurt_Bleed_Crit | Bleed crit |
| 31 | SpiritToPlayer | Spirit damage |

### Attributes
| Attribute | ID | Role |
|-----------|------|------|
| total_dam_add | 1081 | Final DMG Bonus |
| total_dam_def | 1082 | Final DMG Resistance |

---

## ELO / Ranking System

### 1v1 Arena
| Parameter | Value | Description |
|-----------|-------|-------------|
| `pvp_k` | 30 | ELO K-factor |
| `pvp_initial_score` | 1000 | Starting ELO |
| `pvp_s` | [1.3, 0] | Score curve parameters |
| `pvp_score_change_range` | [-30, 30] | Min/max ELO change per match |
| `pvp_match_range` | [100, 52, -50] | Matchmaking range parameters |
| `pvp_ticket_max` | 3 | Max free challenges |
| `pvp_ticket_price` | [40, 80, 120, 160, 200] | Extra ticket costs (escalating) |
| `pvp_skip_time` | 15 | Auto-skip timer (seconds) |

### Cross-Server PvP
| Parameter | Value | Description |
|-----------|-------|-------------|
| `cross_pvp_k` | 30 | ELO K-factor |
| `cross_pvp_initial_score` | 1000 | Starting ELO |
| `cross_pvp_s` | [1.3, 0] | Score curve |
| `cross_pvp_battle_max` | 5 | Max battles |
| `cross_pvp_battle_win_ratio` | 0.8 | Win reward ratio |
| `cross_pvp_battle_lose_ratio` | 0.8 | Lose reward ratio |
| `cross_pvp_ticket_price` | [30, 60, 150, 400, 800] | Extra ticket costs |

### Ranked Match
| Parameter | Value | Description |
|-----------|-------|-------------|
| `ranked_match_challenge_times` | 10 | Daily challenges |
| `ranked_match_win_points` | [300, 200, 150] | Points for win (by tier) |
| `ranked_match_lose_points` | [300, 200, 150] | Points lost (by tier) |
| `ranked_match_time` | [[10,0,0], [22,0,0]] | Active hours (10AM-10PM) |
| `maxpoints` | 2000 | Max rank points |

### Ranked Win Buff (Streak-Based Scaling)
| Wins | Buff Multiplier |
|------|----------------|
| 0 | 15000 (150%) |
| 3 | 14500 (145%) |
| 5 | 14000 (140%) |
| 7 | 13500 (135%) |
| 10 | 13000 (130%) |
| 15 | 12500 (125%) |
| 20 | 12000 (120%) |
| 25 | 11500 (115%) |
| 30 | 11000 (110%) |
| 40 | 10500 (105%) |
| 60+ | 10000 (100%) |

Winning streak **reduces** the buff, creating a self-balancing mechanism.

### Double Ladder
| Parameter | Value |
|-----------|-------|
| `double_ladder_match_num` | 3 |
| `double_ladder_partner_num` | 10 |
| `double_ladder_rest_recover` | 5000 |
| `double_ladder_initial_level` | 2 |
| `double_ladder_assist_num` | 20 |
| `double_ladder_assist_reward_max` | 20 |
| `double_ladder_last_chapter` | 151 |

---

## Attribute Caps in PvP

| Attribute | ID | Cap (Raw) | Cap (Effective) | Scope |
|-----------|------|-----------|-----------------|-------|
| miss (evasion) | 1008 | 8000 | 80% | PvP only |
| partner_resist | 1020 | — | 80% (from docs) | Universal |
| crit_multiplier | — | — | min 1.5× | Formula floor |
| crit_def | 1006 | — | min 0.5 | Formula floor |
| total_dam multiplier | — | 2000 | min 0.20× | Universal |
| pierce/block amount | — | — | ±0.5 (50%) | Per-hit cap |
| inspire/suppress amount | — | — | ±0.5 (50%) | Per-hit cap |

---

## HP-Based Damage in PvP

HP%-based skills use a multiply-then-divide pattern to ensure proper clamping:

```
Step 1: hp_dmg = roundInt(hp_value * skill_percent)
Step 2: hp_dmg = roundInt(hp_dmg * injuryReduce)        // multiply UP
Step 3: base_atk = roundInt(max(roundInt(ATK - DEF*(1+DEF_COE)), 1) * ATT_DAM)
Step 4: hp_dmg = clamp(hp_dmg, roundInt(base_atk * limit[0]), roundInt(base_atk * limit[1]))
Step 5: final = max(roundInt(hp_dmg / injuryReduce), 1)  // divide back DOWN
```

### Clamp Limits
| Source | Min | Max |
|--------|-----|-----|
| Player HP% (current HP) | 0.8× base_atk | 50× base_atk |
| Player HP% (max HP) | 0.8× base_atk | 100× base_atk |
| Pal HP% | 0.8× base_atk | 2000× base_atk |

The multiply-up/divide-down ensures the clamp operates on "raw" pre-PvP values.

---

## PvP Damage Pipeline (Complete Order)

```
 1. Base Damage:    baseDmg = max(roundInt(ATK - DEF * (1 + DEF_COE)), 1)
 2. Type Multiplier: × att_dam / partner_dam / double_hit_dam / counter_dam / skill_dam_extra
 3. Resistance:      × (1 - type_resist) after Pierce/Block or Inspire/Suppress roll
 4. calHurt:         × (1 - resist) × (1 + pve_dam) × (1 - pve_resist)
 5. Crit:            × max(1.5, crit_dam / max(0.5, crit_def))
 6. Buff Modifiers:  FRAGILE → EXTRA_DAMAGE → GIANT_SLAYER → boss_dam
 7. Total DMG:       × max(1 + total_dam_add - total_dam_def, 0.20)
 8. PvP Division:    ÷ injuryReduce (level-based)
 9. Absorption:      Shield → Block → DEFER_DAMAGE
10. HP Reduction:    currenHp -= damage
11. Death Prevent:   TIME_REVERSAL → REMAKE_HP → IMMUNE_DEATH
```
