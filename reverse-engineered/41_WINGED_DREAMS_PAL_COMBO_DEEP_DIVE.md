# 41 — Winged Dreams: Pal Combo Mechanics Deep Dive

> **Verified against game_script.js source code**, not just reverse-engineered docs.
> All byte offsets and code excerpts traced from the minified source.

---

## 1. Skill Overview (from tooltip)

**Winged Dreams** — Event Immortal Active Skill:
1. Deals 5549% DMG
2. Grants all pals +20% Combo Rate
3. Every 1% Combo Rate increases a pal's Combo Multiplier by 0.5%
4. Effect lasts 5 seconds

---

## 2. Verified Source: normalDoubleHurt (Combo Damage Formula)

**Source location:** game_script.js, byte offset ~12445965, module `HurtUtil.ts`

### Raw source (deobfuscated with variable mappings)

```javascript
// t = attacker, a = defender, r = crit_flag (1=normal, 2=crit), e = usePierceResist (default true)
// i = AttribDefine enum, n = FixMath, d = UnitType enum
// l = calArmorAndBlock, p = calSuppressAndInspire, _ = calHurt

function normalDoubleHurt(t, a, r, e) {
    e = e ?? true;

    var ATK           = t.data.getAttrib(i.att);              // 1001
    var DEF           = a.data.getAttrib(i.def);              // 1024
    var DEF_COE       = a.data.getAttrib(i.def_coe);          // 1060
    var CRIT_DAM      = t.data.getAttrib(i.crit_dam);         // 1005
    var CRIT_DEF      = Math.max(0.5, a.data.getAttrib(i.crit_def));  // 1006, floor 0.5
    var DH_DEF_RAW    = a.data.getAttrib(i.double_hit_def);   // 1034
    var DH_DEF        = DH_DEF_RAW;
    if (e) DH_DEF    = calArmorAndBlock(a, t, DH_DEF_RAW, i.double_hit_def);  // pierce/block
    var DH_DAM        = t.data.getAttrib(i.double_hit_dam);   // 1032 — ATTACKER's own

    var dmg = 0;

    if (t.config.type == UnitType.Partner) {
        // ═══════════════════════════════════════════
        // PAL BRANCH
        // ═══════════════════════════════════════════
        ATK = t.parent.data.getAttrib(i.att);                  // parent player's ATK
        var PAL_DAM     = t.data.getAttrib(i.partner_dam);     // 1040, pal's own
        var PAL_EXTRA   = t.parent.data.getAttrib(i.partner_dam_extra);  // 1047, from parent
        PAL_DAM = n.round(PAL_DAM * PAL_EXTRA);

        var PAL_RESIST  = a.data.getAttrib(i.partner_resist);  // 1020, defender's
        var RESIST      = calSuppressAndInspire(a, t.parent, PAL_RESIST, i.partner_resist);

        var x = n.roundInt(Math.max(n.roundInt(ATK - DEF * (1 + DEF_COE)), 1) * PAL_DAM)
                * n.round(1 - RESIST);

        dmg = n.roundInt(n.roundInt(x) * DH_DAM);  // ← double_hit_dam applied
        dmg = n.roundInt(dmg);

        // *** NOTE: DH_DEF (double_hit_def / Combo Resistance) is NEVER applied ***

    } else if (t.config.type == UnitType.Gun) {
        // ═══════════════════════════════════════════
        // GUN BRANCH
        // ═══════════════════════════════════════════
        var GUN_DAM = t.data.getAttrib(i.partner_dam);
        var CANNON_DEF = a.data.getAttrib(i.season_cannon_att_def);
        var y = n.roundInt(Math.max(n.roundInt(ATK - DEF * (1 + DEF_COE)), 1) * GUN_DAM)
                * n.round(1 - CANNON_DEF);

        dmg = n.roundInt(n.roundInt(y) * DH_DAM) * n.round(1 - DH_DEF);  // ← combo resist applied
        dmg = n.roundInt(dmg);

    } else {
        // ═══════════════════════════════════════════
        // PLAYER BRANCH (also Boss, Monster, etc.)
        // ═══════════════════════════════════════════
        dmg = n.roundInt(Math.max(n.roundInt(ATK - DEF * (1 + DEF_COE)), 1) * DH_DAM)
              * n.round(1 - DH_DEF);  // ← combo resist applied
        dmg = n.roundInt(dmg);
    }

    // Common: apply calHurt (DMG RES, PvE bonuses)
    dmg = calHurt(dmg, a, t);

    // Common: apply crit
    if (r != 1) {
        dmg = n.roundInt(dmg * Math.max(1.5, n.round(CRIT_DAM / CRIT_DEF)));
    }

    return Math.max(1, dmg);
}
```

### Key finding: double_hit_def is NOT applied to Pal combos

| Branch | Formula | Combo Resistance? |
|--------|---------|-------------------|
| **Player** | `baseDmg × double_hit_dam × (1 - double_hit_def)` | YES |
| **Gun** | `baseDmg × gun_dam × (1 - cannon_def) × double_hit_dam × (1 - double_hit_def)` | YES |
| **Pal** | `parentATK × pal_mult × (1 - partner_resist) × double_hit_dam` | **NO** |

The variable `DH_DEF` (pierced double_hit_def) is calculated at the top of the function but **never used** in the Partner branch. Only `partner_resist` via suppress/inspire acts as resistance.

### Damage ordering for Pal combo (left to right)

```
1. max(roundInt(parentATK - DEF × (1 + def_coe)), 1)   ← base raw damage
2. × round(partner_dam × partner_dam_extra)              ← pal damage multiplier
3. × round(1 - suppress_inspire(partner_resist))         ← pal resistance (ONLY resistance layer before combo mult)
4. × double_hit_dam                                      ← combo multiplier (UNRESISTED)
5. → calHurt (resist, pve_dam, pve_resist)               ← general DMG RES
6. × crit_multiplier (if crit)                           ← crit
```

---

## 3. Verified Source: checkDoubleAct (Combo Trigger)

**Source location:** game_script.js, byte offset ~12448976, module `HurtUtil.ts`

### Raw source (deobfuscated)

```javascript
function checkDoubleAct(attacker, defender) {
    var comboRate = attacker.data.getAttrib(AttribDefine.double_hit);     // 1016
    var ignoreCombo = 0;
    if (defender) {
        ignoreCombo = defender.data.getAttrib(AttribDefine.ignore_double_hit);  // 1048
    }

    var scaledChance = FixMath.roundInt(10000 * Math.max(FixMath.round(comboRate - ignoreCombo), 0));
    if (scaledChance <= 0) return false;

    var roll = battleMain.random.randomInt(0, 10000);
    // Debug: "连击 rand: {roll} tem: {scaledChance}"
    return roll <= scaledChance;
}
```

### Key findings

- Uses `attacker.data.getAttrib(double_hit)` — the **attacker's own** attribute 1016
- **NO branching on unit type** — same logic for Player, Partner, Gun, Boss, etc.
- For pals, this reads the PAL unit's own `double_hit`, NOT the player's `partner_double_hit` (4005)
- `ignore_double_hit` (1048) is subtracted before the roll
- A combo CANNOT trigger another combo (recursive call uses pass=1, check only fires on pass=-1)

---

## 4. Verified Source: setPlayerPets (Pal Stat Loading)

**Source location:** game_script.js, byte offset ~8298269 (server version)

### Raw source (deobfuscated)

```javascript
function setPlayerPets(playerData, petList, bonusData) {
    if (!petList || petList.length == 0) return;

    var moduleAttrs = configAttribute.getDataByList("module", 1);  // ← ONLY module=1 attributes

    for (var pet of petList) {
        if (pet.pet_id == 0) continue;

        var petConfig = configPet.getDataByKey(pet.pet_id);
        var petLevel  = configPetlevel.getDataByKeys("id", pet.pet_id, "level", pet.pet_lev);
        var unit = new BattleUnit();
        unit.attribs = {};
        unit.config = configUnit.getDataByKey(petConfig.unitId);

        // Load ALL module=1 attributes from ConfigPetlevel
        for (var attr of moduleAttrs) {
            var meta = new MetaAttrib(attr);
            meta.baseValue = getPetFactAttrValue(bonusData, petLevel[attr.key], pet.pet_id, attr.id);
            unit.attribs[attr.id] = meta;
        }

        // INHERIT specific stats from parent player (units[0])
        unit.attribs[hp].baseValue              = playerData.units[0].attribs[hp].baseValue;
        unit.attribs[att].baseValue             = playerData.units[0].attribs[att].baseValue;
        unit.attribs[partner_dam_extra].baseValue = playerData.units[0].attribs[partner_dam_extra].baseValue;
        unit.attribs[skill_dam_extra].baseValue = playerData.units[0].attribs[skill_dam_extra].baseValue;
        unit.attribs[skill_crit_rate].baseValue = playerData.units[0].attribs[skill_crit_rate].baseValue;
        unit.attribs[skill_crit_dam].baseValue  = playerData.units[0].attribs[skill_crit_dam].baseValue;
        unit.attribs[boss_dam].baseValue        = playerData.units[0].attribs[boss_dam].baseValue;

        unit.idleIndex = pet.pet_pos + 1;
        playerData.units.push(unit);
    }
}
```

### Key findings: What pals inherit vs own

| Source | Attributes |
|--------|-----------|
| **From ConfigPetlevel** (pal's own) | All module=1 attrs including: `double_hit` (1016), `double_hit_dam` (1032), `partner_dam` (1040), `crit_rate` (1004), `att_speed` (1003), etc. |
| **Inherited from parent player** | `hp` (1002), `att` (1001), `partner_dam_extra` (1047), `skill_dam_extra` (1045), `skill_crit_rate` (1037), `skill_crit_dam` (1038), `boss_dam` (1046) |
| **NOT loaded (not module=1)** | `partner_double_hit` (4005), `partner_crit_rate` (4001), and all other 4000/2000/3000/5000/10000-range attributes |

**The pal's `double_hit` (1016) and `double_hit_dam` (1032) are loaded from ConfigPetlevel, NOT inherited from the player. The player's `partner_double_hit` (4005) is never transferred to pal units.**

### 4001-4006 are display-only attributes (NOT combat stats)

The 4000-range "partner" attributes are **not in the battle engine's `AttribDefine` enum at all**. The enum jumps from 1082 (`total_dam_def`) to 6001 (`spirit_dam_add`). They are `type=3` derived display attributes used only in the equipment UI:

```javascript
// ConfigGlobal.equip_attr — controls what shows in equipment details
equip_attr: [1002, 1001, 1024, 1003, 1004, 1016, 1017, 1023, 1008, 1012, 1037, 4001, 4005]

// ConfigGlobal.high_attr — controls which stats are highlighted
high_attr: [1004, 1016, 1017, 1023, 1008, 1012, 1037, 4001, 4005]
```

When displayed, they are computed as derived ratios from other attributes via the `group` field:
```javascript
// getAttrValue for type==3 attributes
if (0 == value && 3 == config.type && config.group != null) {
    var a = getRoleAttrById(config.group - 1000);
    var b = getRoleAttrById(config.group);
    value = (a - b) / b * displayScale;  // derived ratio for UI display
}
```

**`partner_double_hit` (4005) is purely an equipment display stat. It cannot be referenced by the battle engine, is never loaded into any battle unit, and has zero effect on combat.**

### Client version differences (byte offset ~8709215)

The client version is similar but only inherits 3 attributes:
```javascript
unit.attribs[hp].baseValue              = playerData.units[0].attribs[hp].baseValue;
unit.attribs[att].baseValue             = playerData.units[0].attribs[att].baseValue;
unit.attribs[partner_dam_extra].baseValue = playerData.units[0].attribs[partner_dam_extra].baseValue;
// Missing: skill_dam_extra, skill_crit_rate, skill_crit_dam, boss_dam
```

This means the client-side damage preview may underestimate pal damage compared to server-side calculation.

---

## 5. Verified Source: BuffAttribConvert (Attribute Conversion)

**Source location:** game_script.js, byte offset ~8517724, module `BuffAttribConvert.ts`

### Raw source (deobfuscated)

```javascript
class BuffAttribConvert extends Buff {
    _calType;       // param1
    _attribId;      // param2 — source attribute ID
    _tagAttribId;   // param3 — target attribute ID
    _limit;         // param5 — optional [min_ratio, max_ratio]
    _lastValue;     // stored for cleanup

    onBegin() {
        var value = this._calValue();
        var targetMeta = this.owner.data.getAttribMeta(this._tagAttribId);
        this._lastValue = value;
        targetMeta.addExtraValue(this._lastValue);   // ← post-multiplicative addition
    }

    _calValue() {
        var owner = this.owner;
        var result = 0;
        var maxHp = owner.data.getAttrib(AttribDefine.hp);
        var currentHp = owner.data.currenHp;

        switch (this._calType) {
            case 0:  // BASE VALUE of source attribute
                result = owner.data.getAttribMeta(this._attribId).baseValue;
                break;
            case 1:  // Current HP (absolute)
                result = owner.data.currenHp;
                break;
            case 2:  // Lost HP (absolute)
                result = FixMath.round(FixMath.roundInt(maxHp - currentHp));
                break;
            case 3:  // Current HP% × 10000
                result = Math.max(FixMath.round(currentHp / maxHp * 10000), 10000);
                break;
            case 4:  // Lost HP% × 10000
                result = FixMath.round((maxHp - currentHp) / maxHp * 10000);
                break;
            case 5:  // Lost HP% via CURRENT_HP buff
                var actualHp = currentHp;
                var hpBuffs = owner.buffCtr.getBuffByType(BuffGroupType.CURRENT_HP);
                if (hpBuffs.length > 0) {
                    actualHp = FixMath.round(hpBuffs[0].getFixHp() * maxHp);
                }
                freeBuffList(hpBuffs);
                result = FixMath.round((maxHp - actualHp) / maxHp * 10000);
                break;
        }

        var targetMeta = owner.data.getAttribMeta(this._tagAttribId);
        result = FixMath.roundInt(result * this.skillPar);  // scale by skill parameter

        // Apply limits as ratio of target attribute's current value
        if (this._limit && this._limit.length == 2) {
            result = Math.min(
                Math.max(result, FixMath.round(this._limit[0] * targetMeta.value)),
                FixMath.round(this._limit[1] * targetMeta.value)
            );
        }
        return result;
    }

    onDestroy() {
        var targetMeta = this.owner.data.getAttribMeta(this._tagAttribId);
        if (this._lastValue) targetMeta.addExtraValue(-this._lastValue);
    }

    static alloc(config) {
        var inst = BuffAttribConvert._pool.alloc();
        inst.config = config;
        inst._calType    = config.param1;   // calculation type
        inst._attribId   = config.param2;   // source attribute
        inst._tagAttribId = config.param3;  // target attribute
        inst._limit      = config.param5;   // limits
        return inst;
    }
}
```

### Critical detail: calType 0 reads baseValue ONLY

When calType is 0, it reads `getAttribMeta(sourceAttr).baseValue` — the **raw base value** before any `addValue`, `addMultiples`, or `addExtraValue` modifications. This means if Winged Dreams uses BuffAttribConvert calType 0 for the conversion:

- The +20% combo rate buff (likely a separate BuffAttrib adding to `double_hit`) would **NOT** be included in the conversion
- Only the pal's base `double_hit` from ConfigPetlevel (plus proficiency/talent bonuses) would be read

### addExtraValue is post-multiplicative

From MetaAttrib._calculateValue:
```javascript
finalValue = roundInt(roundInt(baseValue + _addValue) * _time + _addExtraValue)
```

`addExtraValue` bypasses the multiplicative layer (`_time`), making it a flat addition after all percentage scaling.

---

## 6. Verified Source: BuffAttribCondition (NOT attribute-to-attribute conversion)

**Source location:** game_script.js, byte offset ~8513000, module `BuffAttribCondition.ts`

### CORRECTION from earlier conversation

BuffAttribCondition does **NOT** convert one attribute to another based on reading a source attribute's value. Its calTypes are:

| calType | What it reads | Description |
|---------|---------------|-------------|
| 0 | HP lost ratio (with CURRENT_HP override) | `(maxHp - currentHp) / maxHp` |
| 1 | Speed LOST ratio | `max(0, baseSpeed - currentSpeed) / baseSpeed` |
| 2 | HP lost ratio (simple) | `(maxHp - currentHp) / maxHp` |
| 3 | Speed GAINED ratio | `max(0, currentSpeed - baseSpeed) / baseSpeed` |

It can only scale attributes based on **HP loss percentage** or **speed change percentage**. It **cannot** read combo rate and convert it to combo multiplier.

**Therefore, the "every 1% combo rate → 0.5% combo multiplier" mechanic MUST use BuffAttribConvert (calType 0), not BuffAttribCondition.**

---

## 7. Verified Source: MetaAttrib (Attribute Calculation)

**Source location:** game_script.js, byte offset ~13549769

### Complete formula

```javascript
class MetaAttrib {
    _baseValue = 0;       // set from config or inheritance
    _addValue = 0;        // from addValue() — BuffAttrib, BuffAttribCondition
    _addExtraValue = 0;   // from addExtraValue() — BuffAttribConvert ONLY
    _time = 1;            // from addMultiples() — multiplicative layer

    _calculateValue(baseValue) {
        var result = roundInt(roundInt(baseValue + this._addValue) * this._time + this._addExtraValue);

        if (this.config.up_limit != 0) {
            result = Math.min(result, this.config.up_limit);
        }
        if (this.config.num_type == 2) {
            result = round(result / 10000);  // convert from basis points to decimal
        }
        return result ?? 0;
    }

    get value() {
        if (this._change) {
            this._value = this._calculateValue(this._baseValue);
            this._change = false;
        }
        return this._value;
    }

    get baseValue() { return this._baseValue; }
    set baseValue(v) {
        this._baseValue = roundInt(Number(v) || (num_type == 2 ? 10000 : 0));
        this._checkValue = 32 ^ this._baseValue;  // XOR for cheat detection
        this._change = true;
    }
}
```

### Three modification layers

| Method | Layer | Used by | Position in formula |
|--------|-------|---------|---------------------|
| `addValue(v)` | `_addValue` | BuffAttrib, BuffAttribCondition | Added to base BEFORE multiplication |
| `addMultiples(v)` | `_time` | BuffAttrib (param2=2), BuffAttribCondition (param3=2) | Multiplicative layer |
| `addExtraValue(v)` | `_addExtraValue` | **BuffAttribConvert only** | Added AFTER multiplication |

Formula: `final = roundInt(roundInt(base + addValue) × time + addExtraValue)`

---

## 8. Corrections to Earlier Conversation Claims

### CONFIRMED correct:
- Pal combo damage does NOT apply `double_hit_def` (Combo Resistance)
- `checkDoubleAct` uses the pal's own `double_hit` (1016), not the player's `partner_double_hit` (4005)
- `partner_double_hit` (4005) is NOT inherited to pal units during battle loading
- Pals have their own `double_hit` and `double_hit_dam` from ConfigPetlevel
- `double_hit_dam` (1032) is read from the pal's own attributes in normalDoubleHurt
- `partner_resist` is applied BEFORE `double_hit_dam` in the pal combo formula
- `ignore_double_hit` reduces proc chance but doesn't affect combo damage
- The combo trigger function is identical for all unit types

### CORRECTED:
- **BuffAttribCondition cannot do attribute-to-attribute conversion.** I incorrectly described it as a possible mechanism for "combo rate → combo multiplier." Its calTypes only check HP loss and speed change ratios. The conversion must use **BuffAttribConvert** instead.
- **BuffAttribConvert calType 0 reads `baseValue`, not the final value.** If the conversion uses this mechanism, it only reads the pal's raw base combo rate from config — NOT including any buffs (like the +20% combo rate from Winged Dreams itself). This is a significant difference from what I initially claimed about "total combo rate."
- **The ordering of `partner_resist` vs `double_hit_dam` doesn't change the percentage reduction** — multiplication is commutative. The real defensive gap is the complete absence of any `double_hit_def` equivalent for pal combos, not the ordering.

### UNCERTAIN (cannot verify without buff config data):
- The exact buff IDs and implementation of Winged Dreams' effects
- Whether the combo rate → combo multiplier conversion uses BuffAttribConvert calType 0 (baseValue only) or some other mechanism (e.g., skill_effect with custom code)
- If using calType 0, whether the +20% combo rate from the skill contributes to the conversion (it would NOT, since addValue doesn't affect baseValue)

---

## 9. Defensive Analysis (verified from formulas)

### Defensive layers against Pal combo damage

| Layer | Attribute | Where in formula | Cap |
|-------|-----------|------------------|-----|
| DEF + def_coe | 1024, 1060 | `max(ATK - DEF×(1+def_coe), 1)` | None |
| Partner Resist | 1020 | `× (1 - suppress_inspire(partner_resist))` | 80% (8000) |
| **[MISSING]** | ~~double_hit_def~~ | ~~not applied~~ | ~~80%~~ |
| DMG Resistance | 1021 | via calHurt | 80% (8000) |
| PvE Resist | 1058 | via calHurt | None |
| Total DMG DEF | 1082 | via calHurt | None |

### Comparison: Player combo vs Pal combo resistance

**Player combo** has TWO dedicated resistance checks:
1. `att_resist` (1018) on the normal attack base damage
2. `double_hit_def` (1034) on the combo multiplied result

**Pal combo** has ONE resistance check:
1. `partner_resist` (1020) on the pal base damage — combo multiplier applied AFTER, with no resistance

There is no attribute in the game that specifically resists the `double_hit_dam` multiplier on pal combo attacks.
