# 11 — Pal Damage System

## Code Location
**Pal Basic Attack:** Lines 322765-322769 (in normalHurt)
**Pal Combo Attack:** Lines 322851-322859 (in normalDoubleHurt)
**Pal Counter Attack:** normalCounterHurt uses parent ATK via same pattern

---

## A. Pal Basic Attack (normalHurt, Partner branch)

### Code (Lines 322765-322771)
```javascript
if (t.config.type == d.Partner) {
    // Use PARENT's ATK, not pal's own
    o = t.parent.data.getAttrib(i.att);

    // Use partner_resist instead of att_resist
    m = a.data.getAttrib(i.partner_resist);

    // Apply Suppress/Inspire to resistance
    m = p(a, t.parent, m, i.partner_resist);  // calSuppressAndInspire

    // Use pal's own partner_dam multiplier
    A = t.data.getAttrib(i.partner_dam);

    // Multiply by parent's partner_dam_extra
    var c = t.parent.data.getAttrib(i.partner_dam_extra);
    A = n.round(A * c);
}

// Then standard formula with modified values:
var f = n.roundInt(
    Math.max(n.roundInt(o - u * (1 + g)), 1)  // (ParentATK - DEF*(1+DEF_COE))
    * n.round(A * n.round(1 - m))              // × (partner_dam × partner_dam_extra) × (1 - partner_resist)
);
f = _(f, a, t);  // calHurt: DMG RES
// crit check same as player
```

### Extracted Formula
```
base_raw = max(roundInt(PARENT_ATK - DEF × (1 + DEF_COE)), 1)
pal_mult = round(PARTNER_DAM × PARENT_PARTNER_DAM_EXTRA)
resistance = calSuppressAndInspire(target, parent, PARTNER_RESIST)
pal_dmg = roundInt(base_raw × round(pal_mult × round(1 - resistance)))
pal_dmg = calHurt(pal_dmg, target, attacker)  // DMG RES
if CRIT:
    pal_dmg = roundInt(pal_dmg × max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF))))
result = max(1, pal_dmg)
```

---

## B. Pal Combo Attack (normalDoubleHurt, Partner branch)

### Code (Lines 322851-322859)
```javascript
if (t.config.type == d.Partner) {
    o = t.parent.data.getAttrib(i.att);    // parent's ATK
    var v = t.data.getAttrib(i.partner_dam),    // pal's damage mult
        h = t.parent.data.getAttrib(i.partner_dam_extra);  // parent's extra mult
    v = n.round(v * h);  // combined pal multiplier

    var M = a.data.getAttrib(i.partner_resist),
        I = p(a, t.parent, M, i.partner_resist);  // suppress/inspire

    var x = n.roundInt(Math.max(n.roundInt(o - u * (1 + g)), 1) * v)
            * n.round(1 - I);

    // Then multiply by combo multiplier
    f = n.roundInt(n.roundInt(x) * c);  // c = double_hit_dam
    f = n.roundInt(f);
}
```

### Extracted Formula
```
base_raw = max(roundInt(PARENT_ATK - DEF × (1 + DEF_COE)), 1)
pal_mult = round(PARTNER_DAM × PARTNER_DAM_EXTRA)
resistance = calSuppressAndInspire(target, parent, PARTNER_RESIST)

pal_base = roundInt(base_raw × pal_mult) × round(1 - resistance)
pal_combo = roundInt(roundInt(pal_base) × DOUBLE_HIT_DAM)
pal_combo = roundInt(pal_combo)
```

**Note:** For pal combo, the combo multiplier (`double_hit_dam`) is applied AFTER the pal damage calculation, not combined with `partner_dam`.

---

## C. Key Pal Attributes

| Attribute | ID | Owner | Description |
|-----------|----|-------|-------------|
| partner_dam | 1040 | Pal | Pal's base damage multiplier |
| partner_dam_extra | 1047 | Player (parent) | Player's pal damage bonus multiplier |
| partner_resist | 1020 | Target | Target's pal damage resistance |
| partner_inspire | 1074 | Attacker | Inspire value (reduces target resistance) |
| partner_inspire_rate | 1073 | Target | Inspire proc rate |
| partner_suppress | 1077 | Target | Suppress value (increases target resistance) |
| partner_suppress_rate | 1076 | Attacker | Suppress proc rate |
| ignore_partner_inspire | 1075 | Target | Ignore inspire |
| ignore_partner_suppress | 1078 | Attacker | Ignore suppress |

---

## D. Pal ATK Source

**Critical finding:** Pal damage uses the **PARENT player's ATK stat**, not the pal's own ATK:
```javascript
o = t.parent.data.getAttrib(i.att);  // parent's ATK
```

This is consistent across basic attack, combo, and counter. The pal's own contribution is through `partner_dam` (its damage multiplier).

---

## E. Pal in HP-Based Damage (_calHpHurt)

From BuffSkillValue._calHpHurt (lines 195801-195806):
```javascript
if (!r.isCallType && r.config.type == s.Partner) {
    c = r.parent.data.getAttrib(u.att);     // parent's ATK
    var _ = r.data.getAttrib(u.partner_dam),
        v = r.data.getAttrib(u.partner_dam_extra);
    p = n.round(p * _ * v);  // combine att_dam × partner_dam × partner_dam_extra
}
```
For HP-based damage clamping, pal uses: `ATT_DAM × PARTNER_DAM × PARTNER_DAM_EXTRA` as the multiplier.

---

## Comparison with Known Documentation

### Expected (Yuko PDF):
```
Pal Basic = (ATK - DEF) × Pal_Mult × Pal_DMG% × (1 - Pal_RES%) × (1 - DMG_RES%)
Pal Combo = Pal_Basic × Pal_Combo_Mult%
```

### Actual:
```
Pal Basic = roundInt(
    max(roundInt(PARENT_ATK - DEF × (1 + DEF_COE)), 1)
    × round(round(PARTNER_DAM × PARTNER_DAM_EXTRA) × round(1 - PARTNER_RESIST_after_inspire))
)
then: calHurt(result) for DMG RES

Pal Combo = roundInt(roundInt(pal_base_before_resist) × DOUBLE_HIT_DAM)
then: calHurt for DMG RES
```

### DISCREPANCIES:
1. **DEF_COE applies to pal damage too** — `DEF × (1 + DEF_COE)`, not just DEF
2. **Pal combo applies combo multiplier AFTER the pal damage calc**, not as a simple multiplication of the basic result
3. **partner_dam_extra is from the PARENT player**, not the pal itself
4. **Suppress/Inspire modifies partner_resist**, not applied as a separate multiplier
5. **The `Pal_DMG%` in Yuko's formula is actually `partner_dam × partner_dam_extra`**, a combined multiplier
