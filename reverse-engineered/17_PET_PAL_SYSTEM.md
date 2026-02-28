# 17 — Pet/Pal System

## Overview

Pals (Pets) are companion creatures that fight alongside the player in battle. They **inherit the player's ATK** and apply their own damage multipliers (`partner_dam`). Each pet has a level, race, talent, and proficiency system.

---

## Config Tables

| Table | Source Line | Main Key | Description |
|-------|-----------|----------|-------------|
| ConfigPet | 252193 | id | Base pet definitions (name, quality, unitId, talent slots) |
| ConfigPetlevel | 252287 | id + level | Per-level stats (partner_dam, def, hp, 60+ combat stats) |
| ConfigPetrace | 252643 | id | Race/type names |
| ConfigPet_talent | 252111 | id + all_star | Talent effects unlocked at star thresholds |
| ConfigPet_proficiency | 252044 | id + level | Proficiency EXP, extra stars, attribute bonuses |
| ConfigPet_pos | 251997 | id | Position slot unlock conditions |

---

## A. Battle Loading — setPlayerPets

### Server Data Version (Lines 187544-187562)

```javascript
t.setPlayerPets = function(t, i, a) {
    if (null != i && 0 != i.length)
        for (var r, l = configAttribute.getDataByList("module", 1), s = e(i); !(r = s()).done;) {
            var f = r.value;
            if (0 != f.pet_id) {
                var c = configPet.getDataByKey(f.pet_id),
                    v = configPetlevel.getDataByKeys("id", f.pet_id, "level", f.pet_lev),
                    d = new o;
                d.attribs = {}, d.roleId = t.id;
                var b = configUnit.getDataByKey(c.unitId);
                d.config = b, d.skillList = [];
                // Apply getPetFactAttrValue to each attribute
                for (var k, g = e(l); !(k = g()).done;) {
                    var _ = k.value,
                        p = new n(_);
                    p.baseValue = this.getPetFactAttrValue(a, v[_.key], f.pet_id, _.id);
                    d.attribs[_.id] = p
                }
                // INHERIT from parent player:
                d.attribs[u.hp].baseValue = t.units[0].attribs[u.hp].baseValue;
                d.attribs[u.att].baseValue = t.units[0].attribs[u.att].baseValue;
                d.attribs[u.partner_dam_extra].baseValue = t.units[0].attribs[u.partner_dam_extra].baseValue;
                d.attribs[u.skill_dam_extra].baseValue = t.units[0].attribs[u.skill_dam_extra].baseValue;
                d.attribs[u.skill_crit_rate].baseValue = t.units[0].attribs[u.skill_crit_rate].baseValue;
                d.attribs[u.skill_crit_dam].baseValue = t.units[0].attribs[u.skill_crit_dam].baseValue;
                d.attribs[u.boss_dam].baseValue = t.units[0].attribs[u.boss_dam].baseValue;
                d.idleIndex = f.pet_pos + 1;
                t.units.push(d)
            }
        }
}
```

### Client Local Version (Lines 199092-199107)

```javascript
e.setPlayerPets = function(e) {
    for (var a, i = IS(I).getWearPetList(), r = configAttribute.getDataByList("module", 1), n = t(i); !(a = n()).done;) {
        var l = a.value,
            s = configPet.getDataByKey(l.pet_id),
            o = configPetlevel.getDataByKeys("id", l.pet_id, "level", l.level);
        // ... create unit, apply attributes via getPetFactAttrValue ...
        // INHERIT from parent:
        h.attribs[c.hp].baseValue = e.units[0].attribs[c.hp].baseValue;
        h.attribs[c.att].baseValue = e.units[0].attribs[c.att].baseValue;
        h.attribs[c.partner_dam_extra].baseValue = e.units[0].attribs[c.partner_dam_extra].baseValue;
        h.idleIndex = l.pos + 1;
        e.units.push(h)
    }
}
```

### Inherited Attributes from Player

The following attributes are **copied from the parent player** to the pal at battle load time:

| Attribute | Server Version | Client Version |
|-----------|---------------|----------------|
| hp | Yes | Yes |
| att | Yes | Yes |
| partner_dam_extra | Yes | Yes |
| skill_dam_extra | Yes | No |
| skill_crit_rate | Yes | No |
| skill_crit_dam | Yes | No |
| boss_dam | Yes | No |

---

## B. getPetFactAttrValue — Attribute Calculation

### Code (Lines 187495-187505)

```javascript
t.getPetFactAttrValue = function(t, e, i, a) {
    if (null == t) return e;
    // Step 1: base + pet-specific bonus + global bonus
    var l = r.roundInt(e + this.getPetAttrByAttrId(t, i, a) + this.getPetAttrByAttrId(t, 0, a));

    // Step 2: check for group multipliers
    var s = configAttribute.getDataByList("group", a);
    if (null == s || s.length <= 0) return l;

    // Step 3: apply each group multiplier
    for (var n = 0; n < s.length; n++) {
        var u = r.roundInt(this.getPetAttrByAttrId(t, i, s[n].id) + this.getPetAttrByAttrId(t, 0, s[n].id));
        var o = r.round(r.round(u / 1e4) + 1);
        l = r.roundInt(l * o)
    }
    return l
}
```

### Formula

```
final_value = base_value + pet_bonus(petId, attrId) + global_bonus(0, attrId)

For each group_attr in attribute_group(attrId):
    group_sum = pet_bonus(petId, group_attr) + global_bonus(0, group_attr)
    multiplier = round(round(group_sum / 10000) + 1)
    final_value = roundInt(final_value * multiplier)
```

**Note:** `pet_bonus(petId, attrId)` comes from proficiency/talent bonus data (`t` parameter), indexed by pet ID and attribute ID. `global_bonus(0, attrId)` is the bonus shared across all pets (index 0).

---

## C. Pal Damage in Combat

### Basic Attack (normalHurt, Lines 322765-322771)

When `attacker.config.type == Partner`:

```javascript
o = t.parent.data.getAttrib(i.att);           // PARENT's ATK
m = a.data.getAttrib(i.partner_resist);        // target's pal resistance
m = p(a, t.parent, m, i.partner_resist);       // calSuppressAndInspire
A = t.data.getAttrib(i.partner_dam);           // pal's own multiplier
var c = t.parent.data.getAttrib(i.partner_dam_extra); // parent's extra multiplier
A = n.round(A * c);                           // combined multiplier

var f = n.roundInt(
    Math.max(n.roundInt(o - u * (1 + g)), 1)  // (ParentATK - DEF*(1+DEF_COE))
    * n.round(A * n.round(1 - m))             // * combined_mult * (1 - resistance)
);
f = _(f, a, t);  // calHurt (DMG RES + PvE)
// crit: f = roundInt(f * max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF))))
```

### Formula

```
base_raw    = max(roundInt(PARENT_ATK - DEF * (1 + DEF_COE)), 1)
pal_mult    = round(PARTNER_DAM * PARTNER_DAM_EXTRA)
resistance  = calSuppressAndInspire(target, parent, PARTNER_RESIST)
pal_dmg     = roundInt(base_raw * round(pal_mult * round(1 - resistance)))
pal_dmg     = calHurt(pal_dmg, target, pal)   // applies DMG RES
if CRIT:
    pal_dmg = roundInt(pal_dmg * max(1.5, round(CRIT_DAM / max(0.5, CRIT_DEF))))
result      = max(1, pal_dmg)
```

### Combo Attack (normalDoubleHurt, Lines 322851-322859)

```javascript
if (t.config.type == d.Partner) {
    o = t.parent.data.getAttrib(i.att);
    var v = t.data.getAttrib(i.partner_dam),
        h = t.parent.data.getAttrib(i.partner_dam_extra);
    v = n.round(v * h);

    var M = a.data.getAttrib(i.partner_resist),
        I = p(a, t.parent, M, i.partner_resist);

    var x = n.roundInt(Math.max(n.roundInt(o - u * (1 + g)), 1) * v)
            * n.round(1 - I);
    f = n.roundInt(n.roundInt(x) * c);   // c = double_hit_dam
}
```

### Formula

```
pal_base  = roundInt(max(roundInt(PARENT_ATK - DEF*(1+DEF_COE)), 1) * pal_mult)
            * round(1 - resistance)
pal_combo = roundInt(roundInt(pal_base) * DOUBLE_HIT_DAM)
```

**Important:** The combo multiplier (`double_hit_dam`) is applied AFTER the pal damage calculation, not combined with `partner_dam`.

### HP-Based Damage Clamping (Lines 195801-195806)

When a pal fires an HP-based skill, the clamping uses a modified att_dam:

```javascript
if (!r.isCallType && r.config.type == s.Partner) {
    c = r.parent.data.getAttrib(u.att);
    var _ = r.data.getAttrib(u.partner_dam),
        v = r.data.getAttrib(u.partner_dam_extra);
    p = n.round(p * _ * v);  // att_dam * partner_dam * partner_dam_extra
}
```

---

## D. Key Combat Attributes

| Attribute | Attr ID | Owner | Description |
|-----------|---------|-------|-------------|
| partner_dam | 1040 | Pal | Pal's base damage multiplier (from ConfigPetlevel) |
| partner_dam_extra | 1047 | Player | Player's pal damage bonus (inherited by pal) |
| partner_resist | 1020 | Target | Target's resistance to pal damage |
| partner_inspire | 1074 | Attacker | Inspire value for partner_resist |
| partner_suppress | 1077 | Target | Suppress value for partner_resist |
| att (inherited) | 1001 | Pal (from Player) | ATK used for pal damage is PARENT's ATK |
| hp (inherited) | 1002 | Pal (from Player) | HP inherited from parent |

---

## E. Pal Display Stats

From line 5239:
```javascript
this.txtPetDam.string = String(Math.floor(e.partner_dam) / 1e4);
this.txtPetAtkSpd.string = String(Math.floor(e.att_speed / 100) / 100);
```

- **Pal Damage** is displayed as `partner_dam / 10000` (e.g., 15000 = 1.5x multiplier)
- **Pal Attack Speed** is displayed as `att_speed / 10000` (divided by 100 twice)

---

## F. ConfigPetlevel Full Stat List (64 Fields)

The Petlevel config contains an extensive set of combat stats (all XOR-encoded):

```
partner_dam, def, hp, att_range, detection_range, att_speed,
crit_rate, crit_dam, crit_def, boss_dam, double_hit, hit, miss,
speed, vertigo, suspend, target_num, double_hit_dam,
skill_dam_extra, power_recovery, att_hpsteal, skill_hpsteal, power,
skill_crit_rate, skill_crit_dam, hp_recovery, counter, att_resist,
skill_resist, partner_resist, resist, suspend_def, vertigo_def,
att_hpsteal_def, skill_hpsteal_def, vertigo_times, vertigo_res,
counter_dam, double_hit_def, counter_def, counter_suspend,
ignore_double_hit, ignore_counter, boss_def, hpsteal_rate,
hpsteal_amount, ignore_hpsteal, hpsteal_res, pve_dam, pve_resist,
shield_time_extra, shield_hp_extra, skillbuff_time_all, control_res,
total_dam_add, total_dam_def
```

---

## G. Talent System

**Config:** ConfigPet_talent (line 252111)

- Talents are indexed by `(id, all_star)` — the talent ID and the total star level required to unlock
- Each talent has an `effect` array (stat bonuses) and a `power` array (power bonuses)
- Talents are listed per-pet in ConfigPet's `talent` field

---

## H. Proficiency System

**Config:** ConfigPet_proficiency (line 252044)

- Indexed by `(id, level)` — proficiency type and level
- Each level grants `extra_star` (additional stars), `own_attrs` (attribute bonuses), and `power`
- Proficiency EXP is tracked via `exp` and `addexp` fields
- These bonuses feed into `getPetFactAttrValue()` as the group multiplier data

---

## I. Race/Type System

**Config:** ConfigPetrace (line 252643)

- Simple mapping of race ID to name
- Pet type is stored in ConfigPet's `type` field (optional array)
- Race affects categorization and potentially type-advantage mechanics

---

## J. Pet Skill Loading

From line 278634, skill types include:
```javascript
e[e.PARTNER_SKILL = 4] = "PARTNER_SKILL"
```

Pet skills are loaded as passive skills attached to the player unit. At line 450356-450358:
```javascript
if (a.type == B.PARTNER_SKILL) {
    t.petPassiveSkillList = null != (s = t.petPassiveSkillList) ? s : [];
    t.petPassiveSkillList.push(r)
}
```

Pet passive skills are stored in a separate `petPassiveSkillList` on the player unit data.
