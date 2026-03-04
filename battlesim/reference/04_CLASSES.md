# 04 — Classes

> All 8 Tier 5 classes: passives, actives, ownEffect arrays.

---

## Class Tree Structure

```
Starting: Shroomie (1001) → Adventurer (1002)

Warrior Path (job_class=2):
  T1: Warrior (1101)
  T2: Swordsman (1201) / Axe Warrior (1202)
  T3: Claymore Wielder (1301) / Berserker (1302)
  T4: Swordmaster (1401) / Warmonger (1402)
  T5: Martial Sage (1511, type=2) / Warbringer (1512, type=5)

Archer Path (job_class=3):
  T1: Archer (1102)
  T2: Shadow Sniper (1203) / Wind Crossbower (1204)
  T3: Sharpshooter (1303) / Dual Crossbower (1304)
  T4: Shadow Hunter (1403) / Arrowgod (1404)
  T5: Sacred Hunter (1521, type=3) / Plume Monarch (1522, type=6)

Mage Path (job_class=4):
  T1: Mage (1103)
  T2: Healer (1205) / Spellcaster (1206)
  T3: Chronomancer (1305) / Storm Priest (1306)
  T4: Holy Guide (1405) / Bishop (1406)
  T5: Prophet (1531, type=4) / Darklord (1532, type=7)

Beast Path (job_class=5):
  T1: Spirit Channeler (1104)
  T2: Beast Tamer (1207) / Skeleton Mage (1208)
  T3: Soul Hunter (1307) / Spirit Shepherd (1308)
  T4: Beastsoul Master (1407) / ??? (1408)
  T5: Beastmaster (1541, type=8) / Supreme Spirit (1542, type=9)
```

---

## 1. Martial Sage (Job 1511, type=2)

**Identity:** Tanky regen counter-attacker. Shield + HP regen + DMG RES.

### Active Skill — Blades Reunion (ID: 1053)
- 15157% AoE DMG at lv220
- Reduce Counter DMG RES of targets by 40% for 8s
- Each counterstrike within 8s deals extra DMG equal to **1% of target's current HP**

### Passive Skills

| Level | Skill ID | Effect | ownEffect |
|-------|----------|--------|-----------|
| Lv30 | 2001 | Counter +30%, Counter Multiplier +30% | `[1017, 3000], [1033, 3000]` |
| Lv40 | 2005 | DEF +30% | `[2006, 3000]` |
| Lv50 | 2008 | DMG RES +15% | `[1021, 1500], [1057, 500]` |
| Lv70 | 2033 | Restore **8% Max HP every 5s** | buff 20033 |
| Lv100 | 2022 | Shield every 10s absorbing **8% max HP** for 5s | `[1057, 500]` + buff 20036 |

---

## 2. Warbringer (Job 1512, type=5)

**Identity:** Counter-attack specialist. Gets stronger as HP drops.

### Active Skill — Shattering Axe (ID: 1054)
- 15157% AoE DMG at lv220
- Reduce Counter DMG RES of targets by 40% for 8s
- Gain **0.15 DEF per 1 ATK** and **0.75 ATK per 1 DEF** for 8s (stat conversion)

### Passive Skills

| Level | Skill ID | Effect | ownEffect |
|-------|----------|--------|-----------|
| Lv30 | 2001 | Counter +30%, Counter Multiplier +30% | `[1017, 3000], [1033, 3000]` |
| Lv40 | 2005 | DEF +30% | `[2006, 3000]` |
| Lv50 | 2020 | Counter DMG +**140%** | `[2018, 14000]` |
| Lv70 | 2123 | Deal **20%** of counter DMG as AoE when hit (can crit) | `[1057, 500]` + buff 20002 + 20107 |
| Lv100 | 2028 | Per 10% HP lost → ATK **+3%** | buff 20028 (attrib_condition) |

---

## 3. Sacred Hunter (Job 1521, type=3)

**Identity:** Burst DPS assassin. Crit-scaling, HP%-based extra damage, energy denial.

### Active Skill — Piercing Boneforge (ID: 1055)
- 15157% AoE DMG at lv220
- Reduce Combo DMG RES of targets by 40% for 8s
- **Block energy regen** on 6 active skills for **4s**

### Passive Skills

| Level | Skill ID | Effect | ownEffect |
|-------|----------|--------|-----------|
| Lv30 | 2003 | Combo +30% | `[1016, 3000]` |
| Lv40 | 2007 | ATK Speed +15%, Ignore Evasion +10% | `[2021, 1500], [1007, 1000]` |
| Lv50 | 2021 | Base Crit DMG +20% | `[1005, 2000]` |
| Lv70 | 2126 | Basic attacks deal **1% of target's current HP** as extra DMG | buff 20039 |
| Lv100 | 2031 | After crit → ATK **+40%** for 1s | buff 20033 |

---

## 4. Plume Monarch (Job 1522, type=6)

**Identity:** Multi-hit combo specialist. Extra bullets on every attack.

### Active Skill — Sun Pursuit (ID: 1056)
- 15157% AoE DMG at lv220
- Reduce Combo DMG RES of targets by 40% for 8s
- **Ignore enemy evasion** for 10s

### Passive Skills

| Level | Skill ID | Effect | ownEffect |
|-------|----------|--------|-----------|
| Lv30 | 2003 | Combo +30% | `[1016, 3000]` |
| Lv40 | 2007 | ATK Speed +15%, Ignore Evasion +10% | `[2021, 1500], [1007, 1000]` |
| Lv50 | 2013 | Combo DMG +**140%** | `[2017, 14000]` |
| Lv70 | 2118 | **+3 extra bullets** during combos | buff 20040 (10% per bullet) |
| Lv100 | 2032 | **+2 extra bullets** during basic attacks | buff 20035 (20% per bullet) |

---

## 5. Prophet (Job 1531, type=4)

**Identity:** Skill-spam support. Faster energy, longer buffs, shield-breaking, stun-based CD reduction.

### Active Skill — Crane's Whisper (ID: 1057)
- 15157% AoE DMG at lv220
- Reduce Skill DMG RES of targets by **20%** for 8s
- **Break enemy shields instantly** with attacks within 10s

### Passive Skills

| Level | Skill ID | Effect | ownEffect |
|-------|----------|--------|-----------|
| Lv30 | 2002 | Skill Crit +15% | `[1037, 1500]` |
| Lv40 | 2004 | ATK +12% | `[2002, 1200]` |
| Lv50 | 2016 | Active Skill Energy Regen +20% | `[2016, 2000]` |
| Lv70 | 2124 | Prolong active skills by **40%**, boost DMG by **10%** | `[2024, 4000]` + buff 20037 |
| Lv100 | 2029 | Every 1 stun trigger → all active skill CDs **-0.3s** | buff 20026 |

---

## 6. Darklord (Job 1532, type=7)

**Identity:** Pure skill damage glass cannon. Highest skill crit stats, real damage bypassing immunity.

### Active Skill — Galaxy Dive (ID: 1058)
- 15157% AoE DMG at lv220
- Reduce Skill DMG RES of targets by **20%** for 8s
- Boost Base Skill Crit DMG by **+50%** for 10s

### Passive Skills

| Level | Skill ID | Effect | ownEffect |
|-------|----------|--------|-----------|
| Lv30 | 2002 | Skill Crit +15% | `[1037, 1500]` |
| Lv40 | 2004 | ATK +12% | `[2002, 1200]` |
| Lv50 | 2017 | Skill Crit DMG +**50%**, Skill Crit +15% | `[1038, 5000], [1037, 1500]` |
| Lv70 | 2125 | All skills deal **20% extra DMG** (ignores Immunity) | buff 20078 (skill_real_damage) |
| Lv100 | 2030 | Per 10% HP lost → Skill DMG **+3%** | buff 20030 (attrib_condition) |

---

## 7. Beastmaster (Job 1541, type=8)

**Identity:** Pal damage multiplier stacking. Extra pal slot + pal crit + pal DMG scaling.

### Active Skill — Tamer of Beasts (ID: 1066)
- 15166% AoE DMG at lv220
- Reduce Pal DMG RES of targets by **20%** for 8s
- Pals **ignore enemy evasion** for 10s

### Passive Skills

| Level | Skill ID | Effect | ownEffect |
|-------|----------|--------|-----------|
| Lv30 | 2101 | **+1 Pal slot** | — |
| Lv40 | 2102 | Pal ATK SPD +10%, Ignore Evasion +10% | `[1003, 1000], [1007, 1000]` |
| Lv50 | 2103 | Pal Crit Rate +25%, Crit DMG +20% | `[1004, 2500], [1005, 2000]` |
| Lv70 | 2114 | Pal DMG Multiplier +**20%** | `[2032, 2000]` |
| Lv100 | 2105 | Per 10% HP lost → Pal DMG **+3%** | buff 20054 (attrib_condition) |

---

## 8. Supreme Spirit (Job 1542, type=9)

**Identity:** Pal synergy/race bonuses. Deploy effects + race combinations.

### Active Skill — Wilting Souls (ID: 1067)
- 15166% AoE DMG at lv220
- Reduce Pal DMG RES of targets by **20%** for 8s
- Pals gain **40% chance** of dealing **1% target current HP** extra DMG for 8s

### Passive Skills

| Level | Skill ID | Effect | ownEffect |
|-------|----------|--------|-----------|
| Lv30 | 2101 | **+1 Pal slot** | — |
| Lv40 | 2102 | Pal ATK SPD +10%, Ignore Evasion +10% | `[1003, 1000], [1007, 1000]` |
| Lv50 | 2106 | Enhance Pal Deploy Effects by **20%** | — |
| Lv70 | 2117 | Extra effects based on first 2 pals' races (no stack) | — |
| Lv100 | 2108 | Extra effects based on deployed pal race count | — |

---

## ConfigJobs Schema (28 Fields)

| # | Field | Type | Description |
|---|-------|------|-------------|
| 0 | id | number | Unique job ID |
| 1 | name | string_ref | Localized name |
| 2 | type | number | Job type (equipment wearability) |
| 5 | skill | array | Active skill IDs |
| 6 | passive_skill | array | Passive skill IDs |
| 7 | passive_imprint | array | GvG passive imprint skills |
| 9 | job_change | array | Available promotion targets |
| 20 | front_job | number | Pre-requisite job ID |
| 21 | unlock | number | Unlock level |
| 27 | job_class | number | Class grouping (2=Warrior, 3=Archer, 4=Mage, 5=Beast) |

---

## Class Shared Passives Summary

| Lv30 | Warriors | Archers | Mages | Beast |
|------|----------|---------|-------|-------|
| Effect | Counter +30%, Counter Mult +30% | Combo +30% | Skill Crit +15% | +1 Pal Slot |

| Lv40 | Warriors | Archers | Mages | Beast |
|------|----------|---------|-------|-------|
| Effect | DEF +30% | ATK SPD +15%, Hit +10% | ATK +12% | Pal SPD +10%, Hit +10% |

---

## Key ownEffect Attribute IDs

| ID | Meaning |
|----|---------|
| 1005 | crit_dam |
| 1007 | hit (ignore evasion) |
| 1016 | double_hit (combo rate) |
| 1017 | counter (counter rate) |
| 1021 | resist (DMG RES) |
| 1033 | counter_dam |
| 1037 | skill_crit_rate |
| 1038 | skill_crit_dam |
| 1057 | pve_dam |
| 2002 | global ATK % |
| 2006 | global DEF % |
| 2016 | energy regen % |
| 2017 | combo DMG |
| 2018 | counter DMG |
| 2021 | ATK speed % |
| 2024 | skill buff duration |
| 2032 | pal DMG multiplier bonus |
