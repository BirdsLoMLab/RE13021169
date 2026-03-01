# 36 — Hidden Combat Mechanics (Undiscovered)

> **Sources:** game_script_pretty.js deep trace; Buff.json full scan of 4,155 entries
> **Scope:** Combat mechanics not covered in existing documentation — discovered through source code analysis

---

## 1. The 0.98 Exponent: Skill Crit Dampening

**Code:** Lines 192786, 195885

When a **bleed or skill** scores a critical hit, the damage is raised to the power of 0.98 **after** the crit multiplier is applied:

```javascript
// Line 192786 (BuffBleed.ts):
A = roundInt(A * round(1 + skill_crit_dam));
A = roundInt(Math.pow(A, 0.98));   // ← HIDDEN DAMPENING
healthType = Hurt_Bleed_Crit;

// Line 195885 (Skill effect handler):
x = roundInt(x * round(1 + skill_crit_dam));
x = roundInt(Math.pow(x, 0.98));   // ← SAME DAMPENING
healthType = Hurt_Crit;
```

**Impact by damage level:**

| Raw Crit Damage | After ^0.98 | Effective Reduction |
|-----------------|-------------|---------------------|
| 1,000 | 986 | -1.4% |
| 10,000 | 9,772 | -2.3% |
| 100,000 | 95,499 | -4.5% |
| 1,000,000 | 912,011 | -8.8% |
| 10,000,000 | 8,709,636 | -12.9% |

**Key Insight:** This is a **progressive tax on skill crit damage** that scales with the damage value. At endgame where skill crits hit in the millions, this is a 10-13% hidden damage reduction. It specifically targets skill crits (not normal crits), making normal ATK crits relatively more efficient than skill crits at very high damage values.

**Who this matters for:**
- **Darklord** loses the most (heavy skill crit reliance: +150% Skill Crit DMG during active)
- **Sacred Hunter** is barely affected (relies on normal ATK crits, not skill crits)
- **Prophet** is mildly affected (skill-focused but lower raw damage)

**Not applied to:** Normal attack crits (Hurt_Crit from checkHit), combo crits, counter crits. Only skill effect damage and bleed damage that crits.

---

## 2. DEFER_DAMAGE: Damage Deferral System

**Code:** Lines 193504-193558 (`BuffDeferDamage.ts`)
**In pipeline:** Line 431471 (`healthTarget`)

A buff that **absorbs a percentage of incoming damage** and releases it gradually over time.

```javascript
calDamage(damage, target) {
    if (this.checkTime < this.getDamTime) {
        var deferred = round(damage * getDamRatio / 10000);
        this.totalDam += deferred;       // Store deferred damage
        return round(damage - deferred); // Return reduced damage
    }
    return damage;  // After defer window, full damage passes through
}

onUpdate(deltaTime) {
    if (checkTime >= getDamTime && checkTime <= getDamTime + releaseDamTime) {
        // Release stored damage at releaseDamRatio rate
        var release = totalDam * releaseDamRatio / 10000;
        owner.hit(null, release, Hurt, 0, buffId, 0, 0, 0);
    }
}
```

**Parameters:**
- `param1` (getDamRatio): % of damage deferred (e.g., 50020 = 500.2%? likely a buff ID reference)
- `param2` (getDamTime): Duration of deferral window (seconds)
- `param3` (releaseDamRatio): Rate of damage release per tick
- `param4` (releaseDamTime): Duration of release phase

**Only 1 buff uses this:** Buff 50019 (param1=50020, param2=5, param3=0, param4=0). With releaseRatio=0, the deferred damage is **never released** — it's effectively a damage absorption that disappears when the buff expires.

**Pipeline Position:** Applied in `healthTarget()` just before final damage application, AFTER Total DMG Bonus/RES. This means it works on the post-multiplier damage value.

---

## 3. TotalDamageTrigger: Cumulative Damage Threshold

**Code:** Lines 196369-196416 (`BuffTotalDamageTrigger.ts`)

Tracks **cumulative damage dealt** and triggers effects when a threshold is crossed.

```javascript
onTotalDamage(attackerId) {
    if (!this.hasTrigger) {
        var totalDmg = this.owner.data.totalDamage;
        if (calType == 0) {
            if (totalDmg < threshold) return;  // Absolute threshold
        } else if (calType == 1) {
            if (totalDmg / maxHp < threshold / 10000) return;  // HP% threshold
        }
        // Apply buffs and set one-time flag
        for (buff of addBuffList) this.runner.addBuff(target, buff, duration, skillPar);
        this.hasTrigger = true;
    }
}
```

**Buff 51015** (the only TotalDamageTrigger in data):
- `param1=1` → calType 1 = HP% threshold
- `param2=5` → threshold value (likely 50% of max HP in damage dealt?)
- `param5=[10001]` → applies buff 10001 when triggered

**Where called:** Line 449322 — every time damage is dealt via `addDamage()`.

**Exploit potential:** This means certain artifact/mount skills can trigger powerful one-shot buffs after dealing enough total damage. The threshold is checked against cumulative damage, not per-hit.

---

## 4. AddBuffTrigger: Buff Chain Reactions

**Code:** Lines 192229-192270 (`BuffAddBuffTrigger.ts`)

Watches for a **specific buff ID** being applied and triggers additional effects after N applications.

```javascript
onAddBuffTrigger(target, buffId, duration) {
    if (buffId == this._trigerbuffid) {
        this._currentTriggerValue++;
        if (this._currentTriggerValue >= this._triggercount) {
            this._currentTriggerValue = 0;
            for (buff of addBuffList) {
                addBuff(target, buff, duration || customDuration, skillPar);
            }
        }
    }
}
```

**Active buffs using this:**
- **Buff 30006**: Watches for buff 10012, triggers after 1 application → applies buff from param5
- **Buff 30009**: Watches for buff 1, triggers after 1 application
- **Buff 51566**: Watches for buff 51561, triggers after 10 applications

**Significance:** This enables **buff chain combos** — one buff's application triggers another. Combined with STATE_TRIGER and parse_skill mechanics, this allows multi-stage combo chains that are invisible to the player.

---

## 5. BuffCurrentHp: HP Percentage Illusion

**Code:** Lines 193455-193502 (`BuffCurrentHp.ts`)

Creates a **fake HP percentage** for buff trigger calculations.

```javascript
getFixHp() {
    var maxHp = owner.data.getAttrib(hp);
    var currentHp = owner.data.currenHp;
    var hpPercent = round(currentHp / maxHp * 10000);

    switch (operator) {
        case 0: triggered = (hpPercent > checkNum); break;  // HP% > X
        case 1: triggered = (hpPercent < checkNum); break;  // HP% < X
    }

    return triggered ? round(lookNum / 10000) : round(hpPercent / 10000);
}
```

**What this does:** When HP is above/below a threshold, the system reports a **different HP percentage** to HpChangeTrigger calculations. This can:
- Make HP-loss scaling effects (like Sage's ATK+3% per 10% HP lost) activate earlier
- Make HP-threshold buffs trigger at different HP values than expected
- Create "phantom HP" scenarios where the character appears healthier/weaker than reality

**Interaction with HpChangeTrigger (line 194267-194275):** When operator < 10, HpChangeTrigger uses `getFixHp()` instead of actual HP%, meaning all HP-based trigger calculations are using the illusion value.

---

## 6. Speed Attribute Cascading

**Code:** Line 192412 (`BuffAttrib.ts`)

When the speed attribute (1009) changes, **ALL ATTRIB_CONDITION buffs re-evaluate:**

```javascript
if (this._id == r.speed) {
    for (var i, a = this.owner.buffCtr.getBuffByType(n.ATTRIB_CONDITION); ...) {
        i.value.updateAttrib()
    }
}
```

This is unique to the speed attribute — no other attribute triggers this cascade. The motorcycle mount's speed stacking (50 stacks) causes **50 re-evaluations** of all conditional attribute buffs.

**Exploit:** If a build has ATTRIB_CONDITION buffs with HP-threshold conditions, each speed stack could potentially trigger/untrigger these conditions, causing stat fluctuations. In practice, this mainly matters for builds that combine motorcycle mount with HP-scaling passive effects.

---

## 7. Double Hit Trigger: Hidden Combo Counter

**Code:** Lines 429942-429947 (SkillHandleNormal.ts)
**Buff Group Type:** 170 (DOUBLE_TRIGGER)

A separate trigger system that fires when combo/double hits occur, independent of the STATE_TRIGER system:

```javascript
var N = r.cast.buffCtr.getBuffByType(c.DOUBLE_TRIGGER);
if (N.length > 0)
    for (var L, M = a(N); !(L = M()).done;) {
        L.value.onStateTrigger(o.Double_Act, t)
    }
```

**Key difference from STATE_TRIGER:** DOUBLE_TRIGGER is called **inside the double hit damage calculation**, meaning it has access to the target unit and fires before damage modifiers are applied. STATE_TRIGER for Double_Act fires in `healthTarget`, after damage.

**Active buffs:**
- Buff 30003 (param1=3, param5=[51141]): After every 3 double hits → applies buff 51141
- Buff 51008 (param1=3, param5=[51009]): After every 3 double hits → applies buff 51009

These are used by mount skins (like Koi Paper Kite for Plume Monarch) to trigger AoE effects after every N combos.

---

## 8. PvP Evasion: The Real Formula

The evasion (miss) system uses a **power curve with diminishing returns**, capped in PvP:

```javascript
// Line 322896-322917 (checkHit)
raw_evasion = max(miss - hit, 0)                    // Flat subtraction
corrected = (100 × raw_evasion)^(miss_correct/10000) / 100  // Power curve
pvp_evasion = min(corrected, battle_up_limit)        // PvP cap

// Constants:
miss_correct = 9000 → exponent = 0.9
battle_up_limit = [[1008, 8000]] → cap = 0.8 (80%)
```

**Effective evasion by raw value (PvP):**

| Raw Evasion (miss - hit) | After ^0.9 correction | PvP Capped |
|--------------------------|----------------------|------------|
| 0.10 (10%) | 7.9% | 7.9% |
| 0.20 (20%) | 14.9% | 14.9% |
| 0.30 (30%) | 21.3% | 21.3% |
| 0.40 (40%) | 27.4% | 27.4% |
| 0.50 (50%) | 33.1% | 33.1% |
| 0.60 (60%) | 38.6% | 38.6% |
| 0.70 (70%) | 43.9% | 43.9% |
| 0.80 (80%) | 49.0% | 49.0% |
| 1.00 (100%) | 58.5% | 58.5% |
| 1.50 (150%) | 77.6% | 77.6% |
| 1.60 (160%) | 80.8% | **80.0% (capped)** |

**Key Insight:** To hit the 80% PvP evasion cap, you need **~160% raw evasion** (miss stat 160% higher than enemy hit stat). The motorcycle mount's base +30% evasion alone gives ~21.3% effective evasion — significant but far from cap. Stacking additional evasion from gear pushes toward cap.

**In PvE:** No cap. With 150%+ raw evasion, you dodge >77% of attacks, making PvE content trivially easy.

---

## 9. Healing Decay vs Shield Decay: The Asymmetry

**Healing (treatDecay):** `hp_recovery_correct = 3000 → 0.3` (30% effective)
**Shields (shieldDecay):** `shield_correct = 4000 → 0.4` (40% effective)

But DEFER_DAMAGE (damage absorption) has **no decay modifier** — it absorbs raw damage at full value.

**Exploit:** If a buff uses DEFER_DAMAGE with releaseRatio=0 (like buff 50019), it provides damage absorption that is **more efficient than both shields and healing** in PvP because it bypasses decay.

---

## 10. Summary: Previously Undocumented Mechanics

| Mechanic | Impact | Affected Classes |
|----------|--------|-----------------|
| 0.98 skill crit exponent | 5-13% hidden damage reduction on skill crits | Darklord most affected |
| DEFER_DAMAGE no decay | Full damage absorption, no PvP penalty | Any build with buff 50019 |
| Speed cascade re-eval | ATTRIB_CONDITION recalculation on speed change | Motorcycle mount builds |
| BuffCurrentHp illusion | Fake HP% for trigger calculations | HP-scaling builds |
| TotalDamageTrigger | One-time buff at cumulative damage threshold | Specific artifact/mount skins |
| AddBuffTrigger chains | Multi-stage buff combos | Advanced builds |
| PvE evasion uncapped | >77% dodge rate possible | Evasion builds in PvE |
