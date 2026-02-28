# 99 — Full Damage Pipeline (End-to-End Trace)

Tracing a single basic attack from start to finish in PvP.

---

## Setup
- Attacker (Player 1): ATK=10000, att_dam=2.5, crit_dam=1.8, crit_rate=0.6
- Defender (Player 2): DEF=5000, def_coe=0.1, att_resist=0.3, crit_def=0.8, resist=0.15
- PvP: injuryReduce=25.0, shieldDecay=0.4, treatDecay=0.3
- Defender has 500 shield HP

---

## Step 1: Hit Check (checkHit)

**Code:** Lines 322896-322917

```
miss = defender.miss (e.g., 0.05)
hit = attacker.hit (e.g., 0.02)
raw_evasion = max(round(0.05 - 0.02), 0) = 0.03
corrected = round((100 × 0.03)^0.9 / 100) = round(3^0.9 / 100) = round(2.6878 / 100) = 0.0269

ignore_crit = defender.ignore_crit_rate (e.g., 0.1)
effective_crit = max(0.6 - 0.1, 0) = 0.5

P(miss) = 0.0269 → 269/10000
P(normal) = roundInt(269 + roundInt(round(1-0.0269) × round(1-0.5) × 10000))
         = roundInt(269 + roundInt(0.9731 × 0.5 × 10000))
         = roundInt(269 + roundInt(4865.5)) = roundInt(269 + 4865) = 5134
P(crit) = 10000

Roll random 0-10000. Assume roll = 7000 → CRIT (7000 > 5134)
```

---

## Step 2: Armor/Block Check (calArmorAndBlock)

**Code:** Lines 322773-322801

```
Assume: armor_penetration=0, block=0 → neither procs
att_resist stays at 0.3
```

---

## Step 3: Base Damage (normalHurt)

**Code:** Lines 322756-322771

```
Step 3a: raw_base = roundInt(ATK - DEF × (1 + def_coe))
       = roundInt(10000 - 5000 × (1 + 0.1))
       = roundInt(10000 - 5500)
       = roundInt(4500) = 4500

Step 3b: max(4500, 1) = 4500

Step 3c: resistance_factor = round(att_dam × round(1 - att_resist))
       = round(2.5 × round(1 - 0.3))
       = round(2.5 × 0.7)
       = round(1.75) = 1.75

Step 3d: base_damage = roundInt(4500 × 1.75)
       = roundInt(7875) = 7875
```

---

## Step 4: DMG Resistance (calHurt)

**Code:** Lines 322831-322838

```
resist = 0.15 (defender.resist)
pve_dam = 0, pve_resist = 0 (PvP)

Step 4a: after_pve = roundInt(7875 × round(1 + 0)) = 7875
Step 4b: after_resist = roundInt(roundInt(7875 × round(1 - 0.15)) × round(1 - 0))
       = roundInt(roundInt(7875 × 0.85) × 1)
       = roundInt(roundInt(6693.75) × 1)
       = roundInt(6693 × 1)
       = 6693
Step 4c: max(6693, 1) = 6693
```

---

## Step 5: Critical Damage

**Code:** Line 322771

```
Since hitType = Crit (not 1/Normal):
crit_mult = max(1.5, round(crit_dam / max(0.5, crit_def)))
          = max(1.5, round(1.8 / max(0.5, 0.8)))
          = max(1.5, round(1.8 / 0.8))
          = max(1.5, round(2.25))
          = max(1.5, 2.25)
          = 2.25

crit_damage = roundInt(6693 × 2.25) = roundInt(15059.25) = 15059
```

---

## Step 6: Post-Damage Buffs (in SkillHandleNormal.att)

**Code:** Lines 429988-430015

```
Assume no FRAGILE_EFFECT, EXTRA_DAMAGE, or GIANT_SLAYER buffs.
boss_dam = 0 (target is not boss)

final_pre_pvp = 15059
healthType = Hurt_Crit
```

---

## Step 7: healthTarget → Queue Damage

The damage value 15059 is queued as a health action with type `Hurt_Crit`.

---

## Step 8: Damage Application (Unit.addDamage)

**Code:** Lines 449270-449330

### Step 8a: PvP Reduction
```
W = Math.max(roundInt(15059 / 25.0), 1)
  = Math.max(roundInt(602.36), 1)
  = Math.max(602, 1)
  = 602
```

### Step 8b: Shield Absorption
```
Defender has 500 shield HP.
Shield absorbs: min(500, 602) = 500
Remaining damage: roundInt(602 - 500) = 102
Shield depleted: shieldHp = 0
```

### Step 8c: Block Check
```
Assume no block buffs. damage_through = 102
```

### Step 8d: HP Reduction
```
defender.currenHp = roundInt(currenHp - 102)
```

---

## Summary: Full Pipeline

```
ATK=10000, DEF=5000, def_coe=0.1, att_dam=2.5, att_resist=0.3
resist=0.15, crit_dam=1.8, crit_def=0.8, PvP_factor=25.0, Shield=500

1. Hit check         → Crit
2. Armor/Block       → No proc
3. Base damage       → roundInt(max(roundInt(10000-5500),1) × round(2.5×0.7)) = 7875
4. DMG Resistance    → roundInt(roundInt(7875 × 0.85) × 1) = 6693
5. Crit multiplier   → roundInt(6693 × 2.25) = 15059
6. Buff modifiers    → 15059 (no buffs)
7. PvP reduction     → max(roundInt(15059 / 25), 1) = 602
8. Shield absorb     → 602 - 500 = 102 through to HP
9. HP reduction      → currenHp -= 102
```

**Pre-PvP damage: 15,059**
**Post-PvP damage: 602**
**After shields: 102 actual HP lost**

---

## Pipeline Diagram

```
[ATK, DEF, def_coe] → Base Raw: max(roundInt(ATK - DEF×(1+coe)), 1)
        ↓
[att_dam, att_resist] → × round(att_dam × round(1 - resist))
        ↓
[calHurt: resist, pve_dam, pve_resist] → × round(1+pve) × round(1-resist) × round(1-pve_res)
        ↓
[If CRIT: crit_dam, crit_def] → × max(1.5, round(crit_dam / max(0.5, crit_def)))
        ↓
[boss_dam, FRAGILE_EFFECT, EXTRA_DAMAGE, GIANT_SLAYER] → buff modifiers
        ↓
[healthTarget → Unit.addDamage]
        ↓
[÷ injuryReduce] → PvP reduction
        ↓
[Shield absorption] → damage overflow
        ↓
[Block absorption] → remaining damage
        ↓
[HP -= remaining] → Death check → Game over / continue
```
