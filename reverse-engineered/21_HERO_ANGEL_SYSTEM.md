# 21 -- Hero / Angel (Guardian Spirit) System

> **MERGED**: This content has been consolidated into `battlesim/reference/15_ANGELS.md` which now contains the complete Angel/Star Heroes system reference including formation mechanics, config table schemas (with field indices and types), skill system, gacha, code locations, and all 33 Star Hero details.

See `battlesim/reference/15_ANGELS.md` for the unified reference.

## Overview (archived)

Angels (internally "Guardian Spirits") are companion units that boost player stats, contribute battle skills, and provide passive development effects. They are organized into a typed formation, star-upgraded for power growth, and acquired through a gacha draw system.

## Code Locations

| Module | Lines | Purpose |
|--------|-------|---------|
| ConfigAngel.ts | 218577 | Base angel definitions |
| ConfigAngel_star.ts | 218461 | Per-star-level data (skills, stats, costs) |
| ConfigAngel_skill.ts | 218397 | Angel-specific skill definitions (slot 2) |
| ConfigAngel_develop.ts | 218064 | Development effect macro mappings |
| ConfigAngel_array.ts | 218018 | Formation slot layout |
| ConfigAngel_draw.ts | 218306 | Permanent gacha banners |
| ConfigAngel_draw_time_limit.ts | 218177 | Limited-time gacha banners |
| ConfigAngel_draw_package.ts | 218110 | Draw milestone rewards |
| GuardianSpiritBattleView.ts | ~305100 | Battle UI rendering for angels |

## Data Architecture

### ConfigAngel (9 fields)
```
id            -- Unique angel identifier
name          -- Localized name (string_ref)
quality       -- Rarity tier (1-5)
type          -- Type class; controls which formation slots accept this angel
desc          -- Description (string_ref)
image         -- Primary portrait asset
image2        -- Secondary portrait asset
image3        -- Icon asset (used in skill display UI)
open_time     -- [optional] Time-gated availability window
```

### ConfigAngel_star (16 fields, keyed by [id, star])
```
id                -- Angel ID (FK -> ConfigAngel)
star              -- Star level (1, 2, 3, ...)
expend            -- Upgrade cost items [[itemId, count], ...]
frame             -- UI frame asset for this star level
attr              -- Stat bonuses [[attrId, value], ...]
skill1_type       -- Skill slot 1 category (1=active, 2=passive, 3=aura)
battle_skill1     -- Skill slot 1: [[skillId, skillLevel]] -> ConfigSkill_level
battle_skill1_cost -- Energy cost for skill 1
skill2_type       -- Skill slot 2 category
battle_skill2     -- Skill slot 2 ID -> ConfigAngel_skill
battle_skill2_cost -- Energy cost for skill 2
develop_effect    -- Development passive effect data
develop_desc      -- Development description template
develop_desc_num  -- Parameters for develop_desc formatting
develop_cost      -- Energy cost for the development slot
power             -- Combat power contribution
```

### ConfigAngel_skill (6 fields)
```
id            -- Skill ID
skill_name    -- Localized name
skill_effect  -- Effect IDs triggered
skillPar      -- Skill parameters (damage coefficients)
skill_dec     -- Description template
desc_parm     -- Description format parameters
```

## Formation System

Angels are placed into a formation defined by `ConfigAngel_array`:

```
type     -- Formation type
pos      -- Slot position (1-based)
pos_type -- Angel type allowed in this slot
```

The battle UI (line ~305100) shows two formation groups:

- **Main Slots (1-3):** These angels contribute battle skills directly.
  - Slot 1 is the primary slot with the skill 1 display.
  - Slots 2-3 use skill 2 from `ConfigAngel_skill`.
- **Development Slots (1-4):** These angels provide passive development bonuses.

### Formation Cost Budget

All angel skills share a single energy pool. The UI displays total cost:

```javascript
// Line ~305140
// Main formation cost
this.all_cost1 = sum of battle_skill1_cost + battle_skill2_cost for main slots
// Development formation cost
this.all_cost2 = sum of develop_cost for development slots
// Display
this.cost_label.string = cost + "/" + maxBudget
```

## Star Upgrade Mechanics

Each angel has per-star data in `ConfigAngel_star`. Upgrading requires:

1. **Materials:** Defined in `expend` field as `[[itemId, count], ...]`
2. **Stat Growth:** `attr` provides attribute bonuses per star (e.g., `[[attrId, value]]`)
3. **Skill Unlocks:** Higher stars may unlock or upgrade `battle_skill1` and `battle_skill2`
4. **Development Effect:** `develop_effect` becomes available at certain star levels

### Skill Slot Details

**Slot 1** (battle_skill1):
- References the standard `ConfigSkill` + `ConfigSkill_level` system
- Looked up as: `configSkill_level.getDataByKeys("id", skillId, "level", skillLevel)`
- `skill1_type` determines the visual category badge (1/2/3 mapped to type_desc1/2/3)

**Slot 2** (battle_skill2):
- References `ConfigAngel_skill` directly
- Looked up as: `configAngel_skill.getDataByKey(battle_skill2)`
- Description rendered as: `formatStr(skill_dec, ...desc_parm)`

```javascript
// Line ~305509: Skill 2 lookup
var r = configAngel_skill.getDataByKey(s.battle_skill2);
r ? this.skill_list[2].desc.string = formatStr(r.skill_dec, ...r.desc_parm)
  : this.skill_list[2].desc.string = "";
this.skill_list[2].cost.string = "cost " + d;
```

## Gacha / Draw System

### Permanent Banners (ConfigAngel_draw, 11 fields)
```
id       -- Banner ID
name     -- Display name
type     -- Banner type
banner   -- Banner image asset
normal   -- Normal pool ID
must     -- Pity thresholds [pullCount, ...]
cost     -- Single pull cost [[currencyId, amount]]
cost2    -- Multi-pull cost
prob     -- Probability weights per quality tier
decs     -- Description
```

### Limited-Time Banners (ConfigAngel_draw_time_limit, 18 fields)

Adds rate-up mechanics:

```
is_up               -- Whether rate-up is active (0/1)
prob_up              -- Rate-up probability weights (override base prob)
up_reward            -- Featured angel rewards
special_rewards_times -- Pull count to trigger special reward
special_rewards_pro   -- Special reward probability
special_rewards       -- Special reward items
```

### Milestone Rewards (ConfigAngel_draw_package, 7 fields)

```
premise   -- Pull count threshold
reward    -- Reward items [[itemId, count], ...]
```

## Battle Integration

In battle, angels contribute through their skills:

1. **Skill 1** enters the standard skill execution pipeline (see `22_SKILL_EFFECT_SYSTEM.md`)
2. **Skill 2** triggers via `ConfigAngel_skill.skill_effect` chain
3. **Development effects** apply as passive modifiers

The stat bonuses from `ConfigAngel_star.attr` are added to the player's combat attributes, affecting all damage calculations documented in `01_BASIC_DAMAGE_CALCULATION.md`.

## Dependencies

- `ConfigSkill` / `ConfigSkill_level` -- Skill slot 1 references
- `ConfigSkilleffcet` -- Skill effect chain execution
- `ConfigBuff` -- Buffs applied by angel skills
- `AttribDefine` -- Attribute IDs for stat bonuses
