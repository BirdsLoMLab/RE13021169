# 32 — Class & Skill Reference (Decoded Config Data)

> **Sources:** `Jobs.json`, `Skill.json`, `Skill_level.json`, `Buff.json`, `Language_en.json`
> **Scope:** Complete class tree, all Tier 6 class passives/actives with actual parameter values

---

## Complete Class Tree (38 Jobs, 5 Career Paths)

```
Starting: Shroomie (1001) → Adventurer (1002)

Path A — Warrior (job_class=2):
  Tier 1: Warrior (1101)
  Tier 2: Swordsman (1201) / Axe Warrior (1202)
  Tier 3: Claymore Wielder (1301) / Berserker (1302)
  Tier 4: Swordmaster (1401) / Warmonger (1402)
  Tier 5: Martial Sage (1511, type=2) / Warbringer (1512, type=5)

Path B — Archer (job_class=3):
  Tier 1: Archer (1102)
  Tier 2: Shadow Sniper (1203) / Wind Crossbower (1204)
  Tier 3: Sharpshooter (1303) / Dual Crossbower (1304)
  Tier 4: Shadow Hunter (1403) / Arrowgod (1404)
  Tier 5: Sacred Hunter (1521, type=3) / Plume Monarch (1522, type=6)

Path C — Mage (job_class=4):
  Tier 1: Mage (1103)
  Tier 2: Healer (1205) / Spellcaster (1206)
  Tier 3: Chronomancer (1305) / Storm Priest (1306)
  Tier 4: Holy Guide (1405) / Bishop (1406)
  Tier 5: Prophet (1531, type=4) / Darklord (1532, type=7)

Path D — Beast (job_class=5):
  Tier 1: Spirit Channeler (1104)
  Tier 2: Beast Tamer (1207) / Skeleton Mage (1208)
  Tier 3: Soul Hunter (1307) / Spirit Shepherd (1308)
  Tier 4: Beastsoul Master (1407) / ??? (1408)
  Tier 5: Beastmaster (1541, type=8) / Supreme Spirit (1542, type=9)
```

---

## Tier 5 (Final) Class Details

### Martial Sage (Job 1511) — Warrior Path 1

**Identity:** Tanky regen counter-attacker. Shield + HP regen + DMG RES makes this the most durable class.

**Active Skill — Blades Reunion (1053)**
- 15157% AoE DMG at lv220
- Reduce Counter DMG RES of targets by 40% for 8s
- Each counterstrike within 8s deals extra DMG equal to **1% of target's current HP**

**Passive Progression:**
| Unlock | Skill | Description | ownEffect |
|--------|-------|-------------|-----------|
| Lv30 | 2001 — Warrior 1st | Counter +30%, Counter Multiplier +30% | [1017, 3000], [1033, 3000] |
| Lv40 | 2005 — Warrior 1st | DEF +30% | [2006, 3000] |
| Lv50 | 2008 — 2nd Ascension | DMG RES +15% | [1021, 1500], [1057, 500] |
| Lv70 | 2033 — 4th Ascension (lv2) | Restore **8% Max HP every 5s** | — (buff-based) |
| Lv100 | 2022 — 3rd Ascension | Shield every 10s absorbing **8% max HP** for 5s | [1057, 500] + buff 20036 (trap) |

**PvP Notes:**
- The 8% HP/5s regen is enormous — this is the regen meta class
- Shield (8% HP every 10s) adds another survivability layer
- Counter + 1% current HP on-hit adds passive damage
- Countered by: REDUCE_HEAL (buff group 440), high burst, Ignore Counter

---

### Warbringer (Job 1512) — Warrior Path 2

**Identity:** Counter-attack specialist. Punishes attackers with massive reflected damage, gets stronger as HP drops.

**Active Skill — Shattering Axe (1054)**
- 15157% AoE DMG at lv220
- Reduce Counter DMG RES of targets by 40% for 8s
- Gain **0.15 DEF per 1 ATK** and **0.75 ATK per 1 DEF** for 8s (stat conversion)

**Passive Progression:**
| Unlock | Skill | Description | ownEffect |
|--------|-------|-------------|-----------|
| Lv30 | 2001 | Counter +30%, Counter Multiplier +30% | [1017, 3000], [1033, 3000] |
| Lv40 | 2005 | DEF +30% | [2006, 3000] |
| Lv50 | 2020 — 2nd Ascension | Counter DMG +**140%** | [2018, 14000] |
| Lv70 | 2123 — 3rd Ascension | Deal **20%** of current AoE Counter DMG when hit by basic/combos (can crit) | [1057, 500] + buff 20002 + buff 20107 (trap) |
| Lv100 | 2028 — 4th Ascension | ATK scales with HP loss: every **10%** HP lost → ATK **+3%** | buff 20028 (attrib_condition, attr 1001) |

**PvP Notes:**
- +140% Counter DMG + 30% Counter Multiplier = devastating counter damage
- Passive AoE counter (20% of counter DMG) when hit means attackers hurt themselves
- ATK +3% per 10% HP lost (max +30% at 0 HP) synergizes with being hit
- Active skill's stat conversion (ATK↔DEF) is unique but temporary (8s)
- Countered by: Ignore Counter (1049), not attacking (let the Warbringer time out)

---

### Sacred Hunter (Job 1521) — Archer Path 1

**Identity:** Burst DPS assassin. Crit-scaling, HP%-based extra damage, and energy denial shut down opponents.

**Active Skill — Piercing Boneforge (1055)**
- 15157% AoE DMG at lv220
- Reduce Combo DMG RES of targets by 40% for 8s
- **Block energy regen** on 6 active skills for **4s** (skill lockout)

**Passive Progression:**
| Unlock | Skill | Description | ownEffect |
|--------|-------|-------------|-----------|
| Lv30 | 2003 | Combo +30% | [1016, 3000] |
| Lv40 | 2007 | ATK Speed +15%, Ignore Evasion +10% | [2021, 1500], [1007, 1000] |
| Lv50 | 2021 — 2nd Ascension | Base Crit DMG +20% | [1005, 2000] |
| Lv70 | 2126 — 3rd Ascension | Basic attacks deal **1% of target's current HP** as extra DMG | — (buff 20039: skill_effect) |
| Lv100 | 2031 — 4th Ascension | After crit → ATK **+40%** for 1s | buff 20033 (skill_effect) |

**PvP Notes:**
- 1% target current HP on every basic attack = consistent HP% damage
- Post-crit ATK +40% (1s) creates burst windows
- Energy denial (4s skill lockout) shuts down active skill rotations
- ATK Speed +15% means more hits = more HP% procs
- Countered by: Basic ATK DMG RES (1018), shields, high evasion

---

### Plume Monarch (Job 1522) — Archer Path 2

**Identity:** Multi-hit combo specialist. Extra bullets on every attack generate massive combo hit counts.

**Active Skill — Sun Pursuit (1056)**
- 15157% AoE DMG at lv220
- Reduce Combo DMG RES of targets by 40% for 8s
- **Ignore enemy evasion** for 10s

**Passive Progression:**
| Unlock | Skill | Description | ownEffect |
|--------|-------|-------------|-----------|
| Lv30 | 2003 | Combo +30% | [1016, 3000] |
| Lv40 | 2007 | ATK Speed +15%, Ignore Evasion +10% | [2021, 1500], [1007, 1000] |
| Lv50 | 2013 — 2nd Ascension | Combo DMG +**140%** | [2017, 14000] |
| Lv70 | 2118 — 3rd Ascension | **+3 extra bullets** during combos | buff 20040 (double_hit_num, 10% per bullet) |
| Lv100 | 2032 — 4th Ascension | **+2 extra bullets** during basic attacks | buff 20035 (double_hit_num, 20% per bullet) |

**PvP Notes:**
- +2 basic bullets (20% proc each) + +3 combo bullets (10% proc each) = maximum hit count
- Each extra bullet can trigger combos/crits independently
- +140% Combo DMG + 30% Combo Rate = combo multiplier stacking
- 10s full evasion ignore from active = guaranteed hits vs dodge builds
- Countered by: Combo DMG RES (1034), Ignore Combo (1048), Counter builds (more hits = more counters)

---

### Prophet (Job 1531) — Mage Path 1

**Identity:** Skill-spam support. Faster energy, longer buffs, shield-breaking, and stun-based cooldown reduction.

**Active Skill — Crane's Whisper (1057)**
- 15157% AoE DMG at lv220
- Reduce Skill DMG RES of targets by **20%** for 8s
- **Break enemy shields instantly** with attacks within 10s

**Passive Progression:**
| Unlock | Skill | Description | ownEffect |
|--------|-------|-------------|-----------|
| Lv30 | 2002 | Skill Crit +15% | [1037, 1500] |
| Lv40 | 2004 | ATK +12% | [2002, 1200] |
| Lv50 | 2016 — 2nd Ascension | Active Skill Energy Regen +20% | [2016, 2000] |
| Lv70 | 2124 — 3rd Ascension | Prolong active skills by **40%**, boost DMG by **10%** | [2024, 4000] + buff 20037 (attrib 1045) |
| Lv100 | 2029 — 4th Ascension | Every 1 stun trigger → all active skill CDs **-0.3s** | buff 20026 (skill_effect) |

**PvP Notes:**
- Shield-breaking counters Martial Sage's shield directly
- +20% energy regen + stun-based CD reduction = more active skill casts
- +40% skill duration + 10% DMG bonus = strong buff uptime
- Only -20% Skill RES (vs -40% for warrior/archer actives) = lower debuff
- Countered by: Stun immunity (high Ignore Stun), fast kill before skill rotation

---

### Darklord (Job 1532) — Mage Path 2

**Identity:** Pure skill damage glass cannon. Highest skill crit stats, real damage that bypasses immunity, scales with HP loss.

**Active Skill — Galaxy Dive (1058)**
- 15157% AoE DMG at lv220
- Reduce Skill DMG RES of targets by **20%** for 8s
- Boost Base Skill Crit DMG by **+50%** for 10s

**Passive Progression:**
| Unlock | Skill | Description | ownEffect |
|--------|-------|-------------|-----------|
| Lv30 | 2002 | Skill Crit +15% | [1037, 1500] |
| Lv40 | 2004 | ATK +12% | [2002, 1200] |
| Lv50 | 2017 — 2nd Ascension | Skill Crit DMG +**50%**, Skill Crit +15% | [1038, 5000], [1037, 1500] |
| Lv70 | 2125 — 3rd Ascension | All skills deal **20% extra DMG** (ignores Immunity) | buff 20078 (skill_real_damage, group 290) |
| Lv100 | 2030 — 4th Ascension | Skill DMG scales with HP loss: every **10%** lost → Skill DMG **+3%** | buff 20030 (attrib_condition) |

**PvP Notes:**
- Total Skill Crit from passives: +30% (2002 at lv30 + 2017 at lv50)
- Total Skill Crit DMG: +50% (2017) + 50% (active) = +100% during active
- 20% extra damage that **ignores immunity** = true/real damage component
- HP-loss scaling (+3% per 10% lost) makes Darklord dangerous when low
- Countered by: Burst before skill rotation, Skill DMG RES (1019), healing/shields

---

### Beastmaster (Job 1541) — Beast Path 1

**Identity:** Pal damage multiplier stacking. Extra pal slot + pal crit + pal DMG scaling creates highest pal DPS.

**Active Skill — Tamer of Beasts (1066)**
- 15166% AoE DMG at lv220
- Reduce Pal DMG RES of targets by **20%** for 8s
- Pals **ignore enemy evasion** for 10s

**Passive Progression:**
| Unlock | Skill | Description | ownEffect |
|--------|-------|-------------|-----------|
| Lv30 | 2101 | **+1 Pal slot** | — |
| Lv40 | 2102 | Pal ATK SPD +10%, Ignore Evasion +10% | [1003, 1000], [1007, 1000] |
| Lv50 | 2103 | Pal Crit Rate +25%, Crit DMG +20% | [1004, 2500], [1005, 2000] |
| Lv70 | 2114 — 3rd Enhanced | Pal DMG Multiplier +**20%** | [2032, 2000] |
| Lv100 | 2105 — 4th Evolution | Pal DMG scales with HP loss: every **10%** lost → Pal DMG **+3%** | buff 20054 (attrib_condition, attr 1047) |

**PvP Notes:**
- Extra pal slot = additional damage source with its own attack cycle
- +25% Pal Crit + 20% Pal Crit DMG = pal crits hit hard
- +20% Pal DMG Multiplier (attr 2032) is a multiplicative bonus
- HP-loss scaling on pal damage (+3% per 10% lost, max +30%)
- Countered by: Pal DMG RES (1020, caps at 80%), AoE that kills pals

---

### Supreme Spirit (Job 1542) — Beast Path 2

**Identity:** Pal synergy/race bonuses. Deploy effects + race combinations for flexible team building.

**Active Skill — Wilting Souls (1067)**
- 15166% AoE DMG at lv220
- Reduce Pal DMG RES of targets by **20%** for 8s
- Pals gain **40% chance** of dealing **1% target current HP** extra DMG for 8s

**Passive Progression:**
| Unlock | Skill | Description | ownEffect |
|--------|-------|-------------|-----------|
| Lv30 | 2101 | **+1 Pal slot** | — |
| Lv40 | 2102 | Pal ATK SPD +10%, Ignore Evasion +10% | [1003, 1000], [1007, 1000] |
| Lv50 | 2106 | Enhance Pal Deploy Effects by **20%** | — |
| Lv70 | 2117 — 3rd Enhanced | Extra effects based on first 2 pals' races (no stack) | — |
| Lv100 | 2108 — 4th Evolution | Extra effects based on deployed pal race count | — |

**PvP Notes:**
- 40% chance of 1% HP damage per pal hit is strong HP% damage
- Race-based bonuses depend on pal lineup composition
- Deploy effect enhancement benefits summon-type pals
- Less raw pal damage than Beastmaster, more utility/flexibility
- Countered by: Pal DMG RES (1020), burst damage

---

## Key Anti-Regen Mechanics

### REDUCE_HEAL (Buff Group 440)
Found in buff IDs: 50815, 50843, 51612, 180352, 300033

| Buff ID | param1 (type) | param2 (amount) | Notes |
|---------|--------------|-----------------|-------|
| 50815 | 1 | 10000 (100%) | Full heal reduction |
| 50843 | 0 | 10000 (100%) | Full heal reduction |
| 51612 | 0 | 10000 (100%) | Full heal reduction |
| 180352 | 1 | 30000 (300%) | Over-reduction (prevents ALL healing) |
| 300033 | 0 | 10000 (100%) | Full heal reduction |

### Related Attributes
- **1055 — Healing RES:** Reduces incoming healing
- **1056 — Ignore Healing:** Bypasses healing
- **1066 — Ignore HP Recovery:** Counters passive HP regen (attr 1012)

---

## Passive Imprint Slots (GvG Win Streak Buffs)

All Tier 4-5 classes share 6 imprint slots with GvG buff choices:

| Slot | Options | Buff Groups |
|------|---------|-------------|
| 1 | 10001 (fixed) | [90001, 90002], par=23131 |
| 2 | 10002 (fixed) | [90001, 90002], par=22083 |
| 3 | 10003 (fixed) | [90001, 90002], par=21035 |
| 4 | **10004** / 10009 / 10010 | par=19987 / 32435 / 31919 |
| 5 | 10005 (fixed) | [90001, 90002], par=19195 |
| 6 | **10006** / 10007 / 10008 | par=18147 / 17099 / 16583 |

---

## Complete Attribute Reference (Combat-Relevant)

### Primary Stats (1001-1082)
| ID | Key | English Name | PvP Role |
|----|-----|-------------|----------|
| 1001 | att | ATK | Base damage scaling |
| 1002 | hp | HP | Survivability |
| 1003 | att_speed | ATK SPD | Hit frequency |
| 1004 | crit_rate | Crit Rate | Burst potential |
| 1005 | crit_dam | Crit DMG | Burst multiplier |
| 1006 | crit_def | Crit RES | Min 0.5x |
| 1007 | hit | Ignore Evasion | Anti-dodge |
| 1008 | miss | Evasion | Dodge chance |
| 1012 | hp_recovery | HP Regen | Sustain |
| 1013 | power_recovery | Energy Regen | Skill frequency |
| 1014 | att_hpsteal | Basic ATK Lifesteal | Sustain |
| 1015 | skill_hpsteal | Skill Lifesteal | Sustain |
| 1016 | double_hit | Combo Rate | Multi-hit proc |
| 1017 | counter | Counter Rate | Reflect proc |
| 1018 | att_resist | Basic ATK DMG RES | Anti-basic |
| 1019 | skill_resist | Skill DMG RES | Anti-skill |
| 1020 | partner_resist | Pal DMG RES | Anti-pal (cap 80%) |
| 1021 | resist | Total DMG RES | Universal defense |
| 1023 | vertigo | Stun Rate | CC |
| 1024 | def | DEF | Armor |
| 1026 | vertigo_def | Ignore Stun | Anti-CC |
| 1032 | double_hit_dam | Combo Multiplier | Combo scaling |
| 1033 | counter_dam | Counter Multiplier | Counter scaling |
| 1034 | double_hit_def | Combo DMG RES | Anti-combo |
| 1035 | counter_def | Counter DMG RES | Anti-counter |
| 1037 | skill_crit_rate | Skill Crit Rate | Skill burst |
| 1038 | skill_crit_dam | Skill Crit DMG | Skill burst multiplier |
| 1039 | att_dam | Basic ATK Multiplier | Basic scaling |
| 1040 | partner_dam | Pal DMG Multiplier | Pal scaling |
| 1045 | skill_dam_extra | Skill DMG Extra | Skill scaling |
| 1047 | partner_dam_extra | Pal DMG Extra | Pal scaling |
| 1048 | ignore_double_hit | Ignore Combo | Anti-combo proc |
| 1049 | ignore_counter | Ignore Counter | Anti-counter proc |
| 1065 | ignore_crit_rate | Ignore Crit Rate | Anti-crit |
| 1066 | ignore_hp_recovery | Ignore HP Regen | Anti-sustain |
| 1067 | armor_pen_rate | Pierce Rate | Armor bypass proc |
| 1068 | armor_penetration | Pierce Value | Armor bypass amount |
| 1069 | ignore_armor_pen | Ignore Pierce | Anti-pierce |
| 1070 | block_rate | Block Rate | Damage block proc |
| 1071 | block | Block Value | Block amount |
| 1072 | ignore_block | Ignore Block | Anti-block |
| 1081 | total_dam_add | **Final DMG Bonus** | Universal multiplier |
| 1082 | total_dam_def | **Final DMG RES** | Universal defense |

### Derived/Bonus Stats (2001-2033)
| ID | Key | English Name |
|----|-----|-------------|
| 2001 | base_att | Base ATK |
| 2002 | global_att | Global ATK % |
| 2003 | base_hp | Base HP |
| 2004 | global_hp | Global HP % |
| 2005 | base_def | Base DEF |
| 2006 | global_def | Global DEF % |
| 2007 | base_att_speed | Base ATK SPD % |
| 2008 | crit_dam_bonus | Crit DMG Bonus |
| 2009 | global_crit_dam | Global Crit DMG |
| 2010 | crit_res_bonus | Crit RES Bonus |
| 2011 | global_crit_res | Global Crit RES |
| 2016 | base_energy_regen | Base Energy Regen % |
| 2017 | combo_dam | Combo DMG |
| 2018 | counter_dam | Counter DMG |
| 2020 | pal_dam_bonus | Pal DMG Bonus |
| 2021 | current_att_speed | Current ATK SPD % |
| 2022 | basic_atk_dam | Basic ATK DMG |
| 2023 | global_basic_atk_dam | Global Basic ATK DMG |
| 2024 | skill_buff_duration | Skill Buff Duration Bonus |
| 2030 | global_combo_dam | Global Combo DMG |
| 2031 | global_counter_dam | Global Counter DMG |
| 2032 | pal_dam_multi_bonus | Pal DMG Multiplier Bonus |
| 2033 | global_skill_dam | Global Skill DMG |
