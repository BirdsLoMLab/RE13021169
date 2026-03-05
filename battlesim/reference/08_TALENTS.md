# 08 — Talents (Back/Wing Talent Trees)

> 120 talent nodes across 4 class paths, 3 tiers each. 2,652 total entries in `ConfigBack_talent`. 12 capstone "final talents" with unique combat skills (e.g., Ascension, Rampage, Gale Barrage).

---

## Overview

Talents are the progression trees tied to **back accessories** (wings/backs). Each class path has 3 independent talent tiers, each forming a branching tree of 10 nodes. Nodes grant attribute bonuses, and the capstone node at the end of each tier grants a unique combat skill — these are the **final talents**.

**Config:** `ConfigBack_talent` (line 220891), keyed by `[id, level]`, 15 fields per entry, 2,652 total entries.

**Class Paths:**
- **job_type 1** — Warrior (Martial Sage / Warbringer)
- **job_type 2** — Archer (Sacred Hunter / Plume Monarch)
- **job_type 3** — Mage (Prophet / Darklord)
- **job_type 4** — Beast (Beastmaster / Supreme Spirit)

---

## Schema — ConfigBack_talent (15 fields)

| # | Field | Type | Description |
|---|-------|------|-------------|
| 0 | `id` | number | Talent node ID (e.g., 1001–1030 for Warrior) |
| 1 | `level` | number | Node level (1–40 for stat nodes, 1 for capstones) |
| 2 | `name` | string_ref | Localized name (Language_en key) |
| 3 | `icon` | number | Icon asset ID |
| 4 | `job_type` | number | Class path (1=Warrior, 2=Archer, 3=Mage, 4=Beast) |
| 5 | `color_type` | number | Tier (1=Tier 1, 2=Tier 2, 3=Tier 3) |
| 6 | `describe` | string_ref | Description template with `##N` placeholders |
| 7 | `desc_parm` | array? | Values to fill `##1`, `##2`, etc. in description |
| 8 | `cost` | array? | Upgrade cost `[[item_id, count], ...]` |
| 9 | `connect_id` | array? | Prerequisite node IDs — defines tree structure |
| 10 | `condition_1` | array? | First unlock condition `[[node_id, level], ...]` |
| 11 | `condition_2` | array? | Second unlock condition |
| 12 | `attr` | array? | Attribute bonuses `[[attr_id, value], ...]` |
| 13 | `skill` | array? | Skill granted `[[skill_id, skill_level]]` |
| 14 | `power` | number | Combat power |

---

## Tree Structure (Same Pattern Per Tier)

Each tier has 10 nodes in a branching tree pattern:

```
Root (40lv)
├── Branch A (40lv)               ├── Branch B (40lv)
│   ├── Stat A1 (20lv)            │   ├── Stat B1 (20lv)
│   └── Stat A2 (20lv)            │   └── Stat B2 (20lv)
│       └── Ignore A (10lv)       │       └── Ignore B (10lv)
│           └─────────────────────>└───> Capstone / Final Talent (1lv)
```

**Unlock flow:** Root at lv10 → branches unlock → branch at lv10 → stats unlock → stats at lv10 → ignore node unlocks → ignore at lv5 → capstone unlocks.

The `connect_id` field defines the tree edges (child→parent), and `condition_1`/`condition_2` define the level requirements.

---

## Final Talents — All 12 Capstones

### Warrior Path (job_type=1)

| Tier | Name | ID | Skill ID | Effect |
|------|------|----|----------|--------|
| T1 | **Regeneration** | 1010 | — | Healing +30 (attr only, no skill) |
| T2 | **Ascension** | 1020 | 17021 | After 15s: ATK SPD +15%. After 30s: Crit Rate +20%. After 45s: ATK +20%. |
| T3 | **Rampage** | 1030 | 17022 | When HP < 20%: ATK +10%, ATK SPD +10%, Crit DMG +10%. |

### Archer Path (job_type=2)

| Tier | Name | ID | Skill ID | Effect |
|------|------|----|----------|--------|
| T1 | **Healing** | 2010 | — | Healing Amount +20 (attr only) |
| T2 | **Eager Momentum** | 2020 | 17023 | Every 3s: Crit DMG +5% (max 25%). |
| T3 | **Gale Barrage** | 2030 | 17024 | Every 2s: Combo DMG +5% (max 50%). |

### Mage Path (job_type=3)

| Tier | Name | ID | Skill ID | Effect |
|------|------|----|----------|--------|
| T1 | **Stun** | 3010 | — | Stun +1500 (attr only) |
| T2 | **Temporal Compression** | 3020 | 17025 | Each skill cast: ATK +2% (max 30%). |
| T3 | **Endless Outburst** | 3030 | 17026 | When HP < 20% (first time): Energy Regen SPD +100% for 5s. |

### Beast Path (job_type=4)

| Tier | Name | ID | Skill ID | Effect |
|------|------|----|----------|--------|
| T1 | **Launch** | 4010 | — | Launch +400 (attr only) |
| T2 | **Crimson Spirit** | 4020 | 17044 | Every 2s: Pal DMG +3% (max 30%). |
| T3 | **Assisted Combo** | 4030 | 17047 | Pal Combo Rate +25%. |

---

## Scaling Skill Nodes (Non-Capstone Nodes With Skills)

Some mid-tree nodes also grant scaling skills as they level:

| Path | Tier | Name | ID | Levels | Lv1 Effect | Max Effect |
|------|------|------|----|--------|------------|------------|
| Warrior | T3 | Counter Rejuvenation | 1024 | 20 | Restore 0.05% Max HP / 5 counters | Restore 1% Max HP / 5 counters |
| Archer | T3 | Combo Healing | 2024 | 20 | Restore 0.05% Max HP / 5 combos | Restore 1% Max HP / 5 combos |
| Mage | T2 | Wound | 3015 | 20 | Enemy Regen & Healing -0.5% | Enemy Regen & Healing -10% |
| Mage | T3 | Skill Regen | 3024 | 20 | Restore 0.04% Max HP / skill | Restore 0.8% Max HP / skill |
| Beast | T2 | Pal Crit DMG | 4017 | 20 | Pal Crit DMG +15% | Pal Crit DMG +300% |
| Beast | T2 | Pal Ignore Evasion | 4018 | 10 | Pal Ignore Evasion +2% | Pal Ignore Evasion +20% |
| Beast | T3 | Pal Healing | 4024 | 20 | Restore 0.02% Max HP / 8 pal attacks | Restore 0.4% Max HP / 8 pal attacks |
| Beast | T3 | Wound | 4025 | 20 | Enemy Regen & Healing -0.5% | Enemy Regen & Healing -10% |
| Beast | T3 | Pal ATK SPD | 4026 | 20 | Pal Base ATK SPD +0.005 | Pal Base ATK SPD +0.1 |
| Beast | T3 | Pal Ignore Evasion | 4028 | 10 | Pal Ignore Evasion +2% | Pal Ignore Evasion +20% |

---

## Full Tree — Warrior Path (job_type=1)

### Tier 1 (color_type=1)

| Node | Name | Max Lv | Max Attr | Prerequisites |
|------|------|--------|----------|---------------|
| 1001 | DEF Boost | 40 | Base DEF +480% | — (root) |
| 1002 | ATK Boost | 40 | Base ATK +160% | 1001 lv10 |
| 1003 | HP Boost | 40 | Base HP +240% | 1001 lv10 |
| 1004 | Counter DMG RES | 20 | Counter DMG RES +10% | 1002 lv10 |
| 1005 | Pal DMG RES | 20 | Pal DMG RES +10% | 1002 lv10 |
| 1006 | Skill DMG RES | 20 | Skill DMG RES +10% | 1003 lv10 |
| 1007 | Combo DMG RES | 20 | Combo DMG RES +10% | 1003 lv10 |
| 1008 | Evasion | 10 | Evasion +20% | 1004 lv10 + 1005 lv10 |
| 1009 | Basic ATK RES | 10 | Basic ATK RES +10% | 1006 lv10 + 1007 lv10 |
| 1010 | **Regeneration** | 1 | Healing +30 | 1008 lv5 + 1009 lv5 |

### Tier 2 (color_type=2)

| Node | Name | Max Lv | Max Attr / Skill | Prerequisites |
|------|------|--------|------------------|---------------|
| 1011 | HP Boost | 40 | Base HP +240% | — (root) |
| 1012 | ATK Boost | 40 | Base ATK +160% | 1011 lv10 |
| 1013 | DEF Boost | 40 | Base DEF +480% | 1011 lv10 |
| 1014 | Regeneration | 20 | Healing +20 | 1012 lv10 |
| 1015 | Crit RES | 20 | Crit RES +200% | 1012 lv10 |
| 1016 | Healing | 20 | Healing Amt +10, Healing Rate +10% | 1013 lv10 |
| 1017 | Counter DMG | 20 | Counter DMG +500% | 1013 lv10 |
| 1018 | Ignore Combo | 10 | Ignore Combo +20% | 1014 lv10 + 1015 lv10 |
| 1019 | Ignore Evasion | 10 | Ignore Evasion +20% | 1016 lv10 + 1017 lv10 |
| 1020 | **Ascension** | 1 | skill 17021 | 1018 lv5 + 1019 lv5 |

### Tier 3 (color_type=3)

| Node | Name | Max Lv | Max Attr / Skill | Prerequisites |
|------|------|--------|------------------|---------------|
| 1021 | ATK Boost | 40 | Base ATK +160% | — (root) |
| 1022 | DEF Boost | 40 | Base DEF +480% | 1021 lv10 |
| 1023 | HP Boost | 40 | Base HP +240% | 1021 lv10 |
| 1024 | Counter Rejuvenation | 20 | skill 17001 (1% HP/5 counters at lv20) | 1022 lv10 |
| 1025 | Basic ATK DMG | 20 | Basic ATK DMG +500% | 1022 lv10 |
| 1026 | Crit DMG | 20 | Crit DMG +300% | 1023 lv10 |
| 1027 | Counter DMG | 20 | Counter DMG +500% | 1023 lv10 |
| 1028 | Ignore Combo | 10 | Ignore Combo +20% | 1024 lv10 + 1025 lv10 |
| 1029 | Ignore Evasion | 10 | Ignore Evasion +20% | 1026 lv10 + 1027 lv10 |
| 1030 | **Rampage** | 1 | skill 17022 | 1028 lv5 + 1029 lv5 |

---

## Full Tree — Archer Path (job_type=2)

### Tier 1 (color_type=1)

| Node | Name | Max Lv | Max Attr | Prerequisites |
|------|------|--------|----------|---------------|
| 2001 | DEF Boost | 40 | Base DEF +480% | — (root) |
| 2002 | ATK Boost | 40 | Base ATK +160% | 2001 lv10 |
| 2003 | HP Boost | 40 | Base HP +240% | 2001 lv10 |
| 2004 | Counter DMG RES | 20 | Counter DMG RES +10% | 2002 lv10 |
| 2005 | Pal DMG RES | 20 | Pal DMG RES +10% | 2002 lv10 |
| 2006 | Skill DMG RES | 20 | Skill DMG RES +10% | 2003 lv10 |
| 2007 | Combo DMG RES | 20 | Combo DMG RES +10% | 2003 lv10 |
| 2008 | Evasion | 10 | Evasion +20% | 2004 lv10 + 2005 lv10 |
| 2009 | Basic ATK RES | 10 | Basic ATK RES +10% | 2006 lv10 + 2007 lv10 |
| 2010 | **Healing** | 1 | Healing Amount +20 | 2008 lv5 + 2009 lv5 |

### Tier 2 (color_type=2)

| Node | Name | Max Lv | Max Attr / Skill | Prerequisites |
|------|------|--------|------------------|---------------|
| 2011 | HP Boost | 40 | Base HP +240% | — (root) |
| 2012 | DEF Boost | 40 | Base DEF +480% | 2011 lv10 |
| 2013 | ATK Boost | 40 | Base ATK +160% | 2011 lv10 |
| 2014 | Healing | 20 | Healing Amt +10, Healing Rate +10% | 2012 lv10 |
| 2015 | Evasion | 20 | Evasion +20% | 2012 lv10 |
| 2016 | Crit DMG | 20 | Crit DMG +300% | 2013 lv10 |
| 2017 | Combo DMG | 20 | Combo DMG +500% | 2013 lv10 |
| 2018 | Ignore Stun | 10 | Ignore Stun +15% | 2014 lv10 + 2015 lv10 |
| 2019 | Ignore Evasion | 10 | Ignore Evasion +20% | 2016 lv10 + 2017 lv10 |
| 2020 | **Eager Momentum** | 1 | skill 17023 | 2018 lv5 + 2019 lv5 |

### Tier 3 (color_type=3)

| Node | Name | Max Lv | Max Attr / Skill | Prerequisites |
|------|------|--------|------------------|---------------|
| 2021 | ATK Boost | 40 | Base ATK +160% | — (root) |
| 2022 | DEF Boost | 40 | Base DEF +480% | 2021 lv10 |
| 2023 | HP Boost | 40 | Base HP +240% | 2021 lv10 |
| 2024 | Combo Healing | 20 | skill 17048 (1% HP/5 combos at lv20) | 2022 lv10 |
| 2025 | Ignore Launch | 20 | Ignore Launch +200 | 2022 lv10 |
| 2026 | ATK SPD | 20 | Base ATK SPD +2000 | 2023 lv10 |
| 2027 | Combo DMG | 20 | Combo DMG +500% | 2023 lv10 |
| 2028 | Ignore Stun | 10 | Ignore Stun +15% | 2024 lv10 + 2025 lv10 |
| 2029 | Ignore Evasion | 10 | Ignore Evasion +20% | 2026 lv10 + 2027 lv10 |
| 2030 | **Gale Barrage** | 1 | skill 17024 | 2028 lv5 + 2029 lv5 |

---

## Full Tree — Mage Path (job_type=3)

### Tier 1 (color_type=1)

| Node | Name | Max Lv | Max Attr | Prerequisites |
|------|------|--------|----------|---------------|
| 3001 | DEF Boost | 40 | Base DEF +480% | — (root) |
| 3002 | ATK Boost | 40 | Base ATK +160% | 3001 lv10 |
| 3003 | HP Boost | 40 | Base HP +240% | 3001 lv10 |
| 3004 | Counter DMG RES | 20 | Counter DMG RES +10% | 3002 lv10 |
| 3005 | Pal DMG RES | 20 | Pal DMG RES +10% | 3002 lv10 |
| 3006 | Skill DMG RES | 20 | Skill DMG RES +10% | 3003 lv10 |
| 3007 | Combo DMG RES | 20 | Combo DMG RES +10% | 3003 lv10 |
| 3008 | Evasion | 10 | Evasion +20% | 3004 lv10 + 3005 lv10 |
| 3009 | Basic ATK RES | 10 | Basic ATK RES +10% | 3006 lv10 + 3007 lv10 |
| 3010 | **Stun** | 1 | Stun +1500 | 3008 lv5 + 3009 lv5 |

### Tier 2 (color_type=2)

| Node | Name | Max Lv | Max Attr / Skill | Prerequisites |
|------|------|--------|------------------|---------------|
| 3011 | ATK Boost | 40 | Base ATK +160% | — (root) |
| 3012 | DEF Boost | 40 | Base DEF +480% | 3011 lv10 |
| 3013 | HP Boost | 40 | Base HP +240% | 3011 lv10 |
| 3014 | Skill Crit DMG | 20 | Skill Crit DMG +80% | 3012 lv10 |
| 3015 | Wound | 20 | skill 17050 (enemy Regen -10% at lv20) | 3012 lv10 |
| 3016 | Ignore Launch | 20 | Ignore Launch +200 | 3013 lv10 |
| 3017 | Skill DMG | 20 | Skill DMG +200% | 3013 lv10 |
| 3018 | Ignore Counter | 10 | Ignore Counter +20% | 3014 lv10 + 3015 lv10 |
| 3019 | Ignore Evasion | 10 | Ignore Evasion +20% | 3016 lv10 + 3017 lv10 |
| 3020 | **Temporal Compression** | 1 | skill 17025 | 3018 lv5 + 3019 lv5 |

### Tier 3 (color_type=3)

| Node | Name | Max Lv | Max Attr / Skill | Prerequisites |
|------|------|--------|------------------|---------------|
| 3021 | HP Boost | 40 | Base HP +240% | — (root) |
| 3022 | DEF Boost | 40 | Base DEF +480% | 3021 lv10 |
| 3023 | ATK Boost | 40 | Base ATK +160% | 3021 lv10 |
| 3024 | Skill Regen | 20 | skill 17049 (0.8% HP/skill at lv20) | 3022 lv10 |
| 3025 | Skill DMG | 20 | Skill DMG +200% | 3022 lv10 |
| 3026 | Crit RES | 20 | Crit RES +200% | 3023 lv10 |
| 3027 | Energy Regen | 20 | Energy Regen SPD +10% | 3023 lv10 |
| 3028 | Ignore Counter | 10 | Ignore Counter +20% | 3024 lv10 + 3025 lv10 |
| 3029 | Ignore Evasion | 10 | Ignore Evasion +20% | 3026 lv10 + 3027 lv10 |
| 3030 | **Endless Outburst** | 1 | skill 17026 | 3028 lv5 + 3029 lv5 |

---

## Full Tree — Beast Path (job_type=4)

### Tier 1 (color_type=1)

| Node | Name | Max Lv | Max Attr | Prerequisites |
|------|------|--------|----------|---------------|
| 4001 | DEF Boost | 40 | Base DEF +480% | — (root) |
| 4002 | ATK Boost | 40 | Base ATK +160% | 4001 lv10 |
| 4003 | HP Boost | 40 | Base HP +240% | 4001 lv10 |
| 4004 | Counter DMG RES | 20 | Counter DMG RES +10% | 4002 lv10 |
| 4005 | Pal DMG RES | 20 | Pal DMG RES +10% | 4002 lv10 |
| 4006 | Skill DMG RES | 20 | Skill DMG RES +10% | 4003 lv10 |
| 4007 | Combo DMG RES | 20 | Combo DMG RES +10% | 4003 lv10 |
| 4008 | Evasion | 10 | Evasion +20% | 4004 lv10 + 4005 lv10 |
| 4009 | Basic ATK RES | 10 | Basic ATK RES +10% | 4006 lv10 + 4007 lv10 |
| 4010 | **Launch** | 1 | Launch +400 | 4008 lv5 + 4009 lv5 |

### Tier 2 (color_type=2)

| Node | Name | Max Lv | Max Attr / Skill | Prerequisites |
|------|------|--------|------------------|---------------|
| 4011 | HP Boost | 40 | Base HP +240% | — (root) |
| 4012 | ATK Boost | 40 | Base ATK +160% | 4011 lv10 |
| 4013 | DEF Boost | 40 | Base DEF +480% | 4011 lv10 |
| 4014 | Regeneration | 20 | Healing +20 | 4012 lv10 |
| 4015 | Evasion | 20 | Evasion +20% | 4012 lv10 |
| 4016 | Pal DMG Boost | 20 | Pal DMG +200% | 4013 lv10 |
| 4017 | Pal Crit DMG | 20 | skill 17042 (Pal Crit DMG +300% at lv20) | 4013 lv10 |
| 4018 | Pal Ignore Evasion | 10 | skill 17043 (Pal Ign. Evasion +20% at lv10) | 4014 lv10 + 4015 lv10 |
| 4019 | Ignore Evasion | 10 | Ignore Evasion +20% | 4016 lv10 + 4017 lv10 |
| 4020 | **Crimson Spirit** | 1 | skill 17044 | 4018 lv5 + 4019 lv5 |

### Tier 3 (color_type=3)

| Node | Name | Max Lv | Max Attr / Skill | Prerequisites |
|------|------|--------|------------------|---------------|
| 4021 | ATK Boost | 40 | Base ATK +160% | — (root) |
| 4022 | DEF Boost | 40 | Base DEF +480% | 4021 lv10 |
| 4023 | HP Boost | 40 | Base HP +240% | 4021 lv10 |
| 4024 | Pal Healing | 20 | skill 17045 (0.4% HP/8 pal atks at lv20) | 4022 lv10 |
| 4025 | Wound | 20 | skill 17051 (enemy Regen -10% at lv20) | 4022 lv10 |
| 4026 | Pal ATK SPD | 20 | skill 17041 (Pal ATK SPD +0.1 at lv20) | 4023 lv10 |
| 4027 | Pal DMG Boost | 20 | Pal DMG +200% | 4023 lv10 |
| 4028 | Pal Ignore Evasion | 10 | skill 17046 (Pal Ign. Evasion +20% at lv10) | 4024 lv10 + 4025 lv10 |
| 4029 | Ignore Evasion | 10 | Ignore Evasion +20% | 4026 lv10 + 4027 lv10 |
| 4030 | **Assisted Combo** | 1 | skill 17047 | 4028 lv5 + 4029 lv5 |

---

## Tier 1 Capstone Differences By Path

The T1 capstone is the only node that differs between paths:

| Path | Capstone | Attr Effect |
|------|----------|-------------|
| Warrior | Regeneration | Healing +30 |
| Archer | Healing | Healing Amount +20 |
| Mage | Stun | Stun +1500 |
| Beast | Launch | Launch +400 |

All other T1 nodes (stat boosts, DMG RES, Evasion, Basic ATK RES) are identical across paths.

---

## Notes

- **Attr values use `/10000` convention**: `2001 = Base ATK %`, `2003 = Base HP %`, `2005 = Base DEF %`. A value of `1600000` = 160.00% = 160%.
- **All T1 stat nodes are identical** across the 4 paths — only the capstone differs.
- **T2 and T3 are class-specialized**: Warrior focuses on counters, Archer on combos, Mage on skills, Beast on pals.
- **Skill IDs 17xxx** are talent-specific skills — not the same as active skills (1xxx) or back accessory skills (18xxx).
- **Talent trees are tied to back accessories** — unlocking higher tiers requires progressing back accessory levels.
- The old "6 final talents" listed in previous versions of this document referred to **class passive skills** (see `04_CLASSES.md`), not talents.

---

## Data Files

- **Config table**: `data/tables/Back_talent.json` (2,652 entries)
- **Schema**: `data/schemas/ConfigBack_talent.json`
- **Related**: `battlesim/reference/19_BACK_DECORATIONS.md` — back accessory combat skills
- **Related**: `battlesim/reference/back_accessories_master.json` — back accessory master data
