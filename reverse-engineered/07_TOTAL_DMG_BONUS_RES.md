# 07 — Total DMG Bonus / DMG RES (Final DMG Boost / Final DMG Res)

## Code Locations
**SkillRunner.healthTarget():** game_script.js line 7229 (PRIMARY — applies to ALL damage)
**BuffVampire.calDamage:** Lines 196752-196777 (SECONDARY — life steal heal)
**NeedAddDamHurtList:** EnumDefine.ts, game_script.js line 4779
**Config floor:** Line 237503
**Partner sync:** Unit.onLastUpdate(), game_script.js line 7499

---

## A. Primary Application — SkillRunner.healthTarget()

### Code Location
game_script.js line 7229, inside `healthTarget()` method

### Raw Code (Annotated)
```javascript
// After all damage type-specific processing (boss_def, share_damage, delay_damage, etc.)
// and BEFORE DEFER_DAMAGE buff processing:

if (NeedAddDamHurtList.includes(healthType) && attacker != target) {
    var Y = attacker.data.getAttrib(T.total_dam_add),   // 1081
        j = target.data.getAttrib(T.total_dam_def),      // 1082
        q = Math.max(1 + Y - j, a.total_damage_add_down_limit / 1e4);
        // total_damage_add_down_limit = 2000 → floor = 0.20
    e = r.round(e * q);   // damage × multiplier
}
```

### Conditions
1. The damage `healthType` must be in `NeedAddDamHurtList`
2. Attacker must not equal target (`f != t`) — no self-damage boost

### NeedAddDamHurtList (game_script.js line 4779)
All 13 damage types that receive the multiplier:

| HealthType | ID | Description |
|------------|-----|-------------|
| Hurt | 1 | Normal attack damage |
| Hurt_Crit | 2 | Critical hit damage |
| Hurt_Ret | 3 | Return/reflect damage |
| Hurt_Share_Damage | 13 | Shared damage |
| Hurt_Share_Damage_Crit | 14 | Shared damage (crit) |
| Hurt_Double | 15 | Combo/double hit |
| Hurt_Double_Crit | 16 | Combo (crit) |
| Real_Damage | 20 | True damage |
| Hurt_Bleed | 19 | Bleed damage |
| Hurt_Bleed_Crit | 23 | Bleed (crit) |
| Hurt_Counter | 21 | Counter damage |
| Hurt_Counter_Crit | 22 | Counter (crit) |
| SpiritToPlayer | 31 | Spirit → player damage |

**This covers ALL offensive damage types.** HP-based damage (BuffSkillHpHurt) is also affected because it calls `healthTarget()` with `HealthType.Hurt`.

### NOT Affected
| HealthType | ID | Why |
|------------|-----|-----|
| Treat | 4 | Healing |
| Treat_Crit | 5 | Critical healing |
| Skill_Hpsteal | 11 | Skill-based life steal |
| Act_Hpsteal | 12 | Attack-based life steal |
| Miss | 6 | Miss event |
| Shield | 18 | Shield creation |
| SpiritToSpirit | 30 | Spirit vs spirit (has its own formula) |

---

## B. Secondary Application — BuffVampire (Life Steal)

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

---

## C. Extracted Formula

### Total DMG Multiplier:
```
multiplier = max(1 + TOTAL_DAM_ADD - TOTAL_DAM_DEF, 0.20)
```

Where:
- `TOTAL_DAM_ADD` = attacker's attribute 1081 (Total DMG Bonus / Final DMG Boost)
- `TOTAL_DAM_DEF` = target's attribute 1082 (Total DMG Resistance / Final DMG Res)
- Floor = 0.20 (from `total_damage_add_down_limit = 2000 / 10000`)

### Application:
```
modified_damage = round(base_damage × multiplier)
```

---

## D. Where Total DMG Bonus/RES is Applied

### Universal Damage Multiplier (healthTarget):
Total DMG Bonus/RES is a **universal final multiplier** applied to virtually all damage in the game through `SkillRunner.healthTarget()`. This includes:
- Normal attacks and crits
- Combo/double hits and crits
- Counter attacks and crits
- Bleed damage and crits
- Real/true damage
- Return/reflect damage
- Shared damage
- Spirit → player damage
- **HP-based damage** (BuffSkillHpHurt uses `HealthType.Hurt`)

### Pipeline Position:
Applied **after** all buff modifiers (FRAGILE_EFFECT, EXTRA_DAMAGE, GIANT_SLAYER, boss_dam) and **before** DEFER_DAMAGE buff processing. This is the last multiplicative layer before damage hits the target.

### In BuffVampire (Life Steal):
BuffVampire also uses the same formula independently to calculate life steal heal amounts.

### Partner/Summon Sync:
From `Unit.onLastUpdate()` (game_script.js line 7499): Partner and CallUnit types sync their `total_dam_add` from their parent unit:
```javascript
this.data.attribs[I.total_dam_add].setAttribValue(
    this.parent.data.attribs[I.total_dam_add]
)
```
This ensures summoned units also benefit from the player's Final DMG Boost.

---

## E. DMG RES (resist, ID 1021) vs Total DMG (total_dam_add/def, 1081/1082)

**These are SEPARATE systems applied at DIFFERENT stages:**

### DMG RES (`resist`, ID 1021):
- Applied inside `calHurt()` function (line 322831-322838)
- Formula: `damage × round(1 - resist) × round(1 - pve_resist)`
- Applied during base damage calculation (early in pipeline)
- Simple multiplicative reduction

### Total DMG Bonus/RES (`total_dam_add`/`total_dam_def`, 1081/1082):
- Applied in `healthTarget()` — the final damage delivery method (late in pipeline)
- Formula: `damage × max(1 + bonus - resistance, 0.20)`
- Subtractive between attacker and defender
- Has a floor of 0.20x (damage cannot go below 20% of base)
- Applied AFTER resist, crit, buff modifiers — acts as a true "final" multiplier

**Both stack multiplicatively** — a target with both DMG RES and Total DMG RES benefits from both reductions.

---

## F. Comparison with Known Documentation

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
- **Universal scope: CONFIRMED** — applied to all 13 damage types in NeedAddDamHurtList
- **"Final" multiplier position: CONFIRMED** — last multiplicative layer before damage application

### PvE Implication:
In PvE, mobs typically have 0 `total_dam_def`. Any `total_dam_add` stacked by the player becomes a pure multiplicative bonus on ALL damage output. For example, 0.5 total_dam_add = 1.5× all damage = 50% more damage across the board.
