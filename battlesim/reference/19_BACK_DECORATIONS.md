# 19 — Back Decorations (Wings)

> Back talent trees with attrs/skills per class, skin system, and level progression.

---

## Overview

Back decorations (wings/accessories) provide stats through three channels:
1. **Level progression** — ATK/HP/DEF scaling to 260
2. **Skin system** — per-decoration skins with skills
3. **Talent tree** — class-specific talent nodes (2,652 entries)

---

## ConfigBack_decoration (12 fields)

| Field | Description |
|-------|-------------|
| id | Decoration ID |
| name | Display name |
| form | Shape type |
| type | Category |
| path | Model asset |
| binds | Bind points |
| quality | Rarity (mostly 7=Red, starters 4=Purple) |
| sort | Sort order |
| back_location_adjust | Position offset |
| if_activity | Activity-gated |
| position | Position |
| scale | Model scale |

### Notable Decorations
| ID | Name |
|----|------|
| 70001-70003 | Raccoon/Wolf/Fox Tail (Starter, quality 4) |
| 70004 | Lustrous Plumage |
| 70020 | Fallen Angel |
| 70025 | Celestial Gemini |
| 70405 | Dawn Warwing |
| 70907 | Lord of Light |
| 70999 | Frostland Specter |

---

## Level Progression (ConfigBack_level, 260 levels)

### Schema (keyed by [id, level])
| Field | Description |
|-------|-------------|
| id | Back decoration type |
| level | Level number |
| expend_exp | EXP cost |
| expend_goods | Material cost |
| attr | Attribute bonuses |
| power | Combat power |
| era_level | Era/epoch requirement |
| icon_show | Display flag |

### Max Stats at Level 260

| Attribute | Max Value | Power |
|-----------|-----------|-------|
| Base ATK (1001) | 52,919,000 | 20,103,333 |
| Base HP (1002) | 52,919,000 | 20,103,333 |
| Base DEF (1003) | 52,919,000 | 20,103,333 |

`era_level` gates certain levels behind account progression.

---

## Skin System (ConfigBack_skin)

### Schema (keyed by [back_id, skin_level])
| Field | Description |
|-------|-------------|
| back_id | Decoration ID |
| skin_level | Upgrade level |
| expend | Upgrade cost |
| skin_skill | Skills granted `[[skillId, level], ...]` |
| attr | Attribute bonuses |
| power | Combat power |

**495 total skin entries** across 48 decorations.

If current skin level has no skills, system looks ahead to next level for preview.

---

## Talent Tree (ConfigBack_talent)

The most complex talent system — 2,652 entries across all class types.

### Schema (15 fields, keyed by [id, level])
| Field | Description |
|-------|-------------|
| id | Talent node ID |
| level | Talent level |
| name | Localized name |
| icon | Icon asset |
| job_type | Class restriction |
| color_type | Rarity indicator |
| describe | Description |
| cost | Upgrade cost |
| connect_id | Prerequisite node(s) |
| condition_1 | First unlock condition |
| condition_2 | Second unlock condition |
| attr | Attribute bonuses `[[attrId, value], ...]` |
| skill | Skill granted |
| power | Combat power |

### Features
- **Prerequisite chains** via `connect_id` — creates tree structure
- **Class-specific** via `job_type` — different talent paths per class
- **Dual conditions** — both condition_1 and condition_2 must be met
- **Progressive skills** — different skills at each talent level
- **Color-coded** nodes by `color_type` for rarity

---

## Combat Relevance

All three channels feed into the standard stat assembly:
- Level attrs → additive bonuses
- Skin attrs → additive bonuses + skill activation
- Talent attrs → additive bonuses + skill unlocks

The talent tree is class-specific, creating differentiated builds within each class.
