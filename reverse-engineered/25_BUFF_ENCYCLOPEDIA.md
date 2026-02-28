# 25 — Buff Encyclopedia

## Overview

The buff system is the core combat modifier framework. All damage bonuses, shields, crowd control, attribute modifications, and reactive triggers are implemented as buffs. There are **80 unique buff classes** organized into **46 BuffGroupType categories**. Buffs are instantiated via the `buffMap` registry at line 332125.

---

## Architecture

### Buff Lifecycle
```
1. addBuff(target, buffId, duration, skillPar)     [line 431489]
2. ConfigBuff lookup → get action, group, mutex, params
3. IGNORE_BUFFIDS check → skip if target blocks this buff
4. Mutex check (5 types: replace, unique, stack, per-caster, refresh)
5. Control immunity → skip if target has invincible/notControlled
6. Instantiate: buffMap[config.action](config)
7. If type == 0 (instant): onBegin() + destroy immediately
8. If type > 0 (persistent): add to BuffCtr, manage lifecycle
9. AddBuffTrigger notification if active
```

### ConfigBuff Schema (Line 222479, 16 Fields)

| Index | Field | Description |
|-------|-------|-------------|
| 0 | id | Unique buff identifier |
| 1 | name | Localized name |
| 2 | type | 0=instant (execute+destroy), 1+=persistent |
| 3 | group | BuffGroupType value for runtime querying |
| 4 | icon | UI icon asset |
| 5 | effect | Visual effect on target |
| 6 | effect_mirror | Mirrored visual effect |
| 7 | mutex | Stacking rule: 1=replace, 2=unique, 3=stack+max, 4=unique/caster, 5=refresh/caster |
| 8 | add_max | Maximum stack count |
| 9 | bind | BindType (1=bp_lead, 2=bp_bottom, 3=bp_top) |
| 10 | action | String key into buffMap for class instantiation |
| 11-15 | param1-param5 | Class-specific parameters (see per-class docs below) |

---

## All 46 BuffGroupTypes

| ID | Name | Category | Description |
|----|------|----------|-------------|
| 1 | HURT | Damage | Generic damage-dealing buffs |
| 3 | CTR | Control | CC effects (stun, freeze, root, taunt, ban) |
| 4 | ADD | Attribute | Attribute modification buffs |
| 10 | TRAP_FOLLOW | Utility | Trap placement and following |
| 20 | SHIELD | Defense | Shield creation and absorption |
| 30 | NORMAL_ACT_NUM_TRIGGER | Trigger | Triggers after N normal attacks |
| 40 | BULLET_NUM | Modifier | Skill projectile count modification |
| 50 | USE_SKILL_NORMAL_ADD | Trigger | Effects on skill → normal attack sequence |
| 60 | SKILL_DAMAGE_ADD | Damage | Flat skill damage bonus in pipeline |
| 70 | SHARE_DAMAGE | Damage | Splash/shared damage distribution |
| 80 | ATTRIB_CONDITION | Attribute | Conditional attribute modifiers |
| 90 | DESTROY_WHEN_NORMAL_AFTER | Lifecycle | Auto-destroy after normal attack |
| 100 | NORMAL_BULLET_NUM | Modifier | Normal attack projectile count |
| 110 | STATE_TRIGER | Trigger | State-based reactions (Normal_Act, Skill_Effect, etc.) |
| 120 | DELAY_DEMAGE | Damage | Delayed damage application |
| 130 | ADDBUFF_TOPET | Utility | Add buffs to pet/pal units |
| 140 | HP_CHANGE_TRIGER | Trigger | Triggers on HP change events |
| 150 | AddBuffTrigger | Trigger | Triggers when any buff is added |
| 160 | UnitCallDamageAdd | Damage | Bonus damage from summoned units |
| 170 | DOUBLE_TRIGGER | Trigger | Double-action trigger mechanic |
| 180 | TOTAL_DAMAGE_TRIGGER | Trigger | Triggers at cumulative damage threshold |
| 190 | USE_SKILL_ADD | Damage | Accumulates damage record per skill use |
| 200 | FRAGILE_EFFECT | Damage | Fragile debuff: flat bonus damage |
| 210 | TRIGGER_BULLET | Modifier | Triggers additional projectiles |
| 220 | SKILL_COUNTER | Modifier | Skill counter/tracking mechanic |
| 230 | IMMUNE_DEATH | Defense | Prevents lethal damage |
| 240 | BLOCK | Defense | Tiered damage reduction by HP ratio |
| 270 | DESTROY_WHEN_SKILL_AFTER | Lifecycle | Auto-destroy after skill use |
| 280 | TRIGGER_AND_STAY | Trigger | Persistent trigger effect |
| 290 | SKILL_REAL_DAMAGE | Damage | True/real damage as % of skill damage |
| 320 | REMAKE_HP | Defense | HP remake / resurrection |
| 330 | IGNORE_BUFFIDS | Utility | Block specific buff IDs from applying |
| 340 | SKILL_RETURN | Defense | Skill reflection/return |
| 350 | CURRENT_HP | Utility | Fixed HP ratio for calculations |
| 360 | SKILL_BUFFTIME_ADD | Modifier | Extends buff durations |
| 370 | IGNORE_COPY | Utility | Prevents buff copying |
| 380 | VAMPIRE | Healing | Life steal from damage dealt |
| 390 | GIANT_SLAYER | Damage | Bonus dmg from HP difference |
| 400 | DEFER_DAMAGE | Defense | Absorbs damage, releases over time |
| 410 | EXTRA_DAMAGE | Damage | Post-calc multiplicative damage bonus |
| 420 | TIME_REVERSAL | Defense | HP restoration to past state |
| 430 | RECORD_DAMAGE | Trigger | Records damage, triggers at threshold |
| 440 | REDUCE_HEAL | Debuff | Healing reduction/amplification |
| 450 | SPECIAL_EXTRA_BULLET_NUM | Modifier | Extra bullets with probability |
| 460 | DAMAGE_TRIGGER | Trigger | Trigger at HP% damage threshold |

---

## All 80 Buff Classes

### Damage-Dealing Buffs

| Class | buffMap Key | Line | Group | Description |
|-------|-----------|------|-------|-------------|
| BuffBleed | `bleed` | 192750 | HURT(1) | 8-type bleed system |
| BuffSkillValue | `skill_value` | 195728 | HURT(1) | Primary skill damage, 11 calTypes |
| BuffSkillHpHurt | `hp_hurt` | 195492 | HURT(1) | HP%-based damage with resistance |
| BuffDotDamage | `dotdamage` | 193812 | HURT(1) | Damage over time |

#### BuffBleed — 8 Sub-Types (param1 = _type)

| Type | Name | Formula |
|------|------|---------|
| 0 | ATK-based | (ATK-DEF) × ATK_DAM + boss_dam + calHurt |
| 1 | Current HP% | target.curHP × skillPar × injuryReduce |
| 2 | Skill-based | (ATK-DEF) × skill_dam_extra × skillPar + skill_resist + skill crit |
| 3 | ATK+resist | (ATK-DEF) × ATK_DAM + att_resist + normal crit |
| 4 | Combo | (ATK-DEF) × double_hit_dam + double_hit_def + normal crit |
| 5 | Counter | (ATK-DEF) × counter_dam + counter_def + normal crit |
| 6 | Max HP% | target.maxHP × skillPar × injuryReduce |
| 10 | Attribute | Uses param2 attr_id, param3 for target/caster selection |

#### BuffSkillValue — 11 calTypes (param2 = _calType)

| calType | Name | Base Value |
|---------|------|------------|
| 0 | Attribute | attribId value (caster or target via hpType bit 8) |
| 1 | ATK-DEF | max(roundInt(ATK - DEF×(1+DEF_COE)), 1) |
| 2 | HP difference | caster.maxHP - target.curHP |
| 3 | Target curHP | target.curHP |
| 4 | Attack damage | (ATK-DEF) × ATK_DAM |
| 5 | Target ATK | target's (ATK-DEF) × ATK_DAM |
| 6 | Combo | (ATK-DEF) × double_hit_dam |
| 7 | Counter | (ATK-DEF) × counter_dam |
| 8 | Caster curHP | caster.curHP |
| 9 | Caster maxHP | caster.maxHP |
| 10 | Partner | (ATK-DEF) × ATK_DAM × partner_dam × partner_dam_extra |

**Param flags (param4 = _ignoreFlag bitmask):** bit 1=SkillCrit, bit 2=T1045 (skip skill_dam_extra), bit 4=UseCrit (apply normal crit)

#### BuffDotDamage Parameters
- param1 = tick frequency (seconds, /10000)
- param2 = total tick count
- param3 = 1 to apply first tick immediately

---

### Damage Modifier Buffs

| Class | buffMap Key | Line | Group | Description |
|-------|-----------|------|-------|-------------|
| BuffExtraDamage | `extra_damage` | 193970 | EXTRA_DAMAGE(410) | Post-calc multiplier (3 types) |
| BuffGiantSlayer | `giantslayer` | 194150 | GIANT_SLAYER(390) | HP-difference bonus |
| BuffSkillDamageAdd | `skill_damage_add` | 195337 | SKILL_DAMAGE_ADD(60) | Flat damage bonus |
| BuffSkillFragileAdd | `fragile_effect` | 195449 | FRAGILE_EFFECT(200) | Fragile debuff bonus |
| BuffSkillRealDamage | `skill_real_damage` | 195602 | SKILL_REAL_DAMAGE(290) | True damage % |
| BuffShareDamage | `sharedamage` | 195113 | SHARE_DAMAGE(70) | Splash damage |

#### BuffExtraDamage — 3 calTypes (param1)
| Type | Behavior |
|------|----------|
| 0 | Flat: damage × (1 + skillPar) |
| 1 | HP-loss: damage × (1 + (maxHP-curHP)/maxHP × skillPar) |
| 2 | HP-loss with CURRENT_HP buff override |

#### BuffGiantSlayer Formula
```
bonus = min(ceil((targetHP - ownerHP) / ownerHP × 100) × extraDam, cap) / 10000
cap = maxforBoss (if target is Boss) or maxforUnit (otherwise)
```

---

### Defensive Buffs

| Class | buffMap Key | Line | Group | Description |
|-------|-----------|------|-------|-------------|
| BuffShield | `shield` | 195169 | SHIELD(20) | Shield absorption (4 calTypes) |
| BuffBreakShield | `break_shield` | 192989 | SHIELD(20) | Shield-breaking |
| BuffBlock | `block` | 192911 | BLOCK(240) | Tiered damage reduction |
| BuffDeferDamage | `defer_damage` | 193522 | DEFER_DAMAGE(400) | Absorb → release over time |
| BuffImmuneDeath | `immune_death` | 194425 | IMMUNE_DEATH(230) | Survive lethal damage |
| BuffRemake | `remake` | 195014 | REMAKE_HP(320) | Resurrection mechanic |
| BuffTimeReversal | `time_reversal` | 196323 | TIME_REVERSAL(420) | Restore HP to past state |
| BuffInvincible | `invincible` | 194491 | — | Full invincibility |
| BuffNotGetDamage | `not_get_damage` | 194561 | — | Damage immunity |

#### BuffShield — 4 calTypes (param2)
| Type | Base Value |
|------|------------|
| 0 | Attribute value (param3 = attrId) |
| 1 | ATK-DEF base |
| 2 | Caster maxHP - Target curHP |
| 3 | Target curHP |

**Shield formula:** `roundInt(baseValue × skillPar) × (1 + shield_hp_extra) × shieldDecay`

#### BuffBlock — Tiered Reduction (param5)
param5 = `[[threshold1, reduction1], [threshold2, reduction2], ...]`
- Calculates `damage / HP × 10000`, finds matching tier
- Returns `reduction / 10000 × damage`

#### Death Prevention Chain (checked in order in addDamage)
1. **TIME_REVERSAL** → restore HP to recorded state
2. **REMAKE_HP** → resurrect to param1 HP%
3. **IMMUNE_DEATH** → set HP to param1 HP%

---

### Healing Buffs

| Class | buffMap Key | Line | Group | Description |
|-------|-----------|------|-------|-------------|
| BuffVampire | `vampire` | 196744 | VAMPIRE(380) | Life steal |
| BuffReduceHeal | `reduce_heal` | 194970 | REDUCE_HEAL(440) | Healing reduction |
| BuffHpAlter | `hp_alter` | 194201 | — | Direct HP modification |

#### BuffVampire Formula
```
heal = round(damage × totalDamMul) / injuryReduce × skillDamFactor
cap  = maxHP × _max/10000 / treatDecay
totalDamMul = round(1 + total_dam_add) × round(1 - total_dam_def)
```

---

### Control (CC) Buffs

| Class | buffMap Key | Line | Group | Description |
|-------|-----------|------|-------|-------------|
| BuffDizz | `dizz` | 193669 | CTR(3) | Stun/dizziness |
| BuffBound | `bound` | 192952 | CTR(3) | Root/bind |
| BuffFrozen | `frozen` | 194038 | CTR(3) | Freeze |
| BuffTaunt | `taunt` | 196242 | CTR(3) | Forced targeting |
| BuffBanAct | `ban_act` | 192663 | CTR(3) | Action ban |
| BuffBanSkill | `ban_skill` | 192705 | CTR(3) | Skill ban |

#### BuffDizz Parameters
- param1 = dizzType (sub-type)
- param2 = stayTime (min stun before break)
- param3 = triggerType (0/1/2)
- param5[0] = on-stun buffs, param5[1] = on-break buffs, param5[2] = ally spread buffs

All control buffs are blocked by **BuffNotControlled** (`not_controll`) and **BuffInvincible** (`invincible`).

---

### Attribute Modification Buffs

| Class | buffMap Key | Line | Group | Description |
|-------|-----------|------|-------|-------------|
| BuffAttrib | `attrib` | 192402 | ADD(4) | Direct attribute add/multiply |
| BuffAttribContinue | `attrib_continue` | 192533 | ADD(4) | Periodic stacking |
| BuffAttribConvert | `attrib_convert` | 192586 | ADD(4) | Convert one attribute to another |
| BuffAttribCondition | `attrib_condition` | 192453 | ATTRIB_CONDITION(80) | Conditional modifier |
| BuffAttackAdd | `attack_add` | 192334 | ADD(4) | Attack addition |

#### BuffAttrib Parameters
- param1 = AttribDefine ID to modify
- param2 = 2 for multiplicative, else additive
- param3 = value amount
- Applied as: `value × skillPar × getSkillFactAttrValue(skillPar, skillId, 1044)`

#### BuffAttribConvert — 6 calTypes (param1)
| Type | Source |
|------|--------|
| 0 | Base value of source attribute |
| 1 | Current HP |
| 2 | Lost HP |
| 3 | HP% × 10000 |
| 4 | Lost HP% × 10000 |
| 5 | Lost HP% via CURRENT_HP buff |

---

### Trigger / Reactive Buffs

| Class | buffMap Key | Line | Group | Description |
|-------|-----------|------|-------|-------------|
| BuffStateTrigger | `statetrigger` | 196197 | STATE_TRIGER(110) | State-change reactions |
| BuffHpChangeTrigger | `hpchange_trigger` | 194251 | HP_CHANGE_TRIGER(140) | HP threshold triggers |
| BuffAddBuffTrigger | `addbuff_trigger` | 192245 | AddBuffTrigger(150) | Buff-application triggers |
| BuffTotalDamageTrigger | `total_damage_trigger` | 196387 | TOTAL_DAMAGE_TRIGGER(180) | Cumulative damage triggers |
| BuffDoubleTrigger | `double_trigger` | 193921 | DOUBLE_TRIGGER(170) | Double-action triggers |
| BuffTriggerByDamage | `trigger_by_damage` | 196548 | DAMAGE_TRIGGER(460) | HP% damage threshold |
| BuffRecordDamage | `record_damage` | 194848 | RECORD_DAMAGE(430) | Timed damage accumulation |
| BuffAddBuffToTarget | `addbuff_to_target` | 192183 | NORMAL_ACT_NUM_TRIGGER(30) | N-attack triggers |

#### BuffRecordDamage Parameters
- param1 = recording duration (seconds)
- param2 = hurtType (0=HP%-based conversion, 1=raw damage)
- param3 = early trigger HP% threshold
- param5 = [[buffId, duration]...] buffs applied on trigger

---

### Utility Buffs

| Class | buffMap Key | Line | Group | Description |
|-------|-----------|------|-------|-------------|
| BuffClear | `clear` | 193230 | — | Remove buffs |
| BuffCopyUnit | `copy_unit` | 193312 | — | Copy unit attributes/buffs |
| BuffCopyIgnore | `ignore_copy` | 193271 | IGNORE_COPY(370) | Prevent buff copying |
| BuffIgnoreIds | `ignore_buff` | 194383 | IGNORE_BUFFIDS(330) | Block specific buff IDs |
| BuffResetCd | `reset_cd` | 195068 | — | Reset skill cooldowns |
| BuffPauseCd | `pause_cd` | 194596 | — | Pause cooldown timers |
| BuffRecoverPower | `recover_power` | 194909 | — | Restore energy/power |
| BuffCallUnit | `call_unit` | 193130 | — | Summon unit |
| BuffCallSpirit | `call_spirit` | 193038 | — | Summon spirit |
| BuffDirectKill | `direct_kill` | 193620 | — | Instant kill |
| BuffDoubleSkill | `double_skill` | 193858 | DESTROY_WHEN_SKILL_AFTER(270) | Execute skill twice |
| BuffSkillParse | `parse_skill` | 195553 | — | Parse and execute skill |
| BuffSkillEffect | `skill_effect` | 195411 | USE_SKILL_NORMAL_ADD(50) | Trigger effects on skill use |
| BuffSkillCounter | `skill_counter` | 195300 | SKILL_COUNTER(220) | Track skill use count |
| BuffSkillBuffTimeAdd | `skill_bufftime_add` | 195265 | SKILL_BUFFTIME_ADD(360) | Extend buff durations |
| BuffSkillDoubleHitNum | `double_hit_num` | 195380 | BULLET_NUM(40) | Modify hit count |
| BuffCurrentHp | `current_hp` | 193473 | CURRENT_HP(350) | Fixed HP ratio provider |
| BuffPetConvert | `pet_convert` | 194667 | ADDBUFF_TOPET(130) | Convert buffs to pets |
| BuffTrap | `trap` | 196436 | TRAP_FOLLOW(10) | Trap placement |
| BuffSound | `sound` | 195989 | — | Play sound effect |
| BuffAction | `action` | 192088 | — | Generic action |
| BuffCheck | `check` | 193172 | — | Condition checking |
| BuffDelayDamage | `delaydamage` | 193576 | DELAY_DEMAGE(120) | Delayed damage |
| BuffHpTrigger | `hp_trigger` | 194325 | — | HP threshold trigger |
| BuffRandomBuff | `random_buff` | 194721 | — | Random buff from pool |
| BuffRandomSkillTrigger | `random_skill_trigger` | 194788 | — | Random skill trigger |
| BuffAddByCondition | `add_buff_by_condition` | 192288 | — | Conditional buff application |
| BuffAddBuffByMultiplyingPower | `add_buff_by_multiplying_power` | 192134 | — | Power-based conditional buff |
| BuffUseSkillAdd | `use_skill_add` | 196697 | USE_SKILL_ADD(190) | Skill-use accumulation |
| BuffUnitCallDamageAdd | `unit_call_damage_add` | 196656 | UnitCallDamageAdd(160) | Summon damage bonus |
| BuffTrigerByUType | `triger_by_uType` | 196476 | DESTROY_WHEN_NORMAL_AFTER(90) | Unit-type trigger |
| BuffTriggerBullet | `trigger_bullet` | 196513 | TRIGGER_BULLET(210) | Additional projectiles |
| BuffTriggerBySkillParam | `trigger_by_skill_param` | 196607 | TRIGGER_AND_STAY(280) | Skill-param trigger |
| BuffSpecialExtralBullet | `special_extra_bullet_num` | 196027 | SPECIAL_EXTRA_BULLET_NUM(450) | Extra bullets w/ probability |
| BuffSpeedRandom | `speed_random_buff` | 196074 | — | Random speed modification |
| BuffSpeedTrigger | `speed_trigger` | 196125 | — | Speed-based trigger |
| BuffThrowHit | `throw_hit` | 196280 | — | Throw/knockback |
| BuffSkillReturn | `skill_return` | 195659 | SKILL_RETURN(340) | Skill reflection |

---

## Damage Interaction Pipeline

The order in which buff systems interact during damage calculation:

| Step | System | GroupType | Effect |
|------|--------|-----------|--------|
| 1 | SKILL_RETURN | 340 | Check reflection → interrupt if reflected |
| 2 | Base Damage | — | ATK-DEF or calType formula |
| 3 | skillPar | — | Skill factor × active_skilldamage_par |
| 4 | SKILL_DAMAGE_ADD | 60 | Add flat bonus damage |
| 5 | skill_dam_extra | 1045 | Multiply by skill damage extra (unless T1045 flag) |
| 6 | Skill Crit | — | × (1 + skill_crit_dam), then pow(damage, 0.98) |
| 7 | Normal Crit | — | max(1.5, crit_dam / max(0.5, crit_def)) |
| 8 | Boss Damage | — | × (1 + boss_dam) if target is Boss |
| 9 | RECORD_DAMAGE | 430 | × (1 + recordDamage/10000) |
| 10 | Counter Damage | — | × counterDamage multiplier |
| 11 | Resistance | — | × (1 - skill_resist or att_resist) |
| 12 | calHurt | — | Fragile, suppress/inspire |
| 13 | EXTRA_DAMAGE | 410 | Post-calc multiplicative bonus |
| 14 | GIANT_SLAYER | 390 | HP-difference bonus |
| 15 | Deal Damage | — | healthTarget(target, damage, healthType) |
| 16 | STATE_TRIGER | 110 | Skill crit state triggers |
| 17 | skillHpsteal | — | Skill-specific HP steal |
| 18 | SKILL_REAL_DAMAGE | 290 | True damage as % of dealt |
| 19 | VAMPIRE | 380 | Life steal healing |
| 20 | HP_Hurt Effects | — | Trigger skill effects with HP_Hurt type |

---

## Statistics

- **80** unique buff classes in buffMap
- **46** BuffGroupType categories
- **81** buffMap entries (state_triger + statetrigger → same class)
- **4** damage-dealing classes (BuffBleed 8 types, BuffSkillValue 11 calTypes, BuffSkillHpHurt, BuffDotDamage)
- **6** damage-modifying classes
- **9** defensive classes
- **3** healing classes
- **6** control classes
- **8** trigger/reactive classes
- **38** utility/support classes
