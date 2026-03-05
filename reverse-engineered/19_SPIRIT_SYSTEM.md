# 19 — Spirit / Guardian Spirit System

> **MERGED**: This content has been consolidated into `battlesim/reference/14_SPIRITS.md` which now contains the complete spirit system reference: 20 spirits, config tables with source lines, stat formulas, spiritNormalHit code, affix system, crafting, gacha, and battle loading code.

See `battlesim/reference/14_SPIRITS.md` for the unified reference.

## Overview (archived)

Guardian Spirits are summoned combat entities with their own HP, ATK, skills, and a unique damage formula (`spiritNormalHit`). They feature an affix slot system for bonus attributes, a crafting system, and a gacha draw system. Spirits scale from their level config and partially from the parent player's damage output.

---

## Config Tables

| Table | Source Line | Main Key | Description |
|-------|-----------|----------|-------------|
| ConfigSpirit | 262760 | spirit_id | Base spirit definitions (quality, model, bullet type) |
| ConfigSpirit_level | 262673 | spirit_id + spirit_level | Per-level stats, skills, att_dam ratios, slot_amount |
| ConfigSpirit_craft | 262467 | id | Crafting recipes |
| ConfigSpirit_craft_target | 262420 | spirit_level | Level-gated crafting targets |
| ConfigSpirit_affix_group | 262266 | affix_group | Affix category groups |
| ConfigSpirit_attrbonus_affix | 262317 | affix_id | Individual affix definitions |
| ConfigSpirit_attrbonus_slot | 262379 | slot_id | Slot-to-affix-group mapping |
| ConfigSpirit_draw | 262583 | id | Gacha/draw banners |
| ConfigSpirit_draw_prob | — | — | Draw probability tables |

---

## A. Battle Loading — setPlayerSpirit

### Server Data Version (Lines 187576-187578)

```javascript
t.setPlayerSpirit = function(t, e) {
    t.spirit = e    // e = [spirit_id, spirit_level]
}
```

The spirit info is extracted from player ext data during PvP loading (lines 187409-187413):
```javascript
case 12:
    h[0] = Number(e);   // spirit_id
    break;
case 13:
    h[1] = Number(e);   // spirit_level
    break;
// ...
this.setPlayerSpirit(i, h);
```

### Client Local Version (Lines 199122-199124)

```javascript
e.setPlayerSpirit = function(e) {
    var t = IS(B).getCurSpirit();
    null != t && (e.spirit = [t.config_id, t.level])
}
```

Gets the currently equipped spirit from the GuardianSpiritDataCache.

**Note:** Unlike pets and avians, the spirit is NOT added as a unit in `setPlayerSpirit`. It is stored as a `[spirit_id, spirit_level]` tuple on the player list. The spirit unit is created later during battle initialization by the skill/buff system.

---

## B. Spirit Unit Creation in Battle

### Code (Lines 193065-193094)

```javascript
y.spiritInfo = v;        // [spirit_id, spirit_level]
y.attribs = {};
y.config = _;            // unit config
y.roleId = i.data.roleId;

// Base attributes from unit config
for (var A, I = configAttribute.getDataByList("module", 1), B = a(I); !(A = B()).done;) {
    var M = A.value,
        V = new s(M);
    V.baseValue = _[M.key];
    y.attribs[M.id] = V
}

// Apply spirit_attr from ConfigSpirit_level
var m = configSpirit_level.getDataByKeys("spirit_id", v[0], "spirit_level", v[1]);
if (m && m.spirit_attr)
    for (var L, S = m.spirit_attr, k = a(S); !(L = k()).done;) {
        var D = L.value;
        y.attribs[D[0]].baseValue = D[1]   // [attr_id, value]
    }

// Inherit specified attributes from parent player
if (null != this._attribs && this._attribs.length > 0)
    for (var w, U = a(this._attribs); !(w = U()).done;) {
        var F = w.value;
        y.attribs[F].setAttribValue(i.data.getAttribMeta(F))
    }

// HP calculation: base_hp + round(spirit_hp * (1 + spirit_hp_add))
var x = y.getAttrib(l.spirit_hp),
    O = y.getAttrib(l.spirit_hp_add),
    R = y.getAttribMeta(l.hp);
R.baseValue = R.baseValue + n.round(x * (1 + O));

// ATK calculation: base_att + round(spirit_att * (1 + spirit_att_add))
var j = y.getAttrib(l.spirit_att),
    C = y.getAttrib(l.spirit_att_add),
    H = y.getAttribMeta(l.att);
H.baseValue = H.baseValue + n.round(j * (1 + C));

// Load primary skills from ConfigSpirit_level.skill1
for (var K, P = a(m.skill1); !(K = P()).done;) {
    var N, z = K.value,
        Q = f.newSkill(z[0], z[1], y);   // [skill_id, skill_lv]
    y.skillList = null != (N = y.skillList) ? N : [];
    y.skillList.push(Q)
}
```

### Spirit Stat Formulas

```
Spirit HP  = base_hp + round(spirit_hp * (1 + spirit_hp_add))
Spirit ATK = base_att + round(spirit_att * (1 + spirit_att_add))
```

Where:
- `base_hp`, `base_att` come from the unit config
- `spirit_hp`, `spirit_att` come from ConfigSpirit_level.spirit_attr
- `spirit_hp_add`, `spirit_att_add` are percentage multipliers from spirit attributes

---

## C. Spirit Damage — spiritNormalHit

### Code (Lines 322981-323007)

```javascript
t("spiritNormalHit", (function(t, r) {
    var e = t.data.getAttrib(i.spirit_dam_add),
        o = 0;

    // Branch 1: Spirit vs Spirit
    if (r.config.type == d.Spirit) {
        var u = t.data.getAttrib(i.att),
            g = r.data.getAttrib(i.spirit_dam_def),
            l = r.data.getAttrib(i.spirit_dam_def_final);
        o = n.round(u * (e - g + 1) * (1 - l))
    }
    // Branch 2: Spirit vs Normal Target
    else {
        var p = configSpirit_level.getDataByKeys("spirit_id",
            t.data.spiritInfo[0], "spirit_level", t.data.spiritInfo[1]);
        if (p && p.att_dam) {
            // Parse att_dam into ratio map
            var A = {};
            for (var _ of p.att_dam) { A[_[0]] = _[1] }

            // Calculate scaled player damage types
            var h = normalHurt(t.parent, r, 1, false);    // noCrit
            h = n.round(h * A[1] / 1e4);                  // ratio[1]

            var M = normalDoubleHurt(t.parent, r, 1, false);
            M = n.round(M * A[2] / 1e4);                  // ratio[2]

            var I = normalCounterHurt(t.parent, r, 1, false);
            I = n.round(I * A[3] / 1e4);                  // ratio[3]

            var x = skillDamageHurt(t.parent, r, 1, false);
            x = n.round(x * A[4] / 1e4);                  // ratio[4]

            o = n.round(h + M + I + x)                    // sum all
        }
    }
    return o
}))
```

### Spirit vs Spirit Formula

```
damage = round(ATT * (spirit_dam_add - spirit_dam_def + 1) * (1 - spirit_dam_def_final))
```

| Variable | Source | Description |
|----------|--------|-------------|
| ATT | Spirit's att attribute | Spirit's own ATK |
| spirit_dam_add | Attacker attribute | Spirit's damage addition value |
| spirit_dam_def | Target attribute | Target spirit's damage defense |
| spirit_dam_def_final | Target attribute | Target's final damage reduction (0-1) |

### Spirit vs Normal Target Formula

```
h = normalHurt(parent, target, noCrit) * att_dam[1] / 10000
M = normalDoubleHurt(parent, target, noCrit) * att_dam[2] / 10000
I = normalCounterHurt(parent, target, noCrit) * att_dam[3] / 10000
x = skillDamageHurt(parent, target, noCrit) * att_dam[4] / 10000
damage = round(h + M + I + x)
```

| att_dam Key | Description |
|-------------|-------------|
| 1 | Normal hit ratio (/10000) |
| 2 | Combo/double hit ratio (/10000) |
| 3 | Counter hit ratio (/10000) |
| 4 | Skill damage ratio (/10000) |

**Key insight:** Against non-spirit targets, the spirit calculates what the PARENT player's normal hit, double hit, counter, and skill damage would be (without crit), then scales each by the spirit's `att_dam` ratios.

---

## D. Spirit Key Attributes

| Attribute | Description |
|-----------|-------------|
| spirit_dam_add | Spirit's damage addition (used in spirit-vs-spirit) |
| spirit_dam_def | Defense against spirit damage |
| spirit_dam_def_final | Final spirit damage reduction (percentage) |
| spirit_hp | Spirit HP flat bonus |
| spirit_hp_add | Spirit HP percentage multiplier |
| spirit_att | Spirit ATK flat bonus |
| spirit_att_add | Spirit ATK percentage multiplier |
| spirit_att_dam | Spirit attack damage attribute (line 244227, 267643) |

---

## E. Affix / Bonus Slot System

Spirits have affix slots that provide bonus attributes. The number of available slots increases with spirit level.

### How It Works

1. **ConfigSpirit_level.slot_amount** — number of affix slots available at this level
2. **ConfigSpirit_attrbonus_slot** — maps each `slot_id` to an `affix_group`
3. **ConfigSpirit_affix_group** — defines affix categories (name, icon)
4. **ConfigSpirit_attrbonus_affix** — individual affixes with:
   - `affix_group`: Category membership
   - `quality`: Rarity tier
   - `attr_id`: Which attribute this affix modifies
   - `value`: Value range array
   - `power_rate`: Combat power contribution rate

### Example Flow

```
Spirit Level 5 → slot_amount = 3
Slot 1 → affix_group 1 (e.g., "Offensive")
Slot 2 → affix_group 2 (e.g., "Defensive")
Slot 3 → affix_group 1 (e.g., "Offensive")

Each slot rolls an affix from its group:
Affix 101 → attr_id: att, value: [500, 1000], quality: 3
```

---

## F. Crafting System

**Config:** ConfigSpirit_craft (line 262467), ConfigSpirit_craft_target (line 262420)

- Spirits can be crafted from materials
- `craft_type` determines the crafting method
- `spirit_target_id` lists possible output spirits
- Materials divided into `main_craft_material` and `minor_craft_material`
- `ConfigSpirit_craft_target` gates available targets by spirit level and provides `spirit_group` arrays

---

## G. Gacha / Draw System

**Config:** ConfigSpirit_draw (line 262583)

| Field | Description |
|-------|-------------|
| name | Banner display name |
| type | Draw type |
| cost | Pull cost array |
| free_chance_num | Free pulls available |
| must | Guaranteed pull thresholds |
| prob | Probability distribution |

Spirits can be obtained through gacha banners with pity/guaranteed pull mechanics.

---

## H. Battle Update

### Line 201874-201876

```javascript
V.setSpirit = function() {
    var t = this.battleMain.data;
    IS(b).setPlayerSpirit(t.playerList[1])
}
```

Spirit data is refreshed via the `SpiritUpdate` flag in the battle update system (line 201821).
