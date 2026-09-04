# LOM Battle Simulator — Local Session Prompt (Clean-Room Analysis + Full Extraction)

> Paste this whole file as the opening message of the local session. It is a **handoff of verified knowledge**, not a set of conclusions to trust blindly. Every claim below is tagged with how it was verified. The local session's first job is to **re-verify** it against the source files on disk, then do a **complete extraction** of every game file, and only then start on the simulator.

Credit line for all outputs: **Bird → Discord @birrrd08**

---

## 0. Mission and ground rules

1. **Goal:** finish a PvP battle simulator for *Legend of Mushroom* (LOM) that reproduces the client's deterministic combat math bit-for-bit. Accuracy over completeness. Fewer systems implemented exactly beats many systems implemented loosely.
2. **Start from scratch on analysis.** Do not import conclusions from prior docs without re-deriving them from `game_script.js` and the decoded config tables. Prior docs are a map, not evidence.
3. **Verification protocol for every formula:** (a) locate the function in the prettified script and quote it, (b) state the line/module, (c) confirm the constants it reads exist in the hard-coded `ConfigGlobal` defaults object (or the table it names), (d) write a unit test that feeds known inputs through your implementation and compares against a hand-trace of the quoted code. A formula without (a)–(d) is "unverified" and must be labelled as such.
4. **Never double-apply passives.** If a stat already lands in the player's displayed attribute (mounts, backs, artifact skins, "global %" sources), the sim takes the final attribute as input and does not re-add the source.
5. **Preserve engine quirks exactly** (list in §8). Do not "fix" them.
6. Output naming convention: decoded tables are `Like_this.json` (matching the FilePack table name). Attribute keys are `like_this`.

---

## 1. What is on disk

| Path | What it is | Verified |
|---|---|---|
| `lom.joynetgame.com.zip` | Full web capture of the client (130 files, 28.3 MB): `index.html`, Cocos engine `cocos-js/cc.b2b21.js`, app shell `application.16f94.js`, `src/system.bundle.*.js`, `src/polyfills.bundle.*.js`, `src/chunks/bundle.fbbab.js`, bundle index files, **game script `assets/script/index.4c467.js` (18,032,462 bytes)**, 87 `bundle-res` asset files, third-party SDKs (Facebook, Google, Apple, captcha). | Listed this session |
| `game_script.js` | Copy of `assets/script/index.4c467.js`. **md5 `d46684cc63ba58527d7b01521320abdc` — identical to the one inside the zip.** | md5 compared this session |
| `game_script_pretty.js` | Beautified copy (gitignored, ~457k lines). Regenerate locally: `npx js-beautify game_script.js > game_script_pretty.js`. **All line numbers in prior docs refer to this file and will shift if the beautifier or options differ.** | Not regenerated this session |
| `uploads/bundle-firstload-res.zip` | The config bundle: `config.5e4de.json` (bundle manifest), `native/c8/c8ccfd1c-…8e8a4.bin` (**12,441,263 bytes — the entire config database**), `import/38/384ef847-…ceb0d.json` (**protobuf schema for the network protocol**, ~500 KB), `import/c8/…5d048.json` (BufferAsset stub). | Decoded this session |
| `uploads/bundle-LoadingView.zip` | Loading screen bundle. Contains two `*.manifest` files (3.5 MB each) — these are **Cocos hot-update manifests for the iOS build** listing every remote asset with size and md5, and the CDN URL pattern `https://xxjzz-cdnres.joynetgamestudio.com/cdnconfig_{0}/stable/ios_us/ios-sea-branch/public/…`, version string `1.0.476`. Useful as a complete asset inventory. | Inspected this session |
| `data/schemas/` | 712 `Config*.json` field schemas extracted from the prettified script (field order, type, XOR flag, main key). | Used this session |
| `data/enums/` | 96 enums extracted from the script (AttribDefine, HealthType, BuffGroupType, EffectTriggerType, SkillType, UnitConfig …). | Present |
| `data/constants/` | `battle_constants.json`, `pvp_constants.json`, `attribute_caps.json`, `config_global.json`, `config_key.json`. | Present |
| `data/formulas/`, `data/systems/` | Prior-session JSON write-ups of formulas and systems. Treat as hypotheses. | Present |
| `reverse-engineered/` | 46 markdown deep dives + `97_UNKNOWNS.md`, `98_DISCREPANCIES.md`, `99_FULL_DAMAGE_PIPELINE.md`, `LOM_MASTER_FORMULA_REFERENCE.md`, `46_CONFIG_TABLES_MASTER_REFERENCE.md`. Hypotheses with line references. | Present |
| `battlesim/reference/` | 21 reference docs + 8 `*_master.json` files (pals, skills, heroes, mounts, artifacts, avians, backs, bosses) + `LOM_Database-5.xlsx` (community spreadsheet). | Present |
| `uploads/battlesimV1.html` | **V1 simulator (Alpha 6.0)** — the one being finished. `battlesim/index.html` is a separate dark-theme rewrite. `battlesim/battlesim_old_ref-only.html` is frozen. | Present |
| `LOM Math by Yuko (2).pdf` | Community math doc. Secondary source only. | Present |
| Python tools at repo root | `decode_config_data.py`, `extract_schemas.py`, `extract_enums.py`, `extract_constants.py`, `diff_config_data.py`, `filter_capture.py`, `build_lom_database.py`. | Run this session (decode + build) |

---

## 2. Client architecture (what the game is)

- **Engine:** Cocos Creator 3.x web build. Modules are `System.register("chunks:///_virtual/<Name>.ts", …)` blocks inside the 18 MB script. Grep for `chunks:///_virtual/` to enumerate every module (Config classes, buffs, skills, AI, views).
- **Bundles:** `main`, `resources`, `internal`, `bundle-res` (art/prefabs), `bundle-firstload-res` (config), `bundle-LoadingView`. Each bundle has `config.<hash>.json` mapping uuid → path.
- **Config load path:** `BaseConfig.loadBufferData()` reads the FilePack and hands each table's rows (positional arrays) to a `Config<Table>` class whose getters map index → field name. `BaseConfig.loadData()` is the plain-JSON dev path (splice header row, freeze, index by key).
- **Battle is deterministic and client-side**, with server validation. The client replays an `operators` array (unit id, frame, skill id) to the server; every `_s2c` battle result carries a `code` int. All math goes through `FixMath` — there is no floating RNG in damage math. (Hit/crit/combo rolls do use a PRNG; find and quote it: prior docs claim an LCG `(9301*seed+49297)%233280` in a `FixRandom` module. **Verify.**)
- **Frame loop:** 30 FPS logical (`frameTime 0.033`). Attack speed, cooldowns, buff durations are in frames.

---

## 3. Config database: where it is and how to decode it (VERIFIED THIS SESSION)

**File:** `bundle-firstload-res/native/c8/c8ccfd1c-3783-480a-9b7c-6441acd885c0.8e8a4.bin` (path `config/datas` in the bundle manifest).

**Container: FilePack v5**
```
u16 BE  version            (= 5)
u16 BE  table_count        (= 908)
repeat table_count:
  u16 BE name_len, name (utf-8)
  u32 BE data_len,  data
```

**Per-table decode (Layer A):**
1. `byte = 255 & ~(32 ^ byte)` for every byte (equivalently `(byte ^ 32) ^ 0xFF`)
2. zlib-decompress
3. `u32 BE count`, then `count ×` (`u16 BE len` + utf-8 JSON string) → each string is a JSON **array** (positional row)
4. Map positions → names with `data/schemas/Config<Table>.json`

**Layer B — protected ints:** fields flagged `xor: true` are stored as `value ^ 24455` (`CONFIG_KEY`, defined in the script as `t("CONFIG_KEY",24455)`). Only 5 tables use it: `Unit` (97 fields, 12 XOR'd), `MainUnit` (90 fields), `Petlevel`, `Skill` (`autoDis`, `initialPower`, `maxPower`, `powerRecovery`), `Reversion_war_chess`. A raw `24455` in a protected field means `0`.

**Layer C — BigNumber (NEW, found this session):** fields typed `bignum` (unit `att`/`def`/`hp`, boss `damage`, …) are arrays. From `BigNumber.ts` in the script:
```js
var r=1e9, i=534862510;
toNumber(){ if(1==this._nums.length) return this._nums[0]^i;
  for(var t=r, n=this._nums[0]^i, s=1; s<this._nums.length; s++){
    var e=FixMath.roundInt((this._nums[s]^i)*t); n=FixMath.roundInt(n+e); t=FixMath.roundInt(t*r);} return n; }
```
i.e. `value = (nums[0] ^ 534862510) + Σ (nums[k] ^ 534862510) × 1e9^k`. Example: `[534862399]` → 145. `decode_config_data.py` now applies this.

**Sharded tables:** `MainUnit1…MainUnit100` and `Chapter1…Chapter100` are 100 shards each and use the `ConfigMainUnit` / `ConfigChapter` schema. `Language_*` tables are plain `[id, text]` pairs. The decoder now handles both.

**Result of this session's run:** 908/908 tables decoded, 733,618 records, 908/908 schema-mapped. Sanity checks that passed: `Level.pvp_injury_reduce` = 10000 @1, 110000 @50, 569000 @100, 2806000 @150, 6090000 @200, **7540000 @220**; `Goods` 1 = "Gold"; `Mount` 1 = "Lily Pad"; `Spirit` 101 = "Brawl Hound"; `Angel` 10001 = "Sprite of Knowledge".

**Names:** most `name`/`desc` fields are string ids into `Language_en` (27,798 rows). UI strings are in `Language_ui_en` (6,239). Resolve `Language_en` first, then `Language_ui_en`. Note the `Spirit` table misspells its name field as `mame`.

**Protocol schema:** `import/38/384ef847-…ceb0d.json` is a Cocos JsonAsset; element `[5][0][2]` is a protobuf.js JSON descriptor with 79 namespaces (`arena`, `battle_check`, `cross_pvp`, `gvg`, `fly`, `angel`, …). Use it to learn what the server sends for a battle (opponent attribute lists, formations, seeds).

**Commands (all run this session):**
```bash
unzip -o uploads/bundle-firstload-res.zip -d capture/
python3 decode_config_data.py capture/ --output data/tables --proto-output data/proto_schema.json
python3 build_lom_database.py data/tables --out dist   # → lom_config.sqlite + LOM_Items_Mounts_Database.xlsx
```

---

## 4. Key tables for the simulator (row counts from this capture)

| Table | Rows | Main key | Why it matters |
|---|---|---|---|
| `Attribute` | 192 | id | Attribute id → key, `num_type` (1 int / 2 = ÷10000 pct), `up_limit` cap, `module`, `group`. The join everything hangs on. |
| `Global` (**not in the FilePack**) | 744 keys | key | Battle constants (§6). `ConfigGlobal` is hard-coded in the script (~line 235650 pretty) as a defaults object; `extract_constants.py` pulls it into `data/constants/config_global.json`. There is no `Global.json` table. |
| `Level` | 220 | level | `pvp_injury_reduce` (÷1e4 = PvP damage divisor), `power_par`. |
| `Unit` / `MainUnit1-100` | — / 660 per shard | id | Combat stat rows for every unit (players, pals, avians, spirits, bosses). 12 XOR fields, BigNumber att/def/hp. |
| `UnitType`, `UnitModel` | — | id | Per-type constants (`suspend_time`, `vertigo_time`), animation frame data (attack speed derives from frame counts). |
| `Jobs`, `Jobs_wakeup` | 38 / 2000 | id | Classes: `skill`, `passive_skill`, `passive_imprint`, `job_change` tree. |
| `Skill` (1547), `Skill_level` (18,838), `Skilleffcet` (1073, sic), `Skill_pos` | — | id (+level) | Active/passive skill definitions, per-level `skillPar`, effect ids, energy (`initialPower`/`maxPower`/`powerRecovery` — XOR'd). |
| `Buff` (2476), `Specil_buff` (12) | — | id | Buff rows: `type`, `group`, `mutex`, `add_max`, `action` string (→ buff class in `buffMap`), `param1-5`. |
| `Pet` (322), `Petlevel` (19,824), `Pet_talent`, `Pet_proficiency`, `Pet_pos` | — | id | Pals: `unitId`, `talent`, per-level stats (XOR'd). |
| `Fly` (35), `Fly_level`, `Fly_entry` (1734), `Fly_advance`, `Fly_hybrid`… | — | id | Avians. **`ConfigFly` is the avian table; there is no `ConfigBird`.** |
| `Spirit` (20), `Spirit_level` (72), `Spirit_attrbonus_*`, `Spirit_affix_group` | — | spirit_id | Guardian Spirits — a **spawned combat unit** (`unit` → Unit id, `bullet`). |
| `Angel` (35), `Angel_skill` (310), `Angel_star` (350), `Angel_array` (7), `Angel_develop` | — | id | Star Heroes (formation, skill1/skill2, energy). **Separate system from Spirits.** |
| `Mount` (72), `Mount_skin` (660), `Mount_level` (300), `Mount_ability` (1503), `Mount_abilitycost` | — | id / mount_id+skin_level | Mounts and skins: `skin_skill`, `attr`, `power`. |
| `Artifact` (44), `Artifact_skin` (473), `Artifact_level`, `Artifact_gem*` | — | id | Artifacts, skins, gems. |
| `Back_decoration` (48), `Back_skin` (495), `Back_level` (780), `Back_talent` (2652) | — | id | Back accessories + wing talent tree. |
| `Equipment` (5357), `Equipment_attr`, `Equipment_level`, `Equipment_refinement`, `Equipment_resonance`, `Equipment_suit` | — | id | Gear. `preAttr` = `[[attrId,val],…]` pairs. |
| `Relic` (5005), `Relic_pos` | — | id | Relics. |
| `Fate`, `Fate_level` (5600), `Fate_fusion` | — | fate_id | Fate cards. |
| `Path_to_divinity`, `Path_affix` (342), `Path_upper_limit` (213) | — | id | Path to Divinity affix caps. |
| `Ring`, `Ring_level`, `Badge` | — | id | Rings/badges. |
| `Goods` (2353), `Goods_source` | — | id | All items (`type`, `subtype`, `quality`, `effect`, `getItems`). |
| `Chapter_type`, `Pvp_chapter`, `Cross_pvp_*`, `Season_pvp_*`, `Cross_pvp_robot` (275) | — | id | Battle-mode configs; robots are fully-specified PvP opponents = **great regression fixtures**. |
| `Language_en`, `Language_ui_en` | 27,798 / 6,239 | id | Names/descriptions. |

Storage scale: rates and multipliers are basis points ÷ 10,000 (`9000` = 90%, `20000` = 2.0×). Some display fields are ×100. Check `Attribute.num_type` before assuming.

---

## 5. Where the combat code lives (prior-session line numbers in `game_script_pretty.js` — RE-VERIFY)

| Module | Approx. line | Contents |
|---|---|---|
| `BaseConfig` / `CONFIG_KEY` | ~184594 / ~184611 | Table loading, XOR decode |
| `FixMath` | ~292602 | `round`, `roundInt`, `clamp` |
| `EnumDefine` | ~278546 | HealthType, AttackType, StateType, DmgType, BuffGroupType (46), EffectTriggerType (16), SkillType (5), TargetFilter, HitType, BindType |
| `AttribDefine` / `MetaAttrib` | ~349630 | 192 attribute ids; value assembly; `_checkValue = base ^ 32` anti-cheat |
| `buffMap` / `aiMap` / `skillMap` registration | ~332125 | 80 buff action strings → classes; AI types; skill handler types |
| `BattleMain` | ~188200 | `frameTime`, `injuryReduce`, `shieldDecay`, `treatDecay` defaults |
| `HurtUtil` | ~322750–323007 | **All damage functions**: `normalHurt`, `normalDoubleHurt`, `normalCounterHurt`, `calHurt`, `calArmorAndBlock`, `calSuppressAndInspire`, `checkHit`, `checkDoubleAct`, `checkCounterAct`, `checkDizz`, `checkSkillCirt`, `SkillHurt`, `spiritNormalHit`, `hpSteal*` |
| `BattleData.setPlayerList` | ~187356 | Stat assembly entry: job → unit, attrs, equip, pets, skills, spirit, passives |
| `Unit.addDamage` | ~449240 | Damage application: PvP divisor, shield absorb, block, HP change, death prevention chain |
| `SkillHandleNormal` / `SkillHandleCounter` | ~429879 / ~429630 | Normal attack + counter execution |
| `SkillRunner.healthTarget` | (minified line ~7229) | Applies Total DMG Bonus/RES to the 13 types in `NeedAddDamHurtList` |
| Buff classes | ~192229–196788 | `BuffBleed`, `BuffSkillValue` (11 calTypes), `BuffShield`, `BuffVampire`, `BuffExtraDamage`, `BuffGiantSlayer`, `BuffSkillFragileAdd`, `BuffDeferDamage`, … |
| `ChapterArena` | ~197534 | 1v1 PvP: avg level → `injuryReduce`, `shieldDecay`, `treatDecay` |
| `getActSpeed` | ~431378 | `round(att_speed / round(30 / frameCount))` |
| `BigNumber` | (search `"BigNumber",void 0`) | Key 534862510, base 1e9 |

Fast way to rebuild this map: `grep -n 'chunks:///_virtual/' game_script_pretty.js > module_index.txt`.

---

## 6. Constants (from the hard-coded `ConfigGlobal` object in the script; spot-checked in the minified script this session)

| Key | Raw | Effective | Use |
|---|---|---|---|
| `miss_correct` | 9000 | 0.90 | exponent on miss curve: `pow(100·miss, 0.9)/100` |
| `vertigo_correct` | 9000 | 0.90 | same shape for stun |
| `shield_correct` | 4000 | 0.40 | PvP `shieldDecay = round(shield_correct/1e4)` — **level independent** |
| `hp_recovery_correct` | 3000 | 0.30 | PvP `treatDecay = round(hp_recovery_correct/1e4)` |
| `total_damage_add_down_limit` | 2000 | 0.20 | floor of `1 + total_dam_add − total_dam_def` |
| `battle_up_limit` | `[[1008, 8000]]` | 80% | PvP evasion cap (attribute 1008) |
| `initial_power` | 152 | | starting skill energy (verify unit) |
| `auto_skill_delay` | 100 | | |
| `skill_delay` | `[0,500,…,10000]` | ms | |
| `initial_attr` | 74 pairs | | default attribute values for a player unit (e.g. 1003 att_speed 9000, 1005 crit_dam 20000, 1006 crit_def 10000, 1013/1032/1033/1038/1039/1047 = 10000, 1031 = 6000, 1024 def 20) |
| `frameTime` | 0.033 | 30 FPS | `BattleMain` |
| `pvp_k` / `pvp_initial_score` | 30 / 1000 | | ELO |
| Attribute caps (`Attribute.up_limit`) | 1014,1015,1042 = 10000; 1018,1019,1020,1021,1034,1035,1052 = 8000; 1059 = 6000 | | everything else uncapped |

Confirmed present in `game_script.js` by grep this session: `total_damage_add_down_limit/1e4`, `Math.pow(x,.98)`, `shieldDecay=n.round(r.shield_correct/1e4)`, `treatDecay=n.round(r.hp_recovery_correct/1e4)`, `pvp_injury_reduce/1e4`, `"CONFIG_KEY",24455`.

---

## 7. Combat math as currently understood (HYPOTHESES — re-derive from code)

Math primitives:
```
round(x)    = (x > 0 ? floor(1e4·x + 0.5) : ceil(1e4·x − 0.5)) / 1e4
roundInt(x) = floor(round(x))
```
Rounding happens at nearly every multiplication. The sim must replicate the exact order.

Attribute value: `value = roundInt(roundInt(base + addValue) × time + addExtraValue)`, then `min(value, up_limit)` if capped, then `÷1e4` if `num_type == 2`.

Base damage (all types): `base = max(roundInt(ATK − roundInt(DEF × (1 + def_coe))), 1)` — attribute 1060 `def_coe` is missing from all community formulas.

| Type | Multiplier and resistance | Notes |
|---|---|---|
| Basic | `roundInt(base × round(att_dam × round(1 − res)))` | res from `calArmorAndBlock(att_resist)` |
| Combo | `roundInt(roundInt(base × double_hit_dam) × round(1 − res))` | res from `double_hit_def` (1034) |
| Counter | same shape with `counter_dam`, `counter_def` (1035) | |
| Skill | same shape with `skill_dam_extra`; **resistance keyed by `double_hit_def` (1034) not `skill_resist`** — engine quirk | then skill % and `active_skilldamage_par` (1043) |
| Pal basic | `ATK = parent's ATK`; `roundInt(base × round(round(partner_dam × parent.partner_dam_extra) × round(1 − res)))` | res from `calSuppressAndInspire(partner_resist)`; pal combo does **not** apply 1034 |
| Spirit vs spirit | `round(ATT × (spirit_dam_add − spirit_dam_def + 1) × (1 − spirit_dam_def_final))` | |

Then in order: `calHurt` (`max(1 + total_dam_add − total_dam_def, 0.20)` — verify whether this is applied here or only in `healthTarget`), crit `roundInt(dmg × max(1.5, round(crit_dam / max(0.5, crit_def))))`, skill crit `roundInt(pow(roundInt(dmg × round(1 + skill_crit_dam)), 0.98))` (exponent on the whole product), buff modifiers (ExtraDamage, GiantSlayer, Fragile, SkillDamageAdd), Total DMG Bonus/RES in `healthTarget` for all 13 types in `NeedAddDamHurtList`, PvP divisor `max(roundInt(dmg / injuryReduce), 1)` with `injuryReduce = Level[roundInt((lv1+lv2)/2)].pvp_injury_reduce / 1e4`, shield absorb (`shieldDecay`), HP change, death prevention chain (Time Reversal → Remake HP → Immune Death).

Pierce/Block: modify the **resistance**, not damage: `res −= min(0.5, (armor_penetration − ignore)/1e4)`, block adds. Ignore-type stats are subtractive on the rate: `max(rate − ignore_rate, 0)`. Miss: `pow(100·raw, 0.9)/100`, PvP cap 80%. Buff mutex: 1 replace, 2 unique, 3 stack to `add_max` (refresh all), 4 unique per caster, 5 refresh per caster; `type 0` buffs execute instantly. `control_res` (1042) shortens stun/ban_act duration: `round(d − round(d × control_res))`.

Open verification items from prior sessions (`97_UNKNOWNS.md` D12–D15): combo resistance rounding order, `round()` at exact 0.00005 boundaries, effective crit after ignore, PvE vs PvP evasion cap source (`Chapter_type`).

---

## 8. Quirks to preserve (do not "fix")

1. Skill resistance reads attribute **1034 `double_hit_def`**, not `skill_resist`.
2. **Inspire/Suppress rate names are swapped** in the code. Keep the code's naming.
3. `ConfigFly` = avians. No `ConfigBird` exists.
4. Guardian Spirits (`ConfigSpirit`) ≠ Star Heroes (`ConfigAngel`).
5. `Skilleffcet` and `Spirit.mame` are misspelled in the game data. Keep the names for joins.
6. The 0.98 exponent applies to the whole `dmg × (1 + skill_crit_dam)` product.
7. Shield decay 0.40 and heal decay 0.30 in PvP are level-independent.
8. `BuffVampire` reads `total_dam_def` from the buff **owner** (the caster's own unit) — the Dragonic Resonance finding.

---

## 9. State of the V1 simulator (`uploads/battlesimV1.html`) and known gaps

Implemented: FixMath, LCG PRNG, PvP injury table, attributes 1001–1082/2001–2033/6001–6007, 8 T5 classes, 38 active skills, 90 pals (stat toggles), talents, relics, 13 buff classes, damage pipeline, crit, pal damage, spirit tenacity/TPEN.

Not implemented (priority order): pal **battle** effects (only stat toggles exist), Star Hero battle skills + energy + formation, Spirit as a spawned unit with own HP/ATK/skills, skill energy system (skills currently fire on cooldown), execute/bleed DOT/clone/disarm skill effects, death-prevention ordering, freeze/bind/taunt, damage share/reflect, launch mechanic, artifact/back/avian active skills, angel develop passives, suits, fate fusion passives, path caps, ring base skills, badge scaling.

Design: single HTML file, no build step. Pal system split into "stat effects" (toggleable) vs "battle effects" (auto-applied). Attack speed → frames between attacks, skill CDs in frames.

---

## 10. Tasks for this local session, in order

### Phase A — Complete extraction (do all of it before analysis)
1. Unzip all three archives into `capture/`. Run `filter_capture.py` to drop tracking/auth junk. Keep the Cocos bundle index files.
2. Regenerate `game_script_pretty.js` and rebuild `module_index.txt` (`grep -n 'chunks:///_virtual/'`). Record the beautifier version so line numbers are reproducible.
3. Run `extract_schemas.py`, `extract_enums.py`, `extract_constants.py` against the fresh pretty file. **Diff** the outputs against `data/schemas`, `data/enums`, `data/constants` and report any change.
4. Run `decode_config_data.py` → `data/tables/` (expect 908 tables / 733,618 records). Run `build_lom_database.py` → SQLite + XLSX. Compare against the `lom_config.sqlite` shipped with this handoff (`diff_config_data.py` works on table dirs).
5. Extract the protobuf descriptor (`data/proto_schema.json`) and list every `battle`/`arena`/`pvp` message with its fields.
6. Parse both `*.manifest` files in `bundle-LoadingView` into a CSV asset inventory (path, size, md5). Inventory the 87 `bundle-res` files by uuid → path using `bundle-res/config.*.json` if present, else the `import/` JSON headers.
7. Extract `UnitModel` animation frame data (attack frame counts drive real attack speed).
8. Produce `EXTRACTION_REPORT.md`: what was extracted, counts, hashes, anything that failed.

### Phase B — Verification of §3, §6, §7, §8
For each row: quote the code, give the module name and line, and write the unit test. Produce `VERIFICATION_LOG.md` with columns: claim · source quote · status (confirmed / corrected / unverified) · test name. Corrections go to the top of the report.

### Phase C — Simulator
1. Build a **golden-fixture harness**: take `Cross_pvp_robot` / `Season_pvp_robot` rows (fully specified opponents) and any real battle logs the user can capture, and make the sim reproduce them. A sim that matches robots is the acceptance criterion.
2. Implement gaps from §9 in priority order, one system at a time, each with tests, each gated by a code quote.
3. Keep the file single-HTML, keep the stat-toggle / battle-effect split, keep the credit line.

---

## 11. Files shipped with this handoff

| File | Contents |
|---|---|
| `LOM_LOCAL_SESSION_PROMPT.md` | This file. |
| `lom_config.sqlite` | All 908 tables from the 2026-02-28 capture with named columns, XOR and BigNumber decoded, arrays as JSON text; `_tables`, `_fields` (schema types + XOR flags), `names_en`, and 174 `<Table>_named` views with `name_en` resolved. |
| `LOM_Items_Mounts_Database.xlsx` | Curated sheets with English names: Items (Goods), Mounts, Mount Skins/Levels/Abilities, Equipment, Suits, Artifacts + Skins, Back Decorations + Skins, Pets, Avians, Angels, Spirits, Relics, Jobs, Attributes, Skills, Buffs, Fate, Rings, Badges, Level (PvP factor). |
| `lom_re_toolkit.zip` | `data/schemas/` (712), `data/enums/` (96), `data/constants/`, `data/formulas/`, `data/systems/`, `proto_schema.json`, `_index.json` (table → record count), all Python tools, `module_index` hints, and the reference docs most useful for verification (`00_SECTION_MAP`, `97_UNKNOWNS`, `98_DISCREPANCIES`, `99_FULL_DAMAGE_PIPELINE`, `LOM_MASTER_FORMULA_REFERENCE`, `46_CONFIG_TABLES_MASTER_REFERENCE`, `battlesim/CONTEXT_TRANSFER.md`). |
| `decode_config_data.py` | Decoder, updated this session: sharded-table schemas, Language tables, BigNumber decode. |
| `build_lom_database.py` | New: decoded tables → SQLite + XLSX. |
