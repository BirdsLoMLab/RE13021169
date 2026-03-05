# 09 — Relics

> 35 relics across 7 slot categories (6 relic types + 1 spore type). Each relic is a passive skill that provides stat bonuses, conditional attribute boosts, damage procs, or trap/buff mechanics. 7 equip slots, 5 relics per slot.

---

## Overview

Relics are **not simple stat items** — each relic's equip bonus is a **skill reference** (`ConfigSkill_level` keyed by `[[skillId, skillLevel]]`). The game loads relic effects through the passive skill system, meaning relics can:
- Grant flat attribute bonuses (unconditional or conditional)
- Trigger damage procs via skill effect chains
- Create traps, shields, or HP-triggered mechanics
- Boost specific hero skill or pal skill performance

### Dual Bonus System
- **equip** → `[[skillId, skillLevel]]` → looked up via `configSkill_level.getDataByKeys("id", skillId, "level", skillLevel)` — active only when slotted
- **own** → `[[attrId, value], ...]` → passive attribute bonuses always active from ownership
- **equip_effect** → additional skill/buff triggers (only relic 4033 uses this)

### Skill Type Classification
All relic skills use `cat="passive"` with these ConfigSkill types:
- **type=2 (PASSIVE_ADD):** Direct stat additions to character attributes
- **type=3 (PASSIVE_EFFECT):** Passive effects that run during battle (procs, triggers, traps)
- **type=4 (PARTNER_SKILL):** Pal/pet passive — adds skills to specific pal types

---

## Slot System

### ConfigRelic_pos (7 slots)
| Slot | Type | Relics | Max Level | Notes |
|------|------|--------|-----------|-------|
| 1 | Category 1 | 4017-4020, 4025 | 1 (binary) / 150 | Mixed binary + leveled |
| 2 | Category 2 | 4001-4004, 4026 | 150 / 1 | Mixed leveled + binary |
| 3 | Category 3 | 4005-4008, 4027 | 150 | All leveled |
| 4 | Category 4 | 4021-4024, 4028 | 1 (binary) | All binary |
| 5 | Category 5 | 4009-4012, 4029 | 1 (binary) | All binary |
| 6 | Category 6 | 4013-4016, 4030 | 1 (binary) | All binary |
| 7 | **Spore** | 4031-4035 | 1 or 11 | New relic type, separate UI |

**Leveled relics** (150 levels): Scale stats with level. Relics 4001-4008 and 4027.
**Binary relics** (1 level): On/off effects, no scaling. Relics 4009-4026, 4028-4030.
**Spores** (11 levels): Newer system with moderate scaling. Relics 4031-4035.

---

## ConfigRelic Schema (12 fields, keyed by [id, level])

| Field | Type | Description |
|-------|------|-------------|
| id | number | Relic ID (4001-4035) |
| level | number | Relic level |
| name | string_ref | Localized name |
| type | number | Slot category (1-7) |
| desc | string_ref | Description template (shared: 13230001) |
| desc_parm | array | Description format parameters |
| icon | string | Icon asset |
| equip | array | `[[skillId, skillLevel]]` — skill reference for equip bonus |
| own | array | `[[attrId, value], ...]` — ownership bonuses (always active) |
| equip_effect | array\|null | Additional combat effects (only relic 4033) |
| cost | array | Level-up cost `[[itemId, count], ...]` |
| power | number | Combat power |

---

## Complete Relic Catalog

### Slot 1 — Category 1 (5 relics)

#### Relic 4017 — Flat Crit Rate
- **Skill type:** PASSIVE_ADD | **Levels:** 1 (binary)
- **Effect:** `crit_rate +10%` (unconditional)
- **Battlesim:** Flat stat mod

#### Relic 4018 — Flat Double Hit
- **Skill type:** PASSIVE_ADD | **Levels:** 1 (binary)
- **Effect:** `double_hit +10%` (unconditional)
- **Battlesim:** Flat stat mod

#### Relic 4019 — Flat Counter
- **Skill type:** PASSIVE_ADD | **Levels:** 1 (binary)
- **Effect:** `counter +10%` (unconditional)
- **Battlesim:** Flat stat mod

#### Relic 4020 — Crit Rate on Any Skill
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Effect:** `crit_rate +5%` | **Trigger:** ON_SKILL [0] (all skills)
- **Battlesim:** Conditional buff — crit rate boost when any skill activates

#### Relic 4025 — Flat Skill Crit Rate
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Effect:** `skill_crit_rate +5%` (unconditional)
- **Battlesim:** Flat stat mod

---

### Slot 2 — Category 2 (5 relics)

#### Relic 4001 — Damage Proc (Leveled)
- **Skill type:** PASSIVE_EFFECT | **Levels:** 150
- **Buff:** `skill_effect` (buff group 40011) — triggers periodic damage proc
- **skillCoefficient:** Scales from 16,379 (Lv1) → 223,683 (Lv150) [XOR-encoded base damage]
- **desc_parm:** 247% (Lv1) → 2,105% (Lv150)
- **Battlesim:** Periodic damage proc, scaling with level

#### Relic 4002 — Pal Skill Damage Proc (Leveled)
- **Skill type:** PARTNER_SKILL | **Levels:** 150
- **addSkill:** Adds skill to pal race [5] (specific pal type), skill 1042
- **skillCoefficient:** Scales from 30,979 (Lv1) → 71,427 (Lv150) [XOR-encoded]
- **desc_parm:** [10, 6, 591.6%] (Lv1) → [10, 6, 5,046%] (Lv150)
- **Battlesim:** Adds a damage skill to specific pal type, scaling coefficient

#### Relic 4003 — Attack Speed on Pal Skill (Leveled)
- **Skill type:** PASSIVE_EFFECT | **Levels:** 150
- **Effect:** `att_speed_base_add` | **Trigger:** ON_SKILL [2601-2605] (pal skill group)
- **Scaling:** +10% (Lv1) → +85.25% (Lv150)
- **Battlesim:** Conditional attack speed boost when specific pal skills activate

#### Relic 4004 — Partner DMG on Pal Skill (Leveled)
- **Skill type:** PASSIVE_ADD | **Levels:** 150
- **Effect:** `partner_dam_base_add` | **Trigger:** ON_SKILL [2201-2205, 2801-2805] (pal skill groups)
- **Scaling:** +5% (Lv1) → +42.62% (Lv150)
- **Battlesim:** Conditional partner damage boost when specific pal skills activate

#### Relic 4026 — Pal Damage Proc (Binary)
- **Skill type:** PARTNER_SKILL | **Levels:** 1 (binary)
- **addSkill:** Adds skill to pal races [10, 13, 14], skill 4126
- **skillCoefficient via Skill_level:** [24501]
- **desc_parm:** [20, 0.5]
- **Battlesim:** Adds proc skill to specific pal types

---

### Slot 3 — Category 3 (5 relics)

#### Relic 4005 — Crit Rate + Crit DMG on Pal Skill (Leveled)
- **Skill type:** PASSIVE_ADD | **Levels:** 150
- **Effect:** `crit_rate +20%` (fixed), `crit_dam_base_add` (scales) | **Trigger:** ON_SKILL [2701-2705]
- **Scaling:** crit_dam +50% (Lv1) → +426.25% (Lv150); crit_rate stays +20%
- **Battlesim:** Major crit boost conditional on specific pal skills

#### Relic 4006 — Pal Damage Proc (Leveled)
- **Skill type:** PARTNER_SKILL | **Levels:** 150
- **addSkill:** Adds skill to pal race [3], skill 1043
- **skillCoefficient:** Scales from 47,303 (Lv1) → 519,327 (Lv150) [XOR-encoded]
- **desc_parm:** [12, 592%] (Lv1) → [12, 5,046%] (Lv150)
- **Battlesim:** Adds damage skill to specific pal type, heavy scaling

#### Relic 4007 — Double Hit on Pal Skill (Leveled)
- **Skill type:** PASSIVE_ADD | **Levels:** 150
- **Effect:** `double_hit` | **Trigger:** ON_SKILL [2401-2405]
- **Scaling:** +10% (Lv1) → +85.25% (Lv150)
- **Battlesim:** Conditional double hit boost

#### Relic 4008 — Partner DMG on Pal Skill (Leveled)
- **Skill type:** PASSIVE_ADD | **Levels:** 150
- **Effect:** `partner_dam_base_add` | **Trigger:** ON_SKILL [2101-2105, 2901-2905]
- **Scaling:** +5% (Lv1) → +42.62% (Lv150)
- **Battlesim:** Conditional partner damage boost

#### Relic 4027 — Attack Speed on Pal Skill (Leveled)
- **Skill type:** PASSIVE_EFFECT | **Levels:** 150
- **Effect:** `att_speed_base_add` | **Trigger:** ON_SKILL [2908-2910]
- **Scaling:** +3.33% (Lv1) → +28.43% (Lv150)
- **Battlesim:** Conditional attack speed boost (smaller than 4003)

---

### Slot 4 — Category 4 (5 relics)

#### Relic 4021 — Continuous ATK Buff
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Buff:** `attrib_continue` on `att` (1001) — stacking ATK buff over time
- **Buff params:** mode=2, stacks over time, interval from p5=[10]
- **desc_parm:** [1, 10] — likely +1% ATK every 10s
- **Battlesim:** Ramping ATK buff, significant in long fights

#### Relic 4022 — Flat Boss DMG
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Effect:** `boss_dam +20%` (unconditional)
- **Battlesim:** Flat stat mod, PvE boss damage only

#### Relic 4023 — HP Threshold Trap
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Buff chain:** `hpchange_trigger` → when HP rises above 70% (p2=7000), triggers buff 40232 → `trap` #402
- **desc_parm:** [70, 3] — 70% HP threshold, 3 related parameter
- **Battlesim:** Creates trap when HP exceeds 70%

#### Relic 4024 — Trap Spawner
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Buff:** `trap` #403
- **skillCoefficient via Skill_level:** [23663]
- **desc_parm:** [5, 10] — likely 5s interval, 10% damage
- **Battlesim:** Periodic trap placement

#### Relic 4028 — Flat Defensive Bundle
- **Skill type:** PASSIVE_ADD | **Levels:** 1 (binary)
- **Effect:** `att_resist +5%`, `skill_resist +5%`, `partner_resist +5%`, `double_hit_def +5%`, `counter_def +5%`
- **Battlesim:** Flat defensive stat bundle — all 5 resistance types +5%

---

### Slot 5 — Category 5 (5 relics)

#### Relic 4009 — Skill Damage for Mythic Skills
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Effect:** `skill_damage_add +30%` | **Trigger:** HAS_SKILL [Batty Trace(1012), Nature's Renewal(1019), Shroom Shield(1036)]
- **Battlesim:** +30% skill damage if using any of these 3 Mythic-tier skills

#### Relic 4010 — Skill Buff Coefficient for Epic AoE
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Effect:** `skillbuff_co_add +30%` | **Trigger:** HAS_SKILL [Durian Bomb(1020), Easy Breezy(1023), Take It Slow(1024)]
- **Battlesim:** +30% skill buff coefficient if using any of these 3 Epic-tier skills

#### Relic 4011 — Skill Buff Coefficient for Coin/Slime/Meteor
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Effect:** `skillbuff_co_add +30%` | **Trigger:** HAS_SKILL [Coin Bomb(1044), Slime Bomb(1045), Meteor Fall(1046)]
- **Battlesim:** +30% skill buff coefficient if using any of these 3 Epic-tier skills

#### Relic 4012 — Skill Buff Duration for CC Skills
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Effect:** `id_skillbuff_time_base_add +50%` | **Trigger:** HAS_SKILL [Disarm(1021), Dazzled(1022), Smoke Bomb(1029)]
- **Battlesim:** +50% buff/debuff duration for these CC Legendary skills

#### Relic 4029 — Skill Buff Duration for Immortal Set A
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Effect:** `id_skillbuff_time_base_add +50%` | **Trigger:** HAS_SKILL [Hundred Slashes(1060), Worldly Snare(1061), Star Array(1064), Ancestral Will(1069)]
- **Battlesim:** +50% buff duration for these Immortal-tier skills

---

### Slot 6 — Category 6 (5 relics)

#### Relic 4013 — Skill Damage for Grim Reaper
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Effect:** `skill_damage_add +80%` | **Trigger:** HAS_SKILL [Grim Reaper(1047)]
- **Battlesim:** Massive +80% skill damage, but only for Grim Reaper

#### Relic 4014 — Periodic Proc (Ignore Counter + Shield HP)
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Buff:** `skill_effect` (buff 40141), associated with `ignore_counter`(1049) and `shield_hp_extra`(1051)
- **Secondary buff 40142:** `skill_value` on `hp`(1002) — likely shield/HP effect
- **desc_parm:** [2.5]
- **Battlesim:** Proc that grants counter immunity and shield bonus

#### Relic 4015 — Pal Summon Damage Boost
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Buff:** `unit_call_damage_add` (buff group 160) — boosts damage from summoned pal units
- **desc_parm:** [30] — +30% summoned pal damage
- **Battlesim:** +30% to all pal summon damage

#### Relic 4016 — Periodic Proc (Shield Duration)
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Buff:** `skill_effect` (buff 40161), associated with `shield_time_extra`(1050)
- **Secondary buff 40162:** `attrib` on `att_dam`(1039)
- **desc_parm:** [15]
- **Battlesim:** Grants shield duration extension and ATK damage boost

#### Relic 4030 — Energy Recovery for Immortal Set B
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1 (binary)
- **Effect:** `power_recovery_buff_add +30%` | **Trigger:** HAS_SKILL [Dragonic Resonance(1059), Windborne Arrow(1062), Crimson Moonfall(1063), Winged Dreams(1068)]
- **Battlesim:** +30% skill energy recovery for these Immortal-tier skills → faster skill uptime

---

### Slot 7 — Spores (5 relics)

#### Relic 4031 — PvE Extra Time (Chrono Spore?)
- **Skill type:** PASSIVE_ADD | **Levels:** 11
- **Effect:** `pve_extra_time` | **Scaling:** +5% (Lv1) → +10% (Lv11)
- **Battlesim:** PvE only — extends fight timer. Not relevant for PvP sim.

#### Relic 4032 — HP Threshold Shield (Thorny Spore?)
- **Skill type:** PASSIVE_EFFECT | **Levels:** 1
- **Buff chain:** `current_hp` (buff group 350) — 11 tiered HP thresholds (Lv1: 59.99%, stepping down by 2% each tier to 39.99%)
- **skillCoefficient:** [30871]
- **desc_parm:** [60, 60] — likely 60% HP threshold, 60% shield
- **Battlesim:** Creates shields at HP breakpoints. Significant defensive mechanic.

#### Relic 4033 — Skill Buff Duration for Relic 4023 (Potent Spore?)
- **Skill type:** PASSIVE_ADD | **Levels:** 11
- **Effect:** `id_skillbuff_time_base_add` | **Trigger:** HAS_SKILL [relic skill 4023]
- **Scaling:** +20% (Lv1) → +40% (Lv11)
- **Also has equip_effect:** `[[1, 2000]]` — additional buff trigger
- **Battlesim:** Extends duration of relic 4023's trap/buff effects

#### Relic 4034 — DMG Resistance (Plumed Spore)
- **Skill type:** PASSIVE_ADD | **Levels:** 11
- **Effect:** `resist` (1021) — flat damage resistance
- **Scaling:** +4% (Lv1) → +8% (Lv11)
- **Battlesim:** Flat defensive stat mod. Shows up in player stats, but user can toggle on/off.

#### Relic 4035 — Nirvana Trap (Nirvana Spore?)
- **Skill type:** PASSIVE_EFFECT | **Levels:** 11
- **Buff chain:** buff 40351 → `trap` #404, buff 40352 → `skill_bufftime_add` on [double_hit, counter, att_resist, hpsteal_rate, hpsteal_amount, hpsteal_res, ignore_hpsteal, pve_dam, pve_resist, ignore_crit_rate, ignore_hp_recovery, armor_penetration_rate, skillbuff_time, ...]
- **skillCoefficient:** Scales from 23,663 (Lv1) → 22,615 (Lv11) [XOR-encoded]
- **desc_parm:** 10 (Lv1) → 20 (Lv11)
- **Battlesim:** Creates trap + extends buff durations across many attribute types

---

## Trigger System

### Mode 1: ON_SKILL
Relic's `ownEffect` attributes are temporarily granted when the specified skill **activates** during battle. The bonus is added for the duration of the skill execution.

| Relic | Pal Skill IDs | Effect When Triggered |
|-------|--------------|----------------------|
| 4003 | 2601-2605 | att_speed_base_add |
| 4004 | 2201-2205, 2801-2805 | partner_dam_base_add |
| 4005 | 2701-2705 | crit_rate + crit_dam_base_add |
| 4007 | 2401-2405 | double_hit |
| 4008 | 2101-2105, 2901-2905 | partner_dam_base_add |
| 4020 | [0] (all skills) | crit_rate |
| 4027 | 2908-2910 | att_speed_base_add |

### Mode 2: HAS_SKILL
Relic's `ownEffect` attributes are **permanently active** as long as the specified hero skill is equipped in any slot. This is a loadout check, not a runtime trigger.

| Relic | Required Hero Skill | Bonus |
|-------|-------------------|-------|
| 4009 | Batty Trace / Nature's Renewal / Shroom Shield | skill_damage_add +30% |
| 4010 | Durian Bomb / Easy Breezy / Take It Slow | skillbuff_co_add +30% |
| 4011 | Coin Bomb / Slime Bomb / Meteor Fall | skillbuff_co_add +30% |
| 4012 | Disarm / Dazzled / Smoke Bomb | skillbuff_time +50% |
| 4013 | Grim Reaper | skill_damage_add +80% |
| 4029 | Hundred Slashes / Worldly Snare / Star Array / Ancestral Will | skillbuff_time +50% |
| 4030 | Dragonic Resonance / Windborne Arrow / Crimson Moonfall / Winged Dreams | power_recovery_buff +30% |
| 4033 | Relic 4023's skill effect | skillbuff_time +20-40% |

---

## Level Scaling Summary

### Leveled Relics (150 levels) — Key Milestones

| Relic | Effect | Lv1 | Lv50 | Lv100 | Lv150 |
|-------|--------|-----|------|-------|-------|
| 4001 | Damage proc % | 247% | 857% | 1,480% | 2,105% |
| 4002 | Pal proc damage % | 591.6% | 2,056.8% | 3,550.8% | 5,046% |
| 4003 | att_speed on pal skill | +10% | +34.75% | +60% | +85.25% |
| 4004 | partner_dam on pal skill | +5% | +17.37% | +30% | +42.62% |
| 4005 | crit_dam on pal skill | +50% | +173.74% | +300% | +426.25% |
| 4006 | Pal proc damage % | 592% | 2,057% | 3,551% | 5,046% |
| 4007 | double_hit on pal skill | +10% | +34.75% | +60% | +85.25% |
| 4008 | partner_dam on pal skill | +5% | +17.37% | +30% | +42.62% |
| 4027 | att_speed on pal skill | +3.33% | +11.58% | +20% | +28.43% |

### Spores (11 levels)

| Relic | Effect | Lv1 | Lv6 | Lv11 |
|-------|--------|-----|-----|------|
| 4031 | pve_extra_time | +5% | +7.5% | +10% |
| 4033 | skillbuff_time (for 4023) | +20% | +30% | +40% |
| 4034 | resist (dmg res) | +4% | +6% | +8% |
| 4035 | Nirvana trap effect | 10 | 15 | 20 |

---

## Battlesim Relevance

### High Priority (mechanic-changing)
- **Relic 4012/4029:** +50% buff/debuff duration on equipped skill — directly changes CC uptime and buff windows
- **Relic 4030:** +30% energy recovery — faster skill rotations for Immortal skills
- **Relic 4013:** +80% skill damage for Grim Reaper — massive single-skill boost
- **Relic 4009:** +30% skill damage for Mythic trio
- **Relic 4021:** Ramping ATK buff over time — affects long fight outcomes
- **Relic 4032 (Spore):** HP threshold shields — defensive breakpoints
- **Relic 4035 (Spore):** Trap + multi-attribute buff duration extension

### Medium Priority (conditional stat boosts)
- **Relics 4003/4004/4005/4007/4008/4027:** ON_SKILL triggers tied to specific pal skills — need to know which pal is equipped to determine if these activate
- **Relics 4010/4011:** +30% skill buff coefficient for specific skills

### Low Priority (flat stats or PvE-only)
- **Relics 4017/4018/4019/4025:** Flat stat mods — already in player stats
- **Relic 4022:** Boss damage only
- **Relic 4028:** Flat defensive bundle
- **Relic 4031 (Spore):** PvE timer only
- **Relic 4034 (Plumed Spore):** Flat resist — shows in stats

### Recommended Sim Approach
1. **Stat-only relics** (4017-4019, 4022, 4025, 4028, 4034): Tell user to include/exclude in their stat export. Sim doesn't need to model these.
2. **HAS_SKILL relics** (4009-4013, 4029-4030): Check equipped skills at sim setup. If condition met, apply the attribute bonus globally.
3. **ON_SKILL relics** (4003-4005, 4007-4008, 4020, 4027): Need to track pal skill activations and apply temporary buffs during skill windows.
4. **Proc/trap relics** (4001, 4002, 4006, 4014-4016, 4021, 4023-4024, 4026, 4032, 4035): Full combat simulation needed — these trigger damage/effects during battle.

---

## Dependencies

- ConfigSkill / ConfigSkill_level — Relic equip bonuses are skill references
- ConfigSkilleffcet — Effect chain execution for proc relics
- ConfigBuff — Buff mechanics (traps, HP triggers, continuous effects)
- AttribDefine — Attribute IDs for all stat bonuses
- ConfigRelic_pos — 7 equip slot definitions
- ConfigRelic_get — Gacha acquisition system (not battlesim relevant)
