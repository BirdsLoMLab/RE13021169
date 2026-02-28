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

### 5. Avian / Bird System
The task mentions avian attacks and passive affixes. Initial grep for "avian", "bird", "passive_affix" found limited direct results in combat code. The avian system likely uses the general skill/buff framework (BuffSkillValue, skill effects) rather than having dedicated avian-specific combat code.

**What we know:**
- Avian attacks use the standard skill damage pipeline
- HP percentage attacks from avians would use BuffSkillValue with `_calType` 2 or 3
- "Divine Touch" mechanic (25% pal crit → HP damage) likely implemented as a STATE_TRIGER buff

**To resolve:** Need to trace specific avian skill IDs through configSkill.

### 6. Artifact Effects
Artifacts like Beastrow Bow, Thousandfold Pagoda, and Dragonweave Circlet use the skill effect system. Their specific implementations would be configured via skill effect configs, not dedicated code modules.

**What we know:**
- Artifact procs trigger via the skill effect framework (EffectTriggerType)
- Damage from artifacts goes through standard damage pipeline
- Cooldowns are managed by the skill system

**To resolve:** Need artifact skill IDs to trace their specific configurations.

### 7. Star Hero Effects
Hero passive effects likely modify attributes directly through the buff/attribute system rather than having dedicated combat code.

**To resolve:** Need hero config data to map effects to attribute modifications.

### 8. Stat Assembly (Final ATK/HP/DEF Computation)
The code has `setPlayerAttrib` and attribute initialization functions, but the full stat assembly pipeline (base stats × multipliers × equipment × enchants) spans multiple functions across setPlayerList, setPlayerEquip, and attribute initialization code that wasn't fully traced.

**What we know:**
- Attributes are stored in `data.attribs[id].value`
- `getAttrib()` returns `attribs[id].value`
- `getAttribMeta()` returns the full metadata including `baseValue`, `config`, etc.
- Equipment and gems modify attributes during `setPlayerEquip`

**To resolve:** Full trace of attribute assembly pipeline.

---

## C. Multiple Interpretations

### 9. BuffVampire's Scope
BuffVampire applies Total DMG Bonus/RES to life steal calculations. It's unclear whether this buff is always present on units or only activated by specific skills. If always present, it effectively applies Total DMG Bonus/RES to ALL damage through the life steal channel. If only sometimes present, the scope is limited.

**Most likely:** BuffVampire is a buff applied by specific skills (life steal skills), so Total DMG Bonus/RES only affects those specific calculations.

### 10. XOR in BuffVampire
Line 196772: `var g = null != (o = this.runner.useSkill.skillDam[0]) ? o : 1e4 ^ n`
The `^ n` operation uses XOR with `n` (which was the variable name for the FixMath import). This seems like it might be obfuscation or a non-standard pattern. The `skillDam[0]` value likely represents a skill damage percentage.

### 11. CONTROL_RES (ID 1042)
This attribute exists in AttribDefine but its specific usage wasn't found in the primary combat functions. It may be used in buff application/duration calculations or specific skill effects not fully traced.

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
