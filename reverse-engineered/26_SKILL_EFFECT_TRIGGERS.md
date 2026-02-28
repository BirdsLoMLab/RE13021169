# 26 — Skill Effect & Trigger System

## Overview

The skill effect system is the primary execution pipeline for all combat abilities. Skills define targeting, energy, and effect chains. The execution flows: **Skill → SkillEffect (Skilleffcet) → BuffGroup → individual Buff instances**. Passive skills register triggers via `EffectTriggerType` that fire additional effect chains reactively.

---

## Config Tables

| Table | Source Line | Main Key | Fields | Description |
|-------|-----------|----------|--------|-------------|
| ConfigSkill | 261531 | id | 28 | Master skill definitions (4 XOR fields) |
| ConfigSkill_level | 261387 | id + level | 11 | Per-level scaling, damage coefficients |
| ConfigSkill_pos | 261479 | id | 4 | Skill slot unlock conditions |
| ConfigSkilleffcet | 261711 | id | 18 | Effect definitions (typo: "effcet") |
| ConfigBuff | 222479 | id | 16 | Buff definitions |
| ConfigSpecil_buff | 262195 | id | 8 | Special CC/status buffs |

---

## A. SkillType Enum (Line 278634)

| ID | Name | Description |
|----|------|-------------|
| 1 | USE | Active skill (player-triggered, consumes energy) |
| 2 | PASSIVE_ADD | Passive stat addition skill |
| 3 | PASSIVE_EFFECT | Passive effect skill (triggers on conditions) |
| 4 | PARTNER_SKILL | Partner/pal skill |
| 5 | FLY_SKILL | Flying pet skill |

---

## B. EffectTriggerType Enum (Line 278637)

These determine **when** a passive skill effect fires during combat.

| ID | Name | Where It Fires |
|----|------|----------------|
| 0 | NORMAL_ATTACK | SkillHandleNormal.att() — each normal attack hit (line 430047) |
| 1 | HIT | healthTarget() — when target takes hurt damage (line 431409) |
| 2 | COUNTER | SkillHandleCounter.att() — on counter-attack (line 429667) |
| 3 | DOUBLE_ATTACK | SkillHandleNormal.att() — on double/multi-hit (line 429966) |
| 4 | USE_SKILL | SkillHandleEffect.beginRun() — when skill fires (line 429742) |
| 5 | USE_PAR | Partner/pal action trigger |
| 6 | HP_Hurt | Normal/Counter.att() — on target when HP damage dealt (line 430066) |
| 7 | DIZZ | Normal.att() — when stun is inflicted (line 430041) |
| 8 | CRIT_ATTACK | Normal/Counter.att() — on critical hit (line 430052) |
| 9 | NORMAL_DOUBLE_ATTACK | Normal.att() — fires on both normal+double paths (line 430047) |
| 10 | SKILL_CRIT | Referenced in StateTrigerType as Skill_Crit=7 |
| 11 | ALL_ATTACK | Normal, Double, Counter, and Effect handlers (lines 430047, 429966, 429667, 429742) |
| 12 | HP_Heal | Normal.att() — when HP steal heals the caster (line 430021) |
| 13 | Miss | healthTarget() — when a Miss occurs (line 431448) |
| 15 | Spirit_Hit | healthTarget() — on SpiritToPlayer damage (line 431460) |

---

## C. StateTrigerType Enum (Line 278628)

Used by `STATE_TRIGER` (BuffGroupType=110) buffs to listen for specific combat state changes.

| ID | Name | When Fired |
|----|------|------------|
| 0 | All | All state events |
| 1 | Double_Act | healthTarget on Double_Act event (line 431453) |
| 2 | Counter_Act | healthTarget on Counter_Act event (line 431453) |
| 3 | Miss | healthTarget on Miss event (line 431453) |
| 4 | Dizz | When stun is applied |
| 5 | BanAct | When action ban is applied |
| 7 | Skill_Crit | When skill critical hit occurs |
| 8 | Shield | When shield is created |
| 9 | Skill_Effect | During skill effect execution (line 429763) |
| 10 | Normal_Act | At start of normal attack (line 429930) |

---

## D. SpBuffState Enum (Line 278625)

Bitflag-like state indicators on units, checked via `data.getBuffState()` for fast buff queries.

| ID | Name | Purpose |
|----|------|---------|
| 0 | ShareDamage | Unit has active share damage buff |
| 1 | StateTriger | Unit has active state trigger buff |
| 2 | DelayDamage | Unit has active delay damage buff |
| 3 | PetAddBuff | Unit has pet buff conversion active |
| 4 | HpChangeTriger | Unit has HP change trigger buff |
| 5 | AddBuffTrigger | Unit has add-buff trigger buff |
| 6 | TotalDamageTrigger | Unit has total damage trigger buff |

---

## E. Skill Handler Map (Line 332125)

12 handler types registered in `skillMap`:

| Key | Handler | Line | Purpose |
|-----|---------|------|---------|
| `normal` | SkillHandleNormal | 429879 | Standard normal attack — full trigger pipeline |
| `counter` | SkillHandleCounter | 429603 | Counter-attack with COUNTER, ALL_ATTACK, CRIT triggers |
| `effect` | SkillHandleEffect | 429713 | Active skill effect — USE_SKILL + ALL_ATTACK triggers |
| `effect2` | SkillHandleEffect2 | 429775 | Secondary effect — ALL_ATTACK only (no USE_SKILL) |
| `effect_not_count` | SkillHandleEffect3 | 429837 | Effect without passive triggers — USE_SKILL_ADD only |
| `passive` | SkillHandlePassive | 430129 | Passive skill — applies buffGroup, persistent effects |
| `boss_effect` | SkillHandleBossEffect | — | Boss-specific skill effect |
| `thief_normal` | SkillHandleThiefNormal | 430392 | Thief animation only, no damage |
| `thief_normal2` | SkillHandleThiefNormal2 | 430418 | Thief with damage + STATE_TRIGER(Normal_Act) |
| `passive_artiact` | SkillHandlePassive1 | 430185 | Artifact passive with timer + repeating interval |
| `passive_randomskill` | SkillHandleRandomSkill | 430234 | Periodically picks random skill from pool |
| `spirit_normal` | SkillHandleSpiritNormal | 430282 | Spirit attack — SpiritToSpirit/SpiritToPlayer damage |

---

## F. Complete Cascade Flow

```
1. SKILL ACTIVATION
   Active skill (USE=1) OR Passive trigger (PASSIVE_EFFECT=3)

2. HANDLER SELECTION (skillMap[key])
   Active → skillMap.effect     (SkillHandleEffect)
   Normal → skillMap.normal     (SkillHandleNormal)
   Counter → skillMap.counter   (SkillHandleCounter)
   Passive → skillMap.passive   (SkillHandlePassive)

3. SKILL EFFECT EXECUTION (SkillHandleBase)
   a. _skillEffect1(): Process config.skillEffect1 IDs
      - Get targets via config.targetType
      - If config.bullet > 0: fire projectile (deferred hit)
      - Else: addTask() for each effectId immediately

   b. _skillEffect2(): Process config.skillEffect2 / skillEffectList
      - For each position in config.rangeType
      - If skillEffectList (angel enhancement): iterate layers
      - Else: use config.skillEffect2

4. TASK EXECUTION (addTask → execHitAction)
   a. Look up ConfigSkilleffcet by ID
   b. Duration = execute[1] + SKILL_BUFFTIME_ADD modifiers
   c. If duration=0, no delay: immediate execHitAction
   d. Else: queue as timed task

5. HIT ACTION (execHitAction, line 429451)
   a. Damage coefficient: skillDam[skillPar[index]-1] ^ CONFIG_KEY / 10000
   b. Spawn traps if trapId defined
   c. Apply buffGroup2 to caster
   d. checkBuff() on target
   e. execEffectTarget() → chain to skillEffect IDs (→ step 4)

6. CHECK BUFF (checkBuff, line 429312)
   For each buffRate entry:
     - Roll probability: random(0,10000) <= rate × 10000
     - Match buffGroup entries with same groupIndex
     - Get damage coefficient from skillDam
     - Duration + SKILL_BUFFTIME_ADD modifiers
     - addBuff(target, buffId, time, damageCoefficient)

7. ADD BUFF (addBuff, line 431489)
   a. ConfigBuff lookup
   b. IGNORE_BUFFIDS immunity check
   c. Mutex rules (1=replace, 2=unique, 3=stack, 4=per-caster, 5=refresh)
   d. CC immunity (notControlled / invincible)
   e. Create: buffMap[config.action](config)
   f. Dizz/ban_act: CONTROL_RES duration reduction
   g. Shield: +shield_time_extra
   h. Type 0 (instant): start() → destroy()
   i. Persistent: add to BuffCtr, fire AddBuffTrigger

8. PASSIVE TRIGGER CASCADE
   Throughout steps 2-7, multiple triggers can fire:
   - EffectTriggerType on skillctr.skillEffects
   - StateTrigerType on STATE_TRIGER buffs
   - VAMPIRE/FRAGILE/EXTRA_DAMAGE/GIANT_SLAYER modifiers
   - HP_Hurt on target's passive effects
   - HP_Heal on caster's passive effects after steal
   - AddBuffTrigger when new buffs applied
   Each triggered effect recurses through steps 4-7
   (infinite loop guard at line 429488)
```

---

## G. Passive Skill Effect Registration

Passive effects are registered via `BuffSkillEffect` (line 195411, buffMap key `skill_effect`):

```javascript
// BuffSkillEffect.onBegin()
owner.skillctr.addSkillEffect(
    config.param1,    // ConfigSkilleffcet ID to fire
    runner,           // SkillRunner that owns this
    config.param2,    // EffectTriggerType value
    config.param3,    // limit (every N triggers, 0=every time)
    config.param4,    // useType (0=addTask/effect, 1=addSkill/full skill)
    config.param5     // skill ID filter array
);
```

Each registered effect stores:
- `triggerType`: Which EffectTriggerType triggers it
- `limit`: Fires every N occurrences (0 = every time)
- `useType`: 0 = add as effect task, 1 = execute as full skill
- `param5`: Optional skill ID filter (only trigger for specific skills)

---

## H. Angel Skill Enhancement (skillEffectList)

Angel skills can enhance passive skills by adding layers of effects:

```javascript
// setSkillEffect (line 187518)
if (angelData[0] matches passive.skill_id) {
    passive.skillEffectList.push(config.skillEffect2);
    passive.skillDamList.push(config.skillDam);
    setSkillEffect(passive, angelData[1]);  // 1st angel enhancement
    setSkillEffect(passive, angelData[2]);  // 2nd angel enhancement
}
```

During `_skillEffect2()` execution (line 429420):
- If `skillEffectList` exists: iterate each layer, executing effects per range position
- The `index` parameter selects the correct damage coefficient from `skillDamList[index]`

---

## I. Effect Chaining Mechanisms

### 1. Deterministic Chains (execEffectTarget, line 429368)
```javascript
// ConfigSkilleffcet.skillEffect → always chains to listed effects
for each effectId in config.skillEffect:
    if (effectId == config.id) throw "Skill effect infinite loop!";
    addTask(effectId, pos, runner, target);
```

### 2. Probabilistic Chains (onExecuteEffectAction, line 429476)
```javascript
// ConfigSkilleffcet.skillEffect_rate → probability-based chaining
for each [effectId, probability/10000] in skillEffect_rate:
    if (random(0,10000) <= probability):
        queue effectId for each target
```

### 3. AddBuffTrigger Cascades (line 431535)
When any buff is added to a unit, if the caster has `AddBuffTrigger` (BuffGroupType 150):
```javascript
if (owner.data.getBuffState(SpBuffState.AddBuffTrigger) > 0):
    for each AddBuffTrigger buff:
        buff.onAddBuffTrigger(target, buffId, duration)
```

---

## J. ConfigSkill XOR Fields

4 fields in ConfigSkill are XOR-encoded with CONFIG_KEY (24455):

| Field | Index | Purpose |
|-------|-------|---------|
| autoDis | 5 | Auto-targeting distance |
| initialPower | 18 | Starting energy |
| maxPower | 19 | Maximum energy capacity |
| powerRecovery | 20 | Energy per normal attack |

Decode: `realValue = rawValue ^ 24455`

---

## K. Damage Coefficient Lookup

The damage coefficient for a buff comes from this chain:

1. `ConfigSkill.skillPar` → array of indices
2. `ConfigSkill_level.skillCoefficient` → array of coefficient values (/10000 fixed-point)
3. `skillDam[skillPar[groupIndex] - 1]` → raw coefficient (XOR-encoded)
4. Decode: `(skillDam[i] ^ CONFIG_KEY) / 10000` → final multiplier

This coefficient is passed as the `skillPar` argument to `addBuff()`, where individual buff classes use it for their damage/healing calculations.
