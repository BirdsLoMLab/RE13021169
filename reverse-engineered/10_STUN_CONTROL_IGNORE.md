# 10 — Stun / Control / Ignore Mechanics

## A. Stun (Vertigo) System

### Code Location
**checkDizz:** Lines 322947-322955
**Stun application in SkillHandleNormal:** Lines 430035-430043
**Stun duration reduction:** Line 430036

### checkDizz Function (Lines 322947-322955)
```javascript
t("checkDizz", (function(t, a) {
    var r = t.data.getAttrib(i.vertigo),      // attacker's stun rate
        d = a.data.getAttrib(i.vertigo_def),  // target's stun defense
        o = Math.max(0, n.round(r - d));      // effective stun rate (SUBTRACTIVE)
    if (o <= 0) return !1;

    // Apply correction exponent (same as miss correction)
    var u = n.round(Math.pow(n.round(100 * o), n.round(e.vertigo_correct / 1e4)) / 100);
    // vertigo_correct = 9000, so exponent = 0.9

    if ((u = n.roundInt(1e4 * u)) <= 0) return !1;
    var g = t.battleMain.random.randomInt(0, 1e4);
    return g <= u;
}))
```

### Stun Probability Formula
```
raw_stun = max(0, round(VERTIGO - VERTIGO_DEF))
corrected_stun = round((100 × raw_stun) ^ 0.9 / 100)
probability = roundInt(10000 × corrected_stun)
triggers if random(0, 10000) <= probability
```
**Note:** Uses same power curve correction as miss rate (exponent 0.9).

### Stun Duration Application (Lines 430035-430038)
```javascript
if (E(r.cast, t)) {  // checkDizz returned true
    var Ut = r.cast.data.getAttrib(l.vertigo_times)  // base stun duration
           * i.round(1 - t.data.getAttrib(l.vertigo_res));  // × (1 - stun reduction)
    if ((Ut = i.round(Ut)) > 0) {
        r.addBuff(t, Mt.vertigo_time, Ut);  // apply stun buff
    }
}
```

### Stun Duration Formula
```
stun_duration = round(VERTIGO_TIMES × round(1 - VERTIGO_RES))
if stun_duration > 0: apply stun buff
```
Where:
- `VERTIGO_TIMES` (1030) = base stun duration multiplier
- `VERTIGO_RES` (1031) = stun duration reduction

---

## B. Knock-up / Launch System

### checkThrowHit (Lines 322933-322939)
```javascript
t("checkThrowHit", (function(t, a) {
    var r = t.data.getAttrib(i.suspend),      // launch rate
        e = a.data.getAttrib(i.suspend_def),  // launch defense
        d = n.roundInt(1e4 * n.round(r - e)); // SUBTRACTIVE
    if (d <= 0) return !1;
    var o = t.battleMain.random.randomInt(0, 1e4);
    return o <= d;
}))
```

### checkCounterThrowHit (Lines 322940-322946)
```javascript
t("checkCounterThrowHit", (function(t, a) {
    var r = t.data.getAttrib(i.counter_suspend),  // counter launch rate
        e = a.data.getAttrib(i.suspend_def),       // launch defense
        d = n.roundInt(1e4 * n.round(r - e));
    if (d <= 0) return !1;
    var o = t.battleMain.random.randomInt(0, 1e4);
    return o <= d;
}))
```

### Launch Probability Formula
```
effective_launch = round(SUSPEND - SUSPEND_DEF)
probability = roundInt(10000 × effective_launch)
triggers if random(0, 10000) <= probability
```
**Note:** Launch does NOT use the power curve correction (unlike stun and miss).

---

## C. Ignore Mechanics (Complete List)

All ignore mechanics in the code are **SUBTRACTIVE**:

### Confirmed Subtractive Ignores:

| Mechanic | Rate | Ignore | Formula |
|----------|------|--------|---------|
| Crit | crit_rate (1004) | ignore_crit_rate (1065) | `max(crit_rate - ignore_crit_rate, 0)` |
| Combo | double_hit (1016) | ignore_double_hit (1048) | `max(round(double_hit - ignore_double_hit), 0)` |
| Counter | counter (1017) | ignore_counter (1049) | `max(round(counter - ignore_counter), 0)` |
| Armor Pen | armor_penetration (1068) | ignore_armor_penetration (1069) | `armor_pen > ignore_pen` (threshold) |
| Block | block (1071) | ignore_block (1072) | `block > ignore_block` (threshold) |
| Pal Inspire | partner_inspire (1074) | ignore_partner_inspire (1075) | `inspire > ignore_inspire` (threshold) |
| Pal Suppress | partner_suppress (1077) | ignore_partner_suppress (1078) | `suppress > ignore_suppress` (threshold) |
| Stun | vertigo (1023) | vertigo_def (1026) | `max(0, round(vertigo - vertigo_def))` |
| Launch | suspend (1022) | suspend_def (1025) | `round(suspend - suspend_def)` |
| ATK Hpsteal | att_hpsteal (1014) | att_hpsteal_def (1027) | `att_hpsteal - att_hpsteal_def` |
| Skill Hpsteal | skill_hpsteal (1015) | skill_hpsteal_def (1028) | `max(0, round(skill_hpsteal - skill_hpsteal_def))` |
| HP Steal Rate | hpsteal_rate (1053) | hpsteal_res (1055) | `max(0, hpsteal_rate - hpsteal_res)` |
| HP Steal Amount | hpsteal_amount (1054) | ignore_hpsteal (1056) | `amount × max(0, round(1 - ignore_hpsteal))` |
| HP Recovery | hp_recovery (1012) | ignore_hp_recovery (1066) | `hp_recovery - ignore_hp_recovery` |

### Example (from code, line 322903):
```javascript
p = Math.max(b - l, 0)  // effective crit = max(crit_rate - ignore_crit_rate, 0)
```

### Example (from code, line 322922):
```javascript
var d = n.roundInt(1e4 * Math.max(n.round(r - e), 0));
// effective combo = max(round(double_hit - ignore_double_hit), 0)
```

---

## D. CONTROL_RES Attribute

Attribute ID 1042 (`CONTROL_RES`) exists in the AttribDefine but its specific usage location was not found in the primary combat functions analyzed. It may be used in buff application code or specific skill effects.

---

## Comparison with Known Documentation

### Expected:
```
120% counter - 40% ignore counter = 60% final counter (not 80%)
```

### Actual:
**CONFIRMED subtractive model.** `max(round(1.20 - 0.40), 0) = 0.80`, then `probability = roundInt(10000 × 0.80) = 8000`.

Wait — this shows 80%, not 60%. Let me re-examine:
- The code: `Math.max(n.round(r - e), 0)` where r=counter, e=ignore_counter
- If counter = 1.20 and ignore_counter = 0.40: `max(round(1.20 - 0.40), 0) = 0.80`
- This gives **80% effective counter rate**, not 60%

The community example "120% - 40% = 60%" appears to be **incorrect** if the values are in decimal form. If the values are in percentage form (120 and 40, stored as 1.20 and 0.40), then 1.20 - 0.40 = 0.80 = 80%.

**The subtractive model IS confirmed but the arithmetic example in the task description seems off.**
