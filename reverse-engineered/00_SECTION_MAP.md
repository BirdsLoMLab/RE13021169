# LOM Game Script — Section Map

**Source file:** `game_script_pretty.js` (457,538 lines, 28MB beautified)
**Generated from:** `game_script.js` (7,685 lines, 18MB minified)
**Config modules extracted:** 711 schemas → `data/schemas/`
**Enums extracted:** 96 enums → `data/enums/`
**Constants extracted:** 5 files → `data/constants/`

---

## Key Module Locations

### Core Infrastructure
| Module | Lines | Description |
|--------|-------|-------------|
| BaseConfig | ~184594 | Universal config table class, loadData/loadBufferData (binary XOR decode) |
| CONFIG_KEY | ~184611 | `24455` — XOR obfuscation key for config data |
| FixMath | 292602-292620 | Fixed-point math: `round()`, `roundInt()`, `clamp()` |

### Enums & Definitions
| Module | Lines | Description |
|--------|-------|-------------|
| EnumDefine | 278546-278700 | HealthType, AttackType, StateType, DmgType, RunMode, BuffGroupType (46), EffectTriggerType (16), SkillType (5), TargetFilter, SpBuffState, HitType, BindType, etc. |
| AttribDefine (MetaAttrib) | 349630-349675 | 192 attribute IDs across 7 ranges (1-24, 1001-1082, 2001-2036, 3001-3024, 4001-4006, 5001-5012, 6001-6007, 10001-10030), MetaAttrib value calculation class |
| buffMap registration | 332125 | Complete mapping of 80 buff action strings → implementing classes |
| aiMap registration | 332125 | AI type mappings: common, player, boss, tfmonster, spirit, flypet, etc. |
| skillMap registration | 332125 | Skill handler mappings: normal, counter, effect, passive, boss_effect, spirit_normal, etc. |

### Battle Core
| Module | Lines | Description |
|--------|-------|-------------|
| BattleMain (init/reset) | 188200-188210 | Battle initialization, injuryReduce/shieldDecay/treatDecay defaults |
| HurtUtil | 322750-323007 | ALL core damage functions: normalHurt, normalDoubleHurt, normalCounterHurt, calHurt, calArmorAndBlock, calSuppressAndInspire, checkHit, checkDoubleAct, checkCounterAct, checkDizz, checkSkillCirt, checkThrowHit, SkillHurt, spiritNormalHit, hpStealHeal/hpStealCal/hpStealCheck |
| BattleData / setPlayerList | 187356-187578 | Player data setup, attribute initialization, pet/skill/spirit/passive skill loading |

### Stat Assembly Pipeline
| Module | Lines | Description |
|--------|-------|-------------|
| setPlayerList | 187356-187419 | Master entry point: job→unit config, attr, equip, pets, skills, ext, spirit, passives |
| setPlayerAttrib | 187426-187432 | Initialize module=1 attributes from ConfigAttribute, PvE filtering |
| setPlayerEquip | 187440-187491 | Equipment figure processing: 5 slots, artifact override, skin system |
| getPetFactAttrValue | 187495-187505 | Pet attribute bonus with group-based multiplicative scaling |
| setPlayerPets | 187544-187562 | Pet/pal unit initialization, stat inheritance from parent |
| setPlayerFlyPet | 187563-187575 | Avian/fly pet initialization from ConfigFly + ConfigUnit |
| setPlayerSkill | 187506-187517 | Active skill loading sorted by position |
| setPlayerPassiveSkill | 187523-187534 | Passive skills with angel skill enhancements |

### Damage Application
| Module | Lines | Description |
|--------|-------|-------------|
| Unit.addDamage | 449240-449365 | Master damage pipeline: PvP reduction, season bonus, shield absorption, block, HP reduction, death prevention (Time Reversal → Remake HP → Immune Death), record damage, HP change triggers |
| SkillHandleNormal | 429879-430068 | Normal attack execution: hit check, basic/double/counter damage, FRAGILE_EFFECT, EXTRA_DAMAGE, GIANT_SLAYER, buff triggers |
| SkillHandleCounter | 429630-429700 | Counter-attack execution |

### Buff System — Damage Modifiers
| Module | Lines | Description |
|--------|-------|-------------|
| BuffBleed | 192751-192860 | Bleed damage (8 types: basic, curHP%, skill, basic+resist, combo, counter, maxHP%, attribute-based) |
| BuffSkillValue | 195729-195970 | Primary skill damage: 11 calTypes (attrib, ATK-DEF, HP-diff, curHP, atkDmg, targetATK, combo, counter, casterHP, casterMaxHP, partnerDam) |
| BuffSkillHpHurt | 195470-195530 | HP-based damage with resistance and clamping |
| BuffShareDamage | 195114-195144 | Shared/splash damage (full pass-through or percentage-based) |
| BuffExtraDamage | 193971-194016 | Extra damage multiplier (fixed %, HP-loss scaling, CURRENT_HP scaling) |
| BuffGiantSlayer | 194151-194175 | HP-difference based damage bonus with boss/non-boss caps |
| BuffSkillFragileAdd | 195433-195468 | Fragile effect: flat bonus damage from attacker attribute/HP |
| BuffVampire | 196745-196788 | Life steal with Total DMG Bonus/RES, treatDecay, HP cap |
| BuffSkillDamageAdd | ~196700 | Skill-specific damage bonus with Total DMG calc |
| BuffDotDamage | 193836 | Damage over time |

### Buff System — Defense/Utility
| Module | Lines | Description |
|--------|-------|-------------|
| BuffShield | 195173-195250 | Shield creation (4 calTypes), shield_hp_extra, shieldDecay, sub-buff on create/destroy |
| BuffAttrib | 192380 | Attribute modification buffs (addValue flat / addMultiples scaling) |
| BuffAttribContinue | 192517 | Continuous attribute modification |
| BuffAttribCondition | 192431 | Conditional attribute modification |
| BuffSpeedTrigger | 196105 | Speed-threshold triggered buff application |
| BuffStateTrigger | 196181 | State-based trigger (Miss/Counter/Double/Skill/etc.) |
| BuffSkillParse | 195553 | Auto-cast skill at configurable intervals |
| BuffDeferDamage | 193504 | Damage deferral/absorption system |
| BuffCurrentHp | 193455 | HP percentage illusion for trigger calculations |
| BuffHpChangeTrigger | 194229 | HP threshold trigger with 3-frame delay |
| BuffAddBuffTrigger | 192229 | Buff chain reaction trigger |
| BuffTrap | 196418 | Trap deployment (periodic effect trigger) |
| BuffInvincible | ~194070 | Invincibility buff |
| BuffImmuneDeath | ~194100 | Death immunity |
| BuffRemake | ~195050 | HP remake/restore |
| BuffReduceHeal | ~195080 | Healing reduction |
| BuffTotalDamageTrigger | 196369-196410 | Cumulative damage tracking trigger |
| BuffRecordDamage | ~196300 | Damage recording for replay |
| BuffBlock | ~192900 | Block damage absorption |
| BuffNotControll | ~195000 | Control immunity |

### Animation & Model
| Module | Lines | Description |
|--------|-------|-------------|
| AnimatorCtr | 178947-179023 | Animation controller: config from UnitModel, frame-by-frame execution, trigger events |
| ConfigUnitModel | 267701-267920 | Unit model definitions with per-animation frame data (skill1-8, bigskill1-9) |
| ConfigAppearance | 218762-218852 | Weapon/artifact appearance: ani field (index 8) determines attack animation |
| getActSpeed | 431378-431389 | Attack speed calculation: `round(att_speed / round(30 / frameCount))` |

### PvP Systems
| Module | Lines | Description |
|--------|-------|-------------|
| ChapterArena | 197534-197544 | 1v1 PvP: avg level calc, injuryReduce/shieldDecay(0.4)/treatDecay(0.3) |
| ChapterMultipleArena (DoublePvp) | 202647-202660 | Multi-player PvP initialization |
| ChapterRogue | 203550-203560 | Rogue PvP initialization |
| ChapterTeam20 | ~203600 | Team 20 PvP mode |
| ChapterDoubleLadder | ~203650 | Double Ladder PvP mode |
| ConfigLevel | 242991-243045 | Level config: pvp_injury_reduce, power_par |

### Config Schemas (Key Tables)
| Module | Lines | Description |
|--------|-------|-------------|
| ConfigAttribute | 219864 | 12 fields: id, name, key, module, group, up_limit, num_type, etc. |
| ConfigUnit | 267178 | 97 fields (77 XOR-obfuscated): all combat stats, unit type, model |
| ConfigBuff | 222479 | 16 fields: id, group, action, param1-5, skillPar, time, etc. |
| ConfigSkill | 261531 | 28 fields: skillType, buffGroup, skillEffect, targetType, etc. |
| ConfigAngel | 218577 | Hero/angel schema |
| ConfigEquipment | 229175 | Equipment schema |
| ConfigFly | 233576 | Avian/bird schema (12 related tables) |
| ConfigGlobal | 235650 | 744 global constant keys |
| ConfigJobs | 239943 | Class/job schema |
| ConfigMount | 248453 | Mount schema |
| ConfigPet | 252193 | Pet/pal schema |
| ConfigRelic | 254905 | Relic schema |
| ConfigSeason_ship | 259623 | Ship/sailing schema |
| ConfigSpirit | 262760 | Spirit schema |
| ConfigSpecil_buff | ~262200 | Special buff definitions |

---

## HealthType Enum (Complete)

| ID | Name | Category |
|----|------|----------|
| 0 | Invalid | — |
| 1 | Hurt | Damage (basic) |
| 2 | Hurt_Crit | Damage (basic crit) |
| 3 | Hurt_Ret | Damage (return) |
| 4 | Treat | Healing |
| 5 | Treat_Crit | Healing (crit) |
| 6 | Miss | Miss |
| 7 | Absorb | Shield absorbed |
| 8 | Break | — |
| 9 | Double_Act | UI indicator |
| 10 | Counter_Act | UI indicator |
| 11 | Skill_Hpsteal | HP steal (skill) |
| 12 | Act_Hpsteal | HP steal (attack) |
| 13 | Hurt_Share_Damage | Shared/splash damage |
| 14 | Hurt_Share_Damage_Crit | Shared/splash crit |
| 15 | Hurt_Double | Combo hit damage |
| 16 | Hurt_Double_Crit | Combo hit crit |
| 17 | Dizz | Stun |
| 18 | Shield | Shield creation |
| 19 | Hurt_Bleed | Bleed damage |
| 20 | Real_Damage | True/real damage |
| 21 | Hurt_Counter | Counter damage |
| 22 | Hurt_Counter_Crit | Counter crit |
| 23 | Hurt_Bleed_Crit | Bleed crit |
| 24 | Call_unit_Hp | Summon HP |
| 25 | Call_unit_Att | Summon ATK |
| 26 | Suppress | Pal suppress |
| 27 | Inspire | Pal inspire |
| 28 | Armor | Armor penetration |
| 29 | Armor_def | Block |
| 30 | SpiritToSpirit | Spirit→Spirit damage |
| 31 | SpiritToPlayer | Spirit→Player damage |
| 50 | block | Block amount |
| 51 | Hp_recovery | Passive HP recovery |

**NeedAddDamHurtList** (types that count as damage dealt): [1, 2, 3, 13, 14, 15, 16, 20, 19, 23, 21, 22, 31]

---

## AttribDefine Enum (Complete)

| ID | Name | Description |
|----|------|-------------|
| 1001 | att | Attack |
| 1002 | hp | Hit Points |
| 1003 | att_speed | Attack Speed |
| 1004 | crit_rate | Critical Rate |
| 1005 | crit_dam | Critical Damage |
| 1006 | crit_def | Critical Defense (min 0.5) |
| 1007 | hit | Hit/Accuracy |
| 1008 | miss | Evasion |
| 1009 | speed | Movement Speed |
| 1010 | detection_range | Detection Range |
| 1011 | att_range | Attack Range |
| 1012 | hp_recovery | HP Recovery Rate |
| 1013 | power_recovery | Power Recovery Rate |
| 1014 | att_hpsteal | Attack HP Steal |
| 1015 | skill_hpsteal | Skill HP Steal |
| 1016 | double_hit | Combo/Double Hit Rate |
| 1017 | counter | Counter Rate |
| 1018 | att_resist | Basic ATK Resistance |
| 1019 | skill_resist | Skill Resistance |
| 1020 | partner_resist | Pal Resistance |
| 1021 | resist | DMG Resistance (Total) |
| 1022 | suspend | Knock-up/Launch Rate |
| 1023 | vertigo | Stun Rate |
| 1024 | def | Defense |
| 1025 | suspend_def | Knock-up Defense |
| 1026 | vertigo_def | Stun Defense |
| 1027 | att_hpsteal_def | ATK HP Steal Defense |
| 1028 | skill_hpsteal_def | Skill HP Steal Defense |
| 1029 | target_num | Target Count |
| 1030 | vertigo_times | Stun Duration Multiplier |
| 1031 | vertigo_res | Stun Duration Reduction |
| 1032 | double_hit_dam | Combo Damage Multiplier |
| 1033 | counter_dam | Counter Damage Multiplier |
| 1034 | double_hit_def | Combo Damage Resistance |
| 1035 | counter_def | Counter Damage Resistance |
| 1036 | counter_suspend | Counter Knock-up Rate |
| 1037 | skill_crit_rate | Skill Crit Rate |
| 1038 | skill_crit_dam | Skill Crit Damage Bonus |
| 1039 | att_dam | Basic ATK Multiplier |
| 1040 | partner_dam | Pal Damage Multiplier |
| 1041 | active_skillbuff_time | Skill Buff Duration |
| 1042 | CONTROL_RES | Control Resistance |
| 1043 | active_skilldamage_par | Active Skill Damage Factor |
| 1045 | skill_dam_extra | Skill Damage Extra Multiplier |
| 1046 | boss_dam | Boss Damage Bonus |
| 1047 | partner_dam_extra | Pal Damage Extra Multiplier |
| 1048 | ignore_double_hit | Ignore Combo Rate |
| 1049 | ignore_counter | Ignore Counter Rate |
| 1050 | shield_time_extra | Shield Duration Bonus |
| 1051 | shield_hp_extra | Shield HP Bonus |
| 1052 | boss_def | Boss Defense |
| 1053 | hpsteal_rate | HP Steal Proc Rate |
| 1054 | hpsteal_amount | HP Steal Amount |
| 1055 | hpsteal_res | HP Steal Resistance |
| 1056 | ignore_hpsteal | Ignore HP Steal |
| 1057 | pve_dam | PvE Damage Bonus |
| 1058 | pve_resist | PvE Damage Resistance |
| 1059 | season_cannon_att_def | Cannon/Gun ATK Defense |
| 1060 | def_coe | Defense Coefficient |
| 1061 | skillbuff_time_all | All Skill Buff Duration |
| 1062 | pve_extra_time | PvE Extra Time |
| 1064 | power_recovery_buff | Power Recovery Buff |
| 1065 | ignore_crit_rate | Ignore Crit Rate |
| 1066 | ignore_hp_recovery | Ignore HP Recovery |
| 1067 | armor_penetration_rate | Armor Pen Proc Rate |
| 1068 | armor_penetration | Armor Penetration Value |
| 1069 | ignore_armor_penetration | Ignore Armor Penetration |
| 1070 | block_rate | Block Proc Rate |
| 1071 | block | Block Value |
| 1072 | ignore_block | Ignore Block Value |
| 1073 | partner_inspire_rate | Pal Inspire Proc Rate |
| 1074 | partner_inspire | Pal Inspire Value |
| 1075 | ignore_partner_inspire | Ignore Pal Inspire |
| 1076 | partner_suppress_rate | Pal Suppress Proc Rate |
| 1077 | partner_suppress | Pal Suppress Value |
| 1078 | ignore_partner_suppress | Ignore Pal Suppress |
| 1079 | battle_attribute_def | Battle Attribute Defense |
| 1080 | battle_resist_def | Battle Resist Defense |
| 1081 | total_dam_add | Total DMG Bonus |
| 1082 | total_dam_def | Total DMG Resistance |
| 6001 | spirit_dam_add | Spirit DMG Bonus |
| 6002 | spirit_dam_def | Spirit DMG Defense |
| 6003 | spirit_dam_def_final | Spirit DMG Defense Final |
| 6004 | spirit_hp | Spirit HP |
| 6005 | spirit_att | Spirit ATK |
| 6006 | spirit_hp_add | Spirit HP Bonus |
| 6007 | spirit_att_add | Spirit ATK Bonus |

---

## Document Index

### Combat System (01-13)
| Doc | Title | Key Topics |
|-----|-------|------------|
| 01 | Basic Damage Calculation | normalHurt, ATK-DEF formula, multipliers |
| 02 | Combo/Counter/Skill Damage | normalDoubleHurt, normalCounterHurt, SkillHurt |
| 03 | Critical Hit System | checkSkillCirt, crit_dam/crit_def |
| 04 | PvP Damage Reduction | injuryReduce, level-based table |
| 05 | HP-Based Damage | BuffSkillHpHurt, skillPar, clamping |
| 06 | Shield System | BuffShield, 4 calTypes, shieldDecay |
| 07 | Total DMG Bonus/RES | total_dam_add/def, floor=0.20x |
| 08 | Pierce/Block/Inspire/Suppress | calArmorAndBlock, calSuppressAndInspire |
| 09 | Bleed Damage | BuffBleed, 8 types |
| 10 | Stun/Control/Ignore | checkDizz, vertigo, CONTROL_RES |
| 11 | Pal Damage | partner_dam, partner_dam_extra |
| 12 | Battle Flow & Normal Attack | SkillHandleNormal, turn sequence |
| 13 | FixMath & Rounding | round(), roundInt(), clamp() |

### Game Systems (14-24)
| Doc | Title | Key Topics |
|-----|-------|------------|
| 14 | Class/Job System | ConfigJobs, job_figure, model, wakeup |
| 15 | Equipment System | 5 equip slots, upgrade, enchant |
| 16 | Sailing/Season System | Ships, cannons, season buffs |
| 17 | Pet/Pal System | Battle loading, stat inheritance, combat formulas |
| 18 | Avian/Bird System | ConfigFly, hatching, breeding |
| 19 | Spirit System | spiritNormalHit, affix system |
| 20 | Mount System | Cosmetic + stat baking, abilities |
| 21 | Hero/Angel System | ConfigAngel, angel_skill enhancements |
| 22 | Skill Effect System | SkillType, skill handlers, effect triggers |
| 23 | Item/Goods System | ConfigGoods, item types |
| 24 | Relic System | ConfigRelic, relic effects |

### Reference & Encyclopedia (25-31)
| Doc | Title | Key Topics |
|-----|-------|------------|
| 25 | Buff Encyclopedia | 46 named + 34 data-only BuffGroupTypes (76 total), 80 buff classes, damage pipeline |
| 26 | Skill Effect & Triggers | EffectTriggerType cascades, StateTrigerType, cascade flow |
| 27 | Fate System | ConfigFate, gacha, fusion, passive skills |
| 28 | Path to Divinity | ConfigPath_affix, talent tree, attribute caps |
| 29 | Statue System | ConfigStatue_attr/level/pos, reroll/lock |
| 30 | Ring System | ConfigRing, ring levels, path connection |
| 31 | Config Table Reference | Master catalog of all 711 tables, XOR tables |
| 32 | Class & Skill Reference | Complete class tree, Tier 5 passives/actives, attribute reference |
| 33 | Systems Reference | Equipment, mounts, artifacts, pets, spirits, badges with stat values |
| 34 | PvP Meta Analysis | Damage pipeline exploits, class tier list, build guides, matchup matrix |

### Deep Dives (35-39)
| Doc | Title | Key Topics |
|-----|-------|------------|
| 35 | Motorcycle Mount Deep Dive | Mount 404 3-phase cycle, speed stacking, SpeedTrigger, overdrive buffs |
| 36 | Hidden Combat Mechanics | 0.98 skill crit exponent, DEFER_DAMAGE, speed cascade, PvP evasion formula |
| 37 | DEF Coefficient, Giant Slayer & Cleanse | def_coe in all damage formulas, Giant Slayer from Artifact 703, buff cleansability reference |
| 38 | Animation Speed Exploit | Weapon/artifact skin animation timing, first-hit advantage, artifact override trap |
| 39 | Clone & HP-Threshold Triggers | Clone Strike init (no passives), Rampage talent mechanics, Phoenix mount interaction |

### Meta (97-99)
| Doc | Title |
|-----|-------|
| 97 | Unknowns & Open Questions |
| 98 | Discrepancies (Code vs Yuko's PDF) |
| 99 | Full Damage Pipeline Reference |

---

## Data Directory Structure

```
data/
├── schemas/          # 711 auto-extracted Config module schemas
│   └── _index.json   # Master index
├── enums/            # 96 enum definitions
├── constants/        # 5 constant files (config_global, battle, attrib_caps, pvp, config_key)
├── formulas/
│   ├── combat/       # 15 damage function JSONs
│   ├── buffs/        # 9 buff formula JSONs + buff_group_mapping
│   ├── damage_pipeline.json
│   ├── stat_assembly.json
│   └── attribute_calculation.json
├── systems/          # Non-combat system JSONs (equipment, artifact, class, pets, etc.)
├── tables/           # 909 decoded config data tables (from decode_config_data.py)
│   ├── Level.json    # 220 levels with pvp_injury_reduce values
│   ├── Attribute.json # 192 attributes with caps (up_limit)
│   ├── Buff.json     # 4,155 buff entries across 76 groups
│   ├── Skill.json    # Complete skill configuration
│   ├── Unit.json     # All unit base stats (97 fields, 77 XOR-protected)
│   └── ...           # 904 additional config tables
└── proto_schema.json # Client-server protocol definitions
```
