# 97 — Unknowns & Unresolved Items

Items that couldn't be fully resolved from static code analysis alone.

---

## A. Requires Runtime Data

### 1. PvP Factor Table (configLevel) — **RESOLVED**
Complete table extracted from `data/tables/Level.json` (220 levels). Values range from 10,000 (1.0x at L1) to 7,540,000 (754.0x at L220). Key breakpoints: L50=11.0x, L100=56.9x, L150=280.6x, L200=609.0x. See DOCX Section 18 for full table.

### 2. Attribute Caps (up_limit) — **RESOLVED**
Extracted from `data/tables/Attribute.json`. 11 attributes have caps: all resistances capped at 80% (8000), HP steal at 100% (10000), control_res at 100%, boss_def at 80%, season_cannon_att_def at 60%. All damage multipliers, crit stats, and Total DMG Bonus/RES are uncapped. See DOCX Section 19.

### 3. Skill Configuration Data — **RESOLVED**
Full skill config decoded and available in `data/tables/Skill.json` and `data/tables/Skill_level.json` (18,838 records). Includes skillPar, param1-param5, _limit values, all skill types and effects.

### 4. Unit Type Configuration — **RESOLVED**
Decoded and available in `data/tables/UnitType.json`. Includes suspend_time, vertigo_time, and all per-unit-type constants.

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
BuffVampire is confirmed to be a skill-applied buff, not always-present. It's the primary implementation for life steal mechanics. **CORRECTED:** Total DMG Bonus/RES is a universal final multiplier applied via `SkillRunner.healthTarget()` to ALL 13 damage types in `NeedAddDamHurtList` (normal, crit, combo, counter, bleed, real damage, spirit-to-player, shared, return). BuffVampire additionally uses the same formula independently for life steal heal amounts. See `07_TOTAL_DMG_BONUS_RES.md` for full analysis.

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

### 16. Actual Config Row Data — **RESOLVED**
All 909 config tables fully decoded from the 20260228 web capture via `decode_config_data.py`. Data available in `data/tables/` (909 JSON files). Key tables: Unit.json (all unit stats), Buff.json (4,155 buff entries), Skill.json, Level.json (220 levels with PvP factors), Attribute.json (192 attributes with caps), Equipment.json, and 900+ more.

### 17. Server-Side Battle Calculations — **PARTIALLY RESOLVED**
Evidence from client code and protocol schemas (`proto_schema.json`):
- **Deterministic client**: All calculations use `FixMath.round()`/`roundInt()` with no RNG or random seed — identical inputs always produce identical outputs
- **Action replay protocol**: Client sends `operators` array (unit ID, frame number, skill ID per action) to server for complex battles (dungeon, GvG, escort_boss). Simple battles (farm, escort) only send `win_role_id`
- **Server validation**: Every `_s2c` battle result message includes `code: int32` — 0 = success, non-zero = rejection. The server can re-simulate from the operator sequence since calculations are deterministic
- **Anti-tamper**: MetaAttrib uses `_checkValue = 32 XOR baseValue` to detect memory manipulation of stat values
- **Mode-dependent**: Different battle modes have different levels of server involvement — PvP modes (GvG, cross_war) send more detailed reports than PvE auto-battles

**Still unknown:** Exact server validation tolerances, error code meanings, whether server always re-simulates or spot-checks, and how proc rates (crit/combo/counter triggers) are synchronized between client and server.

### 18. Buff Stacking Rules (Mutex Types) — **RESOLVED**
5 mutex types fully traced from `SkillRunner.addBuff`:

| Mutex | Name | Behavior |
|-------|------|----------|
| 1 | Replace | Stop all existing instances of this buff ID on target, then add the new buff |
| 2 | Unique | If any buff with this ID already exists on target, reject the new buff entirely |
| 3 | Stack w/ Max | Multiple instances coexist up to `add_max` limit; all existing durations refreshed; oldest active removed when limit exceeded |
| 4 | Unique per Caster | One instance per caster; if same caster re-applies, new buff is rejected |
| 5 | Refresh per Caster | Like type 4, but resets the existing buff's duration instead of rejecting |

Additional mechanics in addBuff:
- **Type 0 (Instant)**: Buffs with `config.type == 0` execute `start()` + `destroy()` immediately without being tracked in BuffCtr
- **Control immunity**: Before mutex, checks `notControlled`/`invincible` buffs → skips control-type buffs (dizz, ban_skill, throw_hit, bound, ban_act)
- **CONTROL_RES duration reduction**: For stun (dizz param1==0) and ban_act: `duration = round(duration - round(duration × CONTROL_RES))`
- **Shield time extension**: For shield buffs: `duration = round(duration + shield_time_extra)`
- **IGNORE_BUFFIDS**: BuffGroupType that blocks specific buff IDs listed in its param5 array

### 19. AI System Behavior
The AI map (aiMap at line 332125) defines behavior types: common, player, tfmonster, boss, spirit, flypet, etc. The specific targeting and action selection logic for each AI type hasn't been fully traced.

### 20. Rogue System Mechanics
The rogue system has extensive config tables (ConfigRogue_*) but the gameplay loop, reward structure, and progression mechanics need further code tracing.
