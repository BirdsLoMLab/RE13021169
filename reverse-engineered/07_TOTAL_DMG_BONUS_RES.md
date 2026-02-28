# 07 — Total DMG Bonus / DMG RES

## Code Location
**BuffVampire.calDamage:** Lines 196752-196777
**SkillRunner spirit damage:** Lines 431464-431467
**Config floor:** Line 237503

---

## A. Total DMG Bonus/RES Application (BuffVampire)

### Code Location
Lines 196752-196777

### Variable Mapping
| Variable | Attribute | Meaning |
|----------|-----------|---------|
| u | — | Caster (attacker) unit |
| s | total_dam_add (1081) | Attacker's Total DMG Bonus |
| f | total_dam_def (1082) | Target's Total DMG Resistance |
| h | — | Multiplier: max(1 + s - f, floor) |
| e.total_damage_add_down_limit | — | Config: 2000 (= 0.20x floor) |

### Raw Code (Annotated)
```javascript
o.calDamage = function(t, i, a) {
    var o;
    // Check skill whitelist
    if (!(this._limitSkill.length > 0) || this._limitSkill.includes(a)) {
        var u = this.runner.cast,  // attacker

            // Get Total DMG Bonus from ATTACKER
            s = u.data.getAttrib(c.total_dam_add),        // 1081

            // Get Total DMG RES from OWNER (the unit with this buff = target)
            f = this.owner.data.getAttrib(c.total_dam_def), // 1082

            // FORMULA: max(1 + bonus - resistance, floor)
            h = Math.max(1 + s - f, e.total_damage_add_down_limit / 1e4),
            // e.total_damage_add_down_limit = 2000
            // So floor = 2000 / 10000 = 0.20

            p = 0;

        switch (this._calType) {
            case 0:
                p = r.round(t * h);  // damage × multiplier
        }

        // Cap check based on attacker HP
        var _ = 0;
        switch (this._topType) {
            case 0:
                var d = u.data.getAttrib(c.hp);
                _ = r.round(d * this._max / 1e4);  // max heal = attacker_HP × _max/10000
        }

        // Apply PvP factor
        var m = this.runner.battleMain;
        p = Math.max(r.roundInt(p / this.runner.battleMain.injuryReduce), 1);

        // XOR-based skill damage scaling
        var g = null != (o = this.runner.useSkill.skillDam[0]) ? o : 1e4 ^ n,
            v = r.round(p * (g ^ n) / 1e4),
            y = v,
            b = _ / m.treatDecay;

        // Apply heal limit and heal decay
        y < _ && (b = v / m.treatDecay);
        this.runner.healthTarget(u, b, l.Treat, !1, this.config.id);
        return b;
    }
}
```

### Spirit Damage (Lines 431464-431467)
```javascript
var Y = f.data.getAttrib(T.total_dam_add),
    j = t.data.getAttrib(T.total_dam_def),
    q = Math.max(1 + Y - j, a.total_damage_add_down_limit / 1e4);
e = r.round(e * q);
```

---

## B. Extracted Formula

### Total DMG Multiplier:
```
multiplier = max(1 + TOTAL_DAM_ADD - TOTAL_DAM_DEF, 0.20)
```

Where:
- `TOTAL_DAM_ADD` = attacker's attribute 1081 (Total DMG Bonus)
- `TOTAL_DAM_DEF` = target's attribute 1082 (Total DMG Resistance)
- Floor = 0.20 (from `total_damage_add_down_limit = 2000 / 10000`)

### Application:
```
modified_damage = round(base_damage × multiplier)
```

---

## C. Where Total DMG Bonus/RES is Applied

### In BuffVampire (Life Steal):
BuffVampire is the primary carrier of Total DMG Bonus/RES in the game. When life steal triggers:
1. Calculate Total DMG multiplier
2. Apply to damage to determine heal amount
3. Divide by PvP factor
4. Cap by attacker's HP
5. Apply heal decay
6. Heal the attacker

### In Spirit Damage:
Applied directly to spirit damage before it's dealt.

### NOT Applied To:
- HP-based damage (confirmed in 05_HP_BASED_DAMAGE.md)
- Direct damage from `normalHurt` / `normalDoubleHurt` / `normalCounterHurt` — these use `calHurt` which applies `resist` (DMG RES, ID 1021), NOT `total_dam_add/def`

---

## D. DMG RES (resist, ID 1021) vs Total DMG (total_dam_add/def, 1081/1082)

**These are SEPARATE systems:**

### DMG RES (`resist`, ID 1021):
- Applied inside `calHurt()` function (line 322831-322838)
- Formula: `damage × round(1 - resist) × round(1 - pve_resist)`
- Applied to ALL damage types that go through calHurt
- Simple multiplicative reduction

### Total DMG Bonus/RES (`total_dam_add`/`total_dam_def`, 1081/1082):
- Applied in BuffVampire and Spirit damage contexts
- Formula: `damage × max(1 + bonus - resistance, 0.20)`
- Subtractive between attacker and defender
- Has a floor of 0.20x (damage cannot go below 20% of base)

---

## Comparison with Known Documentation

### Expected:
```
Multiplier = max(1 + Bonus - RES, Floor)
```

### Actual:
```
Multiplier = max(1 + total_dam_add - total_dam_def, 0.20)
```

- **Subtractive model: CONFIRMED**
- **Floor value: 0.20 (20%) — from config `total_damage_add_down_limit = 2000`**
- **DISCREPANCY from Yuko:** The floor was unknown. Now confirmed as 0.20.

### Key Discovery:
Total DMG Bonus/RES is NOT a final layer applied to all damage. It's specifically applied through BuffVampire (life steal) and Spirit damage calculations. Normal attack damage, combo, counter, and skill damage use `resist` (ID 1021) via `calHurt()`, not `total_dam_add/def`.

This is a significant finding — Total DMG Bonus/RES may have a more limited scope than previously documented.
