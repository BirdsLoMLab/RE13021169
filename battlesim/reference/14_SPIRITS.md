# 14 — Spirits

> 20 spirits, spirit damage formula, affix system, and spirit-vs-spirit combat.

---

## Overview

Guardian Spirits are summoned combat entities with their own HP, ATK, skills, and a unique damage formula (`spiritNormalHit`). They scale from their level config and partially from the parent player's damage output.

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
- `base_hp`, `base_att` from unit config
- `spirit_hp` (6004), `spirit_att` (6005) from ConfigSpirit_level.spirit_attr
- `spirit_hp_add` (6006), `spirit_att_add` (6007) percentage multipliers

---

## Spirit Damage — spiritNormalHit

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

**Key insight:** Spirits always weight counter damage 5× higher, making counter-focused classes (Warbringer, Martial Sage) have the strongest spirits.

---

## Affix / Bonus Slot System

Spirits have affix slots for bonus attributes, scaling with level.

### How It Works
1. `ConfigSpirit_level.slot_amount` — slots available at this level
2. `ConfigSpirit_attrbonus_slot` — maps slot_id → affix_group
3. `ConfigSpirit_affix_group` — affix categories (name, icon)
4. `ConfigSpirit_attrbonus_affix` — individual affixes

### Affix Fields
| Field | Description |
|-------|-------------|
| affix_id | Unique ID |
| affix_group | Category membership |
| quality | Rarity tier |
| attr_id | Attribute modified |
| value | Value range |
| power_rate | Power contribution |

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

---

## Battle Loading

Spirit stored as `[spirit_id, spirit_level]` tuple on the player list (not added as unit during setPlayerSpirit). The spirit unit is created later during battle initialization by the skill/buff system.

### Battle Update
Spirit data refreshed via `SpiritUpdate` flag.
