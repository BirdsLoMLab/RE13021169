# 02 — Combo / Counter / Skill Damage

## 2A — Combo (Double Hit) Damage

### Code Location
**Module:** HurtUtil.ts
**Lines:** 322839-322868 in `game_script_pretty.js`
**Function:** `normalDoubleHurt(attacker, target, hitType, applyArmorBlock)`

### Variable Mapping
| Variable | Attribute ID | Meaning |
|----------|-------------|---------|
| o | att (1001) | Attacker's ATK |
| u | def (1024) | Target's DEF |
| g | def_coe (1060) | Target's Defense Coefficient |
| b | crit_dam (1005) | Attacker's Crit Damage |
| s | crit_def (1006) | Target's Crit Defense (min 0.5) |
| m, A | double_hit_def (1034) | Target's Combo Resistance |
| c | double_hit_dam (1032) | Attacker's Combo Damage Multiplier |

### Raw Code (Annotated)
```javascript
s = t("normalDoubleHurt", (function(t, a, r, e) {
    void 0 === e && (e = !0);
    var o = t.data.getAttrib(i.att),
        u = a.data.getAttrib(i.def),
        g = a.data.getAttrib(i.def_coe),
        b = t.data.getAttrib(i.crit_dam),
        s = Math.max(.5, a.data.getAttrib(i.crit_def)),
        m = a.data.getAttrib(i.double_hit_def),
        A = m;

    // Apply Armor/Block to combo resistance
    e && (A = l(a, t, m, i.double_hit_def));  // l = calArmorAndBlock

    var c = t.data.getAttrib(i.double_hit_dam);  // combo damage multiplier
    var f = 0;

    // PLAYER FORMULA:
    // (ATK - DEF × (1+def_coe)) × double_hit_dam × (1 - double_hit_def)
    f = n.roundInt(Math.max(n.roundInt(o - u * (1 + g)), 1) * c) * n.round(1 - A);
    f = n.roundInt(f);

    // Apply DMG resistance
    f = _(f, a, t);  // calHurt: DMG RES + PvE

    // Apply crit if applicable
    1 == r || (f = n.roundInt(f * Math.max(1.5, n.round(b / s))));

    return Math.max(1, f)
}))
```

### Extracted Formula (Player)
```
base_raw = max(roundInt(ATK - DEF × (1 + DEF_COE)), 1)
combo_raw = roundInt(base_raw × DOUBLE_HIT_DAM) × round(1 - DOUBLE_HIT_DEF_after_block)
combo_dmg = roundInt(combo_raw)
after_resist = calHurt(combo_dmg, target, attacker)
if CRIT:
    final = roundInt(after_resist × max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF))))
result = max(1, final)
```

### Key Differences from Basic ATK:
- Uses `double_hit_dam` (1032) instead of `att_dam` (1039)
- Uses `double_hit_def` (1034) instead of `att_resist` (1018)
- **IMPORTANT**: Resistance is applied AFTER multiplying by combo multiplier, not combined in one step like basic ATK

---

## 2B — Counter Damage

### Code Location
**Module:** HurtUtil.ts
**Lines:** 322869-322882
**Function:** `normalCounterHurt(attacker, target, hitType, applyArmorBlock)`

### Raw Code (Annotated)
```javascript
m = t("normalCounterHurt", (function(t, a, r, e) {
    void 0 === e && (e = !0);
    var d = t.data.getAttrib(i.att),        // ATK
        o = a.data.getAttrib(i.def),         // DEF
        u = a.data.getAttrib(i.def_coe),     // DEF coefficient
        g = t.data.getAttrib(i.crit_dam),    // crit damage
        b = Math.max(.5, a.data.getAttrib(i.crit_def)),  // crit def (min 0.5)
        p = a.data.getAttrib(i.counter_def), // counter resistance
        s = p;

    e && (s = l(a, t, p, i.counter_def));   // apply armor/block

    var m = t.data.getAttrib(i.counter_dam), // counter damage multiplier
        // FORMULA: (ATK - DEF×(1+def_coe)) × counter_dam × (1 - counter_def)
        A = n.roundInt(Math.max(n.roundInt(d - o * (1 + u)), 1) * m) * n.round(1 - s);

    A = n.roundInt(A);
    A = _(A, a, t);  // calHurt: DMG RES + PvE
    1 == r || (A = n.roundInt(A * Math.max(1.5, n.round(g / b))));  // crit
    return Math.max(1, A)
}))
```

### Extracted Formula
```
base_raw = max(roundInt(ATK - DEF × (1 + DEF_COE)), 1)
counter_raw = roundInt(base_raw × COUNTER_DAM) × round(1 - COUNTER_DEF_after_block)
counter_dmg = roundInt(counter_raw)
after_resist = calHurt(counter_dmg, target, attacker)
if CRIT:
    final = roundInt(after_resist × max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF))))
result = max(1, final)
```

---

## 2C — Skill Damage (SkillHurt)

### Code Location
**Module:** HurtUtil.ts
**Lines:** 322967-322979
**Function:** `SkillHurt(attacker, target, hitType, applyArmorBlock)`

### Raw Code (Annotated)
```javascript
t("SkillHurt", (function(t, a, r, e) {
    void 0 === e && (e = !0);
    var d = t.data.getAttrib(i.att),
        o = a.data.getAttrib(i.def),
        u = a.data.getAttrib(i.def_coe),
        g = t.data.getAttrib(i.crit_dam),
        b = Math.max(.5, a.data.getAttrib(i.crit_def)),
        p = a.data.getAttrib(i.skill_resist),
        s = p;

    // NOTE: applies calArmorAndBlock with double_hit_def, NOT skill_resist!
    e && (s = l(a, t, p, i.double_hit_def));

    var m = t.data.getAttrib(i.skill_dam_extra),  // skill damage multiplier
        A = 0;

    // FORMULA: (ATK - DEF×(1+def_coe)) × skill_dam_extra × (1 - skill_resist)
    A = n.roundInt(Math.max(n.roundInt(d - o * (1 + u)), 1) * m) * n.round(1 - s);
    A = n.roundInt(A);
    A = _(A, a, t);  // calHurt: DMG RES + PvE
    1 == r || (A = n.roundInt(A * Math.max(1.5, n.round(g / b))));
    return Math.max(1, A)
}))
```

### Extracted Formula
```
base_raw = max(roundInt(ATK - DEF × (1 + DEF_COE)), 1)
skill_raw = roundInt(base_raw × SKILL_DAM_EXTRA) × round(1 - SKILL_RESIST_after_block)
skill_dmg = roundInt(skill_raw)
after_resist = calHurt(skill_dmg, target, attacker)
if CRIT:
    final = roundInt(after_resist × max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF))))
result = max(1, final)
```

---

## 2D — Skill Damage via BuffSkillValue (Complex Skills)

### Code Location
**Module:** BuffSkillValue.ts
**Lines:** 195856-195920
**More sophisticated skill damage with separate skill_crit, resist types, etc.**

### Key Code Path (Non-HP Skills)
```javascript
// Line 195863: Get base hurt value
var p = this._calHurt(t, r);   // internal calc based on _calType

// Lines 195870-195897: Apply skill damage pipeline
if (!this._calHpHurt(t, r, p)) {   // Not HP-based damage?
    p = round(p × getSkillFactAttrValue(skillPar, skillId, active_skilldamage_par));

    // Apply SKILL_DAMAGE_ADD buffs
    B = sum of SKILL_DAMAGE_ADD buff contributions

    // Apply skill_dam_extra multiplier (or 1 if T1045 flag set)
    D = (ignoreFlag & T1045) ? 1 : skill_dam_extra
    x = roundInt(p × D)

    // SKILL CRIT (different from normal crit!)
    if (!(ignoreFlag & SkillCrit) && checkSkillCirt(r)) {
        L = skill_crit_dam
        x = roundInt(x × round(1 + L))    // multiply by (1 + skill_crit_dam)
        x = roundInt(Math.pow(x, 0.98))   // CONFIRMED: 0.98 exponent
        P = Hurt_Crit
    }

    // NORMAL CRIT (if UseCrit flag set)
    if ((ignoreFlag & UseCrit) && checkHit == Crit) {
        F = crit_dam
        w = max(0.5, crit_def)
        x = roundInt(x × max(1.5, round(F / w)))
        P = Hurt_Crit
    }

    // Boss damage bonus
    if (target is Boss && boss_dam > 0)
        x = roundInt(x × round(1 + boss_dam))

    // Add skill damage add contributions
    x = roundInt(x + B)

    // Record damage bonus
    x = roundInt(x × round(1 + round(recordDamage / 1e4)))
    x = roundInt(x × counterDamage)

    // Apply resistance (based on _calType)
    N = _calResistPar()  // skill_resist, att_resist, double_hit_def, counter_def, partner_resist
    x = calHurt(roundInt(x × N), target, attacker)

    // Apply EXTRA_DAMAGE buffs
    // Apply GIANT_SLAYER buffs

    healthTarget(target, x, P)
}
```

### Skill Crit Formula (CONFIRMED)
```
skill_crit_dmg = roundInt(roundInt(damage × round(1 + SKILL_CRIT_DAM)) ^ 0.98)
```
**The 0.98 exponent IS confirmed in the code at line 195885.**

### Resist Type Selection (_calResistPar)
| _calType | Resistance Used |
|----------|----------------|
| 0, 1 (default) | skill_resist (1019) |
| 4, 5 | att_resist (1018) |
| 6 | double_hit_def (1034) |
| 7 | counter_def (1035) |
| 10 | partner_resist (1020) |

---

## Comparison with Known Documentation

### Expected (Yuko PDF):
```
Combo = (ATK - DEF) × Combo_Mult% × (1 - Combo_RES%) × (1 - DMG_RES%)
Counter = (ATK - DEF) × Counter_Mult% × (1 - Counter_RES%) × (1 - DMG_RES%)
Skill = (ATK - DEF) × Skill% × Skill_DMG% × (1 - Skill_RES%) × (1 - DMG_RES%)
```

### DISCREPANCIES:
1. **DEF_COE applies to ALL damage types.** All formulas use `DEF × (1 + def_coe)`, not just `DEF`.
2. **Resistance ordering:** For combo/counter, resistance is applied AFTER the multiplier, not combined with it.
3. **Skill damage formula is more complex than documented.** It includes active_skilldamage_par, record damage bonuses, counterDamage multiplier.
4. **Skill Crit is a SEPARATE system from normal crit.** Skill crit uses `(1 + skill_crit_dam)` then `^0.98`. Normal crit uses `max(1.5, crit_dam / crit_def)`.
5. **Boss damage bonus** is applied after crit for BuffSkillValue skills.

---

## Combo/Counter Rate Checks

### checkDoubleAct (Lines 322918-322925)
```
effective_combo = max(round(double_hit - target.ignore_double_hit), 0)
probability = roundInt(10000 × effective_combo)
triggers if random(0, 10000) <= probability
```

### checkCounterAct (Lines 322926-322932)
```
effective_counter = max(round(counter - target.ignore_counter), 0)
probability = roundInt(10000 × effective_counter)
triggers if random(0, 10000) <= probability
```

**CONFIRMED:** Ignore mechanics are SUBTRACTIVE: `effective = max(rate - ignore_rate, 0)`
