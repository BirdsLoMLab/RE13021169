# 39 — Clone Unit Initialization & HP-Threshold Triggers (Rampage, Phoenix)

> **Sources:** game_script_pretty.js lines 193116-193152 (BuffCallUnit), 431572-431604 (addCallUnit/addCopyUnit), 450273-450306 (_createUnit/_addUnit1), 430208-430222 (SkillHandlePassive1.beginRun), 194229-194305 (BuffHpChangeTrigger); data/tables/Buff.json (buffs 20030, 120006-120011, 50482, 50650), data/tables/Skill.json (skills 1052, 17022, 5048, 5060)
> **Key Discovery:** Clone Strike clones do NOT receive passive skills (Rampage, mount skills, artifact passives). Additionally, clones always start at full HP relative to their own max, so even if HP-threshold triggers were present, they would not fire on spawn.

---

## 1. Rampage — The Final Talent

**Skill ID:** 17022 (also duplicated as 4155240)
**Type:** Passive (type 3, quality 7 — final talent tier)
**Action:** `passive` → handled by `SkillHandlePassive1`

### Buff Chain

Rampage applies three `hpchange_trigger` buffs at battle start (duration = -1, permanent):

| Buff ID | Group | Trigger | Threshold | Fires Buff | Effect | CD |
|---------|-------|---------|-----------|------------|--------|-----|
| 120006 | 140 | HP < X% | 20% | 120007 | ATK ×2 (multiplicative) | 900 ticks |
| 120008 | 140 | HP < X% | 20% | 120009 | ATK Speed ×2 (multiplicative) | 900 ticks |
| 120010 | 140 | HP < X% | 20% | 120011 | Crit DMG ×2 (multiplicative) | 900 ticks |

**What Rampage does:** When the unit's HP drops below 20%, it triggers three attribute doublings — ATK, ATK Speed, and Crit DMG. Each has a 900-tick cooldown before it can re-trigger.

### How hpchange_trigger Works

```javascript
// Line 194259-194296 (BuffHpChangeTrigger)
onBegin(): owner.AddBuffState(HpChangeTriger, 1)

onDamage(currentHp):
    ratio = round(currentHp / owner.getAttrib(hp))    // Current HP %
    threshold = round(triggervalue / 10000)             // e.g. 2000 → 0.2 (20%)

    switch(operator):
        case 0: triggered = ratio > threshold           // HP above X%
        case 1: triggered = ratio < threshold           // HP below X%  ← Rampage uses this
        case 2: triggered = ratio == threshold
        case 3: triggered = ratio >= threshold
        case 4: triggered = ratio <= threshold

    if triggered && cooldown <= 0:
        addBuff(owner, addBuffId, duration, skillPar)

// CRITICAL: 3-frame delayed initial check (line 194296):
onUpdate():
    if !delayCheck && delayCount >= 3:
        delayCheck = true
        onDamage(owner.data.currenHp)     // Runs threshold check with CURRENT HP
```

**The 3-frame delay initial check** is important: after the buff is applied, it waits 3 frames then runs `onDamage(currentHP)`. If the unit's HP is already below the threshold at that point, it triggers immediately.

### Parameter Mapping

```
param1 = operator (0=>gt, 1=lt, 2=eq, 3=gte, 4=lte; +10 = ignore CURRENT_HP illusion)
param2 = triggervalue (HP% × 10000, e.g. 2000 = 20%)
param3 = buff ID to apply when triggered
param4 = buff duration (seconds)
param5[0] = cooldown between triggers (ticks)
```

---

## 2. Clone Strike — Unit Creation Mechanics

**Skill ID:** 1052
**Type:** Active effect skill
**Effect Chain:** Skill 1052 → SkillEffect 10521 → Buff 20030 (call_unit)

### Buff 20030 Configuration

```json
{
    "id": 20030,
    "action": "call_unit",
    "param1": 0,              // 0 = clone the CASTER (not a config unit)
    "param5": [
        [1001, 1, 1],         // ATK: multiply by 1 × skillPar (scales with level)
        [1002, 0.3, 0],       // HP: set base to caster's × 0.3 (30% of caster HP)
        [1060, 0, 0]          // def_coe: set to 0
    ]
}
```

### Clone Creation Code Path

```javascript
// Line 431572-431604 (SkillRunner.addCallUnit)
addCallUnit(unitId, position, time, attribs, skillPar):
    if unitId == 0:                            // CLONE THE CASTER
        data = new UnitData()
        data.config = this.cast.config          // Copy config reference
        data.skin = this.cast.data.skin
        data.modelConfig = this.cast.data.modelConfig

        // Copy ALL base attributes from caster
        for attr in configAttribute.getDataByList("module", 1):
            data.attribs[attr.id] = new MetaAttrib(attr, caster.attribs[attr.id])

        data.skillList = []                     // ← EMPTY SKILL LIST
        unit = unitMgr.addUnitImageCall(data)   // → _createUnit (no passive skills)

    else:                                       // SUMMON FROM CONFIG
        unit = unitMgr.addUnitCall(unitId)      // → _addUnit1 (applies passive skills)

    // Apply attribute modifications
    for mod in attribs:
        if unitId == 0 && mod[0] != HP:
            unit.attribs[mod[0]].multiple(mod[1] × skillPar)  // Multiply attribute
        else:
            unit.attribs[mod[0]].baseValue = caster.baseValue × mod[1]  // Set HP base

    // Finalize
    addCopyUnit(unit, position, time)

// Line 431592-431604 (addCopyUnit)
addCopyUnit(unit):
    unit.lifeTime = duration                    // Configurable lifetime
    unit.parent = this.cast
    unit.isCallType = true
    unit.data.currenHp = unit.data.attribs[hp].value  // ← START AT FULL HP
```

### Key Properties of Clones (param1=0)

| Property | Value | Why |
|----------|-------|-----|
| Attributes | Copied from caster, then modified by param5 | MetaAttrib copy constructor |
| HP | 30% of caster's max HP (Clone Strike L1) | param5: [1002, 0.3, 0] sets baseValue |
| Current HP | 100% of clone's own max HP | `currenHp = attribs[hp].value` |
| Active Skills | **NONE** | `skillList = []` (line 431584) |
| Passive Skills | **NONE** | `addUnitImageCall` → `_createUnit` (no skill loading) |
| Buffs | **NONE inherited** | Only gets buffs applied directly to it during battle |
| Lifetime | Scales with skill buff duration | `lifeTime = skillFactAttrValue(active_skillbuff_time)` |
| Attack | Inherits caster's `att_skill` from config | `_createUnit` sets up attack from `unitType.att_skill` |

---

## 3. Do Clones Get Rampage? NO.

### The Passive Skill Application Pipeline

```javascript
// Line 430208-430222 (SkillHandlePassive1.beginRun)
// This runs for EACH passive skill in the unit's skill list
beginRun():
    for each buffGroup in skill.config.buffGroup:
        skillPar = decode(skillDam[i])
        runner.addBuff(cast, buffGroup[i], duration=-1, skillPar)

    if skill.immediate_time > 0:
        timer(immediate_time, () => { skillEffect1(), skillEffect2() })
    if skill.releaseTime > 0:
        timer(releaseInterval, () => { skillEffect1(), skillEffect2() })
```

This only runs for skills in the unit's `skillList` and `passiveSkillList`. Clones have:
- `skillList = []` (explicitly emptied at line 431584)
- `passiveSkillList` — never populated (no call to `addSkill` for passives)

### The Two Creation Paths

| Path | Function | Passive Skills? | Used By |
|------|----------|-----------------|---------|
| Clone caster (param1=0) | `addUnitImageCall` → `_createUnit` | **NO** | Clone Strike buff 20030 |
| Summon unit (param1>0) | `addUnitCall` → `_addUnit1` | **YES** (from config) | Heroic Descent buffs 210018/210019 |

**`_addUnit1`** (line 450287-450306) loads skills from the unit config:
```javascript
if (config.passiveSkills != null)
    for each passiveSkill in config.passiveSkills:
        addSkill(data, passiveSkill, 1)     // Adds passive to unit's lists
```

**`_createUnit`** (line 450273-450286) does NOT load passive skills — it only sets up the basic attack/counter and initializes the unit.

---

## 4. Do Clones Get Mount Skills? NO.

Mount skills (like Phoenix Nirvana skill 5048 or Ethereal Phoenix skill 5060) are applied to the PLAYER unit during `setPlayerMount`:

```javascript
// The mount skill is added to the player's passive skill list
// via setPlayerMount → addSkill during battle setup
```

Since clones skip the entire player setup pipeline (no `setPlayerMount`, no `setPlayerPassiveSkill`, no `setPlayerEquip`), mount skills are **never applied** to clones.

### What This Means for Phoenix Mount

**Ethereal Phoenix (Mount 406, Skill 5060):**
- Buff 50650 (skill_counter): Triggers shield + CC cleanse + ATK buff per 18% HP lost
- This passive is on the CASTER, not the clone
- Clone takes damage → caster's Phoenix effect does NOT trigger
- Clone has no Phoenix passive → no self-shield or ATK stacking

**Phoenix Nirvana (Skill 5048):**
- Applies buff 50482 (hpchange_trigger at 50% HP) and buffs 50465-50467
- These are passive buffs → only applied via SkillHandlePassive1 → only to units with the skill
- Clone has empty skillList → no Phoenix Nirvana effects

---

## 5. Would Rampage Trigger Even If Applied? NO (on spawn).

Even in a hypothetical scenario where Rampage's buffs were somehow applied to a clone:

1. Clone starts at `currenHp = attribs[hp].value` = **100% of its own max HP**
2. The 3-frame delayed initial check computes `ratio = currenHp / maxHP = 1.0` (100%)
3. Rampage's trigger condition is `ratio < 0.20` (less than 20%)
4. `1.0 < 0.2` = **FALSE** → does not trigger

The clone would need to take damage and have its HP drop below 20% of its own max before Rampage could trigger.

---

## 6. Clone Strike Scaling by Level

From Skill_level.json for skill 1052:

| Level | desc_parm | Clone HP | Clone Duration | Clone DMG/hit |
|-------|-----------|----------|---------------|---------------|
| L1 | [30, 10, 200] | 30% of caster | 10s | 200% |
| L5 | [30, 10, 220] | 30% of caster | 10s | 220% |
| L10 | [30, 10, 245] | 30% of caster | 10s | 245% |
| L15 | [30, 10, 270] | 30% of caster | 10s | 270% |

The `ownEffect` field scales attributes 2001/2003/2005 (pet/spirit bonus stats) as the skill levels up, boosting the caster — not the clone.

---

## 7. Heroic Descent vs Clone Strike — A Different Story

**Heroic Descent** (skills 21018-21033, "Zombie Bride" summons) uses `param1: 1703602` (a config unit ID), not `param1: 0`. This goes through `addUnitCall` → `_addUnit1` → which **DOES** load passive skills from the unit config.

This means Heroic Descent summons CAN have passive skills if config unit 1703602 has them defined. However, these would be the summoned unit's OWN passives from its config, not the caster's passives.

---

## 8. Summary

| Question | Answer |
|----------|--------|
| Does Clone Strike clone get Rampage? | **No.** Clone has empty skillList, passive skills never execute. |
| Does Clone Strike clone get mount skills? | **No.** Mount passives are part of player setup, skipped for clones. |
| Does Clone Strike clone get artifact passives? | **No.** Same reason — passive_artiact skills are in the skill list. |
| Would Rampage trigger on clone spawn anyway? | **No.** Clone starts at 100% HP, Rampage needs < 20%. |
| Does the clone trigger the CASTER's Rampage? | **No.** Rampage checks the buff OWNER's HP, not summoned units. |
| Does clone damage count toward caster's HP-threshold? | **No.** Clone is a separate unit with its own HP pool. |
| Do Heroic Descent summons get passives? | **Possibly.** They load from config unit 1703602, which may define its own passives. |

### Implications for PvP

Clone Strike's value is purely from:
1. **Copied base stats** (ATK, DEF, etc.) modified by param5
2. **Basic attack damage** (from the caster's att_skill config)
3. **Tanking/aggro** — clones have maximum taunt priority (`tauntValue = 999999999999999 + caster.tauntValue`)
4. **Duration scaling** — affected by active_skillbuff_time attribute

Clones do NOT benefit from:
- Rampage (or any final talent)
- Mount skills (Phoenix, Motorcycle, any mount)
- Artifact passive skills (Giant Slayer, etc.)
- Equipment passive effects
- Any buff the caster has accumulated during battle
