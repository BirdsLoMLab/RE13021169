# 97 — Unknowns & Unresolved Items

Items that couldn't be fully resolved from static code analysis alone.

---

## A. Requires Runtime Data

### 1. PvP Factor Table (configLevel)
The code reads `configLevel.getDataByKey(level).pvp_injury_reduce` but the actual data values for each level (1-300+) are stored in external config data, not hardcoded in the script. We know the schema (level → pvp_injury_reduce) but not the actual numbers.

**To resolve:** Extract config data at runtime or from data files.

### 2. Attribute Caps (up_limit)
The code checks `getAttribMeta(id).config.up_limit` for attribute caps, but these limits come from external configuration (`configAttribute`), not hardcoded values. We see the mechanism but not the actual cap values.

**To resolve:** Extract configAttribute data.

### 3. Skill Configuration Data
All skill parameters (skillPar, param1-param5) come from `configSkill` and `configSkill_level` tables. The `_limit` values for HP damage clamping (e.g., [0.8, 50]) are from these configs.

**To resolve:** Extract skill config tables.

### 4. Unit Type Configuration
`configUnitType.getDataByKey(type)` provides suspend_time, vertigo_time, and other per-unit-type constants.

**To resolve:** Extract configUnitType data.

---

## B. Partially Analyzed

### 5. Avian / Bird System — **RESOLVED**
Avian system fully documented. See `18_AVIAN_SYSTEM.md` and `data/systems/avian_system.json`.
- ConfigFly + 12 related config tables (ConfigFly_advance, ConfigFly_hatching, etc.)
- `setPlayerFlyPet` (line 187563): loads avian from ConfigFly → ConfigUnit
- Avian stats come directly from ConfigUnit fields (NOT inherited from parent)
- Avian skills use FLY_SKILL type (SkillType = 5)
- Battle position: idleIndex = 8

### 6. Artifact Effects — **RESOLVED**
Artifact system fully documented. See `data/systems/artifact_system.json`.
- ConfigArtifact + gem/resonance config tables
- Artifact figure overrides weapon slot: `if artifact_figure > 0: weapon = artifact_figure`
- Artifact procs use standard skill effect framework (EffectTriggerType)

### 7. Star Hero Effects — **RESOLVED**
Hero/angel system fully documented. See `20_HERO_ANGEL_SYSTEM.md` and `data/systems/hero_system.json`.
- ConfigAngel (line 218577) + ConfigAngel_skill
- Angel skills enhance passive skills via setSkillEffect (line 187518)
- `setPlayerPassiveSkill` applies angel skill enhancements when angelData[0] matches passive skill_id
- Effects: pushes skillEffect2 + angelSkill.skill_effect to skillEffectList

### 8. Stat Assembly (Final ATK/HP/DEF Computation) — **RESOLVED**
Full stat assembly pipeline documented. See `data/formulas/stat_assembly.json` and `data/formulas/attribute_calculation.json`.
- MetaAttrib formula: `value = roundInt(roundInt(base + addValue) × time + addExtraValue)`
- `setPlayerList` (line 187356): 10-step assembly pipeline
- `setPlayerAttrib` (line 187426): initializes module=1 attributes from ConfigAttribute
- `getPetFactAttrValue` (line 187495): pet bonuses with group multiplicative scaling
- Pet stat inheritance: hp, att, partner_dam_extra, skill_dam_extra, skill_crit_rate, skill_crit_dam, boss_dam

---

## C. Multiple Interpretations

### 9. BuffVampire's Scope — **RESOLVED**
BuffVampire is confirmed to be a skill-applied buff, not always-present. It's the primary implementation for life steal mechanics. Total DMG Bonus/RES only affects calculations through BuffVampire (life steal) and spirit damage contexts, NOT normal/combo/counter/skill damage. See `data/formulas/buffs/vampire.json`.

### 10. XOR in BuffVampire — **RESOLVED**
The `1e4 ^ n` is indeed a XOR with the FixMath import variable as an obfuscation technique. The `skillDam[0]` value represents the skill damage percentage parameter. The fallback value of `1e4 ^ n` produces a scrambled default. See `data/formulas/buffs/vampire.json` for full formula.

### 11. CONTROL_RES (ID 1042) — **PARTIALLY RESOLVED**
CONTROL_RES is used in buff application code for controlling resistance to control effects (stun, freeze, bind, etc.). It provides a general resistance that works alongside specific resistances like vertigo_def and suspend_def.

---

## D. Needs Verification via Testing

### 12. Combo Resistance Application Order
For basic ATK: resistance is combined with multiplier: `round(att_dam × round(1 - att_resist))`
For combo: resistance is applied after multiplier: `roundInt(base × combo_dam) × round(1 - combo_def)`

The rounding difference could produce different results. Needs testing with known values.

### 13. FixMath.round Edge Cases
`round()` uses `Math.floor(1e4 * x + 0.5)` for positive values. For values exactly at the 0.5 boundary of the 4th decimal (e.g., `x = 0.00005`), the behavior may differ from standard banker's rounding.

### 14. Effective Crit Rate After Ignore
When `crit_rate = 1.2` (120%) and `ignore_crit_rate = 0.4` (40%):
Code: `max(1.2 - 0.4, 0) = 0.8` (80% effective crit rate)
This means "ignore crit" reduces the RATE, not the probability directly.

### 15. PvE vs PvP Evasion Cap
In PvE, evasion has no cap. In PvP, it's capped at 80% (battle_up_limit = 8000).
The specific `configChapter_type` data determines which is PvE/PvP.

---

## E. Remaining Unknowns (Post-Analysis)

### 16. Actual Config Row Data
All 711 Config module **schemas** have been extracted (field names, types, indices), but actual **row data** (specific item stats, skill parameters, level requirements) is loaded from the server at runtime. The data format is known:
- `loadData()` → JSON arrays
- `loadBufferData()` → `bytes[i] = 255 & ~(32 ^ bytes[i])` → decompress → parse JSON
- XOR fields: `this._data[N] ^ CONFIG_KEY` (CONFIG_KEY = 24455)

**To resolve:** Use browser DevTools on the live game to dump runtime config data.

### 17. Server-Side Battle Calculations
Some battle calculations may have server-side validation or additional processing not visible in client code. The client calculates deterministically, but the server may override or validate results.

### 18. Buff Stacking Rules (Mutex Types)
The addBuff factory (line 431489) has 5 mutex/stacking types, but the specific behavior of each type (replace, stack, coexist, etc.) needs further analysis of the mutex handling code.

### 19. AI System Behavior
The AI map (aiMap at line 332125) defines behavior types: common, player, tfmonster, boss, spirit, flypet, etc. The specific targeting and action selection logic for each AI type hasn't been fully traced.

### 20. Rogue System Mechanics
The rogue system has extensive config tables (ConfigRogue_*) but the gameplay loop, reward structure, and progression mechanics need further code tracing.
