# 12 — Battle Flow & Normal Attack Execution

## A. Battle Initialization

### BattleMain Constructor (Line 188200)
```
Default values:
- injuryReduce = 1 (no PvP reduction)
- shieldDecay = 1 (no shield decay)
- treatDecay = 1 (no heal decay)
- seasonPveDamAdd = 0
- frameTime = 0.033 (30 FPS)
- runningToPart = false
```

### PvP Initialization
When entering PvP:
1. Calculate average level of all players
2. Look up `configLevel[avg_level].pvp_injury_reduce` → `injuryReduce`
3. Read global `shield_correct` → `shieldDecay` (0.4)
4. Read global `hp_recovery_correct` → `treatDecay` (0.3)

---

## B. Normal Attack Execution (SkillHandleNormal.att)

### Code Location
**Module:** SkillHandleNormal.ts
**Lines:** 429925-430068

### Full Attack Flow
```
1. att(target, attackIndex) is called
   ├── attackIndex = -1: first attack (check counter)
   ├── attackIndex = 0: follow-up normal attack
   └── attackIndex > 0: combo/double hit

2. If first attack (-1):
   └── checkCounter(target, attacker)
       └── If counter procs: target queues counter attack

3. Trigger STATE_TRIGER buffs (normal act triggers)

4. checkHit(attacker, target) → Miss / Normal / Crit

5. If MISS: return (no damage)

6. If attackIndex > 0 (COMBO/DOUBLE HIT):
   ├── normalDoubleHurt(attacker, target, hitType) → H
   ├── healthType = Normal ? Hurt_Double : Hurt_Double_Crit
   ├── × (1 + boss_dam) if target is boss
   ├── trigger DOUBLE_TRIGGER buffs
   ├── += FRAGILE_EFFECT damage (additive)
   ├── apply EXTRA_DAMAGE buffs (multiplicative)
   ├── apply GIANT_SLAYER buffs (HP-based bonus)
   ├── healthTarget(target, H, healthType)
   └── trigger DOUBLE_ATTACK / CRIT_ATTACK skill effects

7. If attackIndex <= 0 (NORMAL ATTACK):
   ├── normalActCount++
   ├── normalHurt(attacker, target, hitType) → lt
   ├── healthType = Normal ? Hurt : Hurt_Crit
   ├── += NORMAL_ACT_NUM_TRIGGER value (based on attack count)
   ├── += UnitCallDamageAdd (for summoned units)
   ├── × (1 + boss_dam) if target is boss
   ├── += FRAGILE_EFFECT damage (additive)
   ├── apply EXTRA_DAMAGE buffs (multiplicative)
   ├── apply GIANT_SLAYER buffs (HP-based bonus)
   ├── healthTarget(target, lt, healthType)
   ├── ATK HP steal: normailHpsteal(attacker, target, lt)
   │   └── If > 0: healthTarget(attacker, heal, Act_Hpsteal)
   ├── HP steal proc: checkNormailHpsteal1(attacker, target)
   │   └── If procs: normailHpsteal1(attacker) → heal
   ├── checkThrowHit → knockup
   ├── checkDizz → stun
   │   └── stun_duration = vertigo_times × round(1 - vertigo_res)
   ├── trigger NORMAL_ATTACK / ALL_ATTACK skill effects
   └── if crit: trigger CRIT_ATTACK effects

8. After normal attack: check for combo (checkDoubleAct)
   └── If combo procs: call att(target, 1) recursively
```

---

## C. Counter Attack Execution (SkillHandleCounter)

### Code Location
Lines 429630-429700

### Flow
```
1. checkHit(counterAttacker, originalAttacker)
2. If not miss:
   ├── normalCounterHurt(counter, target, hitType) → f
   ├── healthType = Normal ? Hurt_Counter : Hurt_Counter_Crit
   ├── × (1 + boss_dam) if target is boss
   ├── += FRAGILE_EFFECT damage
   ├── apply EXTRA_DAMAGE buffs
   ├── apply GIANT_SLAYER buffs
   ├── healthTarget(target, f, healthType)
   ├── HP steal
   ├── checkCounterThrowHit → knockup
   └── trigger COUNTER_ATTACK skill effects
```

---

## D. Damage Application Pipeline (Unit.addDamage)

### Code Location
Lines 449240-449363

### Complete Flow for Damage Types
```
For each queued health action:
  switch (healthType):

    case Hurt, Hurt_Crit, Hurt_Ret, Hurt_Share_Damage, Hurt_Share_Damage_Crit,
         Hurt_Double, Hurt_Double_Crit, Real_Damage, Hurt_Bleed, Hurt_Bleed_Crit,
         Hurt_Counter, Hurt_Counter_Crit, SpiritToPlayer:

      1. SKIP if runningToPart (transitioning between battle parts)

      2. PVP REDUCTION: W = max(roundInt(W / injuryReduce), 1)

      3. SEASONAL PVE BONUS: if seasonPveDamAdd > 0 and team 1:
         W = roundInt(W × (1 + seasonPveDamAdd))

      4. SHIELD ABSORPTION: if unit has shields
         for each shield buff:
           absorbed = shield.onShieldAction(W)
           W = roundInt(W - absorbed)
           if all shields depleted: break

      5. BLOCK ABSORPTION: if unit has block buffs
         for each block buff:
           blocked = block.onShieldAction(W)
           W = roundInt(W - blocked)

      6. HP REDUCTION: currenHp = roundInt(currenHp - W)

      7. DEATH PREVENTION:
         - TIME_REVERSAL buffs checked first
         - REMAKE_HP buffs checked second
         - IMMUNE_DEATH buffs checked third
         - If immuneDeath or remakeLock: hp = max(hp, 1)
         - Otherwise: hp = max(hp, 0)

      8. RECORD_DAMAGE tracking

      9. TOTAL DAMAGE accumulation

      10. HP_CHANGE_TRIGER / TOTAL_DAMAGE_TRIGGER buffs

    case Treat, Treat_Crit, Skill_Hpsteal, Act_Hpsteal:
      1. HEAL DECAY: W = roundInt(W × treatDecay)
      2. REDUCE_HEAL buffs
      3. currenHp += W, capped at maxHp

    case Miss:
      → Log only

    case Armor, Armor_def, Inspire, Suppress:
      → Log only (UI effects)

    case SpiritToSpirit:
      → Direct HP reduction (no PvP, no shields)

After all actions:
  - If hp <= 0 and not spirit and recording: force hp = 1
  - Emit UnitHpChange event
  - If hp <= 0: dead()
```

---

## E. Turn/Timing System

### Frame-Based (Not Turn-Based)
The combat is **frame-based** at 30 FPS (frameTime = 0.033s):
```javascript
this.frameTime = .033  // Line 188200
```

### Attack Speed
Units attack based on their `att_speed` attribute (ID 1003). Higher speed = more frequent attacks.

### Battle Duration
Some battle modes have a timer (`chapterTime`). When time runs out, the battle ends.

### runningToPart
When `runningToPart = true`, ALL damage is skipped (line 449284). This happens during transitions between battle phases/parts.

---

## F. HP Recovery (Passive Healing Per Frame)

### Code Location
Lines 449241-449253

```javascript
var u = this.data.getAttrib(I.hp_recovery) - a;  // hp_recovery - ignore_hp_recovery
var d = s.roundInt(s.round(e * u) * this.battleMain.treatDecay);
if (d > 0) {
    // Apply REDUCE_HEAL buffs
    for (var c of reduceHealBuffs) {
        d = c.onCalHeal(d);
    }
    this.data.currenHp = s.round(this.data.currenHp + d);
    this.data.currenHp = Math.min(this.data.currenHp, maxHp);
}
```

Formula:
```
effective_recovery = hp_recovery - ignore_hp_recovery
heal = roundInt(round(maxHp × effective_recovery) × treatDecay)
if heal > 0: apply REDUCE_HEAL buffs, then add to HP (capped at max)
```

---

## Comparison with Known Documentation

### Key Findings:
1. **Combat is frame-based, not turn-based** — 30 FPS simulation
2. **Normal attack can trigger: combo check, counter queue, stun, knockup, HP steal**
3. **Combo is recursive** — att() calls itself with attackIndex > 0
4. **Shield → Block → HP** is the damage application order
5. **Multiple death prevention mechanisms** exist: time reversal, remake HP, immune death
6. **runningToPart skip** prevents damage during phase transitions
7. **HP recovery is per-frame** and affected by treatDecay and REDUCE_HEAL buffs
