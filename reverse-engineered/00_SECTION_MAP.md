# LOM Game Script — Section Map

**Source file:** `game_script_pretty.js` (457,538 lines, 28MB beautified)
**Generated from:** `game_script.js` (7,685 lines, 18MB minified)

---

## Key Module Locations

### Math & Utility
| Module | Lines | Description |
|--------|-------|-------------|
| FixMath | 292602-292620 | Fixed-point math: `round()`, `roundInt()`, `clamp()` |

### Enums & Definitions
| Module | Lines | Description |
|--------|-------|-------------|
| EnumDefine | 278546-278600 | HealthType, AttackType, StateType, DmgType, RunMode enums |
| AttribDefine (MetaAttrib) | 349630-349640 | All attribute IDs (att=1001, hp=1002, def=1024, etc.) |

### Battle Core
| Module | Lines | Description |
|--------|-------|-------------|
| BattleMain (init/reset) | 188200-188210 | Battle initialization, injuryReduce/shieldDecay/treatDecay defaults |
| HurtUtil | 322750-322980 | ALL core damage functions: normalHurt, normalDoubleHurt, normalCounterHurt, calHurt, calArmorAndBlock, calSuppressAndInspire, checkHit, checkDoubleAct, checkCounterAct, checkDizz, checkSkillCirt, SkillHurt |
| BattleData / setPlayerList | 187356-187530 | Player data setup, attribute initialization, pet/skill loading |

### Damage Application
| Module | Lines | Description |
|--------|-------|-------------|
| Unit.addDamage (healthType switch) | 449240-449365 | Master damage application: PvP reduction, shield absorption, HP modification, death handling |
| SkillHandleNormal | 429879-430068 | Normal attack execution: hit check, basic/double/counter damage, buff triggers |
| SkillHandleCounter | 429630-429700 | Counter-attack execution |

### Buff System — Damage Modifiers
| Module | Lines | Description |
|--------|-------|-------------|
| BuffBleed | 192750-192860 | Bleed damage (7 types: basic, HP%, skill, basic+resist, combo, counter, maxHP%) |
| BuffSkillValue | 195700-195970 | Skill damage: HP-based damage with clamping, skill crit, resist, multiple calc types |
| BuffShareDamage | 195095-195144 | Shared/splash damage propagation |
| BuffExtraDamage | 193948-194016 | Extra damage multiplier (fixed %, HP-loss based) |
| BuffGiantSlayer | 194132-194175 | HP-difference based damage bonus |
| BuffSkillFragileAdd | 195433-195468 | Fragile effect: flat bonus damage from attribute/HP |
| BuffVampire | 196720-196788 | Life steal with Total DMG Bonus/RES calculation |

### Buff System — Defense/Utility
| Module | Lines | Description |
|--------|-------|-------------|
| BuffShield | 195146-195250 | Shield creation, decay, damage absorption, duration |
| BuffTotalDamageTrigger | 196369-196410 | Cumulative damage tracking trigger |
| BuffSkillDamageAdd | ~196700 | Skill-specific damage bonus with Total DMG calc |

### PvP Systems
| Module | Lines | Description |
|--------|-------|-------------|
| ChapterArena | 197534-197544 | 1v1 PvP: avg level calc, injuryReduce/shieldDecay/treatDecay |
| ChapterMultipleArena (DoublePvp) | 202647-202660 | Multi-player PvP initialization |
| ChapterRogue | 203550-203560 | Rogue PvP initialization |
| ConfigLevel | 242991-243045 | Level config schema: pvp_injury_reduce, power_par |

### Config Data
| Module | Lines | Description |
|--------|-------|-------------|
| ConfigGlobal (defaults) | 235650-235710 | Default battle constants: miss_correct, shield_correct, hp_recovery_correct |
| battle_up_limit | 237427-237429 | Miss rate cap: [[1008, 8000]] |
| total_damage_add_down_limit | 237503 | Total DMG floor: 2000 (= 0.20x) |

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
