# 22 -- Skill & Effect System

## Overview

The skill system is the core combat engine. Skills define targeting, energy management, multi-stage effect chains, and buff application. The execution pipeline flows:

```
Skill (ConfigSkill)
  -> SkillEffect (ConfigSkilleffcet)
    -> BuffGroup (ConfigBuff, BuffGroupType)
      -> Individual Buff Instances
        -> SpecialBuff (ConfigSpecil_buff) for CC effects
```

## Code Locations

| Module | Lines | Purpose |
|--------|-------|---------|
| ConfigSkill.ts | 261531 | Master skill definitions (28 fields) |
| ConfigSkill_level.ts | 261387 | Per-level scaling and coefficients |
| ConfigSkill_pos.ts | 261479 | Skill slot positions and unlock conditions |
| ConfigSkilleffcet.ts | 261711 | Skill effect definitions (18 fields, typo preserved) |
| ConfigBuff.ts | 222479 | Buff definitions (16 fields) |
| ConfigSpecil_buff.ts | 262195 | Special CC buff definitions (typo preserved) |
| SkillHandleNormal.ts | 429879 | Normal attack execution flow |
| SkillHandleBase.ts | 429258 | Base skill handler with buff/effect logic |
| SkillHandleEffect.ts | 429713 | Skill effect execution handler |
| SkillHandleEffect2.ts | 429775 | Secondary skill effect handler |
| SkillHandleEffect3.ts | (varies) | Tertiary skill effect handler |
| SkillHandleCounter.ts | 429603 | Counter-attack handler |

## ConfigSkill (28 fields)

Key fields with combat relevance:

```
id              -- Unique skill ID
name            -- Localized name
type            -- Skill type classification
chapter_type    -- [optional] Mode restrictions
if_chapter_type -- Whether mode filter is active
autoDis         -- XOR-encoded auto-target distance
quality         -- Rarity tier
buffGroup       -- Buff groups: [[groupIdx, buffId, duration, bgType], ...]
addSkill        -- Additional skill IDs triggered
releaseTime     -- Cast time (frames)
releaseInterval -- Cooldown between casts
targetType      -- [filterType, count, selectFilter]
targetRange     -- Range for target selection
skillEffect1    -- Primary effect IDs -> ConfigSkilleffcet
rangeType       -- AoE specification
skillEffect2    -- Secondary effect IDs
skillPar        -- Parameter indices for coefficient lookup
initialPower    -- XOR: Starting energy
maxPower        -- XOR: Max energy capacity
powerRecovery   -- XOR: Energy gained per normal attack
immediate_time  -- Instant trigger delay (0 = normal timing)
```

### XOR-Encoded Fields

`autoDis`, `initialPower`, `maxPower`, and `powerRecovery` are XOR-encoded:
```javascript
// Decoding pattern observed in SkillHandleBase:
var value = (rawValue ^ xorKey) / 10000;
```

## ConfigSkill_level (11 fields, keyed by [id, level])

Per-level scaling:

```
id                -- Skill ID
level             -- Level number
expend            -- Upgrade cost
ownEffect         -- Passive effects on owner
attrType          -- Attribute types for ownEffect
skillCoefficient  -- Damage coefficients per hit (array, /10000 fixed-point)
desc              -- Active description template
desc_parm         -- Description parameters
power             -- Combat power value
```

### Coefficient Lookup

The `skillCoefficient` array is indexed by `ConfigSkill.skillPar` to determine damage for each buff group:

```javascript
// Line ~429324: SkillHandleBase.checkBuff
var skillDam = runner.useSkill.skillDam;
// skillPar maps buff groups to coefficient indices
var coeffIndex = (config.skillPar.length > h ? config.skillPar[h] : 1) - 1;
var coefficient = skillDam[coeffIndex];  // from skillCoefficient
coefficient = FixMath.round((coefficient ^ xorKey) / 10000);
```

## ConfigSkilleffcet (18 fields)

Skill effect definitions (note: table name has typo "effcet"):

```
id              -- Unique effect ID
type            -- Execution type
trapId          -- Trap/summon IDs spawned
targetType      -- [filterType, selfOrEnemy]; [x,1] = targets self
targetRange     -- Effect range
bullet          -- Projectile visual
execute         -- [duration, totalTime] timing
buffGroup       -- Buffs applied on hit: [[groupIdx, buffId, duration, bgType], ...]
randomType      -- 0=apply all buffs, 1=random pick one
buffRate        -- Probability per group: [[groupIdx, chance/10000], ...]
buffGroup2      -- Secondary buffs (applied to caster)
skillEffect     -- Chained effect IDs (multi-stage)
skillEffect_rate -- Probability for chained effects
effctId         -- Visual effect asset
skillPar        -- Coefficient index overrides
effectDelay     -- Delay in milliseconds
```

### Effect Chaining

Effects can chain into nested effects:

```javascript
// Line ~429369: SkillHandleBase.execEffectTarget
var chainEffects = config.skillEffect;
for (var id of chainEffects) {
    if (id == config.id) throw Error("Skill effect infinite loop!");
    this.addTask(id, position, runner, target);
}
```

## ConfigBuff (16 fields)

Individual buff definitions:

```
id          -- Buff ID
name        -- Display name
type        -- Buff polarity (positive/negative)
group       -- BuffGroupType enum value (determines handler)
icon        -- Status icon
effect      -- Visual effect on unit
mutex       -- Mutex group (same group -> overwrite)
add_max     -- Max stack count
bind        -- Bound to caster (0/1)
param1-4    -- Handler-specific parameters
param5      -- Extended parameters array
```

## Enums

### EffectTriggerType (line 278638)

Controls when passive skill effects trigger:

| Value | Name | Trigger Condition |
|-------|------|-------------------|
| 0 | NORMAL_ATTACK | On each normal attack |
| 1 | HIT | When unit is hit |
| 2 | COUNTER | On counter-attack |
| 3 | DOUBLE_ATTACK | On double/multi-hit |
| 4 | USE_SKILL | When any skill is used |
| 5 | USE_PAR | On partner/pal action |
| 6 | HP_Hurt | When HP damage is taken |
| 7 | DIZZ | When stun is inflicted |
| 8 | CRIT_ATTACK | On critical hit |
| 9 | NORMAL_DOUBLE_ATTACK | On normal + double combined |
| 10 | SKILL_CRIT | On skill critical hit |
| 11 | ALL_ATTACK | On any attack type |
| 12 | HP_Heal | When HP is healed |
| 13 | Miss | On a miss |
| 15 | Spirit_Hit | On guardian spirit hit |

### BuffGroupType (line 278632)

Determines how the buff is processed:

| ID | Name | Description |
|----|------|-------------|
| 1 | HURT | Direct damage |
| 3 | CTR | Control/CC effect |
| 4 | ADD | Attribute modification |
| 20 | SHIELD | Shield/barrier |
| 30 | NORMAL_ACT_NUM_TRIGGER | Triggers after N normal attacks |
| 40 | BULLET_NUM | Modifies skill projectile count |
| 60 | SKILL_DAMAGE_ADD | Flat skill damage addition |
| 70 | SHARE_DAMAGE | Damage sharing between units |
| 80 | ATTRIB_CONDITION | Conditional attribute modifier |
| 110 | STATE_TRIGER | State-based trigger |
| 120 | DELAY_DEMAGE | Delayed damage |
| 160 | UnitCallDamageAdd | Summoned unit bonus damage |
| 200 | FRAGILE_EFFECT | Vulnerability debuff |
| 230 | IMMUNE_DEATH | Survive lethal damage (1 HP) |
| 240 | BLOCK | Damage block/reduction |
| 290 | SKILL_REAL_DAMAGE | True damage (ignores DEF) |
| 340 | SKILL_RETURN | Reflect skill damage |
| 380 | VAMPIRE | Life steal |
| 390 | GIANT_SLAYER | Bonus damage based on target max HP |
| 410 | EXTRA_DAMAGE | Extra damage modifier |
| 440 | REDUCE_HEAL | Healing reduction |

(Full list: 37 types total; see `data/enums/BuffGroupType.json`)

## Execution Flow: Normal Attack

From `SkillHandleNormal.ts` (line 429879):

```javascript
// 1. beginRun: Start attack animation
R.beginRun = function() {
    var a = "skill1";
    if (configWeapon) a = configWeapon.ani;
    runner.changeModeAction(true, a, getActSpeed(a));
    runner.nextTriggerAction(function(a) {
        this.triggerAction(runner, a, -1);
    });
};

// 2. att: Process single target hit
R.att = function(target, bulletIndex) {
    // Check counter-attack eligibility
    if (bulletIndex == -1) this.checkCounter(target, runner.cast);

    // Trigger STATE_TRIGER buffs with Normal_Act
    if (cast.data.getBuffState(SpBuffState.StateTriger) > 0) {
        for (buff of cast.buffCtr.getBuffByType(BuffGroupType.STATE_TRIGER)) {
            buff.onStateTrigger(StateTrigerType.Normal_Act);
        }
    }

    // 3. Check hit type
    var hitType = checkHit(cast, target);  // Miss=0, Normal=1, Crit=2

    if (hitType == AttackType.Miss) {
        runner.healthTarget(target, 0, HealthType.Miss, true);
        return;
    }

    // 4. Calculate damage (normal vs double attack)
    if (bulletIndex > 0) {
        damage = normalDoubleHurt(cast, target, hitType);
        healthType = hitType == Normal ? Hurt_Double : Hurt_Double_Crit;
    } else {
        cast.normalActCount++;
        damage = normalHurt(cast, target, hitType);
        healthType = hitType == Normal ? Hurt : Hurt_Crit;
    }

    // 5. Apply buff modifiers
    // NORMAL_ACT_NUM_TRIGGER: bonus damage after N attacks
    for (buff of cast.buffCtr.getBuffByType(NORMAL_ACT_NUM_TRIGGER)) {
        damage += buff.calValue(cast.normalActCount);
    }

    // UnitCallDamageAdd: summoned unit bonus
    if (cast.isCallType && cast.parent) {
        for (buff of cast.parent.buffCtr.getBuffByType(UnitCallDamageAdd)) {
            damage += buff.calDamage(damage, target);
        }
    }

    // Boss damage multiplier
    if (target.config.type == UnityType.Boss && boss_dam > 0) {
        damage = roundInt(damage * round(1 + boss_dam));
    }

    // FRAGILE_EFFECT: vulnerability
    for (buff of target.buffCtr.getBuffByType(FRAGILE_EFFECT)) {
        damage += buff.calDamage(damage, cast);
    }

    // EXTRA_DAMAGE: caster's extra damage
    for (buff of cast.buffCtr.getBuffByType(EXTRA_DAMAGE)) {
        damage = buff.calDamage(damage, null, skillId);
    }

    // GIANT_SLAYER: max HP based damage
    for (buff of cast.buffCtr.getBuffByType(GIANT_SLAYER)) {
        damage = buff.onCalHpDamage(target, damage);
    }

    // 6. Apply final damage
    runner.healthTarget(target, damage, healthType, true);

    // 7. Life steal
    var hpSteal = normailHpsteal(cast, target, damage);
    if (hpSteal > 0) runner.healthTarget(cast, hpSteal, Act_Hpsteal);

    // 8. Stun check
    if (checkDizz(cast, target)) {
        var stunTime = vertigo_times * round(1 - target.vertigo_res);
        if (stunTime > 0) runner.addBuff(target, vertigoTime, stunTime);
    }

    // 9. Trigger passive effects
    for (effect of cast.skillctr.skillEffects) {
        if (effect.triggerType in [NORMAL_ATTACK, ALL_ATTACK]) {
            effect.num++;
            if (effect.limit == 0 || effect.num % effect.limit == 0)
                addTask(effect.id, target.position, effect.runner, target);
        }
    }

    // 10. Remove one-shot buffs
    cast.buffCtr.removeBuff(DESTROY_WHEN_NORMAL_AFTER);
};
```

## Execution Flow: Skill Effect

From `SkillHandleEffect.ts` (line 429732):

```javascript
beginRun = function() {
    cast.hurtNumCount++;
    cast.buffCtr.removeBuff(DESTROY_WHEN_SKILL_AFTER);

    // Trigger USE_SKILL and ALL_ATTACK passive effects
    if (useSkill.triggerEffect) {
        for (effect of cast.skillctr.skillEffects) {
            if (effect.triggerType == USE_SKILL || effect.triggerType == ALL_ATTACK) {
                effect.num++;
                // Check skill ID filter (param5 restricts to specific skills)
                if (effect.param5 && effect.param5.length > 0) {
                    if (!effect.param5.includes(currentSkillId)) continue;
                }
                addTask(effect.id, cast.position, effect.runner, cast);
            }
        }
    }

    // Process USE_SKILL_ADD buffs (damage accumulation)
    for (buff of cast.buffCtr.getBuffByType(USE_SKILL_ADD)) {
        if (cast.skillctr.getRecordDamage(skillId) <= buff._limit
            && buff.skillList.includes(skillId)) {
            var newDmg = Math.min(getRecordDamage(skillId) + buff._value, buff._limit);
            cast.skillctr.setRecordDamage(skillId, newDmg);
        }
    }

    // Trigger STATE_TRIGER with Skill_Effect
    if (cast.data.getBuffState(SpBuffState.StateTriger) > 0) {
        for (buff of cast.buffCtr.getBuffByType(STATE_TRIGER)) {
            buff.onStateTrigger(StateTrigerType.Skill_Effect);
        }
    }
};
```

## Buff Application Pipeline

From `SkillHandleBase.ts` (line 429312):

```javascript
checkBuff = function(taskItem, target) {
    var config = taskItem.config;  // ConfigSkilleffcet entry
    if (config.buffGroup.length == 0 || config.buffRate.length == 0) return;

    var skillDam = taskItem.runner.useSkill.skillDam;
    if (taskItem.index > 0) skillDam = taskItem.runner.useSkill.skillDamList[taskItem.index];

    for (var rate of config.buffRate) {
        var roll = battleMain.random.randomInt(0, 10000);
        if (roll > roundInt(10000 * rate[1])) continue;  // probability check

        for (var h = 0; h < config.buffGroup.length; h++) {
            var group = config.buffGroup[h];
            if (group[0] != rate[0]) continue;  // match group index

            // Get damage coefficient from skillCoefficient
            var parIndex = (config.skillPar.length > h ? config.skillPar[h] : 1) - 1;
            var coefficient = skillDam[parIndex] ?? (10000 ^ xorKey);
            coefficient = round((coefficient ^ xorKey) / 10000);

            // Get buff duration with modifiers
            var duration = cast.data.getSkillFactAttrValue(group[3], skillId, active_skillbuff_time);
            for (buff of cast.buffCtr.getBuffByType(SKILL_BUFFTIME_ADD)) {
                duration = buff.getFixTime(duration, skillId);
            }

            runner.addBuff(target, group[1], duration, coefficient);
        }
    }
};
```

## Damage Coefficient Flow

```
ConfigSkill.skillPar        -- Indices mapping buff groups to coefficient slots
ConfigSkill_level.skillCoefficient -- Coefficient values (XOR + /10000)
ConfigSkilleffcet.skillPar  -- Override indices for effect-level coefficients
ConfigSkilleffcet.buffRate  -- Probability per group
ConfigSkilleffcet.buffGroup -- [groupIndex, buffId, duration, buffGroupType]
```

Example: If `skillPar = [1, 2]` and `skillCoefficient = [15000, 8000]`:
- Buff group at index 0 uses `skillCoefficient[0]` = 1.5x damage
- Buff group at index 1 uses `skillCoefficient[1]` = 0.8x damage

## Dependencies

- `HurtUtil.ts` -- normalHurt, normalDoubleHurt, calHurt, checkHit
- `BuffCtr.ts` -- Buff controller managing active buffs
- `MetaAttrib.ts` / `AttribDefine` -- Attribute system
- `FixMath.ts` -- Fixed-point math (round, roundInt)
- `01_BASIC_DAMAGE_CALCULATION.md` -- Base damage formula
