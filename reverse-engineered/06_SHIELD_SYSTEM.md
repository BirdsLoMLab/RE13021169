# 06 — Shield System

## Code Location
**Module:** BuffShield.ts
**Lines:** 195146-195250 in `game_script_pretty.js`

---

## Shield Creation (onBegin) — Lines 195180-195213

### Variable Mapping
| Variable | Meaning |
|----------|---------|
| t | Shield owner (unit receiving shield) |
| i | Caster (unit creating the shield) |
| this._calType | Calculation type for shield HP |
| this._hpType | Source flags (Add=1, Sub=2, Attack=4, Target=8) |
| this._attribId | Attribute to use for shield HP calc |
| this._isDec | If 0, apply shieldDecay; if non-zero, skip decay |
| this.skillPar | Skill multiplier for shield HP |
| this._value | Final shield HP amount |

### Raw Code (Annotated)
```javascript
n.onBegin = function() {
    var t = this.owner,    // shield owner
        i = this.runner.cast;  // caster
    var a = 0;

    switch (this._calType) {
        case 0:
            // Use attribute value from target or caster
            a = this._hpType & l.Target
                ? t.data.getAttrib(this._attribId)    // Target's attribute
                : i.data.getAttrib(this._attribId);   // Caster's attribute
            break;
        case 1:
            // ATK - DEF based
            var n = i.data.getAttrib(f.att),
                h = t.data.getAttrib(f.def),
                d = t.data.getAttrib(f.def_coe);
            a = Math.max(r.roundInt(n - h * (1 + d)), 1);
            break;
        case 2:
            // HP difference
            var c = i.data.getAttrib(f.hp);
            a = r.roundInt(c - t.data.currenHp);
            break;
        case 3:
            // Current HP
            a = r.roundInt(t.data.currenHp);
            break;
    }

    // Step 1: Apply skill multiplier
    a = r.roundInt(a * this.skillPar);

    // Step 2: Apply shield HP extra bonus
    a = r.roundInt(a * r.round(1 + t.data.getAttrib(f.shield_hp_extra)));

    // Step 3: Apply shield decay (PvP only, when _isDec == 0)
    0 == this._isDec && (a = r.roundInt(a * t.battleMain.shieldDecay));

    // Store shield value
    this._value = a;

    // Handle associated buffs (from param5)
    // ...

    // Add to unit's total shield HP
    this.owner.data.shieldHp = r.roundInt(this.owner.data.shieldHp + this._value);
}
```

### Shield HP Formula
```
Based on _calType:
  case 0: base = getAttrib(attribId)   [from target or caster]
  case 1: base = max(roundInt(caster_ATK - owner_DEF × (1 + DEF_COE)), 1)
  case 2: base = roundInt(caster_maxHP - owner_currentHP)
  case 3: base = roundInt(owner_currentHP)

shield_hp = roundInt(base × skillPar)
shield_hp = roundInt(shield_hp × round(1 + shield_hp_extra))
if (_isDec == 0):    // standard decay
    shield_hp = roundInt(shield_hp × shieldDecay)
```

In PvP: `shieldDecay = round(shield_correct / 10000) = round(4000/10000) = 0.4`
So shields are **40% of base value** in PvP.

---

## Shield Damage Absorption (onShieldAction) — Lines 195235-195238

```javascript
n.onShieldAction = function(t) {
    if (!this._run) return 0;   // shield not active

    // Absorb: min of shield value and incoming damage
    var i = this._value >= t ? t : this._value;

    // Reduce shield HP
    this.owner.data.shieldHp = r.roundInt(this.owner.data.shieldHp - i);
    this.owner.data.shieldHp = Math.max(0, this.owner.data.shieldHp);

    // Reduce this shield's remaining value
    this._value = r.roundInt(this._value - i);

    // If shield is depleted, stop it
    this._value <= 0 && this.stop();

    return i;  // return amount absorbed
}
```

### Absorption Formula
```
absorbed = min(shield_remaining, incoming_damage)
shield_remaining -= absorbed
if shield_remaining <= 0: shield expires
damage_through = incoming_damage - absorbed
```

---

## Shield Absorption in Damage Pipeline — Lines 449285-449291

```javascript
// In Unit.addDamage, after PvP reduction:
if (w && this.data.shieldHp > 0) {
    for (var X, Z = W, Q = i(w); !(X = Q()).done;) {
        var $ = X.value.onShieldAction(W);
        W = s.roundInt(W - $);         // reduce remaining damage
        if (this.data.shieldHp <= 0) break;  // all shields depleted
    }
    // Log the absorbed amount
    this.battleMain.addLogCount(..., k.Absorb, Z - W, ...);
}
```

### Key Points:
1. **Multiple shields are iterated** — damage passes through each shield sequentially
2. **Damage overflows past shields** — remaining damage after shields are depleted continues to HP
3. **Shield absorption happens AFTER PvP reduction** — the post-PvP damage hits the shield
4. **Block buffs (BLOCK type) are checked AFTER shields** — Lines 449293-449297

---

## Shield Destruction (onDestroy) — Lines 195214-195233

When a shield expires (duration ends or depleted):
1. Any associated buffs are removed
2. Remaining shield value is subtracted from unit's total shieldHp
3. On-destruction buffs can be triggered (from param5[1] config)

---

## Shield Configuration (alloc) — Lines 195239-195241

```javascript
a.alloc = function(t) {
    var i = a._pool.alloc();
    return i.config = t,
           i._hpType = t.param1,      // Source flags (Add/Sub/Attack/Target)
           i._calType = t.param2,     // HP calc type (0=attrib, 1=ATK-DEF, 2=HP diff, 3=current HP)
           i._attribId = t.param3,    // Attribute ID for case 0
           i._isDec = t.param4,       // 0 = apply decay, non-zero = skip decay
           i._buffList = [],
           i._buffs = [],
           i
}
```

---

## PvP Shield/Heal Decay Default Values

From ConfigGlobal (lines 235660-235661):
```
shield_correct = 4000       → shieldDecay = 0.4  (40% of PvE shield)
hp_recovery_correct = 3000  → treatDecay = 0.3   (30% of PvE healing)
```

**Note:** These are GLOBAL defaults. The `shield_correct` and `hp_recovery_correct` values are read from ConfigGlobal (not per-level like pvp_injury_reduce). They're used as `r.shield_correct` where `r` references the global config.

---

## Comparison with Known Documentation

### Key Findings:
1. **Shield decay is level-independent** — uses a global config value (4000 = 40%), not per-level
2. **Heal decay is also level-independent** — global config (3000 = 30%)
3. **Shield HP has a bonus stat** — `shield_hp_extra` (ID 1051) multiplicatively increases shield HP
4. **Some shields skip decay** — `_isDec != 0` bypasses the shieldDecay multiplier
5. **Multiple shields stack additively** — all shield values add to `shieldHp`
6. **Damage fully overflows past shields** — no damage is lost when a shield breaks

---

## Block System (Related)

After shields, Block buffs (BuffGroupType.BLOCK) can also absorb damage:
```javascript
// Lines 449293-449297
if (O && O.length > 0)
    for (var tt, it = i(O); !(tt = it()).done;) {
        var et = tt.value.onShieldAction(W);
        W = s.roundInt(W - et);
        // Log as healthType 'block' (50)
    }
```
Block works identically to shields mechanically but is logged as a different type.
