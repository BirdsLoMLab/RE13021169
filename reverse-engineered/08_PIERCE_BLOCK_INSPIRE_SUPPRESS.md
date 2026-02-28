# 08 — Pierce/Block & Pal Inspire/Suppress

## A. Armor Penetration / Block System

### Code Location
**Module:** HurtUtil.ts
**Function:** `calArmorAndBlock` — Lines 322773-322801

### Variable Mapping
| Variable | Attribute | Meaning |
|----------|-----------|---------|
| g | armor_penetration (1068) | Attacker's Armor Pen value |
| b | ignore_armor_penetration (1069) | Target's Ignore Armor Pen |
| l | ignore_block (1072) | Attacker's Ignore Block |
| p | block (1071) | Target's Block value |
| _ | armor_penetration_rate (1067) | Attacker's Armor Pen proc rate |
| s | block_rate (1070) | Target's Block proc rate |
| r | — | Input resistance value (to modify) |

### Raw Code (Annotated)
```javascript
l = t("calArmorAndBlock", (function(t, a, r, e) {
    // t = defender, a = attacker, r = current resistance, e = resist attribute ID
    var d = [0, 0, 0],   // probability ranges
        g = a.data.getAttrib(i.armor_penetration),      // attacker armor pen
        b = t.data.getAttrib(i.ignore_armor_penetration), // defender ignore pen
        l = a.data.getAttrib(i.ignore_block),            // attacker ignore block
        p = t.data.getAttrib(i.block);                    // defender block

    // Armor Pen probability (only if pen > ignore)
    if (g > b) {
        var _ = a.data.getAttrib(i.armor_penetration_rate);
        d[0] = n.roundInt(1e4 * _);  // pen proc rate
    }

    // Block probability (only if block > ignore, ADDITIVE with pen range)
    if (p > l) {
        var s = t.data.getAttrib(i.block_rate);
        d[1] = d[0] + n.roundInt(1e4 * s);  // block adds on top of pen range
    }

    d[2] = 1e4;  // remainder = normal

    // Random roll: 0 to 10000
    var A = a.battleMain.random.randomInt(0, 1e4);
    for (var m = -1, c = 0; c < 2; c++)
        if (d[c] > 0 && A <= d[c]) {
            m = c;
            break;
        }
    -1 == m && (m = 2);  // default to normal (no proc)

    var f = r;  // start with input resistance

    // ARMOR PENETRATION: reduces resistance
    if (0 == m) {
        f = n.round(r - Math.min(.5, (g - b) / 1e4));
        // Show pierce UI animation
        a.hit(a, n.round(1e4 * f), o.Armor, ...);
    }
    // BLOCK: increases resistance
    else if (1 == m) {
        f = n.round(r + Math.min(.5, (p - l) / 1e4));
        // Show block UI animation
        t.hit(t, n.round(1e4 * f), o.Armor_def, ...);
    }

    // Apply attribute cap (up_limit)
    var v = t.data.getAttribMeta(e).config;
    if (0 != v.up_limit) {
        var h = v.up_limit;
        2 == v.num_type && (h = n.round(h / 1e4));
        f = Math.min(f, h);
    }

    return f;  // modified resistance value
}))
```

### Extracted Formula

#### Probability:
```
Can armor pen proc?  → armor_penetration > ignore_armor_penetration
Can block proc?      → block > ignore_block

pen_probability  = roundInt(10000 × armor_penetration_rate)    [if pen can proc]
block_probability = roundInt(10000 × block_rate)                [if block can proc]

Random roll 0-10000:
  [0..pen_probability]                        → Armor Penetration
  [pen_probability..pen_probability+block]    → Block
  [above]                                      → Normal (no proc)
```

#### Effect on Resistance:
```
If ARMOR PENETRATION procs:
    new_resistance = round(old_resistance - min(0.5, (armor_pen - ignore_pen) / 10000))
    Resistance DECREASES (more damage taken)
    Capped: resistance decrease cannot exceed 0.5 (50%)

If BLOCK procs:
    new_resistance = round(old_resistance + min(0.5, (block - ignore_block) / 10000))
    Resistance INCREASES (less damage taken)
    Capped: resistance increase cannot exceed 0.5 (50%)

If NEITHER procs:
    resistance unchanged

Final: resistance capped by attribute's up_limit config
```

#### Key Properties:
- Pierce and Block are **mutually exclusive** per attack
- Pierce/Block check uses the **same random roll** (priority: pierce first)
- The effect is bounded to ±0.5 (±50% resistance change)
- It modifies the RESISTANCE value that's then used in the damage formula
- Ignore mechanics are **subtractive**: `effective_pen = pen - ignore_pen`

---

## B. Pal Inspire / Suppress System

### Code Location
**Module:** HurtUtil.ts
**Function:** `calSuppressAndInspire` — Lines 322802-322830

### Variable Mapping
| Variable | Attribute | Meaning |
|----------|-----------|---------|
| g | partner_inspire (1074) | Attacker's Pal Inspire value |
| b | ignore_partner_inspire (1075) | Target's Ignore Inspire |
| l | ignore_partner_suppress (1078) | Attacker's Ignore Suppress |
| p | partner_suppress (1077) | Target's Pal Suppress value |
| _ | partner_suppress_rate (1076) | Attacker's Suppress proc rate |
| s | partner_inspire_rate (1073) | Target's Inspire proc rate |

### Extracted Formula

**Identical structure to Armor Penetration / Block, but for Pal damage:**

```
Can suppress proc?  → partner_inspire > ignore_partner_inspire
Can inspire proc?   → partner_suppress > ignore_partner_suppress

suppress_probability = roundInt(10000 × partner_suppress_rate)
inspire_probability  = roundInt(10000 × partner_inspire_rate)

If SUPPRESS procs (analogous to armor pen):
    new_resistance = round(old_resistance - min(0.5, (inspire - ignore_inspire) / 10000))
    Pal takes MORE damage

If INSPIRE procs (analogous to block):
    new_resistance = round(old_resistance + min(0.5, (suppress - ignore_suppress) / 10000))
    Pal takes LESS damage
```

### Where It's Used:
- In `normalHurt` (line 322766) for Pal basic attacks: applied to `partner_resist`
- In `normalDoubleHurt` for Pal combo attacks
- In `BuffSkillValue._calResistPar` case 10 for Pal skill damage

---

## Comparison with Known Documentation

### Key Findings:
1. **Pierce/Block modifies resistance, not damage directly.** The resistance change then affects the damage formula.
2. **Both systems cap the effect at ±50%** (0.5)
3. **Priority: Pierce is checked first.** If both could proc, pierce has priority.
4. **Ignore mechanics are subtractive.** You need `armor_pen > ignore_pen` to even have a chance to proc.
5. **Attribute up_limit caps the final resistance value** regardless of pierce/block effect.
