# 45 — Pal Damage, Pal Crit DMG, and Pal Combo Multiplier — Deep Dive

> **Status:** Verified directly against `game_script.js` (minified, the only build we have locally). Every formula below was extracted from the live JS, not from the V1 simulator. The simulator is **not** a source of truth.

> **Scope:** Everything a player needs to predict the displayed pal panel numbers, the actual damage dealt, and how each `+X% Pal CritDMG` / `+X% Pal Combo Mult` / `+X% Pal DMG` source compounds. Covers normal attack, combo, counter, HP-based, pal active skills, and the Cannon/Gun branch.

---

## 0. The Three Layers (read this first)

Every "Pal X" number in the game lives in one of three layers. Confusing them is the source of every "where does this multiplier come from" question.

| Layer | Where it lives | Who reads it |
|-------|----------------|--------------|
| **A. Pet config tables** | `ConfigPet`, `ConfigPetlevel`, `ConfigPet_talent`, `ConfigPet_proficiency` | Loaded once at battle start by `setPlayerPets` |
| **B. MetaAttrib (per-attribute object)** | `_baseValue`, `_addValue`, `_addExtraValue`, `_time` on the pal unit | Read every frame the attribute is queried; mutated by buffs |
| **C. Damage formula (per-hit)** | `normalHurt`, `normalDoubleHurt`, `normalCounterHurt`, `BuffSkillValue._calHurt`, `_calHpHurt` | Called per damage event |

A flows into B's `_baseValue` (via `getPetFactAttrValue`). B's `.value` getter is what every formula in C calls via `getAttrib(...)`. The pal panel reads the same `.value` getter.

Most pal mechanic surprises (including the "2.7x mystery") come from layer B's formula:

```
displayed = roundInt(roundInt(baseValue + addValue) * _time + addExtraValue)
```

A bonus like "+285% Pal CritDMG" that goes through `addMultiples(2.85)` adds `2.85` to `_time`, not `285` to the displayed number. The displayed delta is therefore `(baseValue + addValue) × 2.85`, not `+285`.

---

## 1. Attribute IDs Used by Pal Damage

| Attribute | ID | Owner | Notes |
|-----------|----|-------|-------|
| `att` | 1001 | **Parent** (read live) | Pal basic/combo damage uses the parent player's *current* ATK, not the pal's. |
| `att_speed` | 1003 | Pal | Affects pal attack cadence, displayed on pal panel. |
| `crit_rate` | 1004 | Pal | Pal's own, used for normal-crit check. |
| `crit_dam` | 1005 | Pal | Pal's own, used for crit multiplier. **NOT inherited from parent at load time.** |
| `crit_def` | 1006 | Target | Floor of 0.5. |
| `hit` | 1007 | Pal | Used in `checkHit`; displayed as "Ignore Evasion". |
| `miss` | 1008 | Target | Capped at 0.80 in PvP via `battle_up_limit`. |
| `double_hit` | 1016 | Pal | Combo proc rate. |
| `double_hit_dam` | 1032 | Pal | Combo damage multiplier. |
| `double_hit_def` | 1034 | Target | Combo resistance (≤80% cap). |
| `att_resist` | 1018 | Target | Basic ATK resistance (only used for non-pal/non-Gun branch). |
| `partner_resist` | 1020 | Target | Pal's analog of `att_resist`. Cap 80%. |
| `partner_dam` | 1040 | Pal | Pal's base damage multiplier (from `ConfigPetlevel`). |
| `partner_dam_extra` | 1047 | **Parent** (copied at load) | Parent's pal-damage scalar; inherited to the pal at battle start. |
| `partner_inspire` | 1074 | Attacker | Reduces `partner_resist` if the inspire roll wins. |
| `partner_inspire_rate` | 1073 | Target *(yes, target — see § 6)* | Probability gate for inspire. |
| `partner_suppress` | 1077 | Target | Increases `partner_resist` if the suppress roll wins. |
| `partner_suppress_rate` | 1076 | Attacker | Probability gate for suppress. |
| `ignore_partner_inspire` | 1075 | Target | Reduces inspire effect. |
| `ignore_partner_suppress` | 1078 | Attacker | Reduces suppress effect. |
| `def` | 1024 | Target | Defense. |
| `def_coe` | 1060 | Target | Defense coefficient (multiplies DEF). |
| `att_dam` | 1039 | Pal | Used **only** for HP-clamp on pal HP-based skills and `BuffSkillValue` case 10. |
| `counter_dam` | 1033 | Pal (if it ever counters) | No Partner branch in `normalCounterHurt` — pal uses its own ATK. |
| `skill_dam_extra` | 1045 | Parent → pal (inherited) | Applied to pal active-skill damage. |
| `skill_crit_rate` | 1037 | Parent → pal (inherited) | Skill crit on pal skills. |
| `skill_crit_dam` | 1038 | Parent → pal (inherited) | Skill crit damage on pal skills. |
| `active_skilldamage_par` | 1043 | Caster (skill-specific param) | Pal active skill multiplier. |
| `boss_dam` | 1046 | Parent → pal (inherited) | Boss-target bonus. |
| `resist` (DMG RES) | 1021 | Target | Final DMG RES, applied by `calHurt`. |
| `pve_dam` | 1057 | Attacker | PvE damage bonus, applied in `calHurt`. |
| `pve_resist` | 1058 | Target | PvE damage resist, applied in `calHurt`. |
| `total_dam_add` | 1081 | Various | Total DMG bonus aggregate. |
| `total_dam_def` | 1082 | Various | Total DMG resistance aggregate. |
| `season_cannon_att_def` | 1059 | Target | Cannon (Gun) ATK resistance. |

Pal-display panel reads exactly **`[1040, 1003, 1004, 1005, 1016, 1032, 1007]`** (see `BattleSubPetPanelView` at script offset ~15573339 and the duplicate offset ~15779692).

---

## 2. Pal Unit Loading — `setPlayerPets` (script offset ~8293223)

```js
setPlayerPets = function(t, i, a) {
  if (!i || !i.length) return;
  for (var r of i) {
    var f = r.value;
    if (f.pet_id == 0) continue;
    var c = configPet.getDataByKey(f.pet_id);
    var v = configPetlevel.getDataByKeys("id", f.pet_id, "level", f.pet_lev);
    var d = new Unit();
    d.attribs = {};
    d.roleId = t.id;
    d.config = configUnit.getDataByKey(c.unitId);
    d.skillList = [];
    for (var _ of configAttribute.getDataByList("module", 1)) {
      var p = new MetaAttrib(_);
      p.baseValue = this.getPetFactAttrValue(a, v[_.key], f.pet_id, _.id);
      d.attribs[_.id] = p;
    }
    // INHERIT seven attributes from parent player[0]:
    d.attribs[hp].baseValue                 = t.units[0].attribs[hp].baseValue;
    d.attribs[att].baseValue                = t.units[0].attribs[att].baseValue;
    d.attribs[partner_dam_extra].baseValue  = t.units[0].attribs[partner_dam_extra].baseValue;
    d.attribs[skill_dam_extra].baseValue    = t.units[0].attribs[skill_dam_extra].baseValue;
    d.attribs[skill_crit_rate].baseValue    = t.units[0].attribs[skill_crit_rate].baseValue;
    d.attribs[skill_crit_dam].baseValue     = t.units[0].attribs[skill_crit_dam].baseValue;
    d.attribs[boss_dam].baseValue           = t.units[0].attribs[boss_dam].baseValue;
    d.idleIndex = f.pet_pos + 1;
    t.units.push(d);
  }
};
```

### Inherited at load only (server build)

`hp · att · partner_dam_extra · skill_dam_extra · skill_crit_rate · skill_crit_dam · boss_dam`

These are **copied as baseValues at battle start**. Subsequent in-battle changes to the parent's `_addValue` / `_time` on these attributes do **not** propagate to the pal — but the pal's normalHurt/normalDoubleHurt branches read `t.parent.data.getAttrib(att)` live, so ATK changes on the parent **do** flow through *that path*.

> ⚠️ `crit_dam`, `crit_rate`, `crit_def`, `partner_dam`, `partner_resist`, `att_dam`, `double_hit`, `double_hit_dam` are **not inherited**. They come from `ConfigPetlevel` + talents + proficiency, then are buffed in-place per pal.

### `getPetFactAttrValue` (script offset ~8295775)

```js
getPetFactAttrValue = function(t, e, i, a) {
  // t: per-pet bonus dictionary (proficiency + talent)
  // e: base value from ConfigPetlevel
  // i: pet ID
  // a: attribute ID
  if (t == null) return e;
  var l = roundInt(e + getPetAttrByAttrId(t, i, a)        // pet-specific bonus
                    + getPetAttrByAttrId(t, 0, a));       // global pet bonus (key 0)
  var s = configAttribute.getDataByList("group", a);
  if (!s || s.length <= 0) return l;
  for (var grp of s) {
    var u = roundInt(getPetAttrByAttrId(t, i, grp.id)
                   + getPetAttrByAttrId(t, 0, grp.id));
    var o = round(round(u / 1e4) + 1);   // = 1 + group_bonus%
    l = roundInt(l * o);
  }
  return l;
};
```

### Formula

```
baseValue = ConfigPetlevel.<attr>
          + petTalentBonus(petId, attr)
          + petGlobalBonus(0, attr)

For each group_attr in ConfigAttribute.group[attr]:
    group_bonus = petTalentBonus(petId, group_attr) + petGlobalBonus(0, group_attr)
    baseValue   = roundInt(baseValue × (1 + group_bonus/1e4))
```

That final `baseValue` is what gets stuffed into the MetaAttrib's `_baseValue`. The MetaAttrib formula in § 3 then runs on top of it.

---

## 3. MetaAttrib — The Universal Stat Formula (script offset ~13546840)

Every combat stat on every unit (player and pal) is a `MetaAttrib` instance.

```js
function MetaAttrib(config) {
  this._baseValue     = 0;
  this._addValue      = 0;   // flat add (pre-multiplier)
  this._addExtraValue = 0;   // flat add (post-multiplier)
  this._time          = 1;   // multiplicative modifier (starts at 1.0)
  this._value         = 0;
  this._change        = false;
  this.config         = config;
}

MetaAttrib.prototype._calculateValue = function(e) {
  var _ = roundInt(roundInt(e + this._addValue) * this._time + this._addExtraValue);
  if (this.config.up_limit != 0) _ = Math.min(_, this.config.up_limit);
  if (this.config.num_type == 2) _ = round(_ / 1e4);   // percentage scaling
  return _ ?? 0;
};

MetaAttrib.prototype.addValue       = function(e) { this._addValue      = round(this._addValue + e);      this._change = true; };
MetaAttrib.prototype.addExtraValue  = function(e) { this._addExtraValue = round(this._addExtraValue + e); this._change = true; };
MetaAttrib.prototype.addMultiples   = function(e) { this._time          = round(this._time + e);          this._change = true; };
MetaAttrib.prototype.multiple       = function(e) { this._time          = this._time * e;                 this._change = true; };

// .value getter recomputes on demand
get value() {
  if (this._change) { this._change = false; this._value = this._calculateValue(this._baseValue); }
  return this._value;
}
```

### The formula in one line

```
displayed = clamp(roundInt(roundInt(baseValue + _addValue) * _time + _addExtraValue),
                  config.up_limit)
          / (1e4 if num_type==2 else 1)
```

### Which buffs use which modifier?

Every buff/effect in `BuffSkillModify` and related buff handlers chooses between `addValue` and `addMultiples` via an `_isMultiples` flag on the config:

```js
this._isMultiples ? t.addMultiples(this._lastValue) : t.addValue(this._lastValue);
```

- `_isMultiples = false` → effect adds to `_addValue`. A "+285%" bonus would add `28500` (or `2.85`, depending on storage) to a flat-only term. This produces a **flat** increase on the display.
- `_isMultiples = true`  → effect adds to `_time`. A "+285%" bonus adds `2.85` to `_time`, scaling the entire `(base+addValue)` chunk. This produces a **multiplicative** increase on the display.

**Avian affixes use `_isMultiples = true`.** That's the whole reason avian Pal CritDMG bonuses don't show up as `+X%` on the panel additively.

### Why a single "+285%" can yield "+2308.5%" on the panel

```
displayed_before = round((base + addValue) × _time_before + extra)
displayed_after  = round((base + addValue) × (_time_before + 2.85) + extra)
delta           ≈ (base + addValue) × 2.85
```

If `(base + addValue)` for `crit_dam` is e.g. **270%** (15000 default base + ~120% in flat-add buffs/equipment/talents), then a +285% multiplicative bonus increases the display by `270% × 2.85 ≈ 770%` *per affix* — and three affixes give `~2310%`. That is the exact 2308.5% Fara observed.

```
3 affixes × 285% = +8.55 to _time
display delta    = (base + addValue) × 8.55
                 = 270%             × 8.55
                 = 2308.5%      ✓
```

### `baseValue` setter quirks

```js
set baseValue(v) {
  this._baseValue = v ?? 0;
  this._baseValue = Number(v);
  if (NaN) this._baseValue = (num_type == 2 ? 1e4 : 0);   // default 100% for pct attrs
  this._baseValue = roundInt(this._baseValue);
  this._checkValue = 32 ^ this._baseValue;   // anti-cheat XOR
  this._change = true;
}
```

`num_type == 2` attributes (most percentage stats, including `crit_dam`, `partner_dam`, `double_hit_dam`, `crit_rate`, `miss`, `att_dam`, etc.) default to **10000 = 100%** when uninitialized. Their displayed value is the stored value divided by 10000.

---

## 4. Pal Basic Attack — `normalHurt` (script offset ~12441031)

```js
normalHurt = function(t, a, r, e) {
  if (e === undefined) e = true;
  var o = t.data.getAttrib(att);
  var u = a.data.getAttrib(def);
  var g = a.data.getAttrib(def_coe);
  var b = t.data.getAttrib(crit_dam);
  var s = Math.max(0.5, a.data.getAttrib(crit_def));
  var m = a.data.getAttrib(att_resist);
  var A = t.data.getAttrib(att_dam);

  if (t.config.type == d.Partner) {                       // <<< pal branch
    o = t.parent.data.getAttrib(att);                     // parent's live ATK
    m = a.data.getAttrib(partner_resist);
    m = calSuppressAndInspire(a, t.parent, m, partner_resist_id);
    A = t.data.getAttrib(partner_dam);
    var c = t.parent.data.getAttrib(partner_dam_extra);
    A = round(A * c);                                     // combined pal mult
  } else if (t.config.type == d.Gun) {                    // cannon branch (§ 9)
    A = t.data.getAttrib(partner_dam);
    m = a.data.getAttrib(season_cannon_att_def);
    m = calSuppressAndInspire(a, t, m, season_cannon_att_def_id);
  } else if (e) {
    m = calArmorAndBlock(a, t, m, att_resist_id);         // pierce/block (non-pal)
  }

  var f = roundInt(Math.max(roundInt(o - u*(1+g)), 1) * round(A * round(1 - m)));
  f = calHurt(f, a, t);                                   // DMG RES + PvE
  if (r != 1) f = roundInt(f * Math.max(1.5, round(b/s)));// crit (r == ignoreCrit)
  return Math.max(1, f);
};
```

### Verified pal-basic formula

```
ATK         = parent.att                                      (live, not the copied baseValue)
DEF         = target.def
DEF_COE     = target.def_coe
base_raw    = max(roundInt(ATK − DEF × (1 + DEF_COE)), 1)

pal_mult    = round(pal.partner_dam × parent.partner_dam_extra)
PR          = target.partner_resist
PR_eff      = calSuppressAndInspire(target, parent, PR, partner_resist_id)
                                                              # may shift PR by ±min(0.5, inspire/suppress)
                                                              # capped at partner_resist.up_limit = 0.80

raw_dmg     = roundInt(base_raw × round(pal_mult × round(1 − PR_eff)))
raw_dmg     = calHurt(raw_dmg, target, pal)                   # × (1+pve_dam), × (1−resist), × (1−pve_resist)
if CRIT (from checkHit):
    raw_dmg = roundInt(raw_dmg × max(1.5, round(pal.crit_dam / max(0.5, target.crit_def))))

final       = max(1, raw_dmg)
```

### Pitfalls

- **Pierce/Block does not apply to pal damage.** Pals go through `calSuppressAndInspire`, not `calArmorAndBlock`. Pierce/armor_penetration is for basic ATK only.
- **DEF_COE applies to pals.** Community formulas that use `(ATK − DEF)` are wrong; it's `(ATK − DEF × (1+DEF_COE))`.
- **`partner_dam_extra` is read from `parent.data` live**, even though it was copied to the pal at load time. The copied pal-side baseValue is essentially ignored by the basic/combo paths — they always go back to the parent.
- **Rounding is aggressive:** every intermediate is `round()` (Banker's-style FixMath) or `roundInt`. Small bonuses can vanish.
- **The `e` flag** in `normalHurt(t, a, r, e)` is the "apply armor/block" flag — only matters for the non-pal branch.

---

## 5. Pal Combo Attack — `normalDoubleHurt` (script offset ~12443967)

```js
normalDoubleHurt = function(t, a, r, e) {
  if (e === undefined) e = true;
  var o = t.data.getAttrib(att);
  var u = a.data.getAttrib(def);
  var g = a.data.getAttrib(def_coe);
  var b = t.data.getAttrib(crit_dam);
  var s = Math.max(0.5, a.data.getAttrib(crit_def));
  var m = a.data.getAttrib(double_hit_def);
  var A = m;
  if (e) A = calArmorAndBlock(a, t, m, double_hit_def_id);   // pierce/block applies
  var c = t.data.getAttrib(double_hit_dam);
  var f = 0;

  if (t.config.type == d.Partner) {
    o = t.parent.data.getAttrib(att);
    var v = t.data.getAttrib(partner_dam);
    var h = t.parent.data.getAttrib(partner_dam_extra);
    v = round(v * h);
    var M = a.data.getAttrib(partner_resist);
    var I = calSuppressAndInspire(a, t.parent, M, partner_resist_id);
    var x = roundInt(Math.max(roundInt(o - u*(1+g)), 1) * v) * round(1 - I);
    f = roundInt(roundInt(x) * c);                            // <-- combo mult applied LAST
    f = roundInt(f);
  } else if (t.config.type == d.Gun) {
    var k = t.data.getAttrib(partner_dam);
    var L = a.data.getAttrib(season_cannon_att_def);
    var y = roundInt(Math.max(roundInt(o - u*(1+g)), 1) * k) * round(1 - L);
    f = roundInt(roundInt(y) * c) * round(1 - A);             // <-- A here is the pierced double_hit_def!
    f = roundInt(f);
  } else {
    f = roundInt(Math.max(roundInt(o - u*(1+g)), 1) * c) * round(1 - A);
    f = roundInt(f);
  }

  f = calHurt(f, a, t);
  if (r != 1) f = roundInt(f * Math.max(1.5, round(b/s)));
  return Math.max(1, f);
};
```

### Verified pal-combo formula

```
ATK       = parent.att
base_raw  = max(roundInt(ATK − DEF×(1+DEF_COE)), 1)
pal_mult  = round(pal.partner_dam × parent.partner_dam_extra)
PR_eff    = calSuppressAndInspire(target, parent, target.partner_resist, partner_resist_id)

pal_base  = roundInt(base_raw × pal_mult) × round(1 − PR_eff)
pal_combo = roundInt(roundInt(pal_base) × pal.double_hit_dam)
pal_combo = calHurt(pal_combo, target, pal)
if CRIT:
    pal_combo = roundInt(pal_combo × max(1.5, round(pal.crit_dam / max(0.5, target.crit_def))))
return max(1, pal_combo)
```

### Key facts about pal combos

| Question | Answer |
|----------|--------|
| Does `double_hit_def` (combo RES) reduce pal combo? | **No.** The pal branch never multiplies by `(1 − double_hit_def)`. Only the non-pal and Gun branches do. Pals are gated by `partner_resist`, not `double_hit_def`. |
| Does pierce/block (armor/block) apply to pal combos? | **No.** Same reason. The `calArmorAndBlock(a, t, m, double_hit_def_id)` call only updates the `A` variable, which is only used in the player and Gun branches. |
| Does Inspire/Suppress apply to pal combos? | **Yes.** Same `calSuppressAndInspire` call as basic attack, modifying `partner_resist`. |
| Is `double_hit_dam` multiplied with `partner_dam`? | **No.** It is applied *after* the pal's pre-resistance damage as a separate `roundInt(x × double_hit_dam)`. This is the structural difference from Yuko's "Pal Basic × Combo Mult" formulation. |
| What checks the combo proc? | `checkDoubleAct(attacker, target)` → effective rate = `max(double_hit − ignore_double_hit, 0)`. Strict-less-equal sample. |
| Does combo use the same crit roll as basic? | **No.** Combo's crit comes from the same `checkHit` family — the pal panel `Crit` displayed (1004) and Crit DMG (1005) apply to both basic and combo. There's no separate "combo crit rate". |
| Where does `1 + total_dam_add` enter? | `total_dam_add` (1081) and `total_dam_def` (1082) feed `calHurt` aggregates. They are *not* in the pal-specific path explicitly — they flow through `resist` and `pve_resist` totals or via separate skill effect buffs. See § 10. |

---

## 6. `calSuppressAndInspire` — Pal Resist Modifier (script offset in `HurtUtil`, ~12442800)

```js
calSuppressAndInspire = function(t, a, r, e) {
  // t = target (pal damage *receiver*)
  // a = attacker's parent (the player who owns the pal)
  // r = raw partner_resist value
  // e = attribute id (used for up_limit lookup)
  var d = [0, 0, 0];
  var g = a.data.getAttrib(partner_inspire);
  var b = t.data.getAttrib(ignore_partner_inspire);
  var l = a.data.getAttrib(ignore_partner_suppress);
  var p = t.data.getAttrib(partner_suppress);

  if (g > b) {
    var rate = a.data.getAttrib(partner_suppress_rate);   // ← yes, suppress_rate (swapped name, see CLAUDE.md)
    d[0] = roundInt(1e4 * rate);
  }
  if (p > l) {
    var rate2 = t.data.getAttrib(partner_inspire_rate);   // ← yes, inspire_rate (swapped name)
    d[1] = d[0] + roundInt(1e4 * rate2);
  }
  d[2] = 1e4;

  var m = -1;
  var roll = battleMain.random.randomInt(0, 1e4);
  for (var c = 0; c < 2; c++)
    if (d[c] > 0 && roll <= d[c]) { m = c; break; }
  if (m == -1) m = 2;

  var f = r;
  if (m == 0)      f = round(r − Math.min(0.5, (g − b) / 1e4));   // Inspire: resist ↓
  else if (m == 1) f = round(r + Math.min(0.5, (p − l) / 1e4));   // Suppress: resist ↑

  // Clamp to attribute up_limit
  var v = t.data.getAttribMeta(e).config;
  if (v.up_limit != 0) {
    var h = v.up_limit;
    if (v.num_type == 2) h = round(h / 1e4);
    f = Math.min(f, h);
  }
  return f;
};
```

### Mechanics

| Outcome | Probability | Effect on `partner_resist` |
|---------|-------------|----------------------------|
| **Inspire wins** (m=0) | `d[0]/10000` (gated by attacker's `partner_inspire > target's ignore_partner_inspire`) | `resist = r − min(0.5, (inspire − ignore_inspire)/10000)` — **lowers** target resistance |
| **Suppress wins** (m=1) | `(d[1]−d[0])/10000` (gated by target's `partner_suppress > attacker's ignore_partner_suppress`) | `resist = r + min(0.5, (suppress − ignore_suppress)/10000)` — **raises** target resistance |
| Neither | `(10000 − d[1])/10000` | unchanged |

- The ± shift is **capped at 0.5 (50% points)** by the inner `Math.min(0.5, ...)`.
- After the shift, `partner_resist` is clamped to the attribute's `up_limit` (0.80 / 80%).
- The role of inspire/suppress rate names is swapped in the code — preserve the swap when reading. (Documented in `CLAUDE.md`.)

### Theoretical edge cases

| Q | A |
|---|---|
| Can resistance go negative? | The `round()` doesn't floor at 0. So **yes**: a strong inspire can push effective resistance below 0, which would **increase** pal damage. The damage formula uses `round(1 − resistance)`, which yields > 1 when resistance < 0. |
| Both Inspire and Suppress procs in one event? | Only one of m=0/1 can win (first-hit array scan). They never both apply on the same hit. |
| Does the suppress/inspire roll RNG share with anything else? | No — `battleMain.random.randomInt(0, 1e4)` is its own independent draw per hit. |

---

## 7. Pal Crit Hit & Pal Crit DMG

### 7.1 Crit roll — `checkHit` (script offset ~12446142)

```js
checkHit = function(t, a, r) {
  if (r === undefined) r = false;
  var d = t.data.getAttrib(hit);
  var o = r ? 0 : a.data.getAttrib(miss);
  var u = round(battle_up_limit[0][1] / 1e4);              // 0.80 in PvP
  var b = t.data.getAttrib(crit_rate);
  var l = a.data.getAttrib(ignore_crit_rate);
  var p = Math.max(b - l, 0);                              // effective crit rate (subtractive)
  var _ = Math.max(round(o - d), 0);
  var s = round(Math.pow(round(100 * _), round(miss_correct / 1e4)) / 100);
  var m = s;
  if (chapterType.pve != 1) m = Math.min(s, u);            // 80% miss cap in PvP only
  var f = roundInt(1e4 * m);
  A[Miss]   = f;
  A[Normal] = roundInt(f + round(1 - m) * round(1 - p) * 1e4);
  A[Cirt]   = roundInt(A[Normal] + round(1 - m) * p * 1e4);
  var roll = battleMain.random.randomInt(0, 1e4);
  for (var h = 0; h < 2; h++) if (A[h] > 0 && roll <= A[h]) return h;
  return Cirt;   // defaults to Crit if no match (rounding edge)
};
```

### 7.2 Crit damage multiplier (used by normalHurt/normalDoubleHurt/normalCounterHurt/SkillHurt)

```
crit_mult = max(1.5, round(attacker.crit_dam / max(0.5, target.crit_def)))
damage    = roundInt(damage × crit_mult)
```

**Implications:**

| Question | Answer |
|---|---|
| Is the minimum crit multiplier 150%? | **Yes.** The `Math.max(1.5, ...)` floor is in the source. |
| Can the target reduce crit damage to below 0.5x via `crit_def`? | **No.** `max(0.5, crit_def)` floor — a target with 0 crit_def is treated as 50%. |
| Is the ratio multiplicative on `crit_dam` (the displayed value)? | Yes — it's a raw ratio of the two stat values. Note: both stats are stored as percentages divided by 10000 (e.g., crit_dam = 7.90479 internally means 7904.79% on the panel). |
| Does pal use its **own** crit_dam or the parent's? | **Own.** Pals never inherit `crit_dam` from the parent; they read `pal.data.getAttrib(crit_dam)` directly in normalHurt/normalDoubleHurt. |
| Does pal use its **own** crit_rate? | Yes (1004 attribute on the pal). |
| What about `skill_crit_rate` / `skill_crit_dam`? | **Inherited** from the parent at load time (§ 2). Used only by the pal active-skill path (§ 8.2). |

### 7.3 Why the panel "Crit DMG" is so much bigger than 150%

`crit_dam` is a `num_type == 2` attribute with default baseValue `10000` (100% = 1.0x). After:
- `ConfigPetlevel.crit_dam` adds intrinsic value
- Talents/proficiency add via `getPetFactAttrValue`
- Buffs apply via `addValue` (flat) or `addMultiples` (multiplicative on `_time`)

…the final displayed `crit_dam` can be in the thousands of percent. **Note this is the displayed crit_dam, not the crit multiplier.** The actual multiplier applied to damage is `crit_dam / crit_def` (still floored at 1.5x). So with `crit_dam = 100x` and `crit_def = 0.5x`, the crit multiplier is `200x`.

### 7.4 The "where does the 2.7x come from" answer in one paragraph

The Avian Active Skill "Lunar Keep" + Altruism + Same Boat + Self Sacrifice each grant `+285%` to pal `crit_dam` via `addMultiples(2.85)`. Three affixes contribute `+8.55` to `_time`. The pal's pre-multiplier `crit_dam` chunk (`baseValue + _addValue`) for that pal/build was `~270%`, so removing them dropped the display by `270% × 8.55 = 2308.5%`. The "2.7x" Fara observed is simply `(base + addValue) / 100` for that specific build — the pal's effective "flat" crit_dam pool sitting beneath the multiplicative bonuses.

### 7.5 Numeric example — the formula at every step

Build state for Fara's Tipsy Snail (Lv 134, Legendary), with the avian:

```
Stored (10000 = 100%):
  _baseValue (pal's intrinsic crit_dam at lv 134)        ≈ 15000          (150%, default)
  _addValue   (flat-add buffs/equipment)                  ≈ 12000          (+120% flat)
  _time       (all multiplicative crit_dam %)             ≈ 37.827          (3782.7%)
  _addExtraValue                                          = 0

calculation:
  withAdd = round(15000 + 12000)                          = 27000
  raw     = round(27000 × 37.827 + 0)                     = 1,021,329
  / 1e4   (num_type 2)                                    = 102.1329       (10,213.29%)

display = 10,213.29%  ✓
```

Remove the three affixes (`_time` ↓ by 8.55):

```
  _time   = 37.827 − 8.55                                 = 29.277
  raw     = round(27000 × 29.277)                         = 790,479
  / 1e4                                                   = 79.0479         (7904.79%)

display = 7,904.79%   ✓
diff    = 2,308.5%    ✓
```

---

## 8. Pal Active Skill Damage — `BuffSkillValue._calHurt` (script offset ~8606354)

Pals fire active skills via the buff-skill framework. The base damage is computed by `_calHurt` with `_calType = 10`:

```js
case 10:
  var g = r.data.getAttrib(att_dam);
  if (r.parent && !r.isCallType) a = r.parent.data.getAttrib(att);
  var h = r.data.getAttrib(partner_dam);
  var p = r.data.getAttrib(partner_dam_extra);
  g = round(g * h * p);
  e = roundInt(Math.max(roundInt(a - i*(1+l)), 1) * g);
  break;
```

### 8.1 Formula

```
ATK       = parent.att  (if pal has parent and !isCallType — else pal.att)
DEF       = target.def
DEF_COE   = target.def_coe
base_raw  = max(roundInt(ATK − DEF×(1+DEF_COE)), 1)

mult      = round(att_dam × partner_dam × partner_dam_extra)
damage    = roundInt(base_raw × mult)
```

> ⚠️ Unlike `normalHurt` (basic attack), pal **active-skill** damage multiplies in `att_dam` (1039) too. Active skills are skill-type, not basic-attack-type — but the pal scaling stacks all three (`att_dam × partner_dam × partner_dam_extra`).

### 8.2 Crit on pal active skills — `BuffSkillValue.onBegin`

```js
var D = ignoreFlag & T1045 ? 1 : r.data.getAttrib(skill_dam_extra);
var x = roundInt(p * D);                                  // skill_dam_extra

if (!(ignoreFlag & SkillCrit) && checkSkillCirt(r)) {
  var L = r.data.getAttrib(skill_crit_dam);
  x = roundInt(x * round(1 + L));
  x = roundInt(Math.pow(x, 0.98));                        // 0.98 exponent on the *product*
  P = Hurt_Crit;
}

if ((ignoreFlag & UseCrit) && checkHit(r, t, true) == Cirt) {
  var F = r.data.getAttrib(crit_dam);
  var w = Math.max(0.5, t.data.getAttrib(crit_def));
  x = roundInt(x * Math.max(1.5, round(F / w)));
  P = Hurt_Crit;
}

var G = r.data.getAttrib(boss_dam);
if (target.type == Boss && G > 0) x = roundInt(x * round(1 + G));
```

### 8.3 Three crit paths

| Path | Triggered by | Multiplier |
|---|---|---|
| **Skill Crit** (default for skill damage) | `checkSkillCirt(caster)` — based on `skill_crit_rate` | `roundInt(x × (1 + skill_crit_dam))` then `pow(x, 0.98)` |
| **Normal Crit on a skill** | only if the skill config has `UseCrit` flag, then `checkHit` returns Crit | `roundInt(x × max(1.5, crit_dam / max(0.5, crit_def)))` |
| **Boss DMG** | target is Boss type | `× (1 + boss_dam)` |

Both crit types **can** stack on a single skill if both flags are set and both roll true. Most pal active skills use only Skill Crit.

### 8.4 `isCallType` — what is it?

`r.isCallType` flags a "called/summoned" unit. When `true`, the pal does **not** inherit the parent's ATK in skill damage; it uses its own. This is mainly for transient summons that don't pretend to be the parent's pal. Most pet companions have `isCallType = false`.

### 8.5 The `T1045` ignore flag

`T1045` (= 2) skips `skill_dam_extra`. Used by skill effects that compute their own scalar and don't want the player's flat skill damage bonus stacking on top.

---

## 9. Pal HP-Based Damage — `BuffSkillValue._calHpHurt` (script offset ~8608869)

When a pal fires a skill that deals damage as a percentage of HP, the *clamp* on the damage uses the pal-aware ATK formula:

```js
_calHpHurt = function(t, r, a) {
  var isHpBased = (3 == this._calType || 2 == this._calType || 8 == this._calType || 9 == this._calType)
               || (0 == this._calType && this._attribId == hp);
  if (!isHpBased) return false;

  var l = roundInt(a * this.skillPar);
  l = roundInt(l * t.battleMain.injuryReduce);

  if (this._limit) {
    var c = r.data.getAttrib(att);
    var g = t.data.getAttrib(def);
    var h = t.data.getAttrib(def_coe);
    var p = r.data.getAttrib(att_dam);
    if (!r.isCallType && r.config.type == s.Partner) {
      c = r.parent.data.getAttrib(att);
      var _ = r.data.getAttrib(partner_dam);
      var v = r.data.getAttrib(partner_dam_extra);
      p = round(p * _ * v);                               // same triple as case 10
    }
    var k     = roundInt(Math.max(roundInt(c - g*(1+h)), 1) * p);
    var lower = roundInt(k * this._limit[0]);
    var upper = roundInt(k * this._limit[1]);
    l = Math.max(l, lower);
    l = Math.min(l, upper);
  }
  this.runner.healthTarget(t, l, Hurt, false, this.config.id);
  return true;
};
```

### Mechanics

- The **raw HP damage** = `roundInt(target_hp × skillPar × battleMain.injuryReduce)`.
- The **clamp band** is `[k×limit[0], k×limit[1]]` where `k` is the pal's basic-attack equivalent damage using `att_dam × partner_dam × partner_dam_extra`.
- So a "deal X% of HP, but at least Y% / at most Z% of your pal damage" skill stays bounded relative to the pal's damage potential.

---

## 10. `calHurt` — DMG RES, PvE DMG, Total DMG (script offset ~12443900)

```js
calHurt = function(t, a, r) {
  var resist     = a.data.getAttrib(resist);
  var pveResist  = a.data.getAttrib(pve_resist);
  var pveDam     = r.data.getAttrib(pve_dam);
  t = roundInt(t * round(1 + pveDam));
  var u = roundInt(roundInt(t * round(1 - resist)) * round(1 - pveResist));
  return Math.max(1, u);
};
```

Applied **after** the pal-specific multiplier and resist, **before** crit. Affects every pal damage path (basic, combo, counter (theoretical), HP-based, skill).

| Layer | What it represents | Where it stacks |
|---|---|---|
| `pve_dam` (1057) | Attacker's PvE DMG bonus | `× (1 + pve_dam)` first |
| `resist` (1021) | Target's **DMG RES** (the universal one) | `× (1 − resist)` |
| `pve_resist` (1058) | Target's PvE DMG RES | `× (1 − pve_resist)` |
| `total_dam_add` / `total_dam_def` (1081/1082) | **Not** applied in `calHurt`. These feed into the `resist` aggregate when present (group_attr mechanism on attribute 1021/1057/1058) — see § 11. |

> Important: `total_dam_add` and `total_dam_def` are *aggregate attributes* used by groupings. The hot path in `calHurt` only reads `resist`, `pve_resist`, `pve_dam`. Any "Total DMG Bonus" buffs ultimately route through one of those three or via separate `SKILL_DAMAGE_ADD` buffs that hook the skill-damage path explicitly.

---

## 11. Group Attributes & `total_dam_add` Interaction

`getPetFactAttrValue` (§ 2) checks `configAttribute.getDataByList("group", attrId)` for **group multipliers** that apply *during base assembly*. Specifically:

- For `att` (1001): group includes `att_base_add` (2001), `att_total_add` (3001).
- For `partner_dam` (1040): group includes `partner_dam_base_add` (~2002x), etc.
- For `crit_dam` (1005): may include `crit_dam_base_add`, etc., but only if the talent/proficiency config provides them. Most do not.

Group multipliers are applied **multiplicatively at base-assembly time** via:

```
baseValue = roundInt(baseValue × (1 + group_bonus / 1e4))
```

This is one place where "X% bonus" can stack onto the pal's *baseValue* directly (i.e., before `_addValue`/`_time` ever run). The avian active-skill bonuses do **not** flow through this — they hit the MetaAttrib directly via `addMultiples`. The group system is mostly for ConfigPet talent/proficiency and core player attributes.

---

## 12. The Cannon / Gun Branch (`d.Gun`) — Not a Pal, but Related

The seasonal cannon system uses the same `normalHurt` / `normalDoubleHurt` plumbing but with a `d.Gun` branch:

- ATK: cannon's own (`o = t.data.getAttrib(att)`)
- Multiplier: `partner_dam` only (no `partner_dam_extra`)
- Resistance attribute: `season_cannon_att_def` (1059) instead of `partner_resist`
- Calls `calSuppressAndInspire(a, t, m, season_cannon_att_def_id)` — but on the cannon itself, not via `t.parent`
- The cannon's `partner_dam` is set per cannon at spawn (`A.data.getAttribMeta(partner_dam).baseValue = round(v × dam_add/1e4 × 1e4)`)

This branch is **completely separate** from pal scaling — it's worth noting only because the same source function (`normalHurt`) handles both, and confusion between the two surfaces in any custom calculator built off the same source.

---

## 13. Counter Attacks and Pals

`normalCounterHurt` (script offset ~12445097) has **no Partner branch**:

```js
normalCounterHurt = function(t, a, r, e) {
  var d = t.data.getAttrib(att);                          // attacker's own ATK
  // ...no `if (t.config.type == d.Partner)` block...
  var m = t.data.getAttrib(counter_dam);
  var A = roundInt(Math.max(roundInt(d - o*(1+u)), 1) * m) * round(1 - s);
  A = roundInt(A);
  A = calHurt(A, a, t);
  if (r != 1) A = roundInt(A * Math.max(1.5, round(g/b)));
  return Math.max(1, A);
};
```

### Implication

If a pal ever **does** counter (it has `counter > 0` and `checkCounterAct` returns true), the counter damage:

- Uses **the pal's own ATK** (`pal.data.getAttrib(att)`) — which was *baseValue-copied* from the parent at battle load, **not refreshed live**.
- Uses `counter_dam` (1033) directly, not `partner_dam`.
- Uses `counter_def` (1035) and `calArmorAndBlock` (pierce/block applies!).
- Uses the pal's own `crit_dam` for the crit multiplier.

In practice, pals do not have meaningful counter rates in most builds, so this path is rarely exercised — but it's a real difference from basic/combo.

---

## 14. Pal Panel Display Stats (verified against code)

`BattleSubPetPanelView` at script offset ~15573339 (and dup at 15779692):

```js
var B = [1040, 1003, 1004, 1005, 1016, 1032, 1007];
var V = (D = {}, D[1] = {cfgName:"partner_dam", attrId:1040},
                  D[2] = {cfgName:"att_speed",  attrId:1003}, … );
```

| Slot | Attribute | ID | Panel label |
|---|---|---|---|
| 1 | partner_dam | 1040 | **DMG Multiplier** |
| 2 | att_speed | 1003 | **ATK SPD** (displayed as `floor(att_speed/100)/100`) |
| 3 | crit_rate | 1004 | **Crit** |
| 4 | crit_dam | 1005 | **Crit DMG** |
| 5 | double_hit | 1016 | **Combo** |
| 6 | double_hit_dam | 1032 | **Combo Multiplier** |
| 7 | hit | 1007 | **Ignore Evasion** |

### How the panel renders the value

For percentage-type attributes (`num_type == 2`):

```
displayed_string = (MetaAttrib.value × 100).toFixed(2) + '%'
                 = (rawStored / 1e4 × 100).toFixed(2) + '%'
                 = (rawStored / 100).toFixed(2) + '%'
```

So `partner_dam = 9000` internal → "90.00%"; `crit_dam = 1021329` internal → "10,213.29%".

For `att_speed` (1003, num_type == 1):

```
panelString = floor(att_speed / 100) / 100
```

`94` internal → "0.94". (att_speed is in centi-units relative to base 100.)

---

## 15. Buff Targeting — How `+X% Pal CritDMG` Actually Hits the Pal

Buffs (`BuffSkillModify` and friends) carry these key fields:

| Field | Meaning |
|---|---|
| `_id` | The attribute ID to modify (e.g., `1005` for crit_dam) |
| `_isMultiples` | If `true` → `addMultiples`; if `false` → `addValue` |
| `_lastValue` / `_totaladdvalue` | The actual numeric delta applied |
| `owner` | The unit whose MetaAttrib gets modified |

For an avian affix like Altruism granting "+285% Pal CritDMG":

```
target = pal
attribId = 1005 (crit_dam)
isMultiples = true
amount = 2.85   (i.e., 28500 in 10000ths)
→ pal.data.getAttribMeta(1005).addMultiples(2.85)
→ pal._time += 2.85
```

When the avian is unequipped, the buff's `onDestroy` reverses with `addMultiples(-2.85)`.

> The pal is targeted *by the buff* — the player-side buff infrastructure walks the player's pet units and applies the modifier to each. This is why pal stat bonuses don't show up on the *player's* panel.

---

## 16. Theoretical Q&A Reference

**Q: If I stack flat Pal CritDMG (`addValue`) bonuses, does it dilute my avian's multiplicative ones?**
A: No — it does the opposite. Higher `(baseValue + _addValue)` makes every `_time` percentage point worth more, so multiplicative bonuses become **more powerful**. This is why flat sources of pal crit_dam (talent/proficiency/some passive skills) are very valuable alongside avian bonuses.

**Q: Does the pal's `crit_dam / crit_def` ratio ever cap?**
A: No upper cap. Only `Math.max(1.5, …)` floor. With crit_dam = 100x and crit_def = 0.5x, the multiplier is 200x; nothing in the formula caps it.

**Q: Why does my pal `Crit` panel show > 100%?**
A: `crit_rate` doesn't cap at 1.0 in the attribute table (no `up_limit`). Effective crit rate in `checkHit` is `max(crit_rate − ignore_crit_rate, 0)`, then `(1 − evasion) × effective_crit × 10000` gets bucketed against the random roll. If effective > 1.0, the bucket saturates the random range, so any non-miss is a guaranteed crit.

**Q: My `Combo Multiplier` shows 100.00%. Does that mean +100% damage on combo?**
A: No — it's the **raw** combo multiplier (`double_hit_dam`). 100% means the combo deals 1.0× the base, *replacing* the basic-attack `att_dam` not adding to it. Most pal builds work up to `double_hit_dam` in the 200–600% range. Note that Combo damage = `roundInt(pal_base × double_hit_dam)`, so 100% = same damage as basic.

**Q: Does `att_dam` (the player's basic-attack multiplier) affect pal basic attacks?**
A: **No** for pal basic and combo (those use only `partner_dam × partner_dam_extra`). **Yes** for pal active skills via `_calType = 10`, which combines `att_dam × partner_dam × partner_dam_extra`.

**Q: Does the pal's `att_dam` matter at all?**
A: Only for HP-based and pal active skill damage. Not for normal pal basic/combo.

**Q: I have `partner_dam_extra` from gear. Does buffing it during battle update the pal panel?**
A: The pal panel reads `pal.data.getAttrib(partner_dam)`, which only changes if the pal's own `partner_dam` MetaAttrib changes. `partner_dam_extra` lives on the parent and is read **live** during damage calc, but it's not shown on the pal panel directly. The product `partner_dam × partner_dam_extra` is the effective multiplier in combat, but the panel only shows `partner_dam`.

**Q: How does Inspire interact with multiple pals attacking the same target?**
A: Each pal hit independently rolls `calSuppressAndInspire`. There's no cross-pal accumulation. Inspire/Suppress is per-hit RNG.

**Q: Can `partner_resist` be reduced below 0 by Inspire?**
A: Yes — `round(r − min(0.5, (inspire − ignore)/10000))` can produce a negative number. Then `round(1 − resistance)` is > 1, which **amplifies** the damage. The 0.80 up_limit cap only applies at the upper bound.

**Q: How is `defCoe` (DEF_COE, 1060) different for pal vs player?**
A: It isn't. Pals read `target.def_coe` the same way the player does — and DEF_COE is on the target, not the attacker. Effective DEF for a pal hit = `def × (1 + def_coe)`. This is in **every** damage path (basic, combo, counter, HP-based, pal skill).

**Q: Does `total_dam_add` apply to pal damage?**
A: Not directly via `calHurt`. It typically routes through `resist` aggregates or via `SKILL_DAMAGE_ADD` buffs that hook in via the skill-damage path (`BuffSkillValue.onBegin`). Pure pal basic attacks don't read it.

**Q: How is the "double-hit" combo proc rolled?**
A: `checkDoubleAct` (`HurtUtil`): `rate = max(round(double_hit − ignore_double_hit), 0)`, then `roll = randomInt(0, 1e4) <= rate × 1e4`. Strict `<=`.

**Q: Does Combo `double_hit_def` reduce pal combo damage at all?**
A: No, never. Verify by reading § 5: the pal branch never references the `A = calArmorAndBlock(…, double_hit_def_id)` variable. The Gun branch and the player branch do; the pal branch only uses `partner_resist` via `calSuppressAndInspire`. This is a meaningful asymmetry — stacking combo RES on a target does **not** mitigate incoming pal combos.

**Q: Does Skill Crit interact with normal Crit on a pal active skill?**
A: They are independent (§ 8.3). A pal skill with both flags can roll Skill Crit and Normal Crit in the same event, stacking both multipliers (Skill Crit applies first, then Normal Crit). In practice, the `_ignoreFlag` config on most pal skills enables only one path.

**Q: What's the 0.98 exponent on Skill Crit doing?**
A: `pow(x, 0.98)` applied to the *product* `(damage × (1 + skill_crit_dam))`. This is a tiny diminishing-returns term — at moderate damage scales (`x ≈ 10^6`), it shaves off roughly `x × 0.02 × ln(x) ≈ 0.3x`. Yuko's PDF has the exponent on `(1 + skill_crit_dam)` alone, which is incorrect — the source applies it to the full product.

**Q: Does `skill_dam_extra` apply to pal basic attacks?**
A: No. It only applies in the skill-damage path (`BuffSkillValue.onBegin`). Pal basic/combo do not multiply by skill_dam_extra.

**Q: Does `boss_dam` apply to pal damage?**
A: For pal **active skills**, yes — it's multiplied in at the end of `onBegin` if the target is `s.Boss`. For pal **basic/combo** (`normalHurt`/`normalDoubleHurt`), it is NOT in the formula explicitly. It's a quiet asymmetry: against bosses, pal active skills get the boss bonus but pal autos do not.

**Q: Why does the simulator show different numbers than the game?**
A: Because (a) it implements idealized "Yuko-style" formulas without DEF_COE, suppress/inspire RNG, the `0.98` exponent, or the asymmetric MetaAttrib `_time` vs `_addValue` paths; (b) it doesn't simulate `_isMultiples` semantics for buff configs; (c) it doesn't track talent/proficiency group-multiplier composition. **Do not use the simulator to validate pal mechanics — always re-derive from `game_script.js`.**

**Q: Does evasion (target `miss`) ever apply to pal damage?**
A: Yes — via `checkHit` in the pal's crit-check path. If `miss > hit`, the corrected evasion rolls Miss before any damage is computed. PvP caps miss at 80% via `battle_up_limit`.

**Q: Are there pal-specific "ignore evasion" stats?**
A: No — the same `hit` (1007) attribute on the pal counters target's `miss` (1008). The pal panel labels `hit` as "Ignore Evasion" because effective miss = `max(miss − hit, 0)`.

**Q: Can the pal's `crit_dam` be reduced to below the default 100%?**
A: Yes — `addValue(-X)` or buffs with negative bonuses reduce `_addValue`. The display can drop below 100%, but the `Math.max(1.5, crit_dam/crit_def)` floor in the actual damage formula ensures crits still deal at least 1.5×.

**Q: Where does pal damage get rounded?**
A: At least four times per hit:
1. `roundInt(ATK − DEF×(1+DEF_COE))`
2. `round(pal_mult × round(1 − PR))` (note the nested round)
3. `roundInt(base_raw × …)` for the pre-crit, pre-resist value
4. `roundInt(damage × …)` for each subsequent multiplication step

Each `round`/`roundInt` is FixMath's banker-style rounding. Small bonuses (< 1 unit at any layer) can vanish.

**Q: How do `partner_inspire_rate` and `partner_suppress_rate` swap?**
A: When the **attacker's** `partner_inspire` exceeds the target's `ignore_partner_inspire`, the gate probability uses `attacker.partner_suppress_rate` (note: suppress_rate). When the **target's** `partner_suppress` exceeds the attacker's `ignore_partner_suppress`, the gate probability uses `target.partner_inspire_rate` (note: inspire_rate). The naming is intentionally swapped in the source — preserve it.

---

## 17. Cross-Reference Map

| Mechanic | Code offset (in `game_script.js`) | Reference doc |
|---|---|---|
| `MetaAttrib` formula | ~13546840 | `data/formulas/attribute_calculation.json` |
| `normalHurt` (basic) | ~12441031 | 11_PAL_DAMAGE.md § A |
| `normalDoubleHurt` (combo) | ~12443967 | 11_PAL_DAMAGE.md § B |
| `normalCounterHurt` (counter) | ~12445097 | 11_PAL_DAMAGE.md § (counter) |
| `SkillHurt` (skill) | ~12449141 | LOM_MASTER_FORMULA_REFERENCE § 3.5 |
| `BuffSkillValue._calHurt` (skill base, case 10) | ~8606354 | 17_PET_PAL_SYSTEM.md § C |
| `BuffSkillValue._calHpHurt` (HP-based) | ~8608869 | 11_PAL_DAMAGE.md § E |
| `BuffSkillValue.onBegin` (skill apply, crits, boss_dam) | ~8610000 | this doc § 8 |
| `calSuppressAndInspire` | ~12442800 | 18_AVIAN_SYSTEM.md (overview) |
| `calArmorAndBlock` (pierce/block — not pals) | ~12442100 | 08_PIERCE_BLOCK_INSPIRE_SUPPRESS.md |
| `calHurt` (DMG RES + PvE) | ~12443900 | 04_PVP_DAMAGE_REDUCTION.md |
| `checkHit` (crit/miss) | ~12446142 | 03_CRITICAL_HIT_SYSTEM.md |
| `checkSkillCirt` | ~12449000 | 03_CRITICAL_HIT_SYSTEM.md |
| `setPlayerPets` (server) | ~8293223 | 17_PET_PAL_SYSTEM.md § A |
| `getPetFactAttrValue` (battle, 4-arg) | ~8295775 | 17_PET_PAL_SYSTEM.md § B |
| `BattleSubPetPanelView` (pal panel render) | ~15573339 | this doc § 14 |

---

## 18. Closing Note — Why This Doc Exists

The "+285% Pal CritDMG → +2308.5% on panel" question doesn't have a single multiplier explaining it. It's the MetaAttrib formula applied to a multiplicatively-stacked `_time`, sitting on top of an additively-built `(base + addValue)` chunk that includes the pal's `ConfigPetlevel.crit_dam`, proficiency bonuses, talent bonuses, and flat-add buffs. Each layer is correct in isolation, but only the source code reveals the whole compositional model. When in doubt, re-derive — never trust a simulator that hasn't been forensically reconstructed from `game_script.js`.

Bird → Discord @birrrd08
