# 05 — HP-Based Damage

## Code Location
**Module:** BuffSkillValue.ts
**Function:** `_calHpHurt` — Lines 195792-195826
**Alloc:** Lines 195965-195968

---

## Variable Mapping
| Variable | Meaning |
|----------|---------|
| t | Target unit |
| r | Attacker/caster unit |
| a | HP value to use (target current HP, max HP, etc.) |
| this.skillPar | Skill parameter (HP% multiplier, from config) |
| this._calType | Calculation type (determines what HP value to use) |
| this._limit | [min_multiplier, max_multiplier] for clamping |
| this._attribId | Attribute ID for the HP value |

## _calType Values for HP Damage
| _calType | HP Value Used |
|----------|---------------|
| 0 (with attribId=hp) | Target's attribute value (HP) |
| 2 | Target's current HP percentage |
| 3 | Direct HP value |
| 8 | HP-based calculation variant |
| 9 | HP-based calculation variant |

## Raw Code (Annotated)

```javascript
// Line 195792: _calHpHurt function
i._calHpHurt = function(t, r, a) {
    // Check if this is an HP-type calculation
    var i = 3 == this._calType || 2 == this._calType || 8 == this._calType || 9 == this._calType;
    if (i = i || 0 == this._calType && this._attribId == u.hp) {

        // Step 1: HP damage = value × skillPar (HP percentage)
        var l = n.roundInt(a * this.skillPar);

        // Step 2: Multiply by PvP factor (making it larger for clamping)
        l = n.roundInt(l * t.battleMain.injuryReduce);

        // Step 3: Clamp against basic ATK damage if _limit exists
        if (this._limit) {
            var c = r.data.getAttrib(u.att),           // Attacker ATK
                g = t.data.getAttrib(u.def),           // Target DEF
                h = t.data.getAttrib(u.def_coe),       // Target DEF coefficient
                p = r.data.getAttrib(u.att_dam);        // ATK multiplier

            // Handle Pal attackers
            if (!r.isCallType && r.config.type == s.Partner) {
                c = r.parent.data.getAttrib(u.att);     // Use parent's ATK
                var _ = r.data.getAttrib(u.partner_dam),
                    v = r.data.getAttrib(u.partner_dam_extra);
                p = n.round(p * _ * v)                   // Combined pal multiplier
            }

            // Calculate base ATK damage for clamping reference
            var k = n.roundInt(Math.max(n.roundInt(c - g * (1 + h)), 1) * p);

            // Compute clamp bounds
            var T = n.roundInt(k * this._limit[0]),  // minimum damage
                b = n.roundInt(k * this._limit[1]);  // maximum damage

            // CLAMP: ensure min <= damage <= max
            l = Math.max(l, T);
            l = Math.min(l, b);
        }

        // Step 4: Apply damage (as Hurt type, NOT Hurt_Share_Damage)
        this.runner.healthTarget(t, l, d.Hurt, !1, this.config.id);

        // Step 5: Trigger life steal (BuffVampire) if applicable
        // ... (vampire buff handling)

        return !0  // consumed as HP damage
    }
    return !1  // not HP damage, continue to normal calculation
}
```

## Extracted Formula

```
Step 1: hp_dmg = roundInt(hp_value × skill_percent)
Step 2: hp_dmg = roundInt(hp_dmg × pvp_factor)          [multiply UP for clamping]
Step 3: base_atk = roundInt(max(roundInt(ATK - DEF × (1 + DEF_COE)), 1) × ATT_DAM)
Step 4: min_dmg = roundInt(base_atk × _limit[0])
Step 5: max_dmg = roundInt(base_atk × _limit[1])
Step 6: hp_dmg = clamp(hp_dmg, min_dmg, max_dmg)
Step 7: healthTarget(target, hp_dmg, Hurt)
        → At Unit.addDamage: final = max(roundInt(hp_dmg / pvp_factor), 1)  [divide BACK DOWN]
```

### Effective Final Formula (PvP):
```
raw_hp_dmg = roundInt(hp_value × skill_percent)
pvp_adjusted = roundInt(raw_hp_dmg × pvp_factor)
base_atk = roundInt(max(roundInt(ATK - DEF×(1+DEF_COE)), 1) × ATT_DAM)
clamped = clamp(pvp_adjusted, roundInt(base_atk × limit[0]), roundInt(base_atk × limit[1]))
final_dmg = max(roundInt(clamped / pvp_factor), 1)
```

---

## Clamp Values (_limit)

The `_limit` array comes from the skill configuration's `param5` field. Common values observed:

| Context | _limit[0] (min) | _limit[1] (max) | Meaning |
|---------|-----------------|-----------------|---------|
| Player HP% skill (current HP) | 0.8 | 50 | Min 80% of base ATK, max 50× base ATK |
| Player HP% skill (max HP) | 0.8 | 100 | Min 80% of base ATK, max 100× base ATK |
| Pal HP% skill | 0.8 | 2000 | Min 80% of base ATK, max 2000× base ATK |

**Note:** These specific values (50, 100, 2000) come from skill configuration data, not from the code itself. The code only reads `this._limit[0]` and `this._limit[1]` — the actual values depend on which skill is being used.

---

## Comparison with Known Documentation

### Expected (Yuko PDF):
```
Step 1: HP_DMG = Target_HP × HP%
Step 2: HP_DMG = HP_DMG × PvP_Factor (multiply UP)
Step 3: Basic_ATK_DMG = (ATK - DEF) × Multiplier
Step 4: Min = Basic_ATK × 0.8, Max = Basic_ATK × 50/100/2000
Step 5: Clamp HP_DMG between Min and Max
Step 6: Final = Clamped_DMG / PvP_Factor (divide back DOWN)
```

### Actual (from code):
- **Multiply UP then divide DOWN pattern: CONFIRMED**
- **Base ATK for clamping uses DEF_COE: `ATK - DEF × (1 + DEF_COE)`, not just `ATK - DEF`**
- **Min/max bounds come from `_limit` config, confirmed read as `_limit[0]` and `_limit[1]`**
- **For Pal: uses combined `att_dam × partner_dam × partner_dam_extra` as the multiplier**

### DISCREPANCIES:
1. **DEF_COE included in base ATK calc** — Yuko says `(ATK - DEF)`, code says `(ATK - DEF × (1 + DEF_COE))`
2. **The specific clamp values (0.8, 50, 100, 2000) cannot be confirmed from code alone** — they come from skill config data. The code structure supports any values.
3. **Pal HP damage multiplier** combines `att_dam × partner_dam × partner_dam_extra`, not just `partner_dam`.
4. **HP damage is applied as healthType `Hurt` (1), not a special HP damage type.** This means it gets all normal damage processing (shield, etc.) after clamping.

---

## Does Total DMG Bonus/RES Affect HP Damage?

**IMPORTANT FINDING:** HP damage from `_calHpHurt` is sent with type `Hurt` (line 195812). In the Unit.addDamage switch (line 449270-449285), `Hurt` is in the damage case that gets divided by `injuryReduce`.

However, Total DMG Bonus/RES is applied in the **BuffVampire.calDamage** function, which is called separately. The HP damage itself does NOT go through the Total DMG Bonus/RES calculation within `_calHpHurt`. It would only be affected if the calling skill pipeline applies it elsewhere.

Looking at the BuffSkillValue.onBegin flow:
1. `_calHpHurt` is called first (line 195870)
2. If it returns `true`, the function exits — Total DMG Bonus/RES is NOT applied
3. Total DMG Bonus/RES is applied via BuffVampire (life steal), not to the HP damage itself

**CONCLUSION: Total DMG Bonus/RES does NOT directly affect HP-based damage.**

---

## Dependencies
- `Unit.addDamage` (line 449285) for PvP division
- `BuffVampire` for life steal interaction
- Skill config for `_limit` values
