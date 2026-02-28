# 18 — Avian (Spirit Bird / FlyPet) System

## Overview

The Avian system ("FlyPet" in code, "Spirit Bird" in-game) provides a flying companion that grants passive skills and stat bonuses in combat. Avians have their own leveling, advancing, entry (sub-stat), breeding, and hatching systems.

---

## Config Tables

| Table | Source Line | Main Key | Description |
|-------|-----------|----------|-------------|
| ConfigFly | 233576 | id | Base avian definitions (name, quality, unitid, fly_special) |
| ConfigFly_level | 233409 | id + level | Per-level stats and costs |
| ConfigFly_advance | 232812 | id + advance_level | Advance tiers, skills, and entry level caps |
| ConfigFly_egg | 232928 | id | Egg hatching weights |
| ConfigFly_entry | 233089 | id + level | Entry (sub-stat) definitions with passive skills |
| ConfigFly_hybrid | 233357 | id1 + id2 | Breeding combination results |
| ConfigFly_entry_num | — | — | Number of entries per avian |
| ConfigFly_entry_weight | — | — | Weighted entry selection |
| ConfigFly_evolution_pro | — | — | Evolution progression |
| ConfigFly_evolution_rate | — | — | Evolution success rates |
| ConfigFly_hybird_template | — | — | Hybrid breeding templates |
| ConfigFly_hybrid_time | — | — | Breeding time costs |
| ConfigFly_remake_cost | — | — | Entry reroll costs |
| ConfigFly_cd | — | — | Cooldown timers |
| ConfigFly_achievement | — | — | Collection achievements |
| ConfigFly_total_achievement | — | — | Total achievement milestones |

---

## A. Battle Loading — setPlayerFlyPet

### Server Data Version (Lines 187563-187575)

```javascript
t.setPlayerFlyPet = function(t, i) {
    var a = configFly.getDataByKey(i);
    if (null != a) {
        var r = configUnit.getDataByKey(a.unitid),
            l = new o;
        l.attribs = {}, l.roleId = t.id, l.config = r, l.skillList = [];
        for (var s, u = configAttribute.getDataByList("module", 1), f = e(u); !(s = f()).done;) {
            var c = s.value,
                v = new n(c);
            v.baseValue = r[c.key];  // attributes from UNIT config directly
            l.attribs[c.id] = v
        }
        l.idleIndex = 8;  // fixed position 8
        t.units.push(l)
    }
}
```

### Client Local Version (Lines 199108-199121)

```javascript
e.setPlayerFlyPet = function(e) {
    var a = IS(C).now_use_pet;   // current active avian ID
    if (0 != a) {
        var i = configFly.getDataByKey(a),
            r = configUnit.getDataByKey(i.unitid);
        // ... same pattern: attributes from unit config ...
        n.idleIndex = 8;
        e.units.push(n)
    }
}
```

### Key Differences from Pet System

| Aspect | Pet/Pal | Avian/FlyPet |
|--------|---------|--------------|
| ATK source | Inherits PARENT's ATK | Uses own unit config stats |
| HP source | Inherits PARENT's HP | Uses own unit config stats |
| partner_dam_extra | Inherits from parent | Not used |
| Position | pet_pos + 1 (variable) | Fixed at 8 |
| Attribute calculation | getPetFactAttrValue() | Direct from unit config |

---

## B. Loading in PvP / Server Context

From line 187375 and 187415:

```javascript
// In the ext parsing loop, the fly pet ID is extracted:
P = this.setPlayerFlyPet;  // function reference
// Later called via ext key processing
```

The avian ID is passed through player ext data. The server version passes the fly pet ID directly to `setPlayerFlyPet(playerList, flyPetId)`.

---

## C. Battle Update (Live Swap)

### Lines 201850-201873

```javascript
V.setFlyPet = function(t) {
    // Remove existing FlyPet units
    for (var l = 0; l < o.length; l++) {
        var s, d = o[l];
        if (d.config.type == h.FlyPet)
            null == (s = a.unitMgr.getUnit(d.unitId)) || s.dead();
            o.splice(l, 1), l--
    }
    // Unload old passive skills
    null == r || r.skillctr.unloadFlyPetPassiveSkill();
    r.flyPet = null;

    // Reload new FlyPet
    IS(b).setPlayerFlyPet(i.playerList[1]);

    // Add new units to battle
    for (var p, u = n(o); !(p = u()).done;) {
        var f = p.value;
        if (f.config.type == h.FlyPet) {
            var c = a.unitMgr.addPlayer(f);
            r && (c.direction = r.direction);
            a.mainCtr.units.push(c);
            r.flyPet = c
        }
    }
    a.mainCtr.positionSelected(a.mapCamera.offsetX, !0, 3)
}
```

The avian can be swapped during battle. The system removes the old FlyPet unit, unloads its passive skills, then loads the new one.

---

## D. Skill System

### Skill Type Enum (Line 278634)

```javascript
e[e.USE = 1] = "USE";
e[e.PASSIVE_ADD = 2] = "PASSIVE_ADD";
e[e.PASSIVE_EFFECT = 3] = "PASSIVE_EFFECT";
e[e.PARTNER_SKILL = 4] = "PARTNER_SKILL";
e[e.FLY_SKILL = 5] = "FLY_SKILL";
```

**FLY_SKILL = 5** is the dedicated type for avian skills.

### Skill Loading (Lines 450359-450361)

```javascript
if (a.type == B.FLY_SKILL) {
    t.flyPetPassiveSkillList = null != (o = t.flyPetPassiveSkillList) ? o : [];
    t.flyPetPassiveSkillList.push(r)
}
```

Avian skills are stored in `flyPetPassiveSkillList` on the player unit, separate from pet skills (`petPassiveSkillList`) and player passive skills (`passiveSkillList`).

### fly_special (ConfigFly field, index 11)

Some avians have a `fly_special` value that grants a special activatable ability. From line 297940:

```javascript
return 1 == e ? "" != i.fly_special   // filter: has special
     : 2 == e ? "" == i.fly_special   // filter: no special
     : ...
```

The special ability icon is loaded from `icon_flypet_special` (line 297880).

### Advance Skills (ConfigFly_advance.fly_skill)

Each advance tier can unlock new skills via the `fly_skill` array. These are the main combat-affecting passive skills that improve with advance level.

### Entry Skills (ConfigFly_entry)

Each entry has:
- `passive_skill`: Passive skill array (combat buffs)
- `special_effect`: Special effect array (additional combat effects)
- `home_effect`: Effect when the bird is in the nest (non-combat)
- `belong_talent`: Which talent group the entry belongs to
- `conflict_entry`: Array of entries that cannot coexist with this one

---

## E. Leveling System

**Config:** ConfigFly_level (line 233409)

| Field | Description |
|-------|-------------|
| id | Avian type ID |
| level | Level number |
| expend | Currency cost to level |
| if_advance | Whether advance is required at this level (gate) |
| attr | Attribute bonuses at this level |
| power | Combat power |

Leveling provides direct attribute bonuses. At certain levels, an advance gate (`if_advance != 0`) requires the player to advance the avian before further leveling.

---

## F. Advance System

**Config:** ConfigFly_advance (line 232812)

| Field | Description |
|-------|-------------|
| id | Avian type ID |
| advance_level | Advance tier |
| expend | Material cost array |
| attr | Attribute bonuses at this advance |
| fly_skill | Skills unlocked at this advance |
| entry_level | Maximum entry level allowed |
| power | Combat power |

Advancing provides attributes, unlocks skills, and raises the cap on entry levels.

---

## G. Hatching System

**Config:** ConfigFly_egg (line 232928)

- Eggs have a quality level
- `fly_weight`: Weighted probability array determining which avian hatches
- `entry_num_weight`: Weighted probability array determining how many entries the bird is born with
- Higher quality eggs have better weights for rarer avians and more entries

---

## H. Breeding / Hybridization System

**Config:** ConfigFly_hybrid (line 233357)

| Field | Description |
|-------|-------------|
| id1 | First parent avian ID |
| id2 | Second parent avian ID |
| template_id | Hybrid template (ConfigFly_hybird_template) |
| fly_weight | Weight array for offspring possibilities |

Two avians are combined as parents. The `template_id` references a breeding template, and `fly_weight` determines the probability distribution of offspring species.

---

## I. Entry System

**Config:** ConfigFly_entry (line 233089)

Entries are sub-stats or passive abilities attached to individual avians. Each entry has:

- Multiple quality tiers
- Leveling through ConfigFly_entry levels
- Passive skills and special effects
- Talent group assignment (`belong_talent`)
- Conflict rules (`conflict_entry`) preventing incompatible combinations
- Entry rerolling via ConfigFly_remake_cost

The maximum entry level is gated by the avian's advance level (ConfigFly_advance.entry_level).
