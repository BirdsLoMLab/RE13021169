# 16 — Fate Cards

> Attribute bonuses, mutual exclusivity, fusion passive skills, and the gacha system.

---

## ConfigFate (7 fields)

| Field | Description |
|-------|-------------|
| fate_id | Unique identifier |
| name | Localized name |
| quality | Rarity tier |
| mutually_exclusive | IDs that cannot coexist with this fate |
| icon | Icon asset |
| effect | Visual effect |
| preview | Preview data |

### Mutual Exclusivity
Fates in `mutually_exclusive` array cannot be equipped simultaneously — creates strategic deck-building choices.

---

## Leveling (ConfigFate_level, 7 fields)

| Field | Description |
|-------|-------------|
| fate_id | FK to ConfigFate |
| level | Current level |
| expend | Upgrade cost `[[itemId, count], ...]` |
| attr | Attribute bonuses `[[attrId, value], ...]` |
| skill | Skills at this level |
| breakdown_reward | Salvage rewards |
| power | Combat power |

### Combat Contribution
- `attr` entries use AttribDefine IDs (1001=ATK, 1002=HP, 1024=DEF, etc.)
- Values are additive bonuses during stat assembly
- Higher levels → higher values → more power

---

## Fusion (ConfigFate_fusion, 6 fields)

| Field | Description |
|-------|-------------|
| id | Recipe ID |
| get_fate_id | Result fate ID |
| material_fate_id | Required material fates |
| passive_skill_group | Passive skills granted |
| desc | Description |
| same_kind | Substitution rules |

### Fusion → Passive Skills
Fusing specific combinations unlocks **passive skill groups** applied via the standard passive skill system. `passive_skill_group` contains skill IDs available after fusion.

---

## Gacha (ConfigFate_draw, 5 fields)

| Field | Description |
|-------|-------------|
| id | Pool entry ID |
| type | Pool type |
| reward | Reward items `[[itemId, count], ...]` |
| weights | Probability weight |
| is_guaranteed | Pity flag (0/1) |

Weighted random selection with pity system for guaranteed rare drops.

---

## Fate Chapters (ConfigFate_chapter, 14 fields)

Dungeon mode for farming fate materials:
- Power requirements and level gates
- Monster waves with timed intervals
- First-clear and daily rewards
- Difficulty adjustment scaling
- Boss encounters

---

## Combat Relevance

Fates affect combat through:
1. **Attribute Bonuses** — Direct stat increases from ConfigFate_level.attr
2. **Passive Skills** — Fusion effects that trigger via EffectTriggerType events

The system is **purely additive** — no new combat mechanics, only attribute modification and passive effects.
