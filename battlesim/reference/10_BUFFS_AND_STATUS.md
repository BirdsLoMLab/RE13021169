# 10 — Buffs and Status Effects

> 46 buff group types, mutex rules, bleed/shield/death prevention, and the complete buff pipeline.

---

## Buff Architecture

### ConfigBuff Schema (16 fields)
| Index | Field | Description |
|-------|-------|-------------|
| 0 | id | Unique buff ID |
| 1 | name | Localized name |
| 2 | type | Duration: 0=instant, 1+=timed |
| 3 | group | BuffGroupType for runtime queries |
| 4 | icon | UI icon |
| 5 | effect | Visual effect |
| 6 | effect_mirror | Mirrored visual |
| 7 | mutex | Stacking: 1=Replace, 2=Unique, 3=Stack, 4=Unique/caster, 5=Refresh/caster |
| 8 | add_max | Max stacks (for mutex=3) |
| 9 | bind | Effect attachment type |
| 10 | action | Handler class key (into buffMap) |
| 11-15 | param1-5 | Class-specific parameters |

### Buff Creation Flow
```
1. SkillRunner.addBuff(target, buffId, duration, skillPar)
2. Look up ConfigBuff
3. IGNORE_BUFFIDS check → skip if blocked
4. Mutex check (types 2,4,5) → prevent duplicates
5. Control immunity check (notControlled/invincible)
6. Instantiate: buffMap[action](config)
7. Set skillPar, duration (with CONTROL_RES / shield_time_extra)
8. type==0: execute + destroy immediately
9. type>0: add to BuffCtr, manage lifecycle
10. Mutex 3: stack, enforce add_max
11. Notify AddBuffTrigger if active
```

---

## Mutex Rules (5 Types)

| Mutex | Name | Behavior |
|-------|------|----------|
| 1 | Replace | Stop existing, add new |
| 2 | Unique | Reject new if exists |
| 3 | Stack w/ Max | Multiple up to add_max; refresh durations |
| 4 | Unique/caster | One per caster; reject re-apply |
| 5 | Refresh/caster | One per caster; reset duration |

---

## 46 Named BuffGroupTypes

| ID | Name | Description |
|----|------|-------------|
| 1 | HURT | Generic damage |
| 3 | CTR | Control effects (stun, freeze, root) |
| 4 | ADD | Attribute modification |
| 10 | TRAP_FOLLOW | Trap placement |
| 20 | SHIELD | Shield creation/absorption |
| 30 | NORMAL_ACT_NUM_TRIGGER | N-attack triggers |
| 40 | BULLET_NUM | Projectile count modification |
| 50 | USE_SKILL_NORMAL_ADD | Skill → normal attack effects |
| 60 | SKILL_DAMAGE_ADD | Flat skill damage bonus |
| 70 | SHARE_DAMAGE | Splash/shared damage |
| 80 | ATTRIB_CONDITION | Conditional attribute modifiers |
| 90 | DESTROY_WHEN_NORMAL_AFTER | Auto-destroy after normal attack |
| 100 | NORMAL_BULLET_NUM | Normal attack projectile count |
| 110 | STATE_TRIGER | State-based reactions |
| 120 | DELAY_DEMAGE | Delayed damage |
| 130 | ADDBUFF_TOPET | Buff pet/pal |
| 140 | HP_CHANGE_TRIGER | HP change triggers |
| 150 | AddBuffTrigger | Buff application triggers |
| 160 | UnitCallDamageAdd | Summon bonus damage |
| 170 | DOUBLE_TRIGGER | Double-action trigger |
| 180 | TOTAL_DAMAGE_TRIGGER | Cumulative damage threshold |
| 190 | USE_SKILL_ADD | Per-skill damage record |
| 200 | FRAGILE_EFFECT | Vulnerability debuff |
| 210 | TRIGGER_BULLET | Additional projectiles |
| 220 | SKILL_COUNTER | Skill counter tracking |
| 230 | IMMUNE_DEATH | Prevents lethal damage |
| 240 | BLOCK | Tiered damage reduction |
| 270 | DESTROY_WHEN_SKILL_AFTER | Auto-destroy after skill |
| 280 | TRIGGER_AND_STAY | Persistent trigger |
| 290 | SKILL_REAL_DAMAGE | True damage % of skill damage |
| 320 | REMAKE_HP | HP restoration/revive |
| 330 | IGNORE_BUFFIDS | Block specific buff IDs |
| 340 | SKILL_RETURN | Skill reflection |
| 350 | CURRENT_HP | Fixed HP ratio for calculations |
| 360 | SKILL_BUFFTIME_ADD | Extend buff durations |
| 370 | IGNORE_COPY | Prevent buff copying |
| 380 | VAMPIRE | Life steal |
| 390 | GIANT_SLAYER | HP-difference bonus damage |
| 400 | DEFER_DAMAGE | Absorb/release damage over time |
| 410 | EXTRA_DAMAGE | Post-calc multiplicative bonus |
| 420 | TIME_REVERSAL | HP history restoration |
| 430 | RECORD_DAMAGE | Damage accumulation trigger |
| 440 | REDUCE_HEAL | Healing reduction/amp |
| 450 | SPECIAL_EXTRA_BULLET_NUM | Probability-based extra bullets |
| 460 | DAMAGE_TRIGGER | HP% damage threshold trigger |

---

## Bleed System (8 Sub-Types)

| calType | Name | Formula | Can Crit |
|---------|------|---------|----------|
| 0 | ATK-based | `(ATK-DEF) × ATK_DAM + boss_dam + calHurt` | No |
| 1 | Current HP% | `target.curHP × skillPar × injuryReduce` | No |
| 2 | Skill-based | `(ATK-DEF) × skill_dam_extra × skillPar + skill_resist` | Yes (skill) |
| 3 | ATK+resist | `(ATK-DEF) × ATK_DAM + att_resist + crit` | Yes (normal) |
| 4 | Combo | `(ATK-DEF) × double_hit_dam + double_hit_def + crit` | Yes (normal) |
| 5 | Counter | `(ATK-DEF) × counter_dam + counter_def + crit` | Yes (normal) |
| 6 | Max HP% | `target.maxHP × skillPar × injuryReduce` | No |
| 10 | Attribute | Uses param2 attr_id, param3 for source | No |

**Hidden mechanic:** Skill crits apply `pow(damage, 0.98)` — a 5-13% reduction scaling with value.

---

## Shield System (4 calTypes)

| calType | Base Value |
|---------|------------|
| 0 | Attribute value (param3 = attrId) |
| 1 | ATK-DEF base |
| 2 | Caster maxHP - Target curHP |
| 3 | Target curHP |

### Shield Formula
```
shield_hp = roundInt(base * skillPar) * (1 + shield_hp_extra) * shieldDecay
duration = round(duration + shield_time_extra)
```

### Absorption
```
absorbed = min(shield_remaining, incoming_damage)
damage_through = incoming_damage - absorbed
```
Multiple shields stack additively on shieldHp. Damage overflows past shields.

---

## Death Prevention Chain

Checked in priority order when HP ≤ 0:

| Priority | Type | Group | Effect |
|----------|------|-------|--------|
| 1 | TIME_REVERSAL | 420 | Restore HP to recorded past state |
| 2 | REMAKE_HP | 320 | Resurrect to param1 HP% |
| 3 | IMMUNE_DEATH | 230 | Set HP to param1 HP% |

Only one triggers per death event.

---

## Giant Slayer (Group 390)

```
if targetHP <= attackerHP: no bonus
hpRatio = ceil((targetHP - attackerHP) / attackerHP * 100)
extraDam = round(hpRatio * param1)
extraDam = min(extraDam, cap)  // param2=bossCap, param3=unitCap
damage = round(baseDamage * (1 + extraDam / 10000))
```

All 3 active buffs (50090, 50105, 51405): 10 per 1% HP diff, capped at 150%.

---

## Vampire / Life Steal (Group 380)

```
heal = round(damage * totalDamMul) / injuryReduce * skillDamFactor
heal = min(heal, maxHP * hpMaxRatio)
heal = roundInt(heal * treatDecay)  // 30% in PvP
```

---

## Extra Damage (Group 410, 3 Types)

| Type | Formula |
|------|---------|
| 0 | Flat bonus: `damage * (extraDam / 10000)` |
| 1 | HP-loss scaling: `damage * (hpLost / maxHP * extraDam / 10000)` |
| 2 | Fixed HP via CURRENT_HP buff illusion |

---

## Control Effects (CC)

### Actions blocked by notControlled/invincible:
```
dizz, ban_skil, throw_hit, bound, ban_act
```

### CONTROL_RES Duration Reduction
```
if (action == "dizz" && param1 == 0) || (action == "ban_act"):
    duration = round(duration - round(duration * CONTROL_RES))
```
At CONTROL_RES = 1.0 → effectively immune to stun/ban_act.

### CC Cleansability
- **CTR group 3:** Cleansable by CC cleanse (90 total buffs)
- **Group 260:** NOT cleansable (enhanced/boss CC)
- **Frozen (groups 271-279):** NOT cleansable, has break conditions
- **Bleed, Fragile, Reduce Heal, Taunt:** NOT cleansable

---

## Damage Interaction Pipeline (BuffSkillValue/BuffBleed)

```
 1. SKILL_RETURN check (reflect)
 2. Base damage calculation (calType)
 3. skillPar × active_skilldamage_par
 4. + SKILL_DAMAGE_ADD (group 60)
 5. × skill_dam_extra (unless T1045)
 6. Skill crit → × (1 + skill_crit_dam) → pow(0.98)
 7. Normal crit → × max(1.5, crit_dam / max(0.5, crit_def))
 8. × boss_dam
 9. × RECORD_DAMAGE (group 430)
10. × counter damage multiplier
11. × (1 - resistance)
12. calHurt (DMG RES, PvE)
13. EXTRA_DAMAGE (group 410)
14. GIANT_SLAYER (group 390)
15. healthTarget → Total DMG → shield → HP reduction
16. STATE_TRIGER if skill crit
17. skillHpsteal
18. SKILL_REAL_DAMAGE (group 290)
19. VAMPIRE (group 380)
20. HP_Hurt effect triggers
```

---

## Speed Attribute Cascade

When speed (1009) changes, ALL ATTRIB_CONDITION buffs re-evaluate:
```javascript
if (this._id == speed) {
    for (buff of getBuffByType(ATTRIB_CONDITION)) {
        buff.updateAttrib()
    }
}
```
Unique to speed — no other attribute triggers this cascade.
