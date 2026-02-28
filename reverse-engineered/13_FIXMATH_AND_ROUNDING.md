# 13 — FixMath & Rounding Behavior

## Code Location
**Module:** FixMath.ts
**Lines:** 292602-292620

---

## Core Functions

### round(x) — Line 292606
```javascript
t.round = function(t) {
    return (t > 0 ? Math.floor(1e4 * t + .5) : Math.ceil(1e4 * t - .5)) / 1e4
}
```

**Behavior:**
- Rounds to 4 decimal places
- For positive: `Math.floor(10000 × x + 0.5) / 10000` — standard rounding
- For negative: `Math.ceil(10000 × x - 0.5) / 10000` — rounds away from zero

**Examples:**
```
round(1.23456) = Math.floor(12345.6 + 0.5) / 10000 = Math.floor(12346.1) / 10000 = 12346 / 10000 = 1.2346
round(0.33333) = Math.floor(3333.3 + 0.5) / 10000 = Math.floor(3333.8) / 10000 = 3333 / 10000 = 0.3333
round(1.00005) = Math.floor(10000.5 + 0.5) / 10000 = Math.floor(10001.0) / 10000 = 10001 / 10000 = 1.0001
round(-0.5)    = Math.ceil(-5000 - 0.5) / 10000 = Math.ceil(-5000.5) / 10000 = -5000 / 10000 = -0.5
```

### roundInt(x) — Line 292608
```javascript
t.roundInt = function(t) {
    return Math.floor(this.round(t))
}
```

**Behavior:**
- First rounds to 4 decimal places via `round()`
- Then floors to integer via `Math.floor()`

**Examples:**
```
roundInt(123.456) = Math.floor(round(123.456)) = Math.floor(123.4560) = 123
roundInt(99.9999) = Math.floor(round(99.9999)) = Math.floor(99.9999) = 99
roundInt(100.00005) = Math.floor(round(100.00005)) = Math.floor(100.0001) = 100
roundInt(99.99999) = Math.floor(round(99.99999)) = Math.floor(100.0000) = 100
```

### clamp(value, min, max) — Line 292613
```javascript
t.clamp = function(t, n, r) {
    if (n > r) { var u = n; n = r; r = u; }  // swap if min > max
    return t < n ? n : t > r ? r : t;
}
```

---

## Why This Matters for Simulation

### Cumulative Rounding Errors
The game applies `roundInt` at EVERY multiplication step. This means:
```
roundInt(A * B) * C  ≠  roundInt(A * B * C)
```

For example, in the basic damage formula:
```javascript
// Step 1: roundInt(ATK - DEF * (1 + def_coe))
// Step 2: Math.max(step1, 1)
// Step 3: roundInt(step2 * round(att_dam * round(1 - att_resist)))
// Each intermediate value is rounded before the next operation
```

A simulator that computes `(ATK - DEF*(1+def_coe)) * att_dam * (1-att_resist)` in one floating-point operation will get slightly different results than the game.

### 1e4 Scaling Convention
Many values are stored as integers and divided by 10000:
```
pvp_injury_reduce / 1e4  → actual multiplier
shield_correct / 1e4     → actual shield decay
skillPar / 1e4           → often (but not always, depends on context)
attrib values            → some are stored as ×10000, others as direct values
```

The `round()` function ensures these divisions produce consistent 4-decimal results.

---

## Impact on Key Formulas

### Example: Basic ATK Damage
```
True formula with rounding:
  step1 = round(1 - att_resist)           // round to 4 decimals
  step2 = round(att_dam * step1)          // round to 4 decimals
  step3 = roundInt(ATK - DEF * (1 + def_coe))  // floor after rounding
  step4 = max(step3, 1)                   // minimum 1
  step5 = roundInt(step4 * step2)         // floor after rounding
  step6 = round(1 + pve_dam)             // in calHurt
  step7 = roundInt(step5 * step6)         // calHurt step 1
  step8 = round(1 - resist)              // DMG RES
  step9 = roundInt(step7 * step8)         // calHurt step 2
  step10 = round(1 - pve_resist)         // PvE resist
  step11 = roundInt(step9 * step10)       // calHurt final
  result = max(step11, 1)
```

That's 11 rounding operations for a single basic attack, each of which can affect the final value by ±1.
