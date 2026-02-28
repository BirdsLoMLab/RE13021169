# 01 — Basic Damage Calculation

## Code Location
**Module:** HurtUtil.ts
**Lines:** 322756-322771 in `game_script_pretty.js`
**Function:** `normalHurt(attacker, target, hitType, applyArmorBlock)`

## Variable Mapping (normalHurt)
| Variable | Attribute ID | Meaning |
|----------|-------------|---------|
| o | att (1001) | Attacker's ATK |
| u | def (1024) | Target's DEF |
| g | def_coe (1060) | Target's Defense Coefficient |
| b | crit_dam (1005) | Attacker's Crit Damage |
| s | crit_def (1006) | Target's Crit Defense (min 0.5) |
| m | att_resist (1018) | Target's Basic ATK Resistance |
| A | att_dam (1039) | Attacker's Basic ATK Multiplier |
| r | — | Hit type (0=miss, 1=normal, 2=crit) via `checkHit` |

## Raw Code (Annotated)

```javascript
// Line 322756: normalHurt function definition
var b = t("normalHurt", (function(t, a, r, e) {
    void 0 === e && (e = !0);  // default: apply armor/block

    // Get base attributes
    var o = t.data.getAttrib(i.att),       // attacker ATK
        u = a.data.getAttrib(i.def),       // target DEF
        g = a.data.getAttrib(i.def_coe),   // target Defense Coefficient
        b = t.data.getAttrib(i.crit_dam),  // attacker crit damage
        s = Math.max(.5, a.data.getAttrib(i.crit_def)),  // target crit def (MIN 0.5)
        m = a.data.getAttrib(i.att_resist),// target basic ATK resistance
        A = t.data.getAttrib(i.att_dam);   // attacker basic ATK multiplier

    // PAL BRANCH: If attacker is a Partner (Pal)
    if (t.config.type == d.Partner) {
        o = t.parent.data.getAttrib(i.att),     // use PARENT's ATK
        m = a.data.getAttrib(i.partner_resist), // target's Pal Resistance
        m = p(a, t.parent, m, i.partner_resist),// apply Suppress/Inspire
        A = t.data.getAttrib(i.partner_dam);    // pal's own damage multiplier
        var c = t.parent.data.getAttrib(i.partner_dam_extra); // parent's pal_dam_extra
        A = n.round(A * c)

    // GUN BRANCH: If attacker is a Cannon/Gun
    } else if (t.config.type == d.Gun) {
        A = t.data.getAttrib(i.partner_dam),
        m = a.data.getAttrib(i.season_cannon_att_def),
        m = p(a, t, m, i.season_cannon_att_def)

    // PLAYER BRANCH: Normal attacker
    } else {
        e && (m = l(a, t, m, i.att_resist));  // l = calArmorAndBlock
    }

    // CORE FORMULA:
    // Step 1: ATK - DEF * (1 + def_coe)  →  min 1
    // Step 2: × (att_dam × (1 - att_resist))
    var f = n.roundInt(
        Math.max(n.roundInt(o - u * (1 + g)), 1)   // (ATK - DEF*(1+DEF_COE)), min 1
        * n.round(A * n.round(1 - m))               // × att_dam × (1 - resistance)
    );

    // Step 3: Apply calHurt (DMG Resistance + PvE modifiers)
    f = _(f, a, t);  // _ = calHurt

    // Step 4: Apply Critical Damage if crit
    // r==1 means Normal (non-crit), so crit applies when r != 1
    1 == r || (f = n.roundInt(f * Math.max(1.5, n.round(b / s))));

    return Math.max(1, f)  // minimum 1 damage
}))
```

## Extracted Formula

### Player Basic Attack:
```
base_raw = max(roundInt(ATK - DEF × (1 + DEF_COE)), 1)
base_dmg = roundInt(base_raw × round(ATT_DAM × round(1 - ATT_RESIST_after_block)))
after_resist = calHurt(base_dmg, target, attacker)   // applies DMG RES + PvE
if CRIT:
    after_crit = roundInt(after_resist × max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF))))
final = max(1, after_crit_or_after_resist)
```

### Pal Basic Attack:
```
ATK = parent.ATK    (uses parent player's ATK, not pal's)
resistance = calSuppressAndInspire(target, parent, partner_resist)
multiplier = round(partner_dam × parent.partner_dam_extra)
base_raw = max(roundInt(ATK - DEF × (1 + DEF_COE)), 1)
base_dmg = roundInt(base_raw × round(multiplier × round(1 - resistance)))
... rest same as player
```

## calHurt Function (DMG Resistance Application)
**Lines:** 322831-322838

```javascript
_ = t("calHurt", (function(t, a, r) {
    var e = a.data.getAttrib(i.resist),     // target's DMG Resistance
        d = a.data.getAttrib(i.pve_resist), // target's PvE Resistance
        o = r.data.getAttrib(i.pve_dam);    // attacker's PvE Damage Bonus

    t = n.roundInt(t * n.round(1 + o));     // apply PvE damage bonus
    var u = n.roundInt(
        n.roundInt(t * n.round(1 - e))      // × (1 - DMG_RES)
        * n.round(1 - d)                     // × (1 - PvE_RES)
    );
    return Math.max(1, u)
}))
```

### calHurt Formula:
```
step1 = roundInt(damage × round(1 + pve_dam))
step2 = roundInt(roundInt(step1 × round(1 - resist)) × round(1 - pve_resist))
result = max(1, step2)
```

## Comparison with Known Documentation

### Expected (Yuko PDF):
```
Basic ATK DMG = (ATK - DEF) × Basic_ATK_Mult% × (1 - Basic_ATK_RES%) × (1 - DMG_RES%)
```

### Actual (from code):
```
Basic ATK DMG = roundInt(max(roundInt(ATK - DEF × (1 + DEF_COE)), 1) × round(ATT_DAM × round(1 - ATT_RESIST)))
Then: roundInt(roundInt(result × round(1 + PvE_DAM)) × round(1 - DMG_RES)) × round(1 - PvE_RES)
```

### DISCREPANCIES:
1. **DEF_COE (Defense Coefficient):** The code uses `DEF × (1 + def_coe)`, NOT just `DEF`. This is an additional stat not in the Yuko formula. The def_coe stat (ID 1060) modifies DEF multiplicatively.
2. **Resistance application order:** ATT_RESIST is combined with the multiplier in one step: `att_dam × (1 - att_resist)`. DMG RES is applied separately inside `calHurt`.
3. **PvE modifiers:** There are separate PvE damage/resistance stats (pve_dam, pve_resist) applied inside calHurt. These are zero in PvP.
4. **Minimum damage is 1** at multiple stages (base_raw, calHurt output, final output).
5. **Rounding:** The code explicitly uses `roundInt` (floor after rounding to 4 decimals) at each multiplication step. This cumulative rounding matters for simulator accuracy.

## Dependencies
- `calArmorAndBlock` (armor penetration / block system)
- `calSuppressAndInspire` (pal inspire / suppress system)
- `calHurt` (DMG resistance application)
- `checkHit` (hit/miss/crit determination)
