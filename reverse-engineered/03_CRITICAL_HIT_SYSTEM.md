# 03 — Critical Hit System

## Code Location
**Module:** HurtUtil.ts
**Lines:** 322896-322961 in `game_script_pretty.js`
**Functions:** `checkHit`, `checkSkillCirt`

---

## A. Normal Crit (checkHit)

### Code Location
Lines 322896-322917

### Variable Mapping
| Variable | Attribute | Meaning |
|----------|-----------|---------|
| d | hit (1007) | Attacker's Hit/Accuracy |
| o | miss (1008) | Target's Evasion (0 if forced hit) |
| u | battle_up_limit[0][1] / 1e4 | Miss rate cap |
| b | crit_rate (1004) | Attacker's Crit Rate |
| l | ignore_crit_rate (1065) | Target's Ignore Crit Rate |
| p | — | Effective crit rate: max(crit_rate - ignore_crit_rate, 0) |
| _ | — | Raw evasion: max(round(miss - hit), 0) |
| s | — | Corrected evasion: round((100 × raw_evasion)^(miss_correct/1e4) / 100) |
| m | — | Capped evasion (capped by battle_up_limit in PvP) |

### Raw Code (Annotated)
```javascript
c = t("checkHit", (function(t, a, r) {
    void 0 === r && (r = !1);  // r = force hit (ignore miss)

    var d = t.data.getAttrib(i.hit),    // attacker's accuracy
        o = r ? 0 : a.data.getAttrib(i.miss),  // target evasion (0 if forced)
        u = n.round(e.battle_up_limit[0][1] / 1e4),  // miss cap = 8000/10000 = 0.80
        b = t.data.getAttrib(i.crit_rate),      // attacker crit rate
        l = a.data.getAttrib(i.ignore_crit_rate), // target ignore crit
        p = Math.max(b - l, 0),  // EFFECTIVE CRIT RATE (subtractive!)

        _ = Math.max(n.round(o - d), 0),  // raw evasion difference
        // Apply miss correction exponent: (100 × evasion)^(9000/10000) / 100
        s = n.round(Math.pow(n.round(100 * _), n.round(e.miss_correct / 1e4)) / 100),
        m = s,
        c = t.battleMain.data.chapterType;

    // Cap evasion in PvP (non-PvE)
    1 != configChapter_type.getDataByKey(c).pve && (m = Math.min(s, u));
    // u = 0.80, so max miss chance is 80% in PvP

    var f = t.battleMain.random.randomInt(0, 1e4);  // random 0-10000

    // Build probability ranges: [0..miss_range] [miss..normal_range] [normal..crit_range]
    A[g.Miss]   = n.roundInt(1e4 * m);  // miss probability
    A[g.Normal] = n.roundInt(A[g.Miss] + n.roundInt(n.round(1 - m) * n.round(1 - p) * 1e4));
    A[g.Cirt]   = n.roundInt(A[g.Normal] + n.roundInt(n.round(1 - m) * p * 1e4));

    // Check which range the random number falls in
    var v = -1;
    for (var h = 0; h < 2; h++)
        if (A[h] > 0 && f <= A[h]) {
            v = h;
            break
        }
    return -1 == v && (v = g.Cirt), v  // default to Crit if no match (rounding edge case)
}))
```

### Extracted Formula

#### Miss Chance:
```
raw_evasion = max(round(MISS - HIT), 0)
corrected_evasion = round((100 × raw_evasion) ^ (miss_correct / 10000) / 100)
    where miss_correct = 9000, so exponent = 0.9

In PvP: final_evasion = min(corrected_evasion, 0.80)
In PvE: final_evasion = corrected_evasion (no cap)
```

#### Crit Chance:
```
effective_crit = max(CRIT_RATE - IGNORE_CRIT_RATE, 0)
```

#### Hit Outcome Probabilities:
```
P(miss) = final_evasion
P(normal) = (1 - final_evasion) × (1 - effective_crit)
P(crit) = (1 - final_evasion) × effective_crit
```

#### Crit Damage (from normalHurt, line 322771):
```
crit_multiplier = max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF)))
crit_damage = roundInt(base_damage × crit_multiplier)
```

---

## B. Skill Crit (checkSkillCirt)

### Code Location
Lines 322956-322961

### Raw Code (Annotated)
```javascript
t("checkSkillCirt", (function(t) {
    var a = t.data.getAttrib(i.skill_crit_rate),  // skill crit rate
        r = n.roundInt(1e4 * a);  // convert to 0-10000 range
    if (r <= 0) return !1;  // no skill crit if rate is 0

    var e = t.battleMain.random.randomInt(0, 1e4);
    return e < r  // NOTE: strict less-than (not <=)
}))
```

### Skill Crit Damage (from BuffSkillValue, lines 195883-195886):
```javascript
if (checkSkillCirt(r)) {
    var L = r.data.getAttrib(u.skill_crit_dam);   // skill crit damage bonus
    x = n.roundInt(x * n.round(1 + L)),           // × (1 + skill_crit_dam)
    x = n.roundInt(Math.pow(x, .98)),              // × x^0.98 (CONFIRMED)
    P = d.Hurt_Crit
}
```

### Extracted Formula:
```
skill_crit_probability = roundInt(10000 × SKILL_CRIT_RATE)
triggers if random(0, 10000) < probability

skill_crit_damage = roundInt(roundInt(damage × round(1 + SKILL_CRIT_DAM)) ^ 0.98)
```

---

## Comparison with Known Documentation

### Expected (Yuko PDF):
```
Crit DMG = DMG × (Crit_DMG% / Crit_RES%)
Min Crit RES = 50%
Min (Crit_DMG / Crit_RES) = 1.5
Skill Crit = Skill × (1 + Skill_Crit_DMG%)^0.98
```

### Actual (from code):

#### Normal Crit:
- **Min Crit DEF = 0.5 (50%) — CONFIRMED** (`Math.max(.5, ...)`)
- **Min crit multiplier = 1.5 — CONFIRMED** (`Math.max(1.5, ...)`)
- Formula: `max(1.5, CRIT_DAM / max(0.5, CRIT_DEF))` — **CONFIRMED**

#### Skill Crit:
- **0.98 exponent — CONFIRMED** (`Math.pow(x, .98)`)
- But formula structure differs slightly: `roundInt(roundInt(x × round(1 + SKILL_CRIT_DAM)) ^ 0.98)`
- The exponent is applied to the RESULT of `damage × (1 + skill_crit_dam)`, NOT to `(1 + skill_crit_dam)` itself
- **DISCREPANCY:** Yuko says `Skill × (1 + Skill_Crit_DMG%)^0.98` (exponent on the multiplier). Code says `(Skill × (1 + Skill_Crit_DMG%))^0.98` (exponent on the product). This is mathematically equivalent: `a × b^0.98 ≠ (a × b)^0.98`, so the code version is different.

#### Ignore Crit:
- **CONFIRMED subtractive:** `effective_crit = max(crit_rate - ignore_crit_rate, 0)`
- Applied BEFORE the random roll, so it reduces the probability directly

#### Miss/Evasion:
- Not in Yuko PDF — evasion uses a power curve: `(100×evasion)^0.9 / 100`
- PvP miss cap = 80%
- PvE has no miss cap

---

## Discoveries

1. **Skill crit exponent applied to product, not factor:** `(DMG × (1+SCRIT))^0.98` not `DMG × (1+SCRIT)^0.98`
2. **checkSkillCirt uses strict less-than** (`<`), while checkHit uses less-than-or-equal (`<=`). This is a subtle difference.
3. **Crit and skill crit are separate systems.** A skill can have BOTH normal crit and skill crit depending on flags.
4. **Miss correction uses power function** with exponent 0.9, creating diminishing returns for high evasion.
