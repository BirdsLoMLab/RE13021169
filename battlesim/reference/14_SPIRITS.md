# 14 — Spirits (Guardian Spirits)

> 20 spirits, spirit damage formula, affix system, crafting, gacha, and spirit-vs-spirit combat.

---

## Overview

Guardian Spirits are summoned combat entities with their own HP, ATK, skills, and a unique damage formula (`spiritNormalHit`). They scale from their level config and partially from the parent player's damage output.

---

## Config Tables

| Table | Source Line | Main Key | Fields | Description |
|-------|-----------|----------|--------|-------------|
| ConfigSpirit | 262760 | spirit_id | 14 | Base definitions (quality, model, bullet type) |
| ConfigSpirit_level | 262673 | spirit_id + spirit_level | 10 | Per-level stats, skills, att_dam ratios, slot_amount |
| ConfigSpirit_affix_group | 262266 | affix_group | 4 | Affix category groups |
| ConfigSpirit_attrbonus_affix | 262317 | affix_id | varies | Individual affix definitions |
| ConfigSpirit_attrbonus_slot | 262379 | slot_id | varies | Slot-to-affix-group mapping |
| ConfigSpirit_craft | 262467 | id | varies | Crafting recipes |
| ConfigSpirit_craft_target | 262420 | spirit_level | varies | Level-gated crafting targets |
| ConfigSpirit_draw | 262583 | id | varies | Gacha/draw banners |
| ConfigSpirit_draw_prob | — | — | varies | Draw probability tables |

**No XOR encoding** — all Spirit config tables have `usesConfigKey: false`. Spirit units are backed by ConfigUnit entries (77 XOR-protected fields, key `24455`).

---

## All 20 Spirits

| ID | Name | Quality | Base ATK (6005) | Base HP (6004) |
|----|------|---------|----------------|----------------|
| 101 | Brawl Hound | 1 | 300 | 15,000 |
| 102 | Magic Kitten | 1 | 800 | 12,000 |
| 103 | Hunter Hare | 1 | 1,600 | 8,000 |
| 104 | Deer Spirit | 1 | 500 | 10,000 |
| 201 | Minotaur | 2 | 360 | 18,000 |
| 202 | Occult Mentor | 2 | 960 | 14,400 |
| 203 | Fate Hunter | 2 | 1,920 | 9,600 |
| 204 | Commander | 2 | 600 | 12,000 |
| 301 | Combat Expert | 3 | 420 | 21,000 |
| 302 | Curse Priest | 3 | 1,120 | 16,800 |
| 303 | Bounty Hunter | 3 | 2,240 | 11,200 |
| 304 | Beast Master | 3 | 700 | 14,000 |
| 401 | Mech Master | 4 | 480 | 24,000 |
| 402 | Crazy Raider | 4 | 1,280 | 19,200 |
| 403 | Domain Hunter | 4 | 2,560 | 12,800 |
| 404 | Death Reaper | 4 | 800 | 16,000 |
| 501 | Flame Spirit | 5 | 540 | 27,000 |
| 502 | Tide Spirit | 5 | 1,440 | 21,600 |
| 503 | Zephyr Spirit | 5 | 2,880 | 14,400 |
| 504 | Litho Spirit | 5 | 900 | 18,000 |

---

## Spirit Stat Formulas

```
Spirit HP  = base_hp + round(spirit_hp * (1 + spirit_hp_add))
Spirit ATK = base_att + round(spirit_att * (1 + spirit_att_add))
```
- `base_hp`, `base_att` from ConfigUnit (spirit's `unit` field; **77 fields XOR-protected** with key `24455`)
- `spirit_hp` (6004), `spirit_att` (6005) from ConfigSpirit_level.spirit_attr
- `spirit_hp_add` (6006), `spirit_att_add` (6007) percentage multipliers

### Unit Creation in Battle (Lines 193065-193094)

```javascript
// Base attributes from unit config
for (var M of configAttribute.getDataByList("module", 1)) {
    var V = new Attrib(M);
    V.baseValue = unitConfig[M.key];
    spirit.attribs[M.id] = V;
}

// Apply spirit_attr from ConfigSpirit_level
var levelData = configSpirit_level.getDataByKeys("spirit_id", id, "spirit_level", level);
if (levelData && levelData.spirit_attr)
    for (var attr of levelData.spirit_attr)
        spirit.attribs[attr[0]].baseValue = attr[1];  // [attr_id, value]

// Inherit specified attributes from parent player
if (this._attribs && this._attribs.length > 0)
    for (var attrId of this._attribs)
        spirit.attribs[attrId].setAttribValue(parent.data.getAttribMeta(attrId));

// HP = base_hp + round(spirit_hp * (1 + spirit_hp_add))
hp.baseValue = hp.baseValue + round(spirit_hp * (1 + spirit_hp_add));
// ATK = base_att + round(spirit_att * (1 + spirit_att_add))
att.baseValue = att.baseValue + round(spirit_att * (1 + spirit_att_add));

// Load primary skills from ConfigSpirit_level.skill1
for (var skill of levelData.skill1) {
    var s = newSkill(skill[0], skill[1], spirit);  // [skill_id, skill_lv]
    spirit.skillList.push(s);
}
```

---

## Spirit Damage — spiritNormalHit (Lines 322981-323007)

### Spirit vs Spirit
```
damage = round(ATT * (spirit_dam_add - spirit_dam_def + 1) * (1 - spirit_dam_def_final))
```
| Variable | ID | Description |
|----------|------|-------------|
| ATT | spirit's att | Spirit's own ATK |
| spirit_dam_add | 6001 | Spirit damage bonus |
| spirit_dam_def | 6002 | Target's spirit defense |
| spirit_dam_def_final | 6003 | Target's final spirit resist (0-1) |

### Spirit vs Normal Target
```
h = normalHurt(parent, target, noCrit) * att_dam[1] / 10000
M = normalDoubleHurt(parent, target, noCrit) * att_dam[2] / 10000
I = normalCounterHurt(parent, target, noCrit) * att_dam[3] / 10000
x = skillDamageHurt(parent, target, noCrit) * att_dam[4] / 10000
damage = round(h + M + I + x)
```

Uses PARENT player's damage calculations, scaled by spirit's `att_dam` ratios.

### Spirit Damage Weights (att_dam)

| Key | Type | Typical Weight |
|-----|------|---------------|
| 1 | Normal ATK | 5,000-16,000 |
| 2 | Combo | 5,000-16,000 |
| 3 | Counter | **25,000-80,000** (always highest) |
| 4 | Skill | 5,000-16,000 |

**Key insight:** Spirits always weight counter damage 5x higher, making counter-focused classes (Warbringer, Martial Sage) have the strongest spirits.

---

## Affix / Bonus Slot System

Spirits have affix slots for bonus attributes, scaling with level.

### How It Works
1. `ConfigSpirit_level.slot_amount` — slots available at this level
2. `ConfigSpirit_attrbonus_slot` — maps slot_id -> affix_group
3. `ConfigSpirit_affix_group` — affix categories (name, icon)
4. `ConfigSpirit_attrbonus_affix` — individual affixes

### Affix Fields
| Field | Description |
|-------|-------------|
| affix_id | Unique ID |
| affix_group | Category membership |
| quality | Rarity tier |
| attr_id | Attribute modified |
| value | Value range array |
| power_rate | Power contribution |

### Example Flow
```
Spirit Level 5 -> slot_amount = 3
Slot 1 -> affix_group 1 (e.g., "Offensive")
Slot 2 -> affix_group 2 (e.g., "Defensive")
Slot 3 -> affix_group 1 (e.g., "Offensive")

Each slot rolls an affix from its group:
Affix 101 -> attr_id: att, value: [500, 1000], quality: 3
```

### Stats
- 4 affix groups
- 22 affix slots available
- 168 possible affixes
- Common affixes: Global ATK % (2002), Crit Rate (1004)

---

## Spirit Key Attributes

| Attribute | ID | Description |
|-----------|------|-------------|
| spirit_dam_add | 6001 | Spirit damage bonus |
| spirit_dam_def | 6002 | Spirit damage resistance |
| spirit_dam_def_final | 6003 | Final spirit resist (%) |
| spirit_hp | 6004 | Spirit HP bonus |
| spirit_att | 6005 | Spirit ATK bonus |
| spirit_hp_add | 6006 | Spirit HP % multiplier |
| spirit_att_add | 6007 | Spirit ATK % multiplier |
| spirit_att_dam | — | Spirit attack damage attribute (line 244227, 267643) |

---

## Crafting System (ConfigSpirit_craft, Line 262467)

- Spirits can be crafted from materials
- `craft_type` determines the crafting method
- `spirit_target_id` lists possible output spirits
- Materials divided into `main_craft_material` and `minor_craft_material`
- `ConfigSpirit_craft_target` gates available targets by spirit level and provides `spirit_group` arrays

---

## Gacha / Draw System (ConfigSpirit_draw, Line 262583)

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

## Battle Loading

### Server Data (Lines 187576-187578)
Spirit stored as `[spirit_id, spirit_level]` tuple on the player list.

```javascript
// Extracted from player ext data during PvP loading (lines 187409-187413)
case 12: h[0] = Number(e);  // spirit_id
case 13: h[1] = Number(e);  // spirit_level
this.setPlayerSpirit(player, h);
```

### Client Local (Lines 199122-199124)
```javascript
e.setPlayerSpirit = function(e) {
    var t = GuardianSpiritDataCache.getCurSpirit();
    if (t) e.spirit = [t.config_id, t.level];
}
```

**Note:** Unlike pets and avians, the spirit is NOT added as a unit in `setPlayerSpirit`. The spirit unit is created later during battle initialization by the skill/buff system (via `call_spirit` buff action).

### Battle Update (Line 201874)
Spirit data refreshed via `SpiritUpdate` flag.
