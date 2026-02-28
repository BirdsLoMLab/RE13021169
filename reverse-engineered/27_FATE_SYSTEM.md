# 27 — Fate System

## Overview

The Fate system provides collectible fate cards that grant **attribute bonuses and passive skills**. Fates have quality tiers, can be leveled up, fused together, and drawn from gacha pools. They plug into the stat assembly pipeline via their `attr` arrays.

---

## Config Tables

| Table | Source Line | Main Key | Fields | Description |
|-------|-----------|----------|--------|-------------|
| ConfigFate | 231972 | fate_id | 7 | Base fate definitions (name, quality, mutually_exclusive, icon, effect, preview) |
| ConfigFate_level | 231902 | fate_id + level | 7 | Per-level scaling: upgrade costs, attribute bonuses, skill unlocks, power |
| ConfigFate_chapter | 231675 | id + index | 14 | Fate dungeon chapters: power req, monster spawns, rewards, time limits |
| ConfigFate_draw | 231781 | id | 5 | Gacha draw pool: type, reward, weighted probability, guaranteed flag |
| ConfigFate_fusion | 231838 | id | 6 | Fusion recipes: material fates → result fate, passive skill groups |

---

## A. Fate Card Definition (ConfigFate)

| Field | Type | Description |
|-------|------|-------------|
| fate_id | number | Unique fate identifier |
| name | string_ref | Localized fate name |
| quality | number | Rarity tier (indexed for filtering by quality) |
| mutually_exclusive | array? | List of fate IDs that cannot coexist with this fate |
| icon | number | Icon asset ID |
| effect | number | Visual effect asset ID |
| preview | array? | Preview display data |

### Mutual Exclusivity
Fates in the `mutually_exclusive` array cannot be equipped simultaneously. This creates strategic deck-building choices.

---

## B. Leveling System (ConfigFate_level)

| Field | Type | Description |
|-------|------|-------------|
| fate_id | number | FK to ConfigFate |
| level | number | Current level |
| expend | array? | Upgrade cost: `[[itemId, count], ...]` |
| attr | array? | Attribute bonuses at this level: `[[attrId, value], ...]` |
| skill | array? | Skills unlocked/enhanced at this level |
| breakdown_reward | array? | Rewards for breaking down this fate at this level |
| power | number | Combat power contribution |

### How Fate Attributes Feed Combat
Fate `attr` values are added to the player's MetaAttrib during stat assembly:
- `attr` entries reference AttribDefine IDs (1001=att, 1002=hp, 1024=def, etc.)
- Values are additive bonuses applied during the attribute initialization phase
- Higher fate levels → higher attribute values → more combat power

---

## C. Gacha System (ConfigFate_draw)

| Field | Type | Description |
|-------|------|-------------|
| id | number | Draw pool entry ID |
| type | number | Pool type classification |
| reward | array? | Reward items/fates: `[[itemId, count], ...]` |
| weights | number | Weighted probability (higher = more common) |
| is_guaranteed | number | Whether this entry is part of pity/guaranteed system (0=no, 1=yes) |

The gacha uses weighted random selection. `is_guaranteed` entries are forced after a certain number of draws without a rare result (pity system).

---

## D. Fusion System (ConfigFate_fusion)

| Field | Type | Description |
|-------|------|-------------|
| id | number | Fusion recipe ID |
| get_fate_id | number | Resulting fate ID |
| material_fate_id | array? | Required material fate IDs |
| passive_skill_group | array? | Passive skill groups granted by the fused fate |
| desc | string_ref | Fusion description text |
| same_kind | array? | Same-kind grouping for substitution |

### Fusion → Passive Skills
Fusing specific combinations of fates unlocks **passive skill groups** that are applied via the standard passive skill system (see `21_HERO_ANGEL_SYSTEM.md`). The `passive_skill_group` array contains skill IDs that become available after fusion.

---

## E. Fate Chapters (ConfigFate_chapter)

| Field | Type | Description |
|-------|------|-------------|
| id | number | Chapter ID |
| index | number | Chapter index within series |
| power | number | Recommended combat power |
| level | number | Required player level |
| map | number | Map/scene ID |
| part_type | number | Chapter part classification |
| interval | array? | Wave timing intervals |
| monster_refresh1 | array? | Monster spawn configuration |
| time | number | Base time limit |
| first_reward | array? | First-clear bonus rewards |
| daily_reward | array? | Daily completion rewards |
| difficulty_adjust | array? | Difficulty scaling parameters |
| bossModel | number | Boss model/unit ID |
| time_limit | number | Hard time limit (seconds) |

---

## F. Combat Relevance

Fates affect combat through two mechanisms:

1. **Attribute Bonuses** — Direct stat increases (ATK, HP, DEF, crit_rate, etc.) from `ConfigFate_level.attr`
2. **Passive Skills** — Skill effects from fusion that trigger during battle via EffectTriggerType events

The Fate system is **purely additive** to the stat assembly pipeline — it does not introduce new combat mechanics, only modifies existing attributes and adds passive effects.
