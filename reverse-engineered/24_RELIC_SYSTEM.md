# 24 -- Relic, Fate, Ring & Statue Systems

## Overview

Four collection-based progression systems that provide passive stat bonuses and combat effects:

- **Relics:** Equippable artifacts with equip and ownership bonuses
- **Fates:** Collectible cards with leveling, fusion, and gacha systems
- **Rings:** Leveled equipment that unlocks base skills
- **Statues:** Permanent stat investment with random attribute rolls

## Code Locations

| Module | Lines | Purpose |
|--------|-------|---------|
| ConfigRelic.ts | 254905 | Relic definitions (12 fields) |
| ConfigRelic_pos.ts | 254859 | Relic slot positions |
| ConfigRelic_get.ts | 254811 | Relic acquisition pools |
| ConfigFate.ts | 231972 | Fate card definitions |
| ConfigFate_level.ts | 231902 | Fate per-level scaling |
| ConfigFate_chapter.ts | 231675 | Fate dungeon chapters |
| ConfigFate_draw.ts | 231781 | Fate gacha pool |
| ConfigFate_fusion.ts | 231838 | Fate fusion recipes |
| ConfigRing.ts | 255436 | Ring definitions |
| ConfigRing_level.ts | 255367 | Ring level progression |
| ConfigStatue_attr.ts | 263229 | Statue attribute pools |
| ConfigStatue_level.ts | 263291 | Statue level costs |
| ConfigStatue_pos.ts | 263343 | Statue slot positions |
| ConfigStatue_spend.ts | 263389 | Statue lock/reroll costs |
| RelicBookView.ts | ~390980 | Relic UI and equip logic |

---

## Relic System

### ConfigRelic (12 fields, keyed by [id, level])
```
id           -- Relic ID
level        -- Relic level (1, 2, 3, ...)
name         -- Localized name
type         -- Relic type classification
desc         -- Description template
desc_parm    -- Description format parameters
icon         -- Icon asset
equip        -- Equip stat bonuses [[attrId, value], ...]
own          -- Ownership (passive) bonuses [[attrId, value], ...]
equip_effect -- Combat effects when equipped (skill/buff IDs)
cost         -- Level-up cost [[itemId, count], ...]
power        -- Combat power
```

### Relic Mechanics

**Dual Bonus System:**
- `equip` bonuses are active only when the relic is in an equipped slot
- `own` bonuses are passive and apply from mere ownership
- `equip_effect` provides combat effects (skills/buffs) when equipped

**Slot Positions** (`ConfigRelic_pos`):
```
id   -- Position slot ID
name -- Slot name
icon -- Slot icon asset
```

**Acquisition** (`ConfigRelic_get`):
```
num        -- Draw attempt number
relic_pool -- Available relic IDs to draw from
cost       -- Cost per attempt [[itemId, count], ...]
```

**Network Protocol:**
```
Client: relic.relic_equip_c2s
Server: relic.relic_equip_s2c
```

```javascript
// Line ~391131: Equip request
netManager.send("relic.relic_equip_c2s", {
    // equip parameters
});
```

### Relic Lookup Pattern
```javascript
// Line ~391083: Look up relic config
var config = configRelic.getDataByKeys("id", relicId, "level", 1);
// Line ~372360: Look up with player's relic level
var config = configRelic.getDataByKeys("id", relic.cfg_id, "level", relic.lv);
```

---

## Fate System

### ConfigFate (7 fields, keyed by [fate_id, quality])
```
fate_id            -- Unique fate ID
name               -- Fate name
quality            -- Quality/rarity tier
mutually_exclusive -- IDs of incompatible fates (cannot equip together)
icon               -- Icon asset
effect             -- Effect ID applied by this fate
preview            -- UI preview data
```

### ConfigFate_level (7 fields, keyed by [fate_id, level])
```
fate_id          -- Fate ID
level            -- Level
expend           -- Upgrade cost [[itemId, count], ...]
attr             -- Stat bonuses [[attrId, value], ...]
skill            -- Skills unlocked at this level
breakdown_reward -- Reward for breaking down at this level
power            -- Combat power
```

### Fate Fusion (ConfigFate_fusion, 6 fields)
```
id                  -- Recipe ID
get_fate_id         -- Resulting fate ID
material_fate_id    -- Required material fate IDs
passive_skill_group -- Passive skills transferred to result
desc                -- Fusion description
same_kind           -- Same-kind substitution rules
```

**Fusion Mechanics:**
- Multiple lower-quality fates combine into a higher-quality one
- `passive_skill_group` transfers from materials to the result
- `mutually_exclusive` on ConfigFate prevents equipping conflicting fates
- `same_kind` allows substituting specific fates with equivalent alternatives

### Fate Gacha (ConfigFate_draw, 5 fields)
```
id            -- Entry ID
type          -- Entry type
reward        -- Reward items
weights       -- Probability weight
is_guaranteed -- Pity/guaranteed entry flag (0/1)
```

### Fate Dungeons (ConfigFate_chapter, 14 fields)

Chapter-based dungeon mode for farming fate materials:
- `difficulty_adjust` provides dynamic scaling
- Separate `first_reward` and `daily_reward` tracks
- Boss encounters with `bossModel` and `time_limit`

---

## Ring System

### ConfigRing (7 fields)
```
id      -- Ring ID
name    -- Ring name
path1   -- Primary model asset
path2   -- Secondary model asset
icon1   -- Primary icon
icon2   -- Secondary icon
quality -- Quality tier
```

### ConfigRing_level (7 fields, keyed by level)
```
level       -- Ring level
expend_exp  -- EXP required
expend_goods -- Material cost [[itemId, count], ...]
attr        -- Stat bonuses [[attrId, value], ...]
base_skill  -- Base skills unlocked at this level
unlock      -- Content unlock flag
power       -- Combat power
```

**Ring Mechanics:**
- Rings level up by consuming EXP and materials
- Each level grants stat bonuses via `attr`
- `base_skill` unlocks combat skills at milestone levels
- Rings have dual visual representations (path1/path2, icon1/icon2)

---

## Statue System

### ConfigStatue_attr (6 fields)
```
id         -- Attribute entry ID
product    -- Statue/product type
attr_id    -- Attribute ID being boosted (AttribDefine)
pro        -- Probability weight for random rolls
value      -- Value range [base, increment]
power_rate -- Combat power conversion rate
```

### ConfigStatue_level (4 fields, keyed by level)
```
level       -- Statue level
expend      -- Currency cost per upgrade
pro_quality -- Quality tier probability thresholds
power       -- Combat power
```

### ConfigStatue_pos (3 fields)
```
id    -- Position/slot ID
level -- Required level to unlock this slot
desc  -- Slot description
```

### ConfigStatue_spend (2 fields)
```
lock_quantity -- Number of locked attributes
spend         -- Cost for reroll with this many locks [[itemId, count], ...]
```

**Statue Mechanics:**

The statue system uses a **random roll** mechanic:

1. Each upgrade costs currency defined by `ConfigStatue_level.expend`
2. The system rolls from `ConfigStatue_attr` pool using probability weights (`pro`)
3. Each roll produces a stat bonus based on `attr_id` and `value`
4. Players can **lock** desirable attributes to prevent them from being re-rolled
5. Locking attributes costs extra, scaled by `ConfigStatue_spend.spend` based on how many attributes are locked
6. `pro_quality` in `ConfigStatue_level` may affect the quality of rolls at higher statue levels

This is conceptually similar to artifact/gem systems in other games where you invest currency for random stat improvements.

---

## Dependencies

- `AttribDefine` -- Attribute IDs for all stat bonuses
- `ConfigSkill` -- Skills unlocked by fates and rings
- `ConfigBuff` -- Buffs applied by relic equip_effects
