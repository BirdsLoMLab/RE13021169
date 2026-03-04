# 08 — Talents

> 6 final talents + 7 leveled talent systems across all progression paths.

---

## Talent System Overview

The game has multiple distinct talent systems across different companion/equipment systems. "Talents" in the index refers to the collective set of progression trees that grant combat-relevant stats and skills.

---

## 6 Final Talent References (Class-Specific)

These are the T5 class passive skill progressions — the "final" talents that define each class's identity. Each has 5 unlock tiers.

| # | Class | Key Talent | Combat Impact |
|---|-------|-----------|---------------|
| 1 | Martial Sage | HP Regen + Shield | Sustain tank: 8% HP/5s regen + 8% HP shield |
| 2 | Warbringer | Counter Scaling + HP-Loss ATK | Counter DPS: +140% counter DMG + ATK scales with HP loss |
| 3 | Sacred Hunter | Crit Burst + HP% Damage | Burst: +20% crit DMG + 1% target HP per hit + 40% ATK after crit |
| 4 | Plume Monarch | Extra Bullets | Multi-hit: +3 combo bullets + 2 basic bullets |
| 5 | Prophet | Skill Spam | Utility: +20% energy regen + 40% skill duration + stun → CD reduction |
| 6 | Darklord | Skill Crit + True DMG | Glass cannon: +50% skill crit + 20% true damage + skill DMG scales HP loss |

See `04_CLASSES.md` for complete passive skill details with ownEffect arrays.

---

## 7 Leveled Talent Systems

### 1. Back/Wing Talent Tree (Primary Talent System)

**Config:** ConfigBack_talent (line 220891)
**Entries:** 2,652 total across all class types

| Field | Description |
|-------|-------------|
| id | Talent node ID |
| level | Talent level |
| name | Localized name |
| icon | Icon asset |
| job_type | Class restriction |
| color_type | Rarity indicator |
| describe | Description |
| cost | Upgrade cost array |
| connect_id | Prerequisite node(s) — tree structure |
| condition_1 | First unlock condition |
| condition_2 | Second unlock condition |
| attr | Attribute bonuses `[[attrId, value], ...]` |
| skill | Skill granted at this level |
| power | Combat power |

**Features:**
- 15 fields — most complex talent system
- Prerequisite chains via `connect_id`
- Class-specific nodes via `job_type`
- Dual conditions for unlock
- Progressive skills at each talent level
- Attribute bonuses scale with level

---

### 2. Pet Talent System

**Config:** ConfigPet_talent (line 252111), keyed by [id, all_star]

| Field | Description |
|-------|-------------|
| id | Talent ID |
| all_star | Total star level threshold |
| name | Talent name |
| effect_des | Effect description |
| effect | Stat bonus array |
| power | Power bonus |

- Unlocks at cumulative star thresholds
- Per-pet talent slots defined in ConfigPet's `talent` field
- Each slot: `[talent_group, talent_tier]`

---

### 3. Mount Ability Branches

**Config:** ConfigMount_ability (line 247718), keyed by [id, level]

| Field | Description |
|-------|-------------|
| id | Branch (1, 2, or 3) |
| level | Branch level |
| value_plus | Attribute bonus `[[attrId, value], ...]` |
| power | Combat power |

- 3 independent branches per mount
- Random branch gains +1 on success
- Success rate decreases with total level
- Currency: Item 1025
- Display: values shown as `value / 100`%

---

### 4. Angel Star Progression

**Config:** ConfigAngel_star (line 218461), keyed by [id, star]

| Field | Description |
|-------|-------------|
| id | Angel ID |
| star | Star level |
| attr | Stat bonuses `[[attrId, value], ...]` |
| battle_skill1/2 | Combat skills at this star |
| develop_effect | Development passive |
| power | Combat power |

- 16 fields per entry
- Skill unlocks and upgrades at higher stars
- Development effects provide passive bonuses

---

### 5. Avian Entry Progression

**Config:** ConfigFly_entry (line 233089), keyed by [id, level]

- Entries are sub-stats/affixes on avians
- Each has passive_skill and special_effect arrays
- Max level gated by avian advance level
- Conflict rules prevent incompatible combinations

See `07_AVIANS.md` for full details.

---

### 6. Ring Level Progression

**Config:** ConfigRing_level, keyed by level

- Attribute bonuses per level
- base_skill unlocks at certain levels
- EXP + material costs

See `18_RINGS_AND_BADGES.md` for full details.

---

### 7. Artifact Skin Progression

**Config:** ConfigArtifact_skin, keyed by [artifact_id, skin_level]

- Attribute bonuses per skin level
- skin_skill unlocks at certain levels
- Material costs to upgrade

See `12_ARTIFACT_SKINS_AND_GEMS.md` for full details.
