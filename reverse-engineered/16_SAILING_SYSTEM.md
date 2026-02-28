# 23 -- Sailing / Season System

## Overview

The seasonal sailing system is a major gameplay system encompassing ships, ship equipment, treasures, cabins, port supplies, and naval PvP combat. Ships level up for stat growth, equip gear with random attributes, and engage in cannon-based naval battles.

## Code Locations

| Module | Lines | Purpose |
|--------|-------|---------|
| ConfigSeason_ship.ts | 259623 | Ship definitions |
| ConfigSeason_ship_level.ts | 259478 | Ship level progression |
| ConfigSeason_ship_draw.ts | 259347 | Ship gacha pool |
| ConfigSeason_equipment.ts | 257932 | Ship equipment definitions |
| ConfigSeason_equipment_attr.ts | 257626 | Equipment random attribute pools |
| ConfigSeason_pvp_chapter.ts | 258898 | Naval PvP chapters |
| ConfigSeason_treasure.ts | 260124 | Ship treasures |
| ConfigSeason_cabin.ts | 257348 | Ship cabin assignments |
| ConfigSeason_ship_appearance.ts | 259210 | Ship appearance/skin data |
| ConfigSeason_kv.ts | (varies) | Season key-value constants |

## Ship System

### ConfigSeason_ship (9 fields)
```
id             -- Ship ID
name           -- Localized name
quality        -- Rarity tier
path           -- Ship model asset
icon           -- Ship icon
appearance     -- Available skin IDs
item_id        -- Inventory item ID
default_unlock -- Unlocked by default (0/1)
open_time      -- Time-gated availability
```

### ConfigSeason_ship_level (6 fields, keyed by level)
```
level       -- Ship level
expend_exp  -- EXP required
expend_goods -- Material costs [[itemId, count], ...]
attr        -- Stat bonuses [[attrId, value], ...]
cost        -- Currency cost
power       -- Combat power
```

### Ship Stats Display

From season constants (line ~258259):
```
SEASON_SHIP_ATTR_SHOW: [10002, 10001, 10003, 10004]
  -> ATK (10002), HP (10001), SPD (10003), DEF (10004)

SEASON_SHIP_DURABILITY_RANGE: [2500, 10000]
  -> Ships have durability between 2500 and 10000

SEASON_SHIP_TREASURE_ITEM: [270012, 1]
  -> Treasure-related item ID
```

## Equipment System

### ConfigSeason_equipment (11 fields, keyed by [id, level, part])
```
id         -- Equipment ID
name       -- Equipment name
level      -- Tier level
part       -- Slot type (hull, sail, cannon, etc.)
quality    -- Rarity
number     -- Grouping number
advanced   -- Advanced upgrade tier
multiple   -- Set bonus multipliers
icon       -- Icon asset
atlas      -- Sprite sheet
gradeRange -- Attribute grade range [min, max]
```

### ConfigSeason_equipment_attr (6 fields)

Random attribute roll pool for equipment:
```
id       -- Entry ID
group_id -- Links to equipment type
attr_id  -- Attribute ID (AttribDefine)
type     -- Flat vs percentage
pro      -- Probability weight
value    -- Roll range [min, max]
```

Equipment attributes are randomly rolled from the pool. The `gradeRange` on the equipment defines quality bounds, and `pro` determines how likely each attribute is to be selected.

### Season 4 Variants

Season 4 introduced separate tables for updated progression:
- `ConfigSeason_equipment_level_s4`
- `ConfigSeason_equipment_attr_s4`
- `ConfigSeason_ship_level_s4`
- `ConfigSeason_treasure_level_s4`

## Treasure System

### ConfigSeason_treasure (13 fields, keyed by [id, level])
```
id          -- Treasure ID
level       -- Treasure level
name        -- Display name
type        -- Treasure type
icon        -- Icon asset
item_id     -- Inventory item ID
attr_type   -- Primary attribute type
own         -- Ownership stat bonuses
extra       -- Extra bonuses at this level
use         -- Active use effects
cost        -- Upgrade cost
power       -- Combat power
season_type -- Season restrictions
```

Treasures provide passive stat bonuses (`own`) that scale with level, plus potential active effects (`use`).

## Naval PvP

### ConfigSeason_pvp_chapter (12 fields, keyed by [id, index])
```
id                -- Chapter ID
index             -- Stage index
power             -- Recommended power
level             -- Enemy level
map               -- Battle map
part_type         -- Battle classification
part              -- Current wave
next_part         -- Next wave transition
ship_cannon_left  -- Left cannon config [[cannonId, ...]]
ship_cannon_right -- Right cannon config
time              -- Time limit
reward            -- Completion rewards
```

### Naval Combat Formula

From line ~203902, naval combat uses ship cannon attributes:

```javascript
// Ship combat setup
var att = FixMath.roundInt(ship.data.getAttribByInt(AttribDefine.att));
var speed = FixMath.roundInt(10000 * ship.data.getAttrib(AttribDefine.speed));
var attDam = ship.data.getAttrib(AttribDefine.att_dam);
var attResist = ship.data.getAttrib(AttribDefine.att_resist);
var cannonMultiplier = FixMath.round(attDam * (1 + attResist));

// Cannon fires with: base ATK * cannonMultiplier
```

The cannon damage resistance uses the `season_cannon_att_def` attribute (referenced in `01_BASIC_DAMAGE_CALCULATION.md` as the Gun branch).

## Ship Gacha

### ConfigSeason_ship_draw (7 fields, keyed by [id, quality])
```
id          -- Draw entry ID
reward      -- Reward items
weight      -- Probability weight
is_jackpot  -- Featured/jackpot flag (0/1)
limited     -- Max draw count (0=unlimited)
quality     -- Quality tier filter
fragment    -- Whether reward is a fragment (0/1)
```

Pity system is handled by `ConfigSeason_ship_draw_guaranteed`.

## Cabin System

### ConfigSeason_cabin (5 fields)
```
cabin_id          -- Cabin ID
condition         -- Unlock condition type
type              -- Cabin parameters
condition_special -- Special unlock requirements
condition_text    -- Display text for conditions
```

Cabins allow assigning crew members for additional bonuses.

## Additional Season Tables

| Table | Purpose |
|-------|---------|
| ConfigSeason_favor | Favor/relationship system |
| ConfigSeason_port_supply | Port supply trading |
| ConfigSeason_station_level | Station upgrade levels |
| ConfigSeason_workshop_level | Workshop crafting levels |
| ConfigSeason_building_function | Building function unlocks |
| ConfigSeason_recovery_speed | Resource recovery rates |
| ConfigSeason_achievement | Season achievements |
| ConfigSeason_rank_reward | Season ranking rewards |
| ConfigSeason_event | Season events |
| ConfigSeason_notice | Notification conditions |

## Dependencies

- `AttribDefine` -- Attribute IDs for ship stats
- `ConfigSkill` -- Ship skills and cannon effects
- `01_BASIC_DAMAGE_CALCULATION.md` -- Gun branch formula
- `HurtUtil.ts` -- Cannon damage calculation
