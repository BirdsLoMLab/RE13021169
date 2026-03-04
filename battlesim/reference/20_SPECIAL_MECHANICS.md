# 20 — Special Mechanics

> 0.98 exponent, clones, speed cascade, DEFER_DAMAGE exploit, and other hidden mechanics.

---

## 1. The 0.98 Skill Crit Exponent

When a **bleed or skill** crits, damage is raised to the power of 0.98 AFTER the crit multiplier:

```javascript
damage = roundInt(damage * round(1 + skill_crit_dam));
damage = roundInt(Math.pow(damage, 0.98));  // HIDDEN DAMPENING
```

### Impact by Damage Level

| Raw Crit Damage | After ^0.98 | Reduction |
|-----------------|-------------|-----------|
| 1,000 | 986 | -1.4% |
| 10,000 | 9,772 | -2.3% |
| 100,000 | 95,499 | -4.5% |
| 1,000,000 | 912,011 | -8.8% |
| 10,000,000 | 8,709,636 | -12.9% |

**Progressive tax** — scales with damage value. At endgame millions, this is 10-13% hidden reduction.

**Only applies to:** Skill effect damage and bleed damage that crits.
**NOT applied to:** Normal attack crits, combo crits, counter crits.

### Class Impact
- **Darklord** — Most affected (heavy skill crit reliance: +150% Skill Crit DMG)
- **Sacred Hunter** — Barely affected (relies on normal ATK crits)
- **Prophet** — Mildly affected (skill-focused but lower raw damage)

---

## 2. DEFER_DAMAGE: No-Decay Damage Absorption

Buff 50019 uses DEFER_DAMAGE with `releaseRatio=0`, meaning deferred damage is **never released** — pure absorption that disappears on expiry.

```
Pipeline position: After Total DMG Bonus/RES, before final HP reduction
No shieldDecay applied → absorbs at FULL value in PvP
```

**Exploit:** More efficient than both shields (40% effective) and healing (30% effective) in PvP because it bypasses decay entirely.

---

## 3. Speed Attribute Cascade

When speed (1009) changes, **ALL ATTRIB_CONDITION buffs re-evaluate:**

```javascript
if (this._id == speed) {
    for (buff of getBuffByType(ATTRIB_CONDITION)) {
        buff.updateAttrib()
    }
}
```

Unique to speed — no other attribute triggers this. The motorcycle mount's speed stacking (50 stacks) causes 50 re-evaluations of all conditional buffs.

**Impact:** Builds combining motorcycle mount speed stacking with HP-threshold ATTRIB_CONDITION buffs may experience stat fluctuations from cascade re-evaluation.

---

## 4. BuffCurrentHp: HP Percentage Illusion

Creates a **fake HP percentage** for trigger calculations:

```javascript
switch (operator) {
    case 0: triggered = (hpPercent > checkNum); break;
    case 1: triggered = (hpPercent < checkNum); break;
}
return triggered ? round(lookNum / 10000) : round(hpPercent / 10000);
```

**Effect:** When HP is above/below threshold, reports a DIFFERENT HP% to HpChangeTrigger:
- Can make HP-loss scaling effects activate earlier
- Creates "phantom HP" scenarios

---

## 5. TotalDamageTrigger: One-Shot Buff

Tracks **cumulative damage dealt** and triggers at threshold:

```javascript
if (calType == 0) {
    if (totalDmg < threshold) return;         // Absolute threshold
} else if (calType == 1) {
    if (totalDmg / maxHp < threshold / 10000) return;  // HP% threshold
}
// Apply buffs (one-time)
this.hasTrigger = true;
```

Buff 51015: calType=1, threshold=5 (50% HP in damage), applies buff 10001.

---

## 6. AddBuffTrigger: Chain Reactions

Watches for specific buff ID and triggers after N applications:

```javascript
if (buffId == triggerBuffId) {
    currentTriggerValue++;
    if (currentTriggerValue >= triggerCount) {
        currentTriggerValue = 0;
        addBuffs(addBuffList);
    }
}
```

Active:
- **Buff 30006:** Watch buff 10012, trigger after 1 → apply param5
- **Buff 30009:** Watch buff 1, trigger after 1
- **Buff 51566:** Watch buff 51561, trigger after 10

Enables multi-stage buff combos invisible to the player.

---

## 7. Double Hit Trigger: Hidden Combo Counter

Separate from STATE_TRIGER. Fires **inside** combo damage calculation:

```javascript
var N = cast.buffCtr.getBuffByType(DOUBLE_TRIGGER);
for (buff of N) { buff.onStateTrigger(Double_Act, target) }
```

Active:
- **Buff 30003:** Every 3 double hits → buff 51141
- **Buff 51008:** Every 3 double hits → buff 51009

Used by mount skins (Koi Paper Kite) for AoE effects after N combos.

---

## 8. PvP Evasion: Power Curve Formula

```
raw_evasion = max(miss - hit, 0)
corrected = (100 * raw_evasion)^(miss_correct/10000) / 100
pvp_evasion = min(corrected, battle_up_limit)

miss_correct = 9000 → exponent 0.9
battle_up_limit = 0.8 (80%)
```

| Raw Evasion | Effective | PvP Capped |
|-------------|-----------|------------|
| 10% | 7.9% | 7.9% |
| 30% | 21.3% | 21.3% |
| 50% | 33.1% | 33.1% |
| 80% | 49.0% | 49.0% |
| 100% | 58.5% | 58.5% |
| 160%+ | 80%+ | **80% cap** |

Need ~160% raw evasion to hit 80% PvP cap. In PvE: no cap, 150%+ → >77% dodge.

---

## 9. Healing vs Shield vs DEFER Asymmetry

| Mechanism | PvP Decay | Effective |
|-----------|-----------|-----------|
| Healing (treatDecay) | 0.30 | 30% |
| Shields (shieldDecay) | 0.40 | 40% |
| DEFER_DAMAGE | **None** | **100%** |

DEFER_DAMAGE is the most efficient damage mitigation in PvP.

---

## 10. Frozen Break Conditions

Unlike regular stun (dizz), frozen has configurable breaks:

```javascript
switch (triggerType) {
    case 0: // No break — full duration
    case 1: // HP threshold — breaks below X%
    case 2: // Damage threshold — breaks at X% HP in cumulative damage
}
```

On break, can apply **second buff set** from `_buffList[1]` — the "shatter" mechanic.

---

## 11. Clone/Copy System

BuffCopyUnit creates copies of units in battle. BuffCopyIgnore prevents being copied. BuffIgnoreCopy prevents copying specific buffs.

---

## 12. Skill Return (Reflection)

SKILL_RETURN (group 340) checks before damage calculation. If active, skill damage is reflected back to caster — interrupts the entire damage pipeline.

---

## Summary: Hidden Mechanics Impact

| Mechanic | Impact | Most Affected |
|----------|--------|--------------|
| 0.98 skill crit | 5-13% hidden skill crit reduction | Darklord |
| DEFER_DAMAGE no decay | Full absorption in PvP | Any build with buff 50019 |
| Speed cascade | ATTRIB_CONDITION recalc | Motorcycle mount builds |
| HP% illusion | Fake HP for triggers | HP-scaling builds |
| Evasion uncapped PvE | >77% dodge rate | Evasion builds in PvE |
| Chain reactions | Invisible multi-stage combos | Advanced builds |
