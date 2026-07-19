# Legend of Mushroom — Config Tables Master Reference

**A guide to the game's 909 configuration tables: how they are stored, how to decode and read them, how they join together, and the combat & progression formulas they drive.**

Reverse-engineering reference for the LOM battle-mechanics project.
Compiled by **Bird → Discord @birrrd08**. Data decoded from the shipped client config (`bundle-firstload-res`) and cross-checked against `game_script_pretty.js`.

---

## 0. What this document is

The LOM client ships **one binary blob** that decompresses into **909 config tables** (≈4,800 fields). Everything the game "knows" — every unit's stats, every skill coefficient, every soul's essence cost, every shop price, every language string — lives in those tables. The game engine is mostly generic; the *content* is data.

This reference covers three things:

1. **How to get the data** — the decode pipeline, the two obfuscation layers, and the schema system (Part 1).
2. **How to read and join tables** — main keys, foreign keys, attribute IDs, and language references (Part 2).
3. **What the tables mean** — the attribute model, the damage pipeline, the progression systems, and the exact formulas each table feeds (Parts 3–5), with worked examples (Part 6).

Part 7 is the **complete catalog** of all 909 tables grouped by system, with row counts, primary keys, and field shapes.

> **Convention.** Table names are written `Like_this` (matching the decoded JSON file names, e.g. `Fate_level.json`). Attribute keys are `like_this`. Numbers marked "basis points" are stored ×100 (a stored `13620` means `136.20%`) or ×10000 depending on the field — see §3.2.

---

# Part 1 — How the config system works

## 1.1 Where the data lives

The full config set is a single file shipped inside the first-load asset bundle:

```
…/bundle-firstload-res/native/<hash>/<hash>.8e8a4.bin      (~12.4 MB)
```

It is a **FilePack v5** container holding 908 named tables (plus the language pack). At runtime the client loads it via `BaseConfig.loadBufferData()`; individual tables are also loadable as plain JSON via `BaseConfig.loadData()` in dev builds.

## 1.2 The decode pipeline (two obfuscation layers)

There are **two independent obfuscation layers**. Decoding is done by `decode_config_data.py` in the repo root:

```
python3 decode_config_data.py <capture_dir> --output data/tables
```

**Layer A — the binary blob** (whole-file):

1. **XOR de-obfuscate** each byte: `byte = 255 & ~(32 ^ byte)`
2. **zlib decompress** the result
3. **Parse records:** `count (4B big-endian)` then `count × [ str_len (2B BE) + JSON_string ]`
4. **Map positional arrays → named fields** using the schema for that table

**Layer B — protected numeric fields** (per-field, combat-critical only):

5. Certain integer fields are additionally XOR'd with the **config key `24455`**. Decode with `realValue = rawValue ^ 24455`. Only **5 tables** use this anti-tamper layer (see §1.5).

The same two-key idea appears in the running client: `CONFIG_KEY = 24455` (used on protected fields) and the byte transform `255 & ~(32 ^ b)` (used on the blob). The `_checkValue = baseValue XOR 32` anti-cheat guard on live attributes is the same `32` constant.

## 1.3 The schema system

Every table has a schema, extracted to `data/schemas/ConfigXxx.json` (700 of 909 tables have one; the rest are trivial or language packs). A schema tells you the field order and which fields are obfuscated:

```json
{
  "className": "ConfigFate_level",
  "tableName": "Fate_level",
  "sourceLine": 231902,
  "mainKey": "fate_id",
  "indexedKeys": { "fate_id": 0, "level": 1 },
  "usesConfigKey": true,
  "fieldCount": 7,
  "fields": [
    { "name": "fate_id", "index": 0, "type": "number",         "xor": false },
    { "name": "level",   "index": 1, "type": "number",         "xor": false },
    { "name": "expend",  "index": 2, "type": "optional_array", "xor": false },
    { "name": "attr",    "index": 3, "type": "optional_array", "xor": false }
  ]
}
```

`data/schemas/_index.json` is a compact master index (className, tableName, sourceLine, mainKey, fieldCount, usesConfigKey) for quick lookup without opening 700 files.

### Field types

| Type | Meaning |
|---|---|
| `number` | Plain integer |
| `string_ref` | **Language string ID** — resolve via the `Language_*` tables (see §2.3) |
| `bignum` | Large number (HP/ATK/DEF that overflow normal int range) |
| `xor_number` | Integer XOR'd with the config key `24455` (Layer B) |
| `optional_array` | Nullable JSON array, e.g. `[[itemId, qty], …]` or `[[attrId, value], …]` |

## 1.4 Anatomy of a decoded table

A decoded table is a JSON **array of record objects**. Records are keyed by `mainKey`; tables with a compound identity list all identity columns in `indexedKeys` (e.g. `Fate_level` is keyed by `fate_id` + `level`). Example row from `Fate_level.json`:

```json
{ "fate_id": 5102, "level": 64,
  "expend": [[1020, 16800]],
  "attr":   [[2006, 13620], [1052, 2355]],
  "power": 122000 }
```

Read as: *soul (fate) 5102 at level 64 costs `16800` of item `1020` (Soul Essence) to upgrade, and grants attribute `2006` = `136.20%` and attribute `1052` = `23.55%`.*

## 1.5 The 5 XOR-protected tables (Layer B)

Only combat-critical stat tables use per-field obfuscation:

| Table | Fields | XOR fields | What it protects |
|---|--:|--:|---|
| `Unit` | 97 | 77 | Every combat stat for all units |
| `MainUnit` | 90 | 70 | Player-character combat stats |
| `Petlevel` | 64 | 56 | Pet per-level combat stats |
| `Skill` | 28 | 4 | `autoDis`, `initialPower`, `maxPower`, `powerRecovery` |
| `Reversion_war_chess` | 14 | 2 | `initialCd`, `maxCd` |

If these fields look like garbage (huge random ints), you forgot to apply `^ 24455`.

---

# Part 2 — Reading & joining tables

## 2.1 Keys and indexes

- **`mainKey`** — the primary identifier (e.g. `id`, `fate_id`, `level`).
- **`indexedKeys`** — all columns that together identify a row. Per-level tables (`*_level`) are almost always keyed `id + level`.
- A table named `X` and a table named `X_level` form the classic **definition + progression** pair: `X` holds identity/metadata (name, icon, quality, rarity), `X_level` holds the per-level numbers (cost, stats, power).

## 2.2 Foreign keys (how tables reference each other)

References are **bare integer IDs** — there is no typing, so you must know the target table by convention:

| A field holding… | …points into |
|---|---|
| an `attr` pair's first element | `Attribute` (attribute ID → key/name/cap) |
| an `expend`/`cost` pair's first element | `Item`/`Goods` (item ID; `1020` = Soul Essence, `1052`-adjacent economy items vary) |
| a `name` / `desc` field (`string_ref`) | `Language_en` (string ID → text) |
| an `effect` / `skill` field | `Skill` / `Skilleffcet` |
| an `icon` field | client sprite atlas (string, not a table) |

## 2.3 Language resolution

Any `string_ref` field is an integer ID resolved through the localisation tables (`Language_en.json` for English; one table per locale). Example: `Fate` row `name = 12810050` → `Language_en[12810050].text = "Forgiving Horns"`.

The engine helper is `GetStrFromConfig(id)`. IDs are global across all systems, so the same `Language_*` table serves every table's display strings.

## 2.4 The attribute-ID convention (the single most important join)

Almost every progression table expresses its bonuses as `attr: [[attributeId, value], …]`. To interpret those you need the **attribute map** (Part 3). This is the backbone that links *soul levels*, *equipment*, *spirits*, *pals*, etc. to the *combat formulas*: they all just add numbers to the same attribute IDs, which the battle engine then reads.

---

# Part 3 — The attribute system (the backbone)

Every stat in the game is an **attribute** defined in `Attribute.json` (192 rows). A progression table never "gives HP" directly — it adds a value to an attribute ID, and the battle/stat engine reads that attribute.

## 3.1 How an attribute value is assembled

`MetaAttrib` computes a live attribute value from four parts (engine line 349642):

```
value = roundInt( roundInt(baseValue + _addValue) × _time + _addExtraValue )
if up_limit ≠ 0:  value = min(value, up_limit)          # cap
if num_type == 2: value = round(value / 10000)          # percentage display
```

- `baseValue` — assembled from all sources (equipment, souls, spirits, …)
- `_addValue` — additive flat buffs
- `_time` — multiplicative modifier (starts `1.0`; `addMultiples(x)`→`+=x`, `multiple(x)`→`*=x`)
- `_addExtraValue` — post-multiplier flat add

Anti-cheat guard: `_checkValue = baseValue XOR 32`, verified by `checkCheat()`.

## 3.2 Storage scale (basis points)

Percentage attributes are stored as integers. **The divisor depends on the field/display, not on a global rule** — verify per table:

- Soul/Fate `attr` values divide by **100** (`13620` → `136.20%`, confirmed against the in-game "Global DEF" readout).
- Many engine-side rates (`crit_rate`, `resist`, …) divide by **10000** (`num_type == 2` display path above).

When in doubt, anchor to a known in-game value (as done for the Soul calculator: `Fate_level` `def_add = 13620` shows as `136.20%`).

## 3.3 Core battle attribute IDs (1001–1082)

| ID | Key | Meaning |
|---|---|---|
| 1001 | att | Attack |
| 1002 | hp | Hit Points |
| 1003 | att_speed | Attack Speed |
| 1004 | crit_rate | Crit Rate |
| 1005 | crit_dam | Crit Damage |
| 1006 | crit_def | Crit Defense (min 0.5) |
| 1007 | hit | Accuracy |
| 1008 | miss | Evasion |
| 1016 | double_hit | Combo Rate |
| 1017 | counter | Counter Rate |
| 1018 | att_resist | Basic-ATK Resistance (cap 80%) |
| 1019 | skill_resist | Skill Resistance (cap 80%) |
| 1020 | partner_resist | Pal Resistance (cap 80%) |
| 1021 | resist | DMG Resistance (cap 80%) |
| 1024 | def | Defense |
| 1032 | double_hit_dam | Combo DMG multiplier |
| 1033 | counter_dam | Counter DMG multiplier |
| 1034 | double_hit_def | Combo Resistance (cap 80%) |
| 1035 | counter_def | Counter Resistance (cap 80%) |
| 1037 | skill_crit_rate | Skill Crit Rate |
| 1038 | skill_crit_dam | Skill Crit Damage |
| 1039 | att_dam | Basic-ATK multiplier |
| 1040 | partner_dam | Pal DMG multiplier |
| 1043 | active_skilldamage_par | Skill Damage factor |
| 1045 | skill_dam_extra | Skill Damage extra |
| 1046 | boss_dam | Boss DMG bonus |
| 1047 | partner_dam_extra | Pal DMG extra |
| 1048 | ignore_double_hit | Ignore Combo |
| 1049 | ignore_counter | Ignore Counter |
| 1051 | shield_hp_extra | Shield HP bonus |
| 1052 | boss_def | Boss DMG Resistance (cap 80%) |
| 1057 | pve_dam | PvE DMG bonus |
| 1058 | pve_resist | PvE Resistance |
| 1060 | def_coe | **Defense Coefficient** (applies in every damage formula) |
| 1065 | ignore_crit_rate | Ignore Crit |
| 1067 | armor_penetration_rate | Armor-pen rate |
| 1068 | armor_penetration | Armor-pen value |
| 1071 | block | Block value |
| 1081 | total_dam_add | **Total DMG Bonus** (final universal layer) |
| 1082 | total_dam_def | **Total DMG Resistance** |

## 3.4 Extended attribute ranges

| ID range | Count | Purpose |
|---|--:|---|
| 1–24 | 4 | Base totals: `total_att`(1), `total_hp`(2), `total_att_speed`(3), `total_def`(24) |
| 2001–2036 | 36 | **Group % bonuses** — `hp_add`, `att_add`, `def_add`, `def_base_add`, … These are the "Global %" stats that souls/gear feed. `2006` = Global DEF, etc. |
| 3001–3024 | 4 | Cumulative totals (`hp_total_add`, `att_total_add`, …) |
| 4001–4006 | 6 | Partner (pal) stats |
| 5001–5012 | 12 | Rogue-mode specialisation |
| 6001–6007 | 7 | Spirit stats |
| 10001–10030 | 30 | Season-mode stats |

## 3.5 Attribute caps (`up_limit`)

Resistances and lifesteal are capped; multipliers and Total-DMG are uncapped.

| Attribute | ID | Cap |
|---|---|---|
| att_hpsteal / skill_hpsteal | 1014 / 1015 | 100% |
| att_resist / skill_resist / partner_resist / resist | 1018–1021 | 80% |
| double_hit_def / counter_def / boss_def | 1034 / 1035 / 1052 | 80% |
| control_res | 1042 | 100% |
| season_cannon_att_def | 1059 | 60% |

---

# Part 4 — Key formulas & the tables that feed them

## 4.1 Math primitives (apply everywhere)

```
round(x)    = (x>0 ? floor(10000x + 0.5) : ceil(10000x − 0.5)) / 10000     # 4 dp
roundInt(x) = floor(round(x))
```
**The engine applies `roundInt` at every multiplication step.** Any simulator must replicate this to match the game to the integer.

## 4.2 Final stat assembly (Total / Base / Global)

The player's displayed final stat is three numbers multiplied — the model used by the Stat Calculator and the Soul calculator:

```
Final = Total × (1 + BaseTotal% / 100) × (1 + Global% / 100)
```

- **Total** — flat sum of all sources (initial attributes, equip, adventure, enchant, avian, …). Tables: `Unit`/`MainUnit`, `Equipment_attr`, `Adventure_*`, etc.
- **BaseTotal%** — the big base multiplier row (attribute group `2001–2036`).
- **Global%** — the outer additive layer; **this is where souls, spirits, and similar "Global HP/ATK/DEF" bonuses land** (e.g. Fate `hp_add`/`att_add`/`def_add`).

*Source of `Global%` from souls:* `Fate_level.attr[[2006, …]]` etc. → attribute group `2001–2036`.

## 4.3 The damage pipeline

Feeder tables: **`Unit`/`MainUnit`** (attacker/defender stats), **`Attribute`** (ids + caps), **`Skill_level`** (skill coefficients), **`Level`** (PvP factor), **`Global`** (battle constants), **`Buff`/`Skilleffcet`** (modifiers).

**Step 1 — base (all damage types):**
```
effective_def = roundInt(DEF × (1 + def_coe))          # def_coe = attr 1060
base_raw      = max(roundInt(ATK − effective_def), 1)
```

**Step 2 — type multiplier & resistance:**
```
Basic ATK : dmg = roundInt(base_raw × round(att_dam       × round(1 − att_resist)))
Combo     : dmg = roundInt(roundInt(base_raw × double_hit_dam) × round(1 − double_hit_def))
Counter   : dmg = roundInt(roundInt(base_raw × counter_dam)   × round(1 − counter_def))
Skill     : dmg = roundInt(roundInt(base_raw × skill_dam_extra) × round(1 − skill_resist))
Pal       : dmg = roundInt(base_raw × round( round(partner_dam × PARENT.partner_dam_extra) × round(1 − partner_resist)))
```
*(Pal uses the parent player's ATK.)*

**Step 3 — DMG resistance (`calHurt`):**
```
dmg = roundInt(dmg × round(1 + pve_dam))
dmg = roundInt(roundInt(dmg × round(1 − resist)) × round(1 − pve_resist))
dmg = max(dmg, 1)
```

**Step 4 — crit:**
```
crit_mult = max(1.5, round(crit_dam / max(0.5, crit_def)))
dmg = roundInt(dmg × crit_mult)
```
Skill crit is special: `roundInt( (dmg × (1 + skill_crit_dam))^0.98 )` — the 0.98 exponent is on the **product**.

**Step 5 — Total DMG Bonus/RES (universal final layer, in `healthTarget`):**
```
dmg = round(dmg × max(1 + total_dam_add − total_dam_def, 0.20))     # floor 20%
```

**Step 6 — application (`Unit.addDamage`):**
```
dmg = max(roundInt(dmg / injuryReduce), 1)      # PvP reduction (see 4.4)
→ shield absorption → block absorption → HP −= remaining
```

## 4.4 PvP reduction (`Level` table)

```
avg_level    = roundInt(sum(player_levels) / player_count)
injuryReduce = Level[avg_level].pvp_injury_reduce / 10000
final_damage = max(roundInt(pre_pvp_damage / injuryReduce), 1)
```
`Level.json` (220 rows) holds `pvp_injury_reduce`, growing ~exponentially to L130 then ~linearly (L1 = 1.0×, L100 = 56.9×, L200 = 609×).

## 4.5 Battle constants (`Global` table)

`Global.json` holds ~744 tunables (key → value, ÷10000 where noted):

| Key | Value | Meaning |
|---|---|---|
| miss_correct | 9000 | Evasion power exponent (0.9) |
| vertigo_correct | 9000 | Stun power exponent (0.9) |
| shield_correct | 4000 | PvP shield decay (0.4) |
| hp_recovery_correct | 3000 | PvP heal decay (0.3) |
| battle_up_limit | [[1008,8000]] | PvP evasion cap (80%) |
| total_damage_add_down_limit | 2000 | Total-DMG floor (0.2) |

---

# Part 5 — Progression systems & their tables

Every progression system is a **definition table + a per-level table**, and the per-level table's `attr` array feeds the attribute IDs the battle formulas read. Learn one and you can read them all.

| System | Definition | Per-level / cost | Cost item | Feeds |
|---|---|---|---|---|
| **Fate / Soul** | `Fate` | `Fate_level` | Soul Essence (`1020`) | Global HP/ATK/DEF (`2001–2036`) + secondaries |
| **Guardian Spirit** | `Spirit`, `Spirit_affix_group` | `Spirit_level` | Spirit mats | `6001–6007` spirit stats |
| **Star Hero (Angel)** | `Angel`, `Angel_skill` | `Angel_star` | Hero shards | Core battle attrs |
| **Pal / Pet** | `Pet`, `Petrace`, `Pet_talent` | `Petlevel` (77-field, XOR), `Pet_proficiency` | Pet food | Pal attrs (`4001–4006`) |
| **Avian (Fly)** | `Fly`, `Fly_affix*` | `Fly_level` | Feathers | Core battle attrs |
| **Equipment** | `Equipment`, `Equipment_attr` | `Equipment_level`, `Equipment_refinement` | Gold/mats | Flat + % attrs |
| **Artifact** | `Artifact`, `Artifact_gemattr` | `Artifact_level`, `Artifact_gemlevel` | Artifact mats | Gem attrs |
| **Relic** | `Relic` | `Relic` levels inline | Relic mats | Battle attrs |
| **Ring** | `Ring` | `Ring_level` | Ring mats | Battle attrs |
| **Statue** | `Statue_attr` | `Statue_level` | Statue mats | Attr pool |
| **Path to Divinity** | `Path_to_divinity`, `Path_affix` | inline | Path mats | Affix bonuses |
| **Mount** | `Mount`, `Mount_ability` | `Mount_level` | Mount mats | Battle attrs |

### 5.1 The Fate / Soul system (worked in detail — drives the Soul Essence Calculator)

- `Fate.json` (56 rows): one row per soul per quality. Fields: `fate_id`, `name`(string_ref), `quality`(1–6, 6=Mythic), `mutually_exclusive`(the soul's family across qualities), `icon`, `effect`, `preview`.
- `Fate_level.json` (5,600 rows = 56 × 100): `fate_id`, `level`(1–100), `expend`(`[[1020, cost]]` — Soul Essence to reach the **next** level), `attr`(`[[attrId, value], …]`), `power`.

**Key facts (verified against the game UI):**
- Max level is **100**; `expend` at L100 is empty (nothing to upgrade to).
- Upgrade cost depends **only on quality** (all souls of a quality share the same curve; qualities 5 & 6 share one). Mythic L64→65 = **16,800**; maxing one Mythic soul = **1,399,000**.
- Each soul's primary attr is a **Global %** stat (`hp_add`/`att_add`/`def_add` = Global HP/ATK/DEF), stored ÷100. Mythic DEF soul at L64: `def_add = 13620` → **136.20%**, `boss_def = 2355` → **23.55%** (matches the in-game "Soul Details" screen exactly).

**Essence "worth" of a soul at level L (quality q)** = Σ `Fate_level[q].expend[1..L−1]` (you start at L1 having spent 0).

---

# Part 6 — Worked examples

## 6.1 Soul set essence + Final HP

*Soul (Fate) side:* HP soul = Mythic, level 100. Essence invested = Σ expend(L1→L100) for a Mythic curve = **1,399,000**. Its `hp_add` at L100 = `20250` → **+202.50%** Global HP.

*Final-stat side:* the player enters their three in-game numbers:
```
HP Total          = 22,276,000   (22276.0K)
Base HP Total %   = 2,308,600    (2308.6K%)
Global % (souls)  = the HP soul contributes +202.50%
Global % (other)  = 505.64%   → Global% total = 505.64 + 202.50 = 708.14%
Final HP = 22,276,000 × (1 + 2,308,600/100) × (1 + 708.14/100) ≈ 4,156,150,977,377 ≈ 4156.2B
```
This is exactly what the Soul Essence Calculator computes: `Fate_level` gives the essence curve and the `hp_add` global; the Total/Base/Global formula (§4.2) gives the final.

## 6.2 One basic attack, end-to-end (PvP)

Attacker ATK 10000, `att_dam` 2.5, `crit_dam` 1.8, `crit_rate` 0.6; Defender DEF 5000, `def_coe` 0.1, `att_resist` 0.3, `crit_def` 0.8, `resist` 0.15; L?? `injuryReduce` 25.0; 500 shield.

```
base_raw = max(roundInt(10000 − 5000×1.1), 1)          = 4500
× resist = roundInt(4500 × round(2.5 × round(1−0.3)))  = 7875
calHurt  = roundInt(roundInt(7875 × 0.85) × 1)         = 6693
crit     = roundInt(6693 × max(1.5, round(1.8/0.8)))   = 15059
TotalDMG = round(15059 × max(1+0−0, 0.20))             = 15059
PvP      = max(roundInt(15059 / 25), 1)                = 602
shield   = 602 − 500                                    = 102 HP lost
```

---

# Part 7 — Complete table catalog

All 909 tables, grouped by system. Columns: **Rows** (record count), **Key** (`mainKey`), **Fields** (first fields, `…` if more). Definition tables pair with their `*_level` progression tables; `attr`/`expend` arrays follow the conventions in Part 2.

### Core Combat & Attributes  
_120 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Attr_source` | 29 | id | id, name, order |
| `Attribute` | 192 | id | id, name, key, type, module, group, num_type |
| `Battle_competition_reward` | 7 | id | id, name, reward |
| `Battle_competition_stage` | 11 | id | id, group, name, open_day, desc |
| `Battle_competition_task` | 10 | id | id, desc, condition, reward |
| `Battlepass` | 1 | id | id, name, bundle_id, bundle_id2, open_time, add_reward_exp, add_reward |
| `Battlepass_reward` | 30 | id | id, level, exp, reward, high_reward, middle_reward |
| `Battlepass_task` | 10 | task_id | task_id, type, reset, condition, reward, desc |
| `Buff` | 2476 | id | id, name, type, group, icon, effect, effect_mirror, … |
| `Bullet` | 357 | id | id, type, effect, destroy_effect, start_bind, end_bind, speed |
| `Level` | 220 | level | level, expend, num, pvp_injury_reduce, power_par |
| `MainUnit1` | 660 | — | — |
| `MainUnit10` | 660 | — | — |
| `MainUnit100` | 660 | — | — |
| `MainUnit11` | 660 | — | — |
| `MainUnit12` | 660 | — | — |
| `MainUnit13` | 660 | — | — |
| `MainUnit14` | 660 | — | — |
| `MainUnit15` | 660 | — | — |
| `MainUnit16` | 660 | — | — |
| `MainUnit17` | 660 | — | — |
| `MainUnit18` | 660 | — | — |
| `MainUnit19` | 660 | — | — |
| `MainUnit2` | 660 | — | — |
| `MainUnit20` | 660 | — | — |
| `MainUnit21` | 660 | — | — |
| `MainUnit22` | 660 | — | — |
| `MainUnit23` | 660 | — | — |
| `MainUnit24` | 660 | — | — |
| `MainUnit25` | 660 | — | — |
| `MainUnit26` | 660 | — | — |
| `MainUnit27` | 660 | — | — |
| `MainUnit28` | 660 | — | — |
| `MainUnit29` | 660 | — | — |
| `MainUnit3` | 660 | — | — |
| `MainUnit30` | 660 | — | — |
| `MainUnit31` | 660 | — | — |
| `MainUnit32` | 660 | — | — |
| `MainUnit33` | 660 | — | — |
| `MainUnit34` | 660 | — | — |
| `MainUnit35` | 660 | — | — |
| `MainUnit36` | 660 | — | — |
| `MainUnit37` | 660 | — | — |
| `MainUnit38` | 660 | — | — |
| `MainUnit39` | 660 | — | — |
| `MainUnit4` | 660 | — | — |
| `MainUnit40` | 660 | — | — |
| `MainUnit41` | 660 | — | — |
| `MainUnit42` | 660 | — | — |
| `MainUnit43` | 660 | — | — |
| `MainUnit44` | 660 | — | — |
| `MainUnit45` | 660 | — | — |
| `MainUnit46` | 660 | — | — |
| `MainUnit47` | 660 | — | — |
| `MainUnit48` | 660 | — | — |
| `MainUnit49` | 660 | — | — |
| `MainUnit5` | 660 | — | — |
| `MainUnit50` | 660 | — | — |
| `MainUnit51` | 660 | — | — |
| `MainUnit52` | 660 | — | — |
| `MainUnit53` | 660 | — | — |
| `MainUnit54` | 660 | — | — |
| `MainUnit55` | 660 | — | — |
| `MainUnit56` | 660 | — | — |
| `MainUnit57` | 660 | — | — |
| `MainUnit58` | 660 | — | — |
| `MainUnit59` | 660 | — | — |
| `MainUnit6` | 660 | — | — |
| `MainUnit60` | 660 | — | — |
| `MainUnit61` | 660 | — | — |
| `MainUnit62` | 660 | — | — |
| `MainUnit63` | 660 | — | — |
| `MainUnit64` | 660 | — | — |
| `MainUnit65` | 660 | — | — |
| `MainUnit66` | 660 | — | — |
| `MainUnit67` | 660 | — | — |
| `MainUnit68` | 660 | — | — |
| `MainUnit69` | 660 | — | — |
| `MainUnit7` | 660 | — | — |
| `MainUnit70` | 660 | — | — |
| `MainUnit71` | 660 | — | — |
| `MainUnit72` | 660 | — | — |
| `MainUnit73` | 660 | — | — |
| `MainUnit74` | 660 | — | — |
| `MainUnit75` | 660 | — | — |
| `MainUnit76` | 660 | — | — |
| `MainUnit77` | 660 | — | — |
| `MainUnit78` | 660 | — | — |
| `MainUnit79` | 660 | — | — |
| `MainUnit8` | 660 | — | — |
| `MainUnit80` | 660 | — | — |
| `MainUnit81` | 660 | — | — |
| `MainUnit82` | 660 | — | — |
| `MainUnit83` | 660 | — | — |
| `MainUnit84` | 660 | — | — |
| `MainUnit85` | 660 | — | — |
| `MainUnit86` | 660 | — | — |
| `MainUnit87` | 660 | — | — |
| `MainUnit88` | 660 | — | — |
| `MainUnit89` | 660 | — | — |
| `MainUnit9` | 660 | — | — |
| `MainUnit90` | 660 | — | — |
| `MainUnit91` | 660 | — | — |
| `MainUnit92` | 660 | — | — |
| `MainUnit93` | 660 | — | — |
| `MainUnit94` | 660 | — | — |
| `MainUnit95` | 660 | — | — |
| `MainUnit96` | 660 | — | — |
| `MainUnit97` | 660 | — | — |
| `MainUnit98` | 660 | — | — |
| `MainUnit99` | 660 | — | — |
| `Merge_element` | 36 | id | id, element_group, element_stage, name_group, image, value, element_name |
| `Monster` | 13 | id | id, obj_type, head, scene_head |
| `Monster_buff_chapter` | 42 | id | id, type, time, skill_id, buff_desc, target |
| `Monster_pve_chapter` | 6 | id | id, name, power, level, map, bossID, bossModel |
| `Monster_pve_main` | 6 | id | id, name, bossModel, rank_id, term_rank_id, picture |
| `Specil_buff` | 12 | id | id, name, type, time, quantity, param1, state_icon |
| `Unit` | 10380 | id | id, model, type, hatred_type, ai, att_skill, skills, … |
| `UnitModel` | 815 | id | id, path, appearance, radius, scale, change_times, skill1, … |
| `UnitType` | 14 | id | id, bar, target, counter, vertigo_time, suspend_time, att_skill |

### Skills & Effects  
_6 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Skill` | 1547 | id | id, name, type, chapter_type, if_chapter_type, autoDis, quality, … |
| `Skill_level` | 18838 | id | id, level, expend, ownEffect, attrType, ownDesc, ownDesc_parm |
| `Skill_pos` | 6 | id | id, condition, type, desc |
| `Skilleffcet` | 1073 | id | id, type, trapId, targetType, targetRange, bullet, execute, … |
| `Talent_show` | 7 | type | type, group, stage, name, item, voting_reward, worship_times, … |
| `Talent_show_lv_limit` | 13 | id | id, time, num |

### Star Heroes / Angels  
_8 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Angel` | 35 | id | id, name, quality, type, desc, image, image2 |
| `Angel_array` | 7 | type | type, pos, pos_type |
| `Angel_develop` | 6 | id | id, serv_macro, desc |
| `Angel_draw` | 1 | id | id, name, type, banner, normal, must, open_time |
| `Angel_draw_package` | 80 | id | id, premise, type, act_group, bundle_id, reward, desc |
| `Angel_draw_time_limit` | 5 | id | id, act_type, group, name, name_color, banner, normal, … |
| `Angel_skill` | 310 | id | id, skill_name, skill_effect, skillPar, skill_dec, desc_parm |
| `Angel_star` | 350 | id | id, star, expend, frame, attr, skill1_type, battle_skill1, … |

### Classes / Jobs  
_3 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Jobs` | 38 | id | id, name, type, job_pos, desc, skill, passive_skill, … |
| `Jobs_wakeup` | 2000 | id | id, level, value_plus, cost, power |
| `Science` | 3286 | id | id, level, name, icon, type, describe, desc_parm, … |

### Pals & Pets  
_15 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Palu_boss` | 6 | id | id, name, index, power, level, map, part_type, … |
| `Palu_client_global` | 5 | id | id, array_value, value |
| `Palu_kv` | 1 | id | id, array_value, value |
| `Palu_new_artiact` | 36 | id | id, type, type_id, level, is_unlock, chapter_progress, rank |
| `Palu_new_equip` | 10 | id | id, equip_id, upgrade_cost |
| `Palu_new_pal` | 69 | id | id, level, is_unlock, chapter_progress |
| `Palu_new_skill` | 38 | id | id, level, is_unlock, chapter_progress |
| `Palu_new_unlock` | 21 | id | id, is_unlock, chapter_progress, job_unlock, skill_unlock, pal_unlock, pass_lv |
| `Palu_world_boss` | 10 | id | id, name, index, power, level, map, part_type |
| `Pet` | 322 | id | id, name, icon, desc, quality, type, unitId |
| `Pet_pos` | 6 | id | id, condition, desc |
| `Pet_proficiency` | 700 | id | id, level, extra_star, exp, addexp, own_attrs, power |
| `Pet_talent` | 70 | id | id, all_star, name, effect_des, desc_parm1, effect, power_des |
| `Petlevel` | 19824 | id | id, level, expend, ownEffect, desc, desc_parm, equipEffect, … |
| `Petrace` | 55 | id | id, name |

### Avians (Fly system)  
_16 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Fly` | 35 | id | id, name, type, icon, quality, hybrid_type, unitid, … |
| `Fly_achievement` | 41 | id | id, group, name, name_num, desc, desc_num, condition |
| `Fly_advance` | 560 | id | id, advance_level, expend, attr, fly_skill, entry_level, power |
| `Fly_cd` | 22 | times | times, type, cd |
| `Fly_egg` | 13 | id | id, name, path, quality, fly_weight, entry_num_weight |
| `Fly_entry` | 1734 | id | id, level, name, quality, passive_skill, special_effect, home_effect |
| `Fly_entry_num` | 7 | id | id, entry_num_weight, entry_num_fixed |
| `Fly_entry_weight` | 88 | id | id, extra_weight, fix_weight, var_weight |
| `Fly_evolution_pro` | 18 | id | id, times, pro |
| `Fly_evolution_rate` | 3 | id | id, rate |
| `Fly_hybird_template` | 21 | id | id, template_weight |
| `Fly_hybrid` | 501 | id1 | id1, id2, template_id, fly_weight |
| `Fly_hybrid_time` | 21 | id | id, time |
| `Fly_level` | 5250 | id | id, level, expend, if_advance, attr, power |
| `Fly_remake_cost` | 5 | id | id, times, cost |
| `Fly_total_achievement` | 4 | id | id, name, desc, num, reward |

### Guardian Spirits  
_9 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Spirit` | 20 | spirit_id | spirit_id, mame, quality, spirit_part_amount, unit, path, model_scale, … |
| `Spirit_affix_group` | 4 | affix_group | affix_group, name, icon, icon_group |
| `Spirit_attrbonus_affix` | 168 | affix_id | affix_id, affix_group, quality, attr_id, value, power_rate |
| `Spirit_attrbonus_slot` | 22 | slot_id | slot_id, affix_group |
| `Spirit_craft` | 10 | id | id, quality, craft_type, spirit_target_id, main_craft_material, minor_craft_material |
| `Spirit_craft_target` | 4 | spirit_level | spirit_level, spirit_group, material_level |
| `Spirit_draw` | 1 | id | id, name, type, banner, normal, must, open_time |
| `Spirit_draw_prob` | 6 | id | id, desc, prob, good_list |
| `Spirit_level` | 72 | spirit_id | spirit_id, spirit_level, expend, spirit_attr, character_attr, slot_amount, skill1 |

### Fate / Soul system  
_5 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Fate` | 56 | fate_id | fate_id, name, quality, mutually_exclusive, icon, effect, preview |
| `Fate_chapter` | 1000 | id | id, index, power, level, map, part_type, interval, … |
| `Fate_draw` | 32 | id | id, type, reward, weights, is_guaranteed |
| `Fate_fusion` | 8 | id | id, get_fate_id, material_fate_id, passive_skill_group, desc, same_kind |
| `Fate_level` | 5600 | fate_id | fate_id, level, expend, attr, skill, breakdown_reward, power |

### Equipment / Artifacts / Relics / Rings / Gems  
_24 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Artifact` | 44 | id | id, name, path, icon, icon_small, icon_group, quality, … |
| `Artifact_gem_chapter` | 25 | id | id, index, power, level, map, part_type, interval |
| `Artifact_gemattr` | 141 | id | id, group_id, attr_id, pro, initial_value, upgrade_value, power_rate |
| `Artifact_gemgenerate` | 6 | id | id, quality_possible, slot_possible, set_possible |
| `Artifact_gemlevel` | 120 | quality | quality, level, exp, is_strengthen, weaken |
| `Artifact_gemquality` | 6 | id | id, max_level, mainattr_groups, viceattr_num, viceattr_group, quality_exp, frame |
| `Artifact_gemsets` | 7 | id | id, name, icon, get_way, bonus2_desc, bonus2_attr, bonus2_skill |
| `Artifact_gemslot` | 6 | id | id, main_attr_group |
| `Artifact_level` | 300 | level | level, expend_exp, expend_goods, attr, base_skill, unlock, power |
| `Artifact_preview_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Artifact_skin` | 473 | artifact_id | artifact_id, skin_level, expend, skin_skill, attr, power |
| `Equipment` | 5357 | id | id, name, level, part, quality, number, advanced, … |
| `Equipment_advancement` | 37 | id | id, attr, cost, limit, power |
| `Equipment_attr` | 2292 | id | id, group_id, attr_id, type, pro, value |
| `Equipment_guarantee` | 11 | num | num, quality, level, part |
| `Equipment_level` | 2200 | part | part, level, basic, price |
| `Equipment_refinement` | 151 | id | id, attar, cost |
| `Equipment_resonance` | 18 | id | id, attr, current_attr, stage, power |
| `Equipment_suit` | 3 | suit_id | suit_id, num, effect, desc, name |
| `Relic` | 5005 | id | id, level, name, type, desc, desc_parm, icon |
| `Relic_get` | 30 | num | num, relic_pool, cost |
| `Relic_pos` | 7 | id | id, name, icon |
| `Ring` | 5 | id | id, name, path1, path2, icon1, icon2, quality |
| `Ring_level` | 301 | level | level, expend_exp, expend_goods, attr, base_skill, unlock, power |

### Mounts  
_15 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Mount` | 72 | id | id, name, type, path, binds, icon, icon_small, … |
| `Mount_ability` | 1503 | id | id, level, value_plus, power |
| `Mount_abilitycost` | 1501 | total_level | total_level, cost, success_rate, success_guaranteed |
| `Mount_chapter` | 1050 | id | id, index, power, level, map, part, next_part, … |
| `Mount_chapter_bufflist` | 34 | mount_buff_id | mount_buff_id, skill_id, buff_desc, quality, weight |
| `Mount_draw` | 895 | id | id, type, group_id, reward, weight, guaranteed, limited, … |
| `Mount_draw_cost_get` | 19 | id | id, cost, reward |
| `Mount_draw_cumulative_times` | 582 | id | id, type, group_id, cumulative_times, reward |
| `Mount_draw_guaranteed` | 340 | id | id, type, group_id, num, reward |
| `Mount_level` | 300 | level | level, name, order, star, expend_exp, expend_goods, attr |
| `Mount_skin` | 660 | mount_id | mount_id, skin_level, expend, skin_skill, attr, power |
| `Parking_design` | 1002 | id | id, level, position, expend, own_attrs, effect, pvp_effect, … |
| `Parking_log` | 26 | id | id, serv_macro, name, type, desc |
| `Parking_mount` | 14000 | id | id, level, expend, own_attrs, rate, drop_id, drop_show |
| `Parking_time` | 10 | id | id, interval, rate_alter, drop_num, if_beaten |

### Statue / Path to Divinity  
_9 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Path_affix` | 342 | affix_id | affix_id, affix_group, quality, attr_id, value, power_rate |
| `Path_affix_levelpro` | 30 | id | id, total_number, pro_quality |
| `Path_sensor_node` | 50 | node_id | node_id, trunk_id, trunk_number, affix_group, desc |
| `Path_to_divinity` | 12 | trunk_id | trunk_id, name, tree_id, sensor_node_list |
| `Path_upper_limit` | 213 | trunk_id | trunk_id, attr_id, upper_limit, show_type, unique, sort |
| `Statue_attr` | 90 | id | id, product, attr_id, pro, value, power_rate |
| `Statue_level` | 10 | level | level, expend, pro_quality, power |
| `Statue_pos` | 5 | id | id, level, desc |
| `Statue_spend` | 5 | lock_quantity | lock_quantity, spend |

### Back / Wing decorations  
_15 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Back_book` | 1 | id | id, condition, level |
| `Back_checkin` | 21 | id | id, open_day, lost_day, day, reward, special |
| `Back_decoration` | 48 | id | id, name, form, type, path, binds, icon_small, … |
| `Back_lamp_attr` | 8 | id | id, name, type |
| `Back_lamp_chapter` | 36 | id | id, chapter, level, name, first_reward, acc_reward, unlock |
| `Back_lamp_item` | 20 | id | id, type, model_change, icon, drop_text, text, bullet_model |
| `Back_lamp_map` | 8 | id | id, unit_event, combine_id, map_long, map_picture |
| `Back_lamp_unit` | 11 | id | id, type, move_type, picture, model |
| `Back_level` | 780 | id | id, level, expend_exp, expend_goods, attr, power, era_level |
| `Back_level_rebate` | 12 | level | level, percent, low_star_diamond, high_star_diamond |
| `Back_mall` | 40 | id | id, open_day, lost_day |
| `Back_pay_rebate` | 15 | number | number, percent, low_star_diamond, high_star_diamond |
| `Back_skin` | 495 | back_id | back_id, skin_level, expend, skin_skill, attr, power |
| `Back_talent` | 2652 | id | id, level, name, icon, job_type, color_type, describe, … |
| `Back_task` | 60 | id | id, type, day, condition, reward, access, open_day |

### Chapters / Stages / PvE  
_165 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Adventure_exp_point` | 11 | lose | lose, win, exp, ponit |
| `Adventure_level` | 15 | id | id, next_id, icon, avatar_frame, effect, task_group, language_id |
| `Adventure_space_back` | 42 | id | id, coordinate, unlock |
| `Adventure_space_group` | 25 | id | id, group_0, group_1, group_2, group_3, group_4, cell_refresh |
| `Adventure_space_item` | 201 | id | id, name, icon_lvl, level, type, quality, upgrade_cost, … |
| `Adventure_space_item_book` | 21 | id | id, type_id, star_id, next_id, thrid_id, last_id |
| `Adventure_space_job` | 51 | id | id, name, attr, second_job, third_job, back_job, star_item, … |
| `Adventure_space_level` | 24 | id | id, active_id, round_id, rank, robot |
| `Adventure_space_number` | 20 | id | id, active_id, challenge_num, reward |
| `Adventure_space_rank` | 8 | id | id, next_rank, need_experience, profession, reward, show_reward, icon |
| `Adventure_space_robot` | 42 | id | id, robot_job, robot_weapon, robot_badge, robot_item |
| `Adventure_space_rule` | 1 | id | id, win_number, lose_number, battle_gold, job_round, job_round_special, job_star |
| `Adventure_space_shop` | 762 | id | id, group, item_id, prob |
| `Adventure_task` | 42 | id | id, condition, desc, reward, guide |
| `Chapter1` | 500 | — | — |
| `Chapter10` | 500 | — | — |
| `Chapter100` | 500 | — | — |
| `Chapter11` | 500 | — | — |
| `Chapter12` | 500 | — | — |
| `Chapter13` | 500 | — | — |
| `Chapter14` | 500 | — | — |
| `Chapter15` | 500 | — | — |
| `Chapter16` | 500 | — | — |
| `Chapter17` | 500 | — | — |
| `Chapter18` | 500 | — | — |
| `Chapter19` | 500 | — | — |
| `Chapter2` | 500 | — | — |
| `Chapter20` | 500 | — | — |
| `Chapter21` | 500 | — | — |
| `Chapter22` | 500 | — | — |
| `Chapter23` | 500 | — | — |
| `Chapter24` | 500 | — | — |
| `Chapter25` | 500 | — | — |
| `Chapter26` | 500 | — | — |
| `Chapter27` | 500 | — | — |
| `Chapter28` | 500 | — | — |
| `Chapter29` | 500 | — | — |
| `Chapter3` | 500 | — | — |
| `Chapter30` | 500 | — | — |
| `Chapter31` | 500 | — | — |
| `Chapter32` | 500 | — | — |
| `Chapter33` | 500 | — | — |
| `Chapter34` | 500 | — | — |
| `Chapter35` | 500 | — | — |
| `Chapter36` | 500 | — | — |
| `Chapter37` | 500 | — | — |
| `Chapter38` | 500 | — | — |
| `Chapter39` | 500 | — | — |
| `Chapter4` | 500 | — | — |
| `Chapter40` | 500 | — | — |
| `Chapter41` | 500 | — | — |
| `Chapter42` | 500 | — | — |
| `Chapter43` | 500 | — | — |
| `Chapter44` | 500 | — | — |
| `Chapter45` | 500 | — | — |
| `Chapter46` | 500 | — | — |
| `Chapter47` | 500 | — | — |
| `Chapter48` | 500 | — | — |
| `Chapter49` | 500 | — | — |
| `Chapter5` | 500 | — | — |
| `Chapter50` | 500 | — | — |
| `Chapter51` | 500 | — | — |
| `Chapter52` | 500 | — | — |
| `Chapter53` | 500 | — | — |
| `Chapter54` | 500 | — | — |
| `Chapter55` | 500 | — | — |
| `Chapter56` | 500 | — | — |
| `Chapter57` | 500 | — | — |
| `Chapter58` | 500 | — | — |
| `Chapter59` | 500 | — | — |
| `Chapter6` | 500 | — | — |
| `Chapter60` | 500 | — | — |
| `Chapter61` | 500 | — | — |
| `Chapter62` | 500 | — | — |
| `Chapter63` | 500 | — | — |
| `Chapter64` | 500 | — | — |
| `Chapter65` | 500 | — | — |
| `Chapter66` | 500 | — | — |
| `Chapter67` | 500 | — | — |
| `Chapter68` | 500 | — | — |
| `Chapter69` | 500 | — | — |
| `Chapter7` | 500 | — | — |
| `Chapter70` | 500 | — | — |
| `Chapter71` | 500 | — | — |
| `Chapter72` | 500 | — | — |
| `Chapter73` | 500 | — | — |
| `Chapter74` | 500 | — | — |
| `Chapter75` | 500 | — | — |
| `Chapter76` | 500 | — | — |
| `Chapter77` | 500 | — | — |
| `Chapter78` | 500 | — | — |
| `Chapter79` | 500 | — | — |
| `Chapter8` | 500 | — | — |
| `Chapter80` | 500 | — | — |
| `Chapter81` | 500 | — | — |
| `Chapter82` | 500 | — | — |
| `Chapter83` | 500 | — | — |
| `Chapter84` | 500 | — | — |
| `Chapter85` | 500 | — | — |
| `Chapter86` | 500 | — | — |
| `Chapter87` | 500 | — | — |
| `Chapter88` | 500 | — | — |
| `Chapter89` | 500 | — | — |
| `Chapter9` | 500 | — | — |
| `Chapter90` | 500 | — | — |
| `Chapter91` | 500 | — | — |
| `Chapter92` | 500 | — | — |
| `Chapter93` | 500 | — | — |
| `Chapter94` | 500 | — | — |
| `Chapter95` | 500 | — | — |
| `Chapter96` | 500 | — | — |
| `Chapter97` | 500 | — | — |
| `Chapter98` | 500 | — | — |
| `Chapter99` | 500 | — | — |
| `Chapter_type` | 58 | id | id, name, config, ad, open_id, desc, time_type, … |
| `Danjon_meshi_dinner` | 10 | id | id, exp, box_reward, count, figure, figure_food, figure_anim |
| `Danjon_meshi_event_preview` | 7 | id | id, type, icon, desc, reward |
| `Danjon_meshi_kv` | 19 | id | id, key, desc, info |
| `Danjon_meshi_lv` | 10 | id | id, exp, atk, monster, food_reward, box_per, box_reward |
| `Danjon_meshi_recipe` | 10 | id | id, exp, reward |
| `Danjon_meshi_recipe_preview` | 3 | id | id, reward |
| `Dragon_map_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Dragon_map_event` | 17 | id | id, type, name, level, model, scale, icon, … |
| `Dragon_map_guide` | 12 | id | id, name, show, show_tab, icon, desc, guaranteed_drop |
| `Dragon_map_kv` | 32 | id | id, key, desc, info, info_type |
| `Dragon_map_pvp_damage` | 6 | id | id, win, loser_hp, coefficient |
| `Dragon_map_rank_reward` | 18 | id | id, type, range, reward, show |
| `Escort_boss_bullet` | 6 | id | id, energy, name, hurt, gap, prob, cost |
| `Escort_boss_report` | 9 | id | id, text |
| `Escort_boss_skill` | 3 | id | id, name, name2, skill_icon, energy, dec, effect, … |
| `Escort_building` | 9 | id | id, name, image |
| `Escort_chapter` | 98 | id | id, part_type, level, index, power, map, part, … |
| `Escort_chapter_reward` | 18 | id | id, type, level, index, output, display, dec |
| `Escort_global` | 36 | id | id, key, desc, info |
| `Escort_goods` | 12 | id | id, name, escort_image, grade, escort_coin, escort_time, dec |
| `Escort_monster` | 120 | id | id, monster_group, image, name, unit, rank, attr |
| `Escort_rank_reward` | 20 | id | id, type, range, show, reward |
| `Escort_route` | 49 | id | id, start, finish |
| `Illustrated` | 1040 | id | id, level, type, name, condition, attr, skill |
| `Reversion_war_boss` | 45 | id | id, name, desc, unitId, range |
| `Reversion_war_chapter` | 15 | id | id, desc, index, power, level, diff, map |
| `Reversion_war_chess` | 31 | id | id, name, spend, unlock_day, initialCd, maxCd, icon, … |
| `Reversion_war_reward` | 45 | id | id, day, star_num, get_way, reward, desc, desc_parm |
| `Rogue_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Rogue_draw` | 12 | id | id, reward, weight, guaranteed, limited, order, is_jackpot, … |
| `Rogue_draw_cumulative_times` | 8 | id | id, cumulative_times, reward |
| `Rogue_draw_guaranteed` | 11 | id | id, num, reward |
| `Rogue_enemy` | 63 | enemy_id | enemy_id, rank_id, main_rank, minor_rank, range, attr_data, luggage |
| `Rogue_gift` | 118 | id | id, level, name, node_type, type, icon, icon_group, … |
| `Rogue_global` | 20 | key | key, info_type, info, desc |
| `Rogue_goods` | 177 | id | id, name, type, quality, effect, uniqueness, loseable |
| `Rogue_goods_mall` | 163 | id | id, goods, price, weight_sidestory, weight_boss, name, limit |
| `Rogue_main_chapter` | 85 | id | id, name, icon, part_type, map, enemy_type, enemy_id, … |
| `Rogue_output` | 267 | id | id, groupid, item, othergroup, probtype, prob |
| `Rogue_rank_reward` | 9 | id | id, rank_range, show, rank_reward |
| `Rogue_sidestory_chapter` | 8 | id | id, group_id, name, pre_level_id, times_limit, part_type, map |
| `Rogue_sidestory_times` | 30 | id | id, cost, random_level |
| `Rogue_weekly_reward` | 10 | id | id, point, reward |
| `Towerdefence` | 16 | id | id, lev, point, num |
| `Towerlevel` | 3 | id | id, num |
| `Towermonster` | 2 | type | type, hp, point |
| `World_boss` | 100 | id | id, index, power, level, map, part_type, part |
| `World_boss_bufflist` | 5 | buff_id | buff_id, skill_id, buff_desc, target |
| `World_boss_rank` | 9 | rank | rank, reward_rank |
| `World_boss_total_dmg` | 30 | day | day, total_dmg, reward_participate |

### PvP / Season / Cross-server / League  
_91 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Cross_limited_rank` | 96 | id | id, match_id, act_type, rank_id, rank_condition, task_group_id, bundle_group_id |
| `Cross_limited_rank_reward` | 479 | id | id, rank_group_id, range, reward, show, spec_reward |
| `Cross_limited_rank_task` | 544 | id | id, task_group_id, small_group_id, is_stage, condition, reward, desc |
| `Cross_pvp_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Cross_pvp_extra_reward` | 30 | id | id, grade_id, rank, reward |
| `Cross_pvp_grade` | 37 | id | id, main_rank, minor_rank, next_rank, range, part_type, part_num, … |
| `Cross_pvp_grading_match` | 11 | id | id, rank_id, promote_win_num |
| `Cross_pvp_robot` | 275 | id | id, rank, level, job, active_skill, passive_skill, pet |
| `Cross_war_head_scale` | 10 | id | id, power_radio, big_scale, small_scale |
| `Cross_war_idle_reward` | 19 | id | id, power, reward |
| `Cross_war_job` | 4 | id | id, name, buff, speed, attack_distance, auto_attack, sight_list |
| `Cross_war_kv` | 28 | id | id, value |
| `Cross_war_match` | 37 | id | id, time, num |
| `Cross_war_point` | 30 | id | id, object, condition, point |
| `Cross_war_rank_reward` | 36 | id | id, type, range, reward |
| `Kf_war_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Kf_war_chapter_monster` | 2 | id | id, index, power, level, map, part_type, part, … |
| `League_gve_bonus_level` | 30 | id | id, bonus_level, prob, desc, base_id, complete_drop_reward |
| `League_gve_buff_effect` | 16 | id | id, type |
| `League_gve_chapter` | 150 | id | id, index, power, level, map, part_type, interval, … |
| `League_gve_chapter_control` | 10 | id | id, type, map_group, level, level_desc, name, open_time, … |
| `League_gve_chapter_monster` | 160 | id | id, index, power, level, map, part_type, part, … |
| `League_gve_chapter_rank` | 80 | rank_damage | rank_damage, reward_rank |
| `League_gve_chapter_show` | 1 | type | type, name, reward_show, key_show, banner |
| `League_gve_chapter_task` | 3 | id | id, desc, val |
| `League_gve_chapter_type` | 13 | id | id, type, name, map_prefab_name, prefab_name |
| `League_gve_event_buff` | 16 | id | id, adventure_event, prob, buffid, desc, icon, icon_group |
| `League_gve_event_game` | 30 | id | id, event_game, name, desc, goal, prob, entryid |
| `League_gve_map` | 1900 | map_id | map_id, id, type, base_id, unlock, event_id, bonus_level_id |
| `League_gve_map_group` | 40 | map_id | map_id, map_group, map_name, weight, aoimap_id |
| `League_solo_chapter` | 100 | id | id, index, power, map, part_type, part, next_part |
| `League_solo_chapter_chest` | 15 | guild_level | guild_level, normal_chest_limit, rare_chest_limit, normal_chest_reward, rare_chest_reward |
| `League_solo_hard_chapter` | 100 | id | id, index, power, map, part_type, part, next_part |
| `League_solo_hard_chest` | 15 | guild_level | guild_level, normal_chest_limit, rare_chest_limit, normal_chest_reward, rare_chest_reward |
| `League_solo_hard_rank` | 20 | id | id, type, range, reward |
| `League_solo_hard_turn` | 4 | turn_number | turn_number, buff_id, desc, bossModel, bossBanner, boss_name, appearance_id |
| `Pvp_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Pvp_competition_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Pvp_reward` | 18 | id | id, type, rank, reward, title_reward |
| `Season_achievement` | 30 | level | level, condition, reward, season_type |
| `Season_battle_guide` | 119 | id | id, season_type, tab, type, txt_title, txt_rule, txt_extra |
| `Season_battle_guide_new` | 147 | id | id, season_type, tab, type, txt_title, txt_rule, txt_extra |
| `Season_battle_score` | 17 | id | id, type, score_method, item_num |
| `Season_building_function` | 9 | id | id, name, icon |
| `Season_building_plot` | 53 | id | id, type, name, plot_number, plot_number_even, prefab_name, ui_scale, … |
| `Season_cabin` | 6 | cabin_id | cabin_id, condition, type, condition_special, condition_text |
| `Season_command_center` | 45 | id | id, level, name, icon, type, describe, desc_parm, … |
| `Season_draw_guaranteed` | 35 | id | id, season_type, type, num, reward |
| `Season_equipment` | 2960 | id | id, name, level, part, quality, number, advanced |
| `Season_equipment_attr` | 500 | id | id, group_id, attr_id, type, pro, value |
| `Season_equipment_attr_s4` | 500 | id | id, group_id, attr_id, type, pro, value |
| `Season_equipment_guarantee` | 11 | num | num, quality, level, part |
| `Season_equipment_level` | 100 | part | part, level, basic, price |
| `Season_equipment_level_s4` | 100 | part | part, level, basic, price |
| `Season_equipment_s4` | 2960 | id | id, name, level, part, quality, number, advanced |
| `Season_event` | 24 | id | id, season_type, type, base_id, map_position, name, event_desc |
| `Season_favor` | 101 | level | level, expend, attr, medal_icon, power |
| `Season_kv_new` | 23 | season_type | season_type, kv_id, desc, info, info_type |
| `Season_mapevent_reward` | 41 | id | id, type, reward_method, reward_cd, reward, buff_reward, level |
| `Season_notice` | 10 | id | id, type, condition, content |
| `Season_notice_condition` | 5 | id | id, name, des |
| `Season_port_supply` | 30 | level | level, cost, reward |
| `Season_port_supply_item` | 3 | id | id, exp, limit_time |
| `Season_pvp_chapter` | 1 | id | id, index, power, level, map, part_type, part |
| `Season_pvp_robot` | 20 | id | id, name, rank, rank_number, robot_ship_attr, level, job, … |
| `Season_rank_reward` | 31 | id | id, type, range, reward, season_type |
| `Season_recovery_speed` | 21 | id | id, level, speed |
| `Season_ship` | 8 | id | id, name, quality, path, icon, appearance, item_id |
| `Season_ship_appearance` | 2168 | id | id, part, spine, atlas, icon, model_ID, ship_plot |
| `Season_ship_draw` | 16 | id | id, reward, weight, is_jackpot, limited, quality, fragment |
| `Season_ship_draw_guaranteed` | 5 | id | id, num, reward |
| `Season_ship_level` | 20 | level | level, expend_exp, expend_goods, attr, cost, power |
| `Season_ship_level_s4` | 20 | level | level, expend_exp, expend_goods, attr, cost, power |
| `Season_ship_skin` | 87 | mount_id | mount_id, skin_level, expend, attr, use_attr, skin_skill_season, skin_skill |
| `Season_station_level` | 20 | level | level, expend, attr, special_attr |
| `Season_target` | 13 | id | id, season_type, condition, name, script_desc, mission_desc, reward |
| `Season_transform` | 8 | id | id, transform_item |
| `Season_treasure` | 165 | id | id, level, name, type, icon, item_id, attr_type, … |
| `Season_treasure_bag_effect` | 9 | id | id, number, attr, skill_buff, desc, power |
| `Season_treasure_draw` | 90 | id | id, season_type, type, reward, weight, is_jackpot, limited |
| `Season_treasure_level` | 15 | level | level, expend, cost, pro_quality |
| `Season_treasure_level_s4` | 15 | level | level, expend, cost, pro_quality |
| `Season_workshop_level` | 11 | level | level, expend, attr, special_attr |
| `Strategy_activity_chapter` | 50 | id | id, name, index, power, level, diff, map, … |
| `Strategy_activity_commodity` | 72 | id | id, name, reward, expend, radio |
| `Strategy_activity_level` | 5 | chapter_progress | chapter_progress, level, equipments, refresh_cost |
| `Strategy_activity_milestone` | 50 | id | id, condition, get_way, reward |
| `Strategy_activity_pet` | 60 | id | id, level, chapter_progress, open_day, unlock_cost, is_unlock |
| `Strategy_activity_shop` | 22 | id | id, commodity, weight, limit, guarantee_num |
| `Strategy_activity_skill` | 34 | id | id, level, chapter_progress, open_day, unlock_cost, is_unlock |
| `Strategy_artiact` | 35 | id | id, type, type_id, chapter_progress, open_day, unlock_cost, is_unlock |

### Guild / Social / Marriage  
_12 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Chat_bubble` | 30 | id | id, name, icon, get_way, text_color, preview, open_time |
| `Chat_keywords` | 2 | id | id, type, keywords, reward, reward_group, title |
| `Guild_activity` | 5 | id | id, name, time_desc, desc, icon, is_show, schedule_button |
| `Guild_career` | 5 | id | id, name, permissions, number, low_job, recall, expel |
| `Guild_level` | 15 | level | level, exp, max_num, max_exp, help_limit, carrer_num |
| `Guild_log` | 13 | id | id, serv_macro, type, name, desc |
| `Guild_permission` | 14 | id | id, permission_desc |
| `Guild_permission_show` | 8 | id | id, text, permission_desc, rank |
| `Guild_rank` | 3 | id | id, refresh, show_num |
| `Marry` | 3 | id | id, spend, reward, show_reward, invite_num, num_max, enter_spend, … |
| `Marry_anniversary` | 24 | time | time, reward, desc |
| `Marry_task` | 7 | id | id, desc, condition, reward |

### Minigames / Farm / Fishing / Mining / Events  
_104 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Break_gold_egg_layers` | 50 | id | id, layers, type, group_id, num |
| `Break_gold_egg_weight` | 16511 | id | id, type, group_id, layers, reward, weight, limited, … |
| `Card_pool` | 40 | type | type, level, num, group |
| `Card_pool_type` | 2 | id | id, name, treasure, icon, condition, open_id |
| `Cut_rope_art` | 5 | id | id, type, avatar |
| `Cut_rope_level` | 13 | id | id, lecel_id, unlock, active_id, line_dot, unit_dot, safe_place |
| `Double_cumulative_reward` | 32 | id | id, act_type, group_id, time, reward |
| `Double_draw` | 4 | act_type | act_type, group_id, turn_id, draw_expand, draw_reward, cumulative_reward_id, reward_inform |
| `Double_draw_guaranteed` | 40 | id | id, turn_id, num, reward |
| `Double_ladder_assist_reward` | 20 | id | id, reward |
| `Double_ladder_chapter` | 150 | id | id, index, power, chapter, map, part_type, interval, … |
| `Double_ladder_strategic` | 9 | id | id, condition, effect1, effect2, effect3, effect4, name |
| `Double_probabillity` | 80 | reward_id | reward_id, id, reward, reward_limit, weight, reward_type, limited |
| `Farm_action` | 11 | id | id, serv_macro, name, type, desc |
| `Farm_buildings` | 33 | id | id, level, effect, pvp_effect, pvp_effect1, time, condition |
| `Farm_buildings_details` | 3 | id | id, name, effect, desc |
| `Farm_greens` | 6 | id | id, time, harvest_time, reward, value, try_stolen_limit, stolen_limit, … |
| `Farm_level` | 50 | level | level, expend, effect, power |
| `Farm_pos` | 6 | id | id, condition, desc |
| `Farm_pvp_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Farm_seed` | 6 | id | id, harvest, icon, activity |
| `Fish_mission` | 45 | id | id, group, day, score, get_way, reward, desc |
| `Fish_ocean` | 3 | id | id, depth, back, brightness, fish_refresh_rate, is_pet_refresh, pet_refresh_rate |
| `Fish_species` | 35 | id | id, group, appearance, image, image_size, obj_type, name, … |
| `Fish_species_reward` | 5 | id | id, group, unlock, reward |
| `Fish_tackle` | 30 | id | id, level, upgrade_cost, effect, num_desc, upgrade_pre, name |
| `Fish_turntable` | 12 | id | id, group, reward, weight, rank |
| `Ggbond_bead` | 24 | bead_id | bead_id, icon, effect, picture_book |
| `Ggbond_chapter` | 7 | chapter_id | chapter_id, type, group_id, monster, initial_bead, bead, open_day |
| `Ggbond_monster` | 8 | monster_id | monster_id, spine, is_model, monster_hp, scale |
| `Goldfish_scooping_fish` | 5 | id | id, name, model, scope, score, radius, normal_speed |
| `Goldfish_scooping_level` | 8 | id | id, open_time, end_time, two_player, pass_score, gold_fish_weight, gold_fish_num |
| `Ippon_matsu_pool` | 4 | gacha_group | gacha_group, pull_price, black_hole_times, act_type, act_group, title |
| `Ippon_matsu_prob` | 28 | id | id, gacha_group, reward, reward_limit, weight, reward_type, limited, … |
| `Ippon_matsu_times` | 98 | id | id, act_type, group_id, times, reward |
| `Left_right_crush` | 10 | difficulty | difficulty, id, effect, picture_book, score, text |
| `Left_right_crush_block` | 24 | id | id, color_class, color_count, icon, trans |
| `Lucky_bag_preview` | 57 | id | id, act_type, type, reward, weight |
| `Lucky_bag_store` | 12 | id | id, type, name, icon, paymall, custom_reward |
| `Lucky_cat` | 1 | type | type, group_id, get_lucky_cat_cost, get_lucky_cat_limit, get_lucky_cat_count, show_per_condition |
| `Lucky_cat_reward` | 64 | id | id, act_type, activity_group, time, per, weight, icon_picture |
| `Merge` | 1558 | id | id, slave_ids, date |
| `Merge_box` | 3 | id | id, image, reward, name, des |
| `Merge_card` | 10 | id | id, icon, num, merge_id |
| `Merge_level` | 10 | id | id, act_type, group, chess_board, initial_element, initial_cover, initial_order, … |
| `Merge_order` | 185 | id | id, order_gruop, order_appear, order_demand, order_reward, box |
| `Merge_pet` | 6 | id | id, model |
| `Mine` | 34 | id | id, range, template |
| `Mine_add` | 32 | id | id, range, template |
| `Mine_grid` | 21 | id | id, goods, reward, icon, num |
| `Mine_hole_auto` | 32 | id | id |
| `Mine_hole_reward` | 60 | id | id, type, range, drop |
| `Mine_hole_type` | 10 | id | id, name, arrange, mine_per, mine_max, small_picture, big_picture |
| `Mine_template` | 22 | id | id, arrange, hole |
| `Mining_config` | 350 | id | id, group, row |
| `Mining_item` | 21 | level | level, hp, attack, image, price, gift |
| `Mining_level` | 5 | id | id, group, round, condition, buy, gift, gift2 |
| `Mining_main` | 1 | id | id, level, initial_coin, initial_pick |
| `Mining_reward` | 13 | id | id, group, free_reward, pay_reward, condition |
| `Mining_soil` | 30 | level | level, hp, attack, image, spine, price, effect |
| `Monopoly` | 40 | id | id, act_type, name, type, city_lvl_reward, reward, random |
| `Monopoly_random` | 48 | id | id, type, desc |
| `Monopoly_turnreward` | 7 | id | id, act_type, turns, reward |
| `Moonfestival_bullet` | 3 | id | id, name, type, first_force, speed_effect, demage_num, bomb |
| `Moonfestival_card` | 31 | id | id, type, group, open_time, item_weight |
| `Moonfestival_riddle` | 10 | id | id, type, group_id, rank_num, subject, subject_detail, answer |
| `Moonfestival_search` | 40 | id | id, type, group_id, rank_num, clue, system_view, picture |
| `Moonfestival_stage` | 7 | id | id, template, open_day, limit, star_step |
| `Moonfestival_stagetemplate` | 12 | id | id, arrange |
| `Moonfestival_unit` | 6 | id | id, type, rebound_effect, speed_effect, enemy_hp, defeat_reward, radius |
| `New_year_couplets` | 30 | id | id, text_group, text |
| `New_year_drive_away` | 20 | id | id, type, grid_id, reward |
| `New_year_gift` | 12 | id | id, send_reward, get_reward |
| `Newyear_dinner_dish` | 6 | id | id, name, picture, foods, reward |
| `Pac_man_cha` | 7 | id | id, monster, Buff, start_point, turning_point |
| `Pac_man_level` | 7 | id | id, open_day, monster, interval, map, hp, start_point |
| `Pac_man_monster` | 4 | id | id, type, image, speed, behavior |
| `Pac_man_plot` | 5 | id | id, type, effect, image, txt |
| `Planting_trees` | 1 | id | id, turns_group, water_reply, water_grow_value, water_upper_limit, water_friend_times, water_friend_get_times |
| `Planting_trees_reward` | 60 | id | id, group, level, exp, reward |
| `Planting_trees_turns` | 3 | id | id, group, turns, tree_type, reward, turn_name, num |
| `Planting_trees_type` | 4 | id | id, type, level, name, shape_change, shape_change2, scale |
| `Seven_sign_loop` | 21 | id | id, name, type, reward |
| `Seven_trial_bullet` | 2 | id | id, name, type, first_force, speed_effect, demage_num, bomb |
| `Seven_trial_chapter` | 100 | id | id, index, power, map, part_type, part, next_part, … |
| `Seven_trial_stage` | 7 | id | id, template, open_day, limit, star_step |
| `Seven_trial_stagetemplate` | 12 | id | id, arrange |
| `Seven_trial_unit` | 6 | id | id, type, rebound_effect, speed_effect, enemy_hp, defeat_reward, radius |
| `Sevenlogin` | 917 | condition | condition, goods, big_pic |
| `Snake_chapter` | 7 | id | id, obstacle, location |
| `Snake_fruit` | 4 | id | id, buff, icon, weight, sound |
| `Sugar_bawl_reward` | 3 | id | id, type, name, icon, limit, reward |
| `Sugar_card_weight` | 8 | id | id, weight |
| `Sugar_chapter` | 8 | id | id, open_day, score, is_challenge |
| `Sugar_item` | 6 | id | id, item_id, type, icon, mult, time, exchange |
| `Sugar_item_new` | 7 | id | id, item_id, type, icon, mult, time, score |
| `Sugar_main` | 13 | id | id, key, desc, info |
| `Toy_game` | 5 | id | id, name, type, score, desc, player_min, player_max, … |
| `Toy_game_global` | 10 | id | id |
| `Treasure_hunt` | 110 | member_num | member_num, turn, chest_num, chest_pick_num, pick_limit, reward |
| `Treasure_hunting` | 3 | type | type, group_id, cost, all_cost, refresh_item, free_refresh_limit, treasure_num |
| `Treasure_hunting_draw` | 88 | id | id, type, group_id, reward_group, reward, weight, guaranteed, … |
| `Treasure_hunting_num_reward` | 30 | id | id, type, group_id, cumulative_times, reward |
| `Turntable` | 12 | id | id, reward, weight |

### Quests / Achievements / Tasks  
_16 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Achievement` | 105 | id | id, group, name, name_num, desc, desc_num, condition |
| `Achievement_total` | 5 | id | id, name, desc, number, reward |
| `Eye_task` | 92 | id | id, name, num, answer |
| `Eye_task_group` | 123 | id | id, task |
| `Quest_house_chapter` | 11 | id | id, index, map, part_type, bossId, time, bossModel |
| `Quest_house_facilities` | 186 | facilities_id | facilities_id, level, name, facilities_icon, effect, money_cost, level_up_exp, … |
| `Quest_house_global` | 18 | id | id, key, desc, info |
| `Quest_house_level` | 23 | id | id, exp, att, def, hp, att_speed, model |
| `Quest_house_pet` | 16 | id | id, name, model, image, cost, three_bar, three_bar_growth |
| `Quest_house_quest` | 41 | id | id, type, name, quest_dec, quest_icon, star, quest_point, … |
| `Quest_house_robot` | 23 | id | id, name, level, job, attr, power |
| `Task_force_attr` | 8 | id | id, name, type |
| `Task_force_chapter` | 7 | id | id, open_time, map, type |
| `Task_force_item` | 20 | id | id, type, model_change, icon, drop_text, text, bullet_model |
| `Task_force_map` | 8 | id | id, unit_event, combine_id, map_long, map_picture |
| `Task_force_unit` | 11 | id | id, type, move_type, picture, model |

### Economy / Shop / Gacha / Rewards  
_22 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Appearance` | 3813 | id | id, name, part, spine, spine2, bullet, soundid |
| `Break_big_prize_preview` | 150 | id | id, type, good_id, level |
| `Break_cumulative_times` | 43 | id | id, type, cumulative_times, reward |
| `Breakbricks` | 25 | id | id, shape, color, hp |
| `Breaklevel` | 7 | id | id, open_day, map, hp, item_prob |
| `Card_card` | 10 | id | id, name |
| `Card_level` | 14 | id | id, open_day, two_player, scope, card, time |
| `Goods` | 2353 | id | id, name, type, subtype, quality, effect, desc, … |
| `Goods_refresh` | 9 | id | id, serv_macro, name, type, init, max, quantity |
| `Goods_source` | 46 | id | id, name, desc, view, show_btn, icon, icon_atlas, … |
| `Mall` | 1370 | id | id, type, goods, price, icon, name, goods_type, … |
| `Output` | 6576 | id | id, groupid, item, othergroup, probtype, prob |
| `Pay_activity` | 3 | activity_code | activity_code, channel_code, reward, mail_id |
| `Pay_mall` | 4791 | id | id, name, type, pre_id, next_id, bundle_group, mutually_exclusive, … |
| `Pay_rebate_reward` | 5 | id | id, act_group, order, limit, reward |
| `Privilege` | 2 | id | id, serv_macro, bundle_id |
| `Privilege_card` | 36 | id | id, privilege_type, desc, value |
| `Privilege_carditem` | 20 | id | id, serv_macro, desc, value |
| `Privilege_cardtype` | 8 | id | id, serv_macro, privilege_type, gift_id, open_condition, card_bg, card_poster, … |
| `Wartoken` | 95 | id | id, serv_macro, name, bundle_id, bundle_id2, wartoken_type, link_id, … |
| `Wartoken_reward` | 1928 | id | id, level, exp, reward, high_reward, middle_reward |
| `Wartoken_task` | 62 | task_id | task_id, type, reset, condition, reward, desc |

### Localization  
_31 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Init_language` | 25 | id | id, zh_text, en_text, tr_text, es_text, pt_text, de_text |
| `Language` | 27952 | id | id, text |
| `Language_ar` | 27800 | id | id, text |
| `Language_de` | 27798 | id | id, text |
| `Language_en` | 27798 | id | id, text |
| `Language_es` | 27798 | id | id, text |
| `Language_fr` | 27798 | id | id, text |
| `Language_id` | 13172 | — | — |
| `Language_it` | 27809 | id | id, text |
| `Language_pt` | 27798 | id | id, text |
| `Language_ru` | 27798 | id | id, text |
| `Language_th` | 13172 | — | — |
| `Language_tr` | 27798 | id | id, text |
| `Language_tw` | 13288 | — | — |
| `Language_ui` | 6230 | id | id, text |
| `Language_ui_ar` | 6238 | id | id, text |
| `Language_ui_de` | 6237 | id | id, text |
| `Language_ui_en` | 6239 | id | id, text |
| `Language_ui_es` | 6237 | id | id, text |
| `Language_ui_fr` | 6237 | id | id, text |
| `Language_ui_id` | 2133 | — | — |
| `Language_ui_it` | 6237 | id | id, text |
| `Language_ui_pt` | 6237 | id | id, text |
| `Language_ui_ru` | 6236 | id | id, text |
| `Language_ui_th` | 2133 | — | — |
| `Language_ui_tr` | 6237 | id | id, text |
| `Language_ui_tw` | 2133 | — | — |
| `Language_ui_vn` | 2134 | — | — |
| `Language_vn` | 13172 | — | — |
| `Tlanguage` | 19 | id | id, language_short, language_name, alliance_language, sdk_language |
| `Trans_language` | 10 | type | type, name, rank, language_t |

### UI / System / Global / Config  
_12 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Ads` | 36 | id | id, serv_macro, name, reward, times, cd, desc, … |
| `Ads_reward` | 11 | id | id, name, des |
| `Appid` | 11 | fnchannel | fnchannel, appid, type |
| `Client_global` | 18 | id | id, array_value, value |
| `Common_condition` | 23 | id | id, name, type, des |
| `Douyin_card` | 11 | id | id, reward_index, card_id, douyin_card_show |
| `Gamecentre` | 7 | id | id, order, icon, name, background, viewName, location |
| `Gameid` | 7 | game_id | game_id, key, desc |
| `Globalzone` | 55 | id | id, zone |
| `Guide` | 175 | id | id, step, force, next, save, scene, clickObj, … |
| `Notice` | 8 | id | id, key, grop, title, tip, desc, limit |
| `Red_packet` | 976 | id | id, amount, quantity_limit, quantity_max, valid_period, valid_period2, quality |

### Other systems  
_211 tables_

| Table | Rows | Key | Fields |
|---|--:|---|---|
| `Act_cohesion_reward` | 6 | id | id, act_type, act_group, goods_id, limit, reward |
| `Act_guild_pay` | 6 | id | id, act_type, group_id, pay_num, reward |
| `Act_login` | 220 | id | id, act_type, group_id, day, reward, acc_login |
| `Acticity_sheet` | 6 | id | id, language_ui_id, banner, open, view_rank, gradientColor1, gradientColor2 |
| `Activity_adjust` | 252 | type | type, week, day |
| `Activity_boss` | 8 | id | id, type, group_id, boss_id, bossModel, serv_reward, reward |
| `Activity_boss_level` | 80 | boss_id | boss_id, level, boss_hp, spine |
| `Activity_control` | 751 | id | id, name, type, is_round, round_day, pre_display, main_icon |
| `Activity_rank_reward` | 689 | id | id, type, group_id, rank_range, show, rank_reward, rank_reward_spec |
| `Activity_rank_score` | 13 | id | id, type, round_range, condition, score |
| `Activity_schedule` | 7 | id | id, name, time_type, type, time_desc, desc, icon |
| `Activity_task` | 3267 | id | id, desc, condition, difference, acces, reward |
| `Activity_task_group` | 453 | id | id, task_list, reward, open_day |
| `Activity_term` | 882 | id | id, type, round_range, name, group_id, task_list, rank_id |
| `Activity_wartoken_reward` | 55 | id | id, num, cost, reward |
| `Alchemy_enemy` | 1 | id | id, name, bossmodel, bossid, time, map, appear_prob, … |
| `Alchemy_enemy_reward` | 14 | id | id, group, damage, reward |
| `Alchemy_main` | 15 | id | id, key, desc, info |
| `Ani_emoji` | 14 | id | id, item_id, spine, get_way, open_time |
| `Appads` | 253 | id | id, fnchannel, desc, key |
| `Archery_chapter` | 7 | id | id, open_day, template, scale, distance, wind_power, wind_direction |
| `Auto_share` | 53 | id | id, text |
| `Avatar_frame` | 100 | id | id, item_id, icon, icon_group, get_way, preview, open_time |
| `Badge` | 25 | badge_id | badge_id, level, all_name, name, get_desc, baege_icon, level_icon |
| `Beast_chapter` | 7 | id | id, open_day, monster, boss, interval |
| `Beast_job` | 7 | id | id, type, att, att_speed, spine |
| `Beast_monster` | 10 | id | id, model, skill, hp, speed, att_speed, skill_interval |
| `Bingo` | 16 | type | type, level, bingo_map, bingo_reward, preview |
| `Bonfire` | 1 | type | type, group, goods_id, progress_speed, progress_reward |
| `Bonfire_donation_reward` | 6 | id | id, exp, reward |
| `Box_tower_box` | 3 | id | id, group, output_id, shape, quality, item, image |
| `Box_tower_level` | 34 | id | id, group, level, final, grand_prize, box_prob, big_prize_prob |
| `Box_tower_reward_preview` | 27 | id | id, group, goods, box_type, prob, shape |
| `Capture_slave` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Capture_slave_earnings` | 11 | id | id, interval, rate |
| `Capture_slave_pvp_debuff` | 6 | num | num, skill_id, desc |
| `Celebration_active_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Christmas_pack` | 16 | id | id, type, name, icon, pay_mall_id, price, buy |
| `Christmas_tree` | 13 | lv | lv, exp, reward |
| `Circle_label` | 20 | id | id, name |
| `Circle_location` | 11 | id | id, belong, type, name, rank |
| `Circle_location_small` | 279 | id | id, name |
| `Coin_chapter` | 150 | id | id, index, power, level, map, part_type, interval |
| `Collect_cards` | 10 | act_type | act_type, cards, gift_live_time |
| `Color` | 11 | id | id, name, statue_name, color, color2, path, big_path |
| `Combat_manual` | 5 | id | id, title, rule |
| `Complaint` | 7 | id | id, desc, complaint_type |
| `Condition` | 211 | id | id, name, des, guide |
| `Connect_pipe_chapter` | 7 | id | id, open_day, template |
| `Connect_pipe_grid` | 19 | id | id, path_way, type, rotate, identifier |
| `Cost_level` | 18 | id | id, USD, HKD, IDR, SGD, THB, PHP, … |
| `Countdown_box` | 9 | id | id, reward, cli_weight, serv_weight, act_day |
| `Craft_preview` | 16 | id | id, craft_target, main_craft_material, minor_craft_material |
| `Custom_mall` | 182 | id | id, regular_reward, custom_reward |
| `Daily_task` | 16 | id | id, desc, guide, condition, reward, value, open_func |
| `Daily_task_reward` | 5 | box_id | box_id, point, reward |
| `Dark_trial_chapter` | 200 | id | id, index, type, power, level, map, part_type, … |
| `Default_speed` | 7000 | level | level, treasure_level, attr |
| `Dialogue` | 34 | id | id, text |
| `Diamond_chapter` | 750 | id | id, index, power, level, map, part, next_part |
| `Diamond_mall` | 6 | id | id, recharge, first_gift, gift |
| `Difficult_artifact_chapter` | 125 | id | id, index, power, level, map, part_type, interval, … |
| `Difficult_chapter_type` | 1 | id | id, name, banner, main_background, attr_background, open, sort |
| `Difficult_coin_chapter` | 125 | id | id, index, power, level, map, part_type, interval, … |
| `Difficult_diamond_chapter` | 625 | id | id, index, power, level, map, part, next_part, … |
| `Difficult_mount_chapter` | 875 | id | id, index, power, level, map, part, next_part, … |
| `Discount_price` | 15 | id | id, item_id, price, discount_price |
| `Divi` | 9 | id | id, level, icon, name_1, frequency, name, weight |
| `Divi_reward` | 22 | id | id, type, fre, act_type, reward |
| `Divi_tree_chapter` | 100 | id | id, index, power, map, part_type, bossId, interval, … |
| `Dup` | 3 | id | id, key, name, scene_list |
| `Effect` | 943 | id | id, path, radius, scale, dead_time, max_num, max_time |
| `Emoji` | 55 | id | id, emoji_icon, emoji_rank, show_time, type, sheet, sheet_icon |
| `ErrorInfo` | 589 | id | id, info |
| `Eye_item` | 76 | id | id, icon, icon_group |
| `Eye_location` | 40 | id | id, location, icon |
| `Facebookshare` | 6 | id | id, name, reward |
| `Fail_tips` | 4 | id | id, name, icon, desc, view, open_id |
| `Fairy_colors` | 19 | id | id, type, reward |
| `Familiybrawl` | 1 | group | group, self_rank_id, self_rank_reward, family_rank_id, family_rank_reward, self_rank_cross_id, self_rank_cross_reward, … |
| `Familiybrawl_rank` | 4 | group | group, rank_name, point_require, rank_picture, rank_name_picture, rank_picture_g, self_rank_reward |
| `Familiybrawl_rank_reward` | 70 | rank_id | rank_id, group, rank_range, show, rank_reward |
| `Familiybrawl_result_reward` | 1 | group | group, self_rank_id, self_rank_reward, family_rank_id, family_rank_reward, win_reward, lose_reward |
| `Family_brawl_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Famliy_gvg_bufflist` | 14 | buff_id | buff_id, skill_id, buff_desc, target |
| `Fashion_mall` | 50 | id | id, type, free, custom_reward, name, price, gift, … |
| `Fashion_skin` | 693 | skin_id | skin_id, skin_level, expend, attr, power |
| `Favorability` | 8 | id | id, serv_macro, favorability, times_limit, desc |
| `Favorability_level` | 14 | level | level, level_group, favorability, reward, reward_times, buff, icon |
| `Flappy_bird` | 5 | score | score, scene_speed, safe_length, lower_half_length, length_offset, barrier_interval |
| `Food` | 5 | id | id, name, icon, approach, power, time |
| `Forum_checkin` | 6 | id | id, desc, condition, reward |
| `Forum_condition` | 14 | id | id, desc |
| `Forum_task` | 6 | id | id, desc, condition, reward, view |
| `Fountain_preview` | 33 | id | id, act_type, type, reward, weight |
| `Fund` | 2 | id | id, serv_macro, name, gift_id, mid_gift_id, open_condition, privilege_poster |
| `Fund_reward` | 30 | id | id, level, condition, reward, high_reward, mid_reward |
| `Halloween_group_buy` | 78 | id | id, type, name, reward, expend, times, members |
| `Halloween_pvp` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Housekeeper` | 2 | id | id, type, name, desc, price |
| `Housekeeper_chapter` | 12 | id | id, type, chapter_type, chapter_name, chapter_banner, condition, dungeon_class |
| `Housekeeper_shopping` | 8 | id | id, type, type_argu_list, mall_name, condition |
| `Ice_game_daily` | 12 | id | id, type, condition, reward, show_item, desc, desc_args |
| `Ice_random_pet` | 4 | id | id, random, type, model_id, reward |
| `Icebond_chapter` | 7 | chapter_id | chapter_id, type, group_id, initial_bead, ice_location, snow_location, bead |
| `Idol_show` | 4 | id | id, name, background, banner, rally, select, story, … |
| `Idol_story` | 16 | id | id, type, condition, story, reward, title |
| `Inspire` | 6 | id | id, cost, skill_id, show |
| `Jump_link` | 30 | id | id, group, language, link, time_stamp, text, pic |
| `Legacy_team_chapter` | 750 | id | id, index, power, level, diff, map, part, … |
| `Likability` | 4 | id | id, type, group, name, model, icon, level |
| `Loop_break_cumulative_times` | 210 | id | id, type, group_id, cumulative_times, reward |
| `Loop_break_gold_egg_weight` | 342 | id | id, type, group_id, loop, layers, reward, weight, … |
| `Mail` | 118 | id | id, title, type, content, mount, time |
| `Main_task` | 715 | id | id, desc_client, desc_parm, trigger, guide, force_guide, condition |
| `Mainicon` | 157 | id | id, order, icon, name, viewName, effect, right_button |
| `Mandela_grass_chapter` | 100 | id | id, index, power, map, part_type, part, next_part |
| `Map` | 55 | id | id, path, points, color, move |
| `Mario_main` | 7 | id | id, type, time, task, day, points, guanqia |
| `Mario_milestone` | 21 | id | id, condition, get_way, reward |
| `Mayday_lottery` | 49 | id | id, day, ball, time, type, rewards, people |
| `Mbti` | 16 | id | id, type |
| `Mix` | 140 | id | id, type, id2, quality, cost |
| `Mole_enemy` | 5 | id | id, type, hp, attack, speed, shape, enter, … |
| `Mole_hammer` | 5 | id | id, type, group, name, attack, attack_range, energy_multiplier, … |
| `Mole_level` | 13 | id | id, type, group, challenge_level, time, monster_id, guard_point, … |
| `Mole_main` | 1 | id | id, type, level, guard_zone, safety_zone, monster_spawning_area, special_move |
| `Music_main` | 5 | id | id, type, rank_id, day, bgm, time, speed |
| `Music_notes` | 829 | id | id, barrier, type, appear_time, number, direction, click_time |
| `Nation_flag` | 11 | id | id, flag_name, person, person_rank, family, family_rank |
| `NewFuncOpen` | 120 | id | id, key, desc, level, taskId, guankaId, open_day |
| `New_server_launch` | 8 | id | id, act_type, group_id, day, free, diamond, diamond_price |
| `New_server_meet` | 8 | id | id, desc, condition, day, reward, access |
| `News` | 684 | id | id, group, condition, coefficient, rank, content, red_packet |
| `Ninja_chapter` | 5 | id | id, level, type, name, unlock, map |
| `Ninja_item` | 7 | id | id, type, move, model, icon |
| `Ninja_map` | 4 | id | id, item_event, long |
| `Note_matching_level` | 7 | id | id, act_day, time, origin_probability, up_probability, ori_speed, up_speed |
| `Paint_color` | 28 | id | id, color, open_times |
| `Panda_enemy` | 3 | id | id, speed, score, image |
| `Panda_level` | 7 | id | id, open_day, enemy, enemy_frequency, hp, time, initial_enemy |
| `Park_cross_pvp_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Park_cross_reward` | 20 | id | id, type, rank, reward |
| `Park_pvp_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Park_pvp_debuff` | 37 | num | num, type, skill_id, time, lose_cd, debuff_desc, desc_parm |
| `Phoenix_tips` | 20 | id | id, type, skill, open_time |
| `Pic_text_guide` | 11 | id | id, type, order, pic, text |
| `Pk_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Pre_func` | 18 | id | id, desc, condition, reward, main_desc, condition_desc, icon |
| `Program_reset` | 12 | id | id, desc, show_descition, icon, sort |
| `Quiz` | 111 | question_id | question_id, question_text, type, options, answers |
| `Quiz_dice` | 16 | dice_point | dice_point, reward |
| `Ranktype` | 171 | id | id, rank_type, refresh_time, show_num, name, prefix, is_show |
| `Recall_reward` | 21 | id | id, desc, type, condition, reward |
| `Recall_turantable` | 8 | id | id, reward, weight, special |
| `Reservation` | 28 | product_id | product_id, reward, mail_id |
| `Robot` | 229 | id | id, level, point, num, type, rank |
| `Scene` | 12 | id | id, name, type, map_wh, desc, picture, level |
| `Scene_object` | 28 | id | id, key, name, forbid_move_range, attack_cd |
| `Server_puzzle` | 4 | type | type, group, goods_id, output, progress_puzzle, progress_speed, progress_reward |
| `Setting` | 14 | id | id, type, rank, state, title, default_value, is_show |
| `Sever_list` | 303 | id | id, name, sever_id, type, plat |
| `Share` | 30 | id | id, type, num, stage_num, reward, desc |
| `Sheep_a_sheep_card` | 16 | id | id, icon |
| `Sheep_a_sheep_chapter` | 21 | id | id, chapter, open_day |
| `Shooting_chapter` | 21 | id | id, open_day, template, scale, distance, speed, wind_power |
| `Shooting_chapter_cha` | 20 | id | id, template, scale, distance, speed, wind_power |
| `Ski` | 10 | id | id, depth, obstacle_condition, obstacle_time, obstacle_generation, coin_condition, coin_generation |
| `Ski_chapter` | 8 | id | id, open_day, coin, is_challenge |
| `Skin` | 74 | id | id, name, type, icon, spine, condition, open_time |
| `Sorting_master_chapter` | 7 | id | id, basket_num, basket_speed, basket_content, shelf_content, star_num, open_day |
| `Sorting_master_item` | 16 | id | id, icon |
| `Sound` | 245 | id | id, path, cd, max |
| `Star_diamond_mall` | 7 | id | id, reward, first_reward |
| `Star_rain` | 5 | type | type, group_id, star_draw, pool_accumulation |
| `Star_rain_draw` | 72 | id | id, type, group_id, goods_icon, percentage, reward, weight, … |
| `Star_rain_draw_guaranteed` | 20 | id | id, type, group_id, num, reward |
| `Star_rain_draw_times` | 40 | id | id, type, group_id, cumulative_times, reward |
| `Summoner_passive` | 20 | id | id, skill, num, passive_skill, petrace |
| `Sys_progress` | 31 | id | id, name, lang_id |
| `Talk_option` | 66 | id | id, type, option, differnece, jump_stage, jump_view, remind |
| `Talk_stage` | 36 | id | id, type, talk, differnece, options, options_color, size |
| `Tanabata_checkin` | 5 | id | id, type, group_id, reward |
| `Tanabata_flower` | 4 | id | id, flower_number, giftflower_number, lovesickness_number, is_show |
| `Text_adventure` | 280 | id | id, chapter, part, next_part, event_group, event_guarantee, map |
| `Text_adventure_buff` | 127 | text_adventure_buff | text_adventure_buff, skill_id, skill_lv, buff_name, buff_desc, restore_blood, pic |
| `Text_adventure_buff_group` | 151 | id | id, group_id, attr_id, type, pro |
| `Text_adventure_chapter` | 14 | id | id, name, map, poster, time_limit, pre_text, poster_position |
| `Text_adventure_event` | 64 | id | id, type, button, map_element, monster, attribute, buff_num |
| `Text_adventure_event_pack` | 71 | id | id, step, weight, desc, button_text1, result_text1, button_text2 |
| `Thanksgiving_food` | 16 | id | id, exp, tag |
| `Thanksgiving_recipe` | 4 | id | id, act_type, act_group, name, pic, cost, level_reward, … |
| `Thanksgiving_serv_level` | 7 | id | id, act_type, act_group, goods_id, level, exp, reward |
| `Title` | 120 | id | id, item_id, icon, icon_group, get_way, preview, open_time |
| `Tournament_chapter` | 1 | id | id, index, power, level, map, part_type, part, … |
| `Trap` | 269 | id | id, type, duration, triggerRange, triggerTarget, target, buffId |
| `Treasure_level` | 35 | level | level, expend, pro_quality, time, ticketprob, ticketmax, skin |
| `Treasure_skin` | 10 | id | id, path, shendeng_plot, shendeng_scale, equip_path, icon, icon_scale, … |
| `Trick_or_treat_chapter` | 15 | chapter_id | chapter_id, type, name, skills, reward |
| `Tzone` | 77 | id | id, zone_id, zone_name, zone_short, language, time_zone, areacode |
| `Valentine_reward` | 13 | id | id, size, num, reward, output, open_view, back_color |
| `Valentine_template` | 8 | id | id, fixed_reward, random_reward, select_gift, diamond_shop |
| `Wedding_talk` | 3 | id | id, question1, answer1, question2, answer2, question3, answer3 |
| `Wedding_time` | 84 | id | id, week, time, pre_time |
| `Weekly_card` | 7 | id | id, act_group, day, reward |
| `Welfare` | 3 | id | id, openfunc, name, last_time, mainicon, wartoken |
| `Welfare_task` | 26 | id | id, group_id, desc, condition, reward, reset |
| `Work_log` | 20 | id | id, serv_macro, type, title_type, title, messge |
| `Work_team` | 9 | team | team, system, type_name, team_name, talent, is_pet_work, desc |
| `Workshop` | 3 | id | id, team_id, name, item, is_lock |
| `_index` | 0 | — | — |