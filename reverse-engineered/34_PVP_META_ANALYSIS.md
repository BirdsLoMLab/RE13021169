# 34 — PvP Meta Analysis & Build Guide

> **Sources:** All 909 decoded config tables, `data/formulas/`, `data/constants/`, reverse-engineered docs 01-33
> **Scope:** Competitive PvP analysis: damage pipeline exploits, class tier list, build recommendations, progression priority

---

## 1. The Complete Damage Pipeline

Every point of damage flows through this exact multiplicative chain. Understanding the order reveals where stacking is most efficient.

```
Step 1: BASE DAMAGE
  baseDmg = max(roundInt(ATK - DEF × (1 + DEF_COE)), 1)

Step 2: TYPE MULTIPLIER
  Player basic:  × att_dam (1039)
  Pal:           × partner_dam (1040) × partner_dam_extra (1047)

Step 3: RESISTANCE CHECK (varies by attack type)
  Basic:   att_resist (1018)
  Combo:   double_hit_def (1034)
  Counter: counter_def (1035)
  Skill:   skill_resist (1019)
  Pal:     partner_resist (1020, cap 80%)

Step 4: PIERCE / BLOCK ROLL (mutually exclusive, random)
  If pierce procs:  resistance -= min(0.5, (pen - ignore_pen) / 10000)
  If block procs:   resistance += min(0.5, (block - ignore_block) / 10000)

Step 5: APPLY RESISTANCE
  dmg = roundInt(baseDmg × round(multiplier × round(1 - resistance)))

Step 6: DMG RES LAYER (calHurt)
  dmg = roundInt(dmg × round(1 - resist))     [resist = attr 1021]

Step 7: CRITICAL (if crit procs)
  crit_multiplier = max(1.5, round(crit_dam / max(0.5, crit_def)))
  dmg = roundInt(dmg × crit_multiplier)

Step 8: BUFF MODIFIERS (sequential)
  → FRAGILE_EFFECT (flat bonus from attacker attribute)
  → EXTRA_DAMAGE (3 types: flat%, HP-loss%, current-HP%)
  → GIANT_SLAYER (HP-difference scaling with boss/player caps)
  → boss_dam

Step 9: TOTAL DMG BONUS/RES ← THE FINAL MULTIPLIER
  multiplier = max(1 + total_dam_add - total_dam_def, 0.20)
  dmg = round(dmg × multiplier)
  *** Applies to ALL 13 damage types: basics, crits, combos, counters,
      bleeds, true damage, HP% damage, reflect, spirit→player ***
  *** Floor: 0.20× (from total_damage_add_down_limit = 2000/10000) ***

Step 10: PVP DIVISION
  final = max(roundInt(dmg / injuryReduce), 1)
  *** Minimum 1 damage always goes through ***

Step 11: ABSORPTION & REDUCTION
  Shield absorption → Block → HP reduction → Death prevention
  (Time Reversal → Remake HP → Immune Death)
```

---

## 2. Key Exploit Mechanics

### Pierce Amplification (3.5× from one proc)
Pierce modifies the resistance value BEFORE it's applied multiplicatively:
```
Target with 0.8 resistance (80% reduction):
  Without pierce: dmg × (1 - 0.8) = dmg × 0.2
  With pierce (-0.5): dmg × (1 - 0.3) = dmg × 0.7
  Effective multiplier: 0.7 / 0.2 = 3.5×
```
Stack armor_penetration_rate and ensure pen > enemy ignore_pen. Even 1 pen over 0 ignore enables the proc.

### Total DMG Bonus: The Universal God Stat
Applied AFTER all other multipliers, to ALL damage types. Every point of total_dam_add is worth more than any individual damage type booster because it multiplies the final result. Equipment Resonance Stage 18 gives +3800 — this is the single highest-impact investment.

### Vampire Double-Dip
BuffVampire applies Total DMG multiplier independently before PvP division:
```
healBase = round(damage × totalDamMultiplier)  ← applied here
healBase = max(roundInt(healBase / injuryReduce), 1)
```
Lifesteal scales better with total_dam_add than raw damage does.

### Shield Decay Asymmetry
- Shields = 40% of PvE value (shield_correct = 4000/10000)
- Damage = ÷ injuryReduce (up to 754× at lv220)
- At endgame, shields are proportionally STRONGER because damage is reduced far more aggressively than shields

### Healing Decay
- treatDecay = 0.3 (hp_recovery_correct = 3000/10000)
- ALL healing is 30% in PvP
- Martial Sage's 8% HP/5s regen becomes 2.4% HP/5s in PvP
- Makes anti-heal less necessary but also makes regen builds weaker

### HP% Damage Clamp
- Clamped to [0.8×, 50×] of base ATK damage against players
- High ATK builds push the 50× ceiling: 100K ATK × 2.5 att_dam = 250K base → 12.5M max HP damage per proc

---

## 3. PvP Injury Reduce Curve

From `Level.json` — the PvP damage divisor scales exponentially:

| Level | Divisor | Effective Damage |
|-------|---------|-----------------|
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
| **220** | **754.0×** | **0.13%** |

At max level (220), you deal 0.13% of your raw damage in PvP. This means **multiplicative modifiers** (Total DMG Bonus, Pierce, Crit) are exponentially more valuable than flat damage.

---

## 4. Active Skill Effect Chain Breakdown

Each active skill fires two effects: an AoE debuff (Effect 2) and a self/target buff (Effect 1).

### AoE Debuffs (shared across class pairs)
| Class Pair | Effect | Debuff | Duration |
|-----------|--------|--------|----------|
| Sage / Warbringer | 10532/10542 | Counter DMG RES (1035) -100% | 8s |
| Sacred Hunter / Plume Monarch | 10552/10562 | Combo DMG RES (1034) -100% | 8s |
| Prophet / Darklord | 10572/10582 | Skill DMG RES (1019) -100% | 8s |
| Beastmaster / Supreme Spirit | 10662/10672 | Pal DMG RES (1020) -100% | 8s |

Note: The actual debuff value is -10000 raw (param3=-10000), which translates to the percentage shown in skill desc after applying skill coefficient divisors.

### Unique Secondary Effects
| Class | Effect ID | Buff Applied | Mechanic |
|-------|-----------|-------------|----------|
| **Martial Sage** | 10531 | Buff 10053 (skill_effect → 10534) | Counter damage adds 1% target current HP |
| **Warbringer** | 10541 | Buff 10061 + 10062 (attrib_convert) | ATK→DEF (0.15) + DEF→ATK (0.75) for 8s |
| **Sacred Hunter** | 10551 | **Buff 20042 (pause_cd, param1=6)** | **Pauses 6 enemy skill cooldowns for 4s** |
| **Plume Monarch** | 10561 | Buff 20043 (attrib 1007 +10000) | Ignore Evasion +100% for 10s |
| **Prophet** | 10574 | Buff 20046 (skill_effect → 10571) | Shield-breaking on attacks for 10s |
| **Darklord** | 10581 | Buff 20045 (attrib 1038 +10000) | Skill Crit DMG +100% for 10s |
| **Beastmaster** | 10661 | Buff 10046 (attrib 1007 +10000) | Pals Ignore Evasion +100% for 10s |
| **Supreme Spirit** | 10671 | Buff 10047 + 10048 (skill_effects) | Pal HP% damage proc (40% chance, 1% HP) for 8s |

---

## 5. Class Tier List (PvP)

### S-Tier

**Sacred Hunter** — The most complete PvP kit in the game.
- **pause_cd (buff 20042)**: The ONLY skill in the game with cooldown freeze. Param1=6 means it pauses 6 skill cooldown levels. No visible counter-mechanic exists in the data.
- 1% target current HP on every basic attack (passive 2126)
- Post-crit ATK +40% for 1s (passive 2031) with +20% base Crit DMG
- Energy denial shuts down opponent's entire skill rotation
- ATK Speed +15% means more hits = more HP% procs

**Darklord** — Highest single-target burst in the game.
- 20% extra damage that **ignores immunity** (buff 20078, skill_real_damage)
- Total Skill Crit: +30% from passives (2002 + 2017)
- Total Skill Crit DMG: +50% passive (2017) + 100% from active (buff 20045) = **+150%** during active
- HP-loss scaling: Skill DMG +3% per 10% HP lost (max +30%)
- All skills bypass immunity — no counter except killing before rotation

### A-Tier

**Warbringer** — Counter-attack specialist that punishes multi-hit builds.
- Counter DMG +140% (passive 2020) with +30% Counter Rate/Multiplier
- 20% passive AoE counter (passive 2123) when hit by basics/combos — attackers damage themselves
- ATK↔DEF conversion active creates burst windows (+0.75 ATK per DEF is massive for tanks)
- ATK scales +3% per 10% HP lost (max +30%)
- Hard counters Plume Monarch (every extra bullet triggers counters)

**Plume Monarch** — Maximum DPS through hit volume.
- +2 extra basic bullets (20% proc each) + +3 combo bullets (10% proc each)
- Combo DMG +140% (passive 2013) with +30% Combo Rate
- 10s full Ignore Evasion from active = guaranteed hits
- Each extra bullet independently triggers combos/crits
- Hard counters evasion builds; hard countered by Warbringer

**Beastmaster** — Independent damage sources that are hard to simultaneously counter.
- Extra pal slot = additional damage cycle
- Pal Crit +25%, Crit DMG +20%, DMG Multiplier +20%
- HP-loss scaling on pals (+3% per 10% HP lost)
- Pals ignore evasion during active (10s)
- Pal DMG RES caps at 80% — pal damage always gets through

### B-Tier

**Martial Sage** — The wall. Strongest in PvE, weaker in PvP due to treatDecay.
- Shield 8% HP every 10s (trap buff — undispellable)
- Regen 8% HP every 5s → **2.4% HP/5s in PvP** (×0.3 treatDecay)
- DMG RES +15%, DEF +30%
- Shield + trap immunity makes it resilient but 2-minute timer + low damage = stalemates
- Loses to Sacred Hunter (energy denial), Darklord (true damage)

**Prophet** — Anti-Sage specialist / support.
- Shield-breaking counters Martial Sage directly
- +20% Energy Regen + stun-based CD reduction (-0.3s per stun)
- +40% skill duration + 10% Skill DMG
- Lower debuff (-20% Skill RES vs -40% Counter/Combo RES)
- Support identity — best in team modes, weaker in 1v1

**Supreme Spirit** — Situational race-based pal synergies.
- 40% chance of 1% target HP per pal hit during active
- Race synergy bonuses from passives (2117, 2108)
- Pal deploy effect enhancement +20%
- Less raw damage than Beastmaster, more conditional

---

## 6. Build Recommendations

### Sacred Hunter — "The Lockdown"
| System | Choice | Reason |
|--------|--------|--------|
| Mount Skin | **Pyrebreaker** (5002) | Crit Rate +2%/s (cap 40%), Crit DMG +10%/s (cap 200%) — feeds ATK+40% post-crit loop |
| Artifact Skin | **Safe Distance** (5115) | 50% chance 0.8% target max HP + 10% wound (regen -50%) — double HP% pressure |
| Gem Set | **Mana Mastery** (103) | Global Basic ATK DMG +1000 — scales basic hits |
| Priority Stats | ATK SPD > Crit Rate (cap 80%) > Ignore Evasion > Pierce > Final DMG Bonus |
| Win Condition | Lock skills with pause_cd → basic ATK loop with 1% HP + crit burst |
| Counters | Sage (energy denial), Darklord (outrange skill cast) |
| Loses to | Warbringer (basics trigger 20% AoE counter + 140% counter DMG) |

### Darklord — "The Delete Button"
| System | Choice | Reason |
|--------|--------|--------|
| Mount Skin | **Cloud Drifter** (5009) | Skill Crit +20% + post-crit ATK +40% for 5s — stacks with +30% passive Skill Crit |
| Artifact Skin | **Snow Sprite** (5110) | 10% max HP AoE every 10s + ATK SPD/Energy reduction 40% — disables enemy rotation |
| Alt Artifact | **Piercing Squail** (5120) | +30% Crit Rate, each crit → +2% Final Crit DMG (cap +40%), max stacks → 1500% AoE |
| Gem Set | **Elemental Wrath** (106) | Global Skill DMG +1000 — direct skill multiplier |
| Priority Stats | Skill Crit > Skill Crit DMG > ATK > Final DMG Bonus > Energy Regen |
| Win Condition | Galaxy Dive (+150% Skill Crit DMG) → skill rotation with 20% true damage bypassing all immunity |
| Counters | Everything that can't survive the burst (Sage's shield gets true-damaged through) |
| Loses to | Sacred Hunter (pause_cd before first skill), CC chains, stun-lock before rotation |

### Warbringer — "The Punisher"
| System | Choice | Reason |
|--------|--------|--------|
| Mount Skin | **Velocity Blitz** (5014) | Each counter → Global Counter DMG +20% for 3s (cap 60%) — snowballs counter damage |
| Artifact Skin | **Chaotic Warlord** (5102) | Basics/combos deal +60% AoE DMG — AoE pressure |
| Alt Artifact | **Spring Chord** (5113) | 2000% AoE every 11s + confuse (enemies deal 30% to themselves for 5s) |
| Gem Set | **Heart of Resilience** (101) | Global Counter DMG +1000 — direct counter scaling |
| Priority Stats | Counter Rate > Counter Multiplier > Counter DMG > Pierce > Final DMG Bonus |
| Win Condition | Get hit → 20% AoE counter procs + 140% Counter DMG + Velocity Blitz stacking → avalanche |
| Counters | Plume Monarch (eats multi-hits), all basic-heavy attackers |
| Loses to | Sacred Hunter (energy denial + single-hit pattern), Ignore Counter builds |

### Plume Monarch — "The Bullet Storm"
| System | Choice | Reason |
|--------|--------|--------|
| Mount Skin | **Koi Paper Kite** (5016) | Every 3 combos → 1000% AoE DMG — massive with +5 bullet spam |
| Artifact Skin | **Candy Gatling** (5106) | 1-5 extra bullets per action, each 20% basic ATK DMG — even more bullets |
| Gem Set | **Furious Gale** (102) | Global Combo DMG +1000 — direct combo multiplier |
| Priority Stats | Combo Rate > ATK SPD > Ignore Evasion > Combo DMG > Final DMG Bonus |
| Win Condition | Sun Pursuit (full evasion ignore) → bullet spam → combo procs → Koi AoE every 3 combos |
| Counters | Evasion/dodge builds (100% ignore evasion), low-counter-rate targets |
| Loses to | Warbringer (every bullet triggers counter), high Combo DMG RES builds |

### Beastmaster — "The Pack Leader"
| System | Choice | Reason |
|--------|--------|--------|
| Mount Skin | **Hot Wheels** (5003) | Pal ATK SPD +3%/s (cap 60%) — more pal hits = more damage |
| Artifact Skin | **Eye of Raven** (5104) | Auto-cast random active skill every 20s — free Tamer of Beasts casts |
| Alt Artifact | **Snow Sprite** (5110) | 10% max HP AoE — independent AoE pressure |
| Gem Set | **Common Foe** (107) | Pal DMG Bonus +1000 — direct pal scaling |
| Priority Stats | Pal DMG Multiplier > ATK > Ignore Evasion > Pierce > Final DMG Bonus |
| Win Condition | Extra pal slot + crit pals + multiplier stacking → overwhelm via multiple damage sources |
| Counters | Single-target defenders (can't counter all pals at once) |
| Loses to | AoE that kills pals, high Pal DMG RES stacking |

---

## 7. Progression Priority (Investment Order)

Based on stat-per-resource efficiency and PvP impact:

| Priority | System | Max Value | Why |
|----------|--------|-----------|-----|
| **1** | Equipment Resonance | +3,800 Final DMG Bonus + +3,800 Final DMG RES | Universal multiplier on ALL damage. Nothing else gives this. |
| **2** | Equipment Advancement | 6,240 Pierce/Block/Inspire/Suppress each | Pierce alone can 3.5× damage. |
| **3** | Artifact Level | 233.7M per stat (ATK/HP/DEF) at lv300 | Highest raw stat source. |
| **4** | Ring Level | 50.1M per stat at lv301 | Second highest stat source. 12,395× power increase from lv1. |
| **5** | Mount Level | 104.8M per stat at lv300 | Third highest stat source. |
| **6** | Path to Divinity (Group 3) | Trunks 10-12: 5-10× stats of earlier groups | Attr 1012 (HP Regen) has power_rate 264.6M — highest in system. |
| **7** | Back/Wing Level + Talents | 52.9M per stat at lv260 + 30M DEF per talent | Talent tree adds massive defensive stats. |
| **8** | Mount/Artifact Skins | Skill unlocks + bonus stats | Skin skills are build-defining (see builds above). |
| **9** | Artifact Gem Sets | +1,000 to class-specific damage type | Class-specific multiplier. |
| **10** | Fate Quality 6 Synergies | Unique paired effects | Strategic advantage, not raw stats. |

---

## 8. The Sacred Hunter Problem

Buff 20042 (`pause_cd`, param1=6) is applied by Skill Effect 10551, which is the secondary effect of Piercing Boneforge (Skill 1055). This is the **only instance** of pause_cd in the entire buff table (4,155 entries scanned).

**What it does:**
- Pauses enemy cooldown progression on 6 skill levels
- Applied to single target (targetType [4,1,0])
- Duration: 4 seconds (from skill desc_parm)
- Cooldown: tied to Piercing Boneforge's own energy cycle

**Why it's broken:**
- No attribute counters pause_cd (unlike stun → Ignore Stun 1026, combo → Ignore Combo 1048)
- No buff action in the 80-class buff system specifically removes pause_cd
- Control RES (1042) reduces stun duration — but pause_cd is NOT a stun (different action type)
- Energy denial + HP% basic damage + crit burst = complete offensive kit

**Possible soft counters:**
- Kill Sacred Hunter before first active skill cast (Darklord burst)
- High ATK SPD to get more hits in between skill lockouts
- Shield stacking to survive the 4s lockout window
- Counter-heavy builds (Warbringer) that punish the basic attack pattern

---

## 9. Matchup Matrix

```
             Sage  Warbr  SHunt  Plume  Proph  Dklord  Beast  SSpir
Sage          —     ○      ●      ○      ●      ●      ○      ○
Warbringer    ○     —      ●      ◉      ○      ○      ○      ○
Sacred Hunt   ◉     ○      —      ○      ◉      ○      ◉      ◉
Plume Mon     ○     ●      ○      —      ○      ○      ○      ○
Prophet       ◉     ○      ○      ○      —      ○      ○      ○
Darklord      ◉     ○      ●      ○      ○      —      ○      ○
Beastmaster   ○     ○      ○      ○      ○      ○      —      ◉
Supreme Spr   ○     ○      ○      ○      ○      ○      ○      —

◉ = strong advantage  ○ = even/skill-dependent  ● = disadvantage
```

**Key matchups:**
- Sacred Hunter beats Sage (energy denial negates regen), Prophet (same), Beastmaster (basics > pals)
- Warbringer beats Plume Monarch (multi-hits feed counters)
- Darklord beats Sage (true damage bypasses shields), loses to Sacred Hunter (rotation denial)
- Prophet beats Sage (shield-breaking)
