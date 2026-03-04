# 03 — Attributes

> All 89+ combat attributes with IDs, key names, initial values, types, and caps.

---

## Attribute Value Types

| num_type | Storage | Display | Example |
|----------|---------|---------|---------|
| 1 | Raw integer | Direct value | ATK 60 = 60 |
| 2 | Parts-per-10000 | Divide by 10000 | crit_dam 20000 = 2.0× |

---

## MetaAttrib Calculation

Each attribute goes through the MetaAttrib system:
```
final_value = min(roundInt(roundInt(base + addValue) * time + addExtraValue), up_limit)
```
- `base` — Base value from unit config
- `addValue` — Sum of all additive bonuses
- `time` — Multiplicative modifier (default 1.0)
- `addExtraValue` — Post-multiplier flat bonus
- `up_limit` — Hard cap (0 = no cap)

---

## Complete Attribute Registry

### Core Combat Stats

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1001 | att | 60 | 1 | Attack power |
| 1002 | hp | 1080 | 1 | Max hit points |
| 1003 | att_speed | 9000 | 2 | Attack speed (0.9 = 90%) |
| 1009 | speed | 300 | 1 | Movement speed |
| 1024 | def | 20 | 1 | Defense |
| 1060 | def_coe | 0 | 2 | DEF coefficient (amplifies DEF: effective_DEF = DEF × (1 + def_coe)) |
| 1029 | target_num | 1 | 1 | Max targets per attack |

### Critical System

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1004 | crit_rate | 0 | 2 | Critical hit rate |
| 1005 | crit_dam | 20000 | 2 | Critical damage multiplier (2.0×) |
| 1006 | crit_def | 10000 | 2 | Crit damage reduction (1.0×, floor 0.5) |
| 1037 | skill_crit_rate | 0 | 2 | Skill crit rate (separate from normal crit) |
| 1038 | skill_crit_dam | 10000 | 2 | Skill crit damage (1.0×) |
| 1065 | ignore_crit_rate | 0 | 2 | Reduces enemy crit rate |

### Hit / Evasion

| ID | Key | Initial | Cap | num_type | Description |
|----|-----|---------|-----|----------|-------------|
| 1007 | hit | 0 | — | 2 | Accuracy (reduces miss chance) |
| 1008 | miss | 0 | **8000 (80%)** | 2 | Evasion rate (only capped attribute) |

### Damage Type Multipliers

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1039 | att_dam | 10000 | 2 | Basic ATK damage multiplier (1.0×) |
| 1040 | partner_dam | — | 2 | Pal damage multiplier |
| 1047 | partner_dam_extra | 10000 | 2 | Pal damage extra multiplier (1.0×) |
| 1032 | double_hit_dam | 10000 | 2 | Combo damage multiplier (1.0×) |
| 1033 | counter_dam | 10000 | 2 | Counter damage multiplier (1.0×) |
| 1045 | skill_dam_extra | 10000 | 2 | Skill damage multiplier (1.0×) |
| 1043 | active_skilldamage_par | — | 2 | Active skill damage parameter |

### Damage Resistance

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1018 | att_resist | 0 | 2 | Basic ATK resistance |
| 1019 | skill_resist | 0 | 2 | Skill damage resistance |
| 1020 | partner_resist | 0 | 2 | Pal damage resistance (cap ~80%) |
| 1021 | resist | 0 | 2 | General damage resistance |
| 1034 | double_hit_def | 0 | 2 | Combo damage resistance |
| 1035 | counter_def | 0 | 2 | Counter damage resistance |

### Combo / Counter Triggers

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1016 | double_hit | 0 | 2 | Combo trigger rate |
| 1017 | counter | 0 | 2 | Counter trigger rate |
| 1048 | ignore_double_hit | 0 | 2 | Reduces enemy combo rate |
| 1049 | ignore_counter | 0 | 2 | Reduces enemy counter rate |
| 1036 | counter_suspend | 0 | 2 | Counter-knockup trigger rate |

### Control (CC) System

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1022 | suspend | 0 | 2 | Knockup/launch rate |
| 1023 | vertigo | 0 | 2 | Stun rate |
| 1025 | suspend_def | 0 | 2 | Knockup resistance |
| 1026 | vertigo_def | 0 | 2 | Stun resistance |
| 1030 | vertigo_times | 1 | 1 | Max stun procs per attack |
| 1031 | vertigo_res | 6000 | 2 | Stun recovery rate (0.6) |
| 1042 | CONTROL_RES | — | 2 | CC duration reduction |

### HP Recovery / Steal

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1012 | hp_recovery | 0 | 2 | HP regen rate per frame |
| 1013 | power_recovery | 10000 | 2 | Energy/power recovery (1.0×) |
| 1014 | att_hpsteal | 0 | 2 | Normal ATK lifesteal rate |
| 1015 | skill_hpsteal | 0 | 2 | Skill lifesteal rate |
| 1027 | att_hpsteal_def | 0 | 2 | Normal ATK lifesteal defense |
| 1028 | skill_hpsteal_def | 0 | 2 | Skill lifesteal defense |
| 1053 | hpsteal_rate | 0 | 2 | % HP steal trigger rate |
| 1054 | hpsteal_amount | 20 | 1 | % HP steal amount |
| 1055 | hpsteal_res | 0 | 2 | % HP steal resistance |
| 1056 | ignore_hpsteal | 0 | 2 | Ignore % HP steal |
| 1066 | ignore_hp_recovery | 0 | 2 | Reduces enemy HP regen |
| 1064 | power_recovery_buff | — | 2 | Power recovery buff |

### Pierce / Block System

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1067 | armor_penetration_rate | 3000 | 2 | Pierce trigger rate (30%) |
| 1068 | armor_penetration | 0 | 1 | Pierce amount |
| 1069 | ignore_armor_penetration | 0 | 1 | Ignore pierce |
| 1070 | block_rate | 3000 | 2 | Block trigger rate (30%) |
| 1071 | block | 0 | 1 | Block amount |
| 1072 | ignore_block | 0 | 1 | Ignore block |

### Inspire / Suppress System (Pal Combat)

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1073 | partner_inspire_rate | 3000 | 2 | Inspire trigger rate (30%) |
| 1074 | partner_inspire | 0 | 1 | Inspire amount |
| 1075 | ignore_partner_inspire | 0 | 1 | Ignore inspire |
| 1076 | partner_suppress_rate | 3000 | 2 | Suppress trigger rate (30%) |
| 1077 | partner_suppress | 0 | 1 | Suppress amount |
| 1078 | ignore_partner_suppress | 0 | 1 | Ignore suppress |

**Quirk:** In `calSuppressAndInspire`, inspire condition uses `partner_inspire` but probability uses `partner_suppress_rate`, and vice versa. The rate attributes are swapped.

### Shield System

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1050 | shield_time_extra | 0 | 2 | Shield duration bonus |
| 1051 | shield_hp_extra | 0 | 2 | Shield HP bonus |

### Boss / PvE

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1046 | boss_dam | — | 2 | Bonus damage vs bosses |
| 1052 | boss_def | 0 | 2 | Boss damage reduction |
| 1057 | pve_dam | 0 | 2 | PvE damage bonus |
| 1058 | pve_resist | 0 | 2 | PvE damage resistance |
| 1062 | pve_extra_time | — | 1 | PvE bonus time |

### Final Damage Layer

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1081 | total_dam_add | — | 2 | Final DMG Bonus (applied to ALL 13 damage types) |
| 1082 | total_dam_def | — | 2 | Final DMG Resistance |

### Battle Attributes

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1079 | battle_attribute_def | 0 | 2 | Battle attribute defense |
| 1080 | battle_resist_def | 0 | 2 | Battle resist defense |

### Buff / Skill Modifiers

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1041 | active_skillbuff_time | — | 2 | Active skill buff duration |
| 1061 | skillbuff_time_all | 0 | 2 | All skill buff duration bonus |

### Range / Detection

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1010 | detection_range | 300 | 1 | Detection range |
| 1011 | att_range | 300 | 1 | Attack range |

### Special / Naval

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1059 | season_cannon_att_def | — | 2 | Naval cannon resistance |

### Spirit Attributes

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 6001 | spirit_dam_add | — | 2 | Spirit damage bonus |
| 6002 | spirit_dam_def | — | 2 | Spirit damage resistance |
| 6003 | spirit_dam_def_final | — | 2 | Spirit final damage resist (percentage) |
| 6004 | spirit_hp | — | 1 | Spirit HP flat bonus |
| 6005 | spirit_att | — | 1 | Spirit ATK flat bonus |
| 6006 | spirit_hp_add | — | 2 | Spirit HP percentage multiplier |
| 6007 | spirit_att_add | — | 2 | Spirit ATK percentage multiplier |

### Global Damage Attributes (2000-series)

Used by gem sets, badges, and equipment advancement:

| ID | Key | Description |
|----|-----|-------------|
| 2002 | — | Global ATK % |
| 2009 | — | Global Crit DMG |
| 2011 | — | Global Crit RES |
| 2017 | — | Global Combo DMG |
| 2018 | — | Global Counter DMG |
| 2020 | — | Pal DMG Bonus |
| 2022 | — | Basic ATK DMG |
| 2023 | — | Global Basic ATK DMG |
| 2030 | — | Global Combo DMG (alternate) |
| 2031 | — | Global Counter DMG (alternate) |
| 2033 | — | Global Skill DMG |

---

## Caps Summary

| Attribute | ID | Cap Source | Cap Value |
|-----------|------|-----------|-----------|
| miss (evasion) | 1008 | battle_up_limit | 80% (PvP) |
| partner_resist | 1020 | formula/docs | ~80% |
| pierce/block amount | 1068/1071 | calArmorAndBlock | ±50% per hit |
| inspire/suppress amount | 1074/1077 | calSuppressAndInspire | ±50% per hit |
| crit multiplier | — | normalHurt formula | min 1.5× |
| crit_def | 1006 | normalHurt formula | floor 0.5 |
| total_dam multiplier | 1081-1082 | healthTarget formula | floor 0.20× |
| path affix per trunk | varies | ConfigPath_upper_limit | per-trunk caps |

---

## ConfigAttribute Schema

Each attribute in ConfigAttribute has 12 fields:

| Field | Description |
|-------|-------------|
| id | Attribute ID (e.g., 1001) |
| name | Localized name (string_ref) |
| key | Internal key string (e.g., "att") |
| type | Attribute category type |
| module | Module classification (1 = combat) |
| group | Grouping for UI display |
| num_type | Value type: 1 = raw integer, 2 = /10000 percentage |
| up_limit | Hard cap value (0 = no cap) |
| add_type | Addition type for stat assembly |
| desc | Description (string_ref) |
| show_type | UI display formatting |
| details | Detailed description (string_ref) |

---

## Stat Assembly Pipeline

Attributes are assembled from multiple sources:
```
1. Base Stats     → Unit config base values
2. Equipment      → base_attr + rand_attr + refinement + advancement + resonance + suit bonuses
3. Mount/Wings    → level attrs + ability attrs + skin attrs + talent attrs
4. Artifact       → level attrs + skin attrs + gem base + gem sub + gem set bonuses
5. Pet/Pal        → talent effects (ownership bonuses)
6. Angel          → star attrs + formation bonuses
7. Spirit         → affix bonuses
8. Fate Cards     → level attrs + fusion passive skills
9. Path/Divinity  → affix bonuses (with per-trunk caps)
10. Statue        → rolled attribute bonuses
11. Ring          → level attrs + base skills
12. Badge         → level attrs
13. Back/Wings    → level attrs + skin attrs + talent attrs
14. Relics        → equip bonuses + own bonuses
15. Buffs         → runtime attrib modifications
```
