# 98 — Discrepancy Report

All differences between code behavior and community documentation / known formulas.

---

## CRITICAL DISCREPANCIES

### 1. Defense Coefficient (def_coe) Missing from All Community Formulas
**Code:** ALL damage types use `DEF × (1 + def_coe)` instead of just `DEF`
**Community docs:** `(ATK - DEF) × multiplier`
**Actual:** `max(roundInt(ATK - DEF × (1 + DEF_COE)), 1) × multiplier`
**Impact:** If def_coe > 0, effective DEF is higher than documented. A def_coe of 0.5 means effective DEF is 150% of base DEF.
**Lines:** 322770, 322866, 322880, 322979, 195192, 195807, 192772

### 2. Skill Crit Exponent Applied to Product, Not Factor
**Community docs:** `Skill × (1 + Skill_Crit_DMG%)^0.98`
**Actual code:** `roundInt(Math.pow(roundInt(Skill × round(1 + SKILL_CRIT_DAM)), 0.98))`
**Difference:** `DMG × (1+SCRIT)^0.98` ≠ `(DMG × (1+SCRIT))^0.98`
**The 0.98 exponent is on the ENTIRE product**, not just the `(1 + skill_crit_dam)` multiplier.
**Impact:** For large damage values, this produces significantly different results.
**Lines:** 195885, 192786

### 3. Total DMG Bonus/RES — Universal Scope CONFIRMED
**Community docs:** Applied as "final layer" to all damage
**Actual code:** CONFIRMED — applied in `SkillRunner.healthTarget()` (game_script.js line 7229) to ALL 13 damage types in `NeedAddDamHurtList` (Hurt, Hurt_Crit, Hurt_Double, Hurt_Counter, Real_Damage, Hurt_Bleed, SpiritToPlayer, etc.)
**This is a universal final multiplier** after all buff modifiers and before DEFER_DAMAGE. Also applied separately in BuffVampire for life steal heal amounts.
**Impact:** Community understanding is correct — this IS a final layer on all damage. In PvE where mobs have 0 total_dam_def, any total_dam_add is pure multiplicative gain.
**Lines:** game_script.js line 7229 (healthTarget), line 4779 (NeedAddDamHurtList)

### 4. Total DMG Floor Value
**Community docs:** Floor unknown
**Actual code:** Floor = 0.20 (20%), from `total_damage_add_down_limit = 2000`
**Formula:** `max(1 + total_dam_add - total_dam_def, 0.20)`
**Line:** 237503

---

## MODERATE DISCREPANCIES

### 5. Pal Damage Uses PARENT's ATK
**Community docs:** Not clearly stated
**Actual code:** `o = t.parent.data.getAttrib(i.att)` — uses parent player's ATK
**Impact:** Pal damage scaling depends on player ATK, not pal ATK.
**Lines:** 322766, 322852

### 6. Pal Combo Formula Different
**Community docs:** `Pal Combo = Pal_Basic × Pal_Combo_Mult%`
**Actual code:** Combo multiplier applied to `(base_raw × pal_mult × (1-resist))` result, not to final pal basic damage
**Impact:** Ordering of resistance application differs.
**Lines:** 322858-322859

### 7. ATT_RESIST Combined with Multiplier for Basic ATK
**Community docs:** Resistance as separate multiplier: `× (1 - ATT_RESIST%)`
**Actual code:** For basic ATK: `round(ATT_DAM × round(1 - ATT_RESIST))` — combined in one step
**For combo/counter:** Resistance applied separately: `× round(1 - RESIST)`
**Impact:** Different rounding behavior between basic ATK and combo/counter.
**Lines:** 322770 vs 322866

### 8. Pierce/Block Modifies Resistance, Not Damage
**Community docs:** Often described as direct damage modification
**Actual code:** Pierce reduces resistance by `min(0.5, (pen-ignore)/10000)`. Block increases it.
**Impact:** The effect is indirect — through resistance modification.
**Lines:** 322793-322794

### 9. Multiple Rounding Operations Affect Final Values
**Community docs:** Simple formula without rounding
**Actual code:** 10+ rounding operations per damage calculation
**Impact:** Simulator must replicate exact rounding to match game values.
**Lines:** Throughout all HurtUtil functions

### 10. Shield Decay Is Level-Independent
**Community docs:** Unclear
**Actual code:** `shieldDecay = round(shield_correct / 10000)` where shield_correct = 4000 (global)
**Impact:** Shield decay is always 40% in PvP, regardless of player levels.
**Lines:** 235660, 197543

### 11. Heal Decay Is Also Level-Independent
**Community docs:** Unclear
**Actual code:** `treatDecay = round(hp_recovery_correct / 10000)` where hp_recovery_correct = 3000
**Impact:** Healing is always 30% in PvP, regardless of player levels.
**Lines:** 235661, 197543

---

## CONFIRMATIONS (Code Matches Documentation)

### C1. PvP Injury Reduce
- Average level calculation: **CONFIRMED** — `roundInt((lv1 + lv2) / 2)`
- Factor lookup: **CONFIRMED** — `configLevel[avg].pvp_injury_reduce / 1e4`
- Application: **CONFIRMED** — `max(roundInt(damage / injuryReduce), 1)`
- Minimum damage 1: **CONFIRMED**

### C2. Critical Hit
- Min crit_def = 0.5 (50%): **CONFIRMED**
- Min crit multiplier = 1.5: **CONFIRMED**
- Formula: `max(1.5, crit_dam / max(0.5, crit_def))`: **CONFIRMED**

### C3. HP Damage Multiply-Then-Divide
- Multiply by injuryReduce → clamp → divide by injuryReduce: **CONFIRMED**

### C4. Ignore Mechanics Are Subtractive
- `max(rate - ignore_rate, 0)`: **CONFIRMED** for all ignore types

### C5. Skill Crit 0.98 Exponent Exists
- `Math.pow(damage, 0.98)`: **CONFIRMED** (though applied differently than documented)

### C6. Dragonic Resonance Uses CASTER's DMG RES
- BuffVampire (life steal) reads `this.owner.data.getAttrib(c.total_dam_def)` where owner is the **target** receiving the buff (which is the caster's own unit for life steal)
- This **CONFIRMS** the previous finding about Dragonic Resonance

---

## PREVIOUSLY UNKNOWN (Now Discovered)

### U1. def_coe (Defense Coefficient)
A new attribute (ID 1060) that multiplicatively increases effective DEF: `DEF × (1 + def_coe)`

### U2. active_skilldamage_par (Skill Damage Factor)
Attribute ID 1043 — an additional skill damage multiplier: `getSkillFactAttrValue(skillPar, skillId, active_skilldamage_par)`

### U3. boss_dam / boss_def
Separate boss damage bonus (1046) and defense (1052) attributes applied in specific contexts.

### U4. Evasion Power Curve
Miss/evasion uses `(100 × evasion)^0.9 / 100` with a PvP cap of 80%.

### U5. Stun Duration Reduction
`stun_duration = VERTIGO_TIMES × round(1 - VERTIGO_RES)` — linear reduction.

### U6. Season PvE Damage Bonus
`seasonPveDamAdd` applies extra damage for team 1 in certain PvE modes.

### U7. Record Damage Bonus
`recordDamage` from skillctr accumulates and provides bonus damage: `damage × (1 + recordDamage/10000)`

### U8. Counter Damage Multiplier on Skills
`counterDamage` is an additional multiplier on BuffSkillValue skill damage.
