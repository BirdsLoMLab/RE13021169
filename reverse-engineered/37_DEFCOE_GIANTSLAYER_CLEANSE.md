# 37 — def_coe, Giant Slayer, and Buff Cleansability Reference

> **Sources:** game_script_pretty.js lines 192345-192373 (NORMAL_ACT_NUM_TRIGGER), 194132-194175 (BuffGiantSlayer), 322756-322885 (HurtUtil damage formulas), 193216-193453 (BuffClear/BuffCtr), 194018-194117 (BuffFrozen), 431489-431541 (SkillRunner.addBuff); data/tables/Buff.json (2,476 entries)

---

## Part 1: def_coe (Attribute 1060) — Defense Coefficient

### What It Does

`def_coe` is a **DEF amplification multiplier** that makes the DEF stat more effective at reducing incoming damage. It appears in every physical damage formula.

### The Core Formula

Every physical damage type uses this pattern:

```javascript
damage = max(roundInt(ATK - DEF × (1 + def_coe)), 1)
```

Without def_coe (def_coe = 0):
```
effective_DEF = DEF × 1.0 = DEF
```

With def_coe = 0.5 (50%):
```
effective_DEF = DEF × 1.5
```

### Every Formula That Uses def_coe

| Function | Line | Formula | Context |
|----------|------|---------|---------|
| `normalHurt` | 322770 | `max(roundInt(ATK - DEF × (1 + def_coe)), 1) × att_dam × (1 - att_resist)` | Normal attacks |
| `normalDoubleHurt` | 322858 | `max(roundInt(ATK - DEF × (1 + def_coe)), 1) × double_hit_dam × (1 - combo_resist)` | Combo hits |
| `normalCounterHurt` | 322873 | `max(roundInt(ATK - DEF × (1 + def_coe)), 1) × counter_dam × (1 - counter_resist)` | Counter attacks |
| `BuffBleed (calType 1)` | 192764 | `max(roundInt(ATK - DEF × (1 + def_coe)), 1)` | ATK-DEF bleed type |
| `BuffBleed (calType 3)` | 192802 | `max(roundInt(roundInt(ATK - DEF × (1 + def_coe)) × combo_dam), 1)` | Combo bleed type |
| `BuffBleed (calType 4)` | 192813 | `max(roundInt(roundInt(ATK - DEF × (1 + def_coe)) × counter_dam), 1)` | Counter bleed type |
| `BuffSkillValue (calType 1)` | 195746 | `max(roundInt(ATK - DEF × (1 + def_coe)), 1)` | Skill ATK-DEF damage |
| `BuffSkillHpHurt` | 195510 | `max(roundInt(ATK - DEF × (1 + def_coe)), 1)` | HP-based skill damage |
| `NORMAL_ACT_NUM_TRIGGER (calType 1)` | 192357 | `max(roundInt(ATK - DEF × (1 + def_coe)), 1)` | N-attack trigger bonus |
| `BuffShield (calType 1)` | 195191 | `max(roundInt(ATK - DEF × (1 + def_coe)), 1)` | ATK-DEF based shield |

### Default Value

From `initial_attr`: `[1060, 0]` — **def_coe starts at 0 for all units**.

### Who Gets def_coe

The only sources of def_coe come from:
- Equipment set bonuses
- Artifact effects
- Specific buff effects (attrib buffs targeting attribute 1060)

There are **no class passives** that grant def_coe. It's an equipment/artifact-exclusive stat.

### Strategic Value

- `def_coe = 0.3` → DEF is 30% more effective → you survive 30% more raw ATK damage
- Stacks additively with itself (multiple sources add together)
- Particularly powerful against high-ATK low-hit-count attackers (burst damage)
- Useless if `ATK > DEF × (1 + def_coe)` by a huge margin (floor of 1 applies)
- **Works on ALL physical damage** — normals, combos, counters, bleeds, skills

---

## Part 2: Giant Slayer (BuffGroupType 390)

### What It Does

Giant Slayer provides **bonus damage scaling based on HP difference** between attacker and target. The MORE HP the target has compared to the attacker, the MORE bonus damage.

### The Formula

```javascript
// Line 194158-194164 (BuffGiantSlayer.ts)
onCalHpDamage(target, baseDamage) {
    attackerHP = owner.getAttrib(hp);      // Attacker's max HP
    targetHP   = target.getAttrib(hp);      // Target's max HP

    if (targetHP <= attackerHP) return baseDamage;  // No bonus if attacker has more HP

    hpRatio = ceil(round((targetHP - attackerHP) / attackerHP * 100));
    extraDam = round(hpRatio * _extraDam);

    // Cap based on unit type
    if (unitType == 1 || unitType == 12)     // Normal unit or specific type
        extraDam = min(extraDam, _maxforUnit);
    else
        extraDam = min(extraDam, _maxforBoss);

    return round(baseDamage * (1 + extraDam / 10000));
}
```

**Parameters from Buff config:**
- `param1` = `_extraDam` — bonus damage per 1% HP difference
- `param2` = `_maxforBoss` — max bonus cap vs bosses
- `param3` = `_maxforUnit` — max bonus cap vs normal units

### Where Giant Slayer Is Applied in the Pipeline

Giant Slayer is called **after** all base damage calculations but **before** `healthTarget()`:

```
1. Base damage (normalHurt / skillDamage / etc.)
2. NORMAL_ACT_NUM_TRIGGER bonus
3. Boss damage multiplier
4. FRAGILE_EFFECT (vulnerability)
5. EXTRA_DAMAGE
6. ★ GIANT_SLAYER ← Here
7. healthTarget() → Total DMG Bonus/RES → shield → final HP reduction
```

It appears in these attack handlers:

| Handler | Line | Context |
|---------|------|---------|
| SkillHandleNormal.att (basic) | 430010 | Normal attack damage |
| SkillHandleNormal.att (double) | 429958 | Combo hit damage |
| SkillHandleCounter | 429657 | Counter attack damage |
| SkillHandleEffect (skill) | 428609 | Skill effect damage |
| BuffBleed calValue | 192839 | Bleed tick damage |
| BuffSkillValue | 195904, 195938 | Skill value damage |

### Active Giant Slayer Buffs

| Buff ID | _extraDam (per 1% HP diff) | Boss Cap | Unit Cap |
|---------|---------------------------|----------|----------|
| 50090 | 10 | 15000 | 15000 |
| 50105 | 10 | 15000 | 15000 |
| 51405 | 10 | 15000 | 15000 |

All three have identical parameters:
- **10 bonus per 1% HP difference** (so +1000 bonus at 100% HP diff)
- **Capped at 150% bonus** (15000/10000) for both bosses and units

### Example Calculation

Attacker HP: 1,000,000. Target HP: 3,000,000.

```
hpRatio = ceil((3M - 1M) / 1M × 100) = ceil(200) = 200
extraDam = round(200 × 10) = 2000
Cap check: min(2000, 15000) = 2000
Final: baseDamage × (1 + 2000/10000) = baseDamage × 1.20
```

At extreme HP differences (10x), the cap of 150% kicks in.

### Who Benefits Most

- **Sacred Hunter** (low HP glass cannon) vs high-HP bosses/tanks → maximum HP ratio
- **Darklord** (moderate HP) vs World Bosses → still benefits from HP gap
- **Sage** (high HP tank) vs anything → minimal benefit (HP ratio is small or negative)

---

## Part 3: Buff Cleansability — Complete Reference

### Buff System Fundamentals

Every buff has these fields that determine removal behavior:

| Field | Meaning |
|-------|---------|
| `type` | 0 = instant (fire & forget, never tracked), 1 = positive, 2 = negative |
| `group` | BuffGroupType — determines handler class |
| `mutex` | 1=Replace, 2=Unique, 3=Stack, 4=Unique/caster, 5=Refresh/caster |
| `action` | Handler class name (determines behavior) |
| `bind` | 0=unbound, 1=bound to caster, 3=special bind |

### Removal Mechanisms

| Mechanism | Code | What It Does |
|-----------|------|-------------|
| **BuffClear (param1=0)** | `removeBuff(groupType)` | Removes ALL active buffs of a given BuffGroupType |
| **BuffClear (param1=1)** | `stopBuffById(buffId)` | Stops all instances of a specific buff ID |
| **Duration Expiry** | `execBuff()` returns false | Buff timer runs out naturally |
| **DESTROY_WHEN_NORMAL_AFTER** | group 90 | Auto-removed after next normal attack |
| **DESTROY_WHEN_SKILL_AFTER** | group 270 | Auto-removed after next skill use |
| **Mutex Replace** | mutex=1 | Old buff removed when same buff ID reapplied |
| **Stack Overflow** | mutex=3, add_max | Oldest stack removed when max exceeded |
| **notControlled** | `statectr.notControlled > 0` | **Blocks** new CC buff application |
| **invincible** | `statectr.invincible > 0` | **Blocks** new CC buff application |
| **IGNORE_BUFFIDS** | group 330 | **Blocks** specific buff IDs listed in param5 |

### Control Effect (CC) Classification

CC actions blocked by `notControlled` / `invincible`:
```javascript
// Line 431314
var C = ["dizz", "ban_skil", "throw_hit", "bound", "ban_act"];
```

| CC Action | Effect | Count | Buff IDs (examples) |
|-----------|--------|-------|---------------------|
| `dizz` | Stun (full action lock) | 15 | 1, 10012, 50533, 110001, 240017, 240058, 270026, 270040, 270079 |
| `ban_act` | Action ban (movement lock) | 2 | 10011, 210017 |
| `throw_hit` | Knockback/airborne | 3 | 50015, 51018, 51607 |
| `bound` | Root (position lock) | 2 | 10002, 10032 |
| `ban_skil` | Silence (skill lock) | 0 | (no buffs in data — may be applied directly) |
| `frozen` | Freeze (stun variant with break conditions) | 12 | 51230, 51237, 51241, 51348, 51399, 51432 |
| `pause_cd` | Cooldown lock (prevents skill recharge) | 1 | 20042 |

**Note:** `frozen` action calls `statectr.dizz++` internally — it IS a stun, just with conditional break (HP threshold, damage taken, or time).

**Note:** `pause_cd` is classified as CTR group 3, so it IS cleansable by CC cleanse.

### CTR Group 3: Everything Cleansable by CC Cleanse

**90 total buffs** in CTR group 3. All are removed by any "clear CTR" effect.

**CC buffs in group 3:**
| Type | Buffs |
|------|-------|
| Stun (dizz) | 1, 10012, 50533, 110001, 240017, 240058, 270026, 270040, 270079 |
| Ban Act | 10011 |
| Bound (root) | 10002, 10032 |
| Throw Hit | 50015, 51018 |
| Pause CD | 20042 |
| Break Shield | 20044, 51435 |

**Stat debuffs in group 3:**
| Debuff | Buffs |
|--------|-------|
| -ATK (1001) | 10013, 50008, 50432, 51002, 51091, 180055, 180302, 240019, 270029, 270048, 270054 |
| -DMG RES (1021) | 10016, 30008, 50007, 50072, 50433, 59032, 180056, 240020, 240158, 270057, 270266 |
| -ATK Speed (1003) | 10014, 50068, 51099, 240015, 253002 |
| -Movement Speed (1009) | 10003, 10026, 50031 |
| -Combo Resist (1034) | 10007, 50059, 51005, 180390 |
| -Counter Resist (1035) | 10008, 51003 |
| -Skill Resist (1019) | 10055, 20021, 51006 |
| -Partner Resist (1020) | 10045, 270068 |
| -HP Recovery (1012) | 51155, 51423, 230038 |
| -Power Recovery (1013) | 51100, 51424, 180382, 253005 |
| -Life Steal Amount (1054) | 51156, 230039 |
| -Crit DMG (1005) | 180386, 230044 |
| -Skill Crit DMG (1038) | 180387 |
| -ATK Resist (1018) | 29002, 51004, 180389 |
| -Crit Rate conversion (1004) | 10 (attrib_convert) |
| -Combo Rate (1016) | 50034, 51512 |
| -Counter Rate (1017) | 50036, 51514 |
| -Skill Crit Rate (1037) | 51516 |
| -Stun Resist (1031) | 10009 |
| -Crit DEF (1006) | 58002 |

**Misc CTR group 3:**
| Type | Buffs |
|------|-------|
| Trap (AoE zone) | 29001 |
| Skill Effect chains | 20001, 51131, 51132, 51133 |
| AddBuff to target | 180388 |

### CC Cleanse Sources (8 buffs that clear CTR group 3)

| Buff ID | Source | Context |
|---------|--------|---------|
| 10017 | Effect 10301 → Skill 1030 | Active skill CC cleanse |
| 50096 | (Internal reference) | Mount/artifact skin effect |
| 50586 | Effect 50551 → Skill 50551 | Mount skin overdrive |
| 50632 | Effect 50573 → Skill 50573 | **Motorcycle mount (404) overdrive** |
| 50652 | Effect 50601 → Skill 50601 | Mount skin effect |
| 50804 | Effect 50704 → Skill 50704 | Mount skin effect |
| 50428 | (Internal reference) | Mount/artifact skin effect |
| 180370 | Effect 180491 → Skill 18049 | Artifact skin passive |

### NOT Cleansable by CC Cleanse (Different Groups)

These debuffs are NOT in CTR group 3 and survive CC cleanse:

| Category | Group | Action | Buff IDs |
|----------|-------|--------|----------|
| **Frozen (some)** | 145, 151, 271-279 | frozen | 51230, 51237, 51241, 51245, 51249, 51253, 51257, 51261, 51265, 51348, 51399 |
| **Bleed** | 0, 1, 2 | bleed | 71 buffs (50495-series, etc.) |
| **DoT Damage** | 1, 4 | dotdamage | 50013, 50030, 51611 |
| **Fragile (Vulnerability)** | 200 | fragile_effect | 8, 10033 |
| **Reduce Heal** | 440 | reduce_heal | 50815, 50843, 51612, 180352, 300033 |
| **Taunt** | 4 | taunt | 110017, 210041 |
| **Direct Kill** | 1 | direct_kill | 10029, 50078 |
| **Frozen (group 4)** | 4 | frozen | 51432 |
| **Bleed (group 4)** | 4 | bleed | 50513, 50842, 51484, 51485, 51539, + more |
| **Ban Act (group 260)** | 260 | ban_act | 210017 |
| **Dizz (group 260)** | 260 | dizz | (some dizz buffs use group 260 instead of 3) |

### Critical Distinction: Group 260 CC

Some CC buffs use **group 260** instead of group 3. These are NOT removed by standard CC cleanse (which only clears group 3). Group 260 CC appears to be "enhanced" or "uncleansable" CC from specific boss/dungeon sources.

| Buff ID | Action | Group |
|---------|--------|-------|
| 210017 | ban_act | 260 |
| Some dizz buffs | dizz | 260 |
| Some attrib debuffs | attrib | 260 |

### Frozen Break Conditions

Unlike regular stun (dizz), `frozen` has configurable break conditions:

```javascript
// BuffFrozen.ts (line 194083)
switch (triggerType) {
    case 0: // No break — lasts full duration
    case 1: // HP threshold — breaks when HP drops below X%
    case 2: // Damage threshold — breaks when cumulative damage reaches X% of HP at freeze time
}
```

When frozen breaks, it can apply a **second set of buffs** from `_buffList[1]`. This is the "shatter" mechanic — the frozen target thaws and additional effects (often AoE damage or stat boosts) trigger.

### Prevention Mechanisms

| Mechanism | Blocks | Provided By |
|-----------|--------|-------------|
| `notControlled` (12 buffs) | dizz, ban_skil, throw_hit, bound, ban_act | not_controll action buffs (e.g., 50631 from motorcycle overdrive) |
| `invincible` (3 buffs) | Same as notControlled | invincible action buffs |
| `CONTROL_RES` (attr 1042) | Reduces duration of dizz (param1=0) and ban_act | Passive stat |
| `IGNORE_BUFFIDS` (group 330) | Blocks specific buff IDs entirely | Specific equipment/buffs |
| `shield_time_extra` (attr 1050) | Extends shield durations (counters break_shield timing) | Passive stat |

### CONTROL_RES Duration Reduction

```javascript
// Line 431510-431512
if ("dizz" == action && param1 == 0 || "ban_act" == action) {
    CONTROL_RES = target.getAttrib(1042);
    duration = round(duration - round(duration × CONTROL_RES));
}
```

At CONTROL_RES = 0.5 (50%), a 3-second stun becomes 1.5 seconds.
At CONTROL_RES = 1.0 (100%), stun duration = 0 → effectively immune.

**Note:** CONTROL_RES only affects `dizz (param1=0)` and `ban_act`. It does NOT affect:
- `throw_hit` (knockback)
- `bound` (root)
- `frozen` (has its own break mechanics)
- `pause_cd` (cooldown lock)

---

## Summary Tables

### def_coe Quick Reference
| Scenario | def_coe | Effective DEF | Impact |
|----------|---------|---------------|--------|
| No def_coe | 0.0 | DEF × 1.0 | Baseline |
| Low gear | 0.2 | DEF × 1.2 | 20% more effective DEF |
| Mid gear | 0.5 | DEF × 1.5 | 50% more effective DEF |
| High gear | 1.0 | DEF × 2.0 | 100% more effective DEF |

### Giant Slayer Quick Reference
| HP Difference | Bonus (uncapped) | Bonus (capped at 150%) |
|---------------|------------------|------------------------|
| Target has 2× your HP | +10% | +10% |
| Target has 5× your HP | +40% | +40% |
| Target has 10× your HP | +90% | +90% |
| Target has 16× your HP | +150% | **+150% (cap)** |
| Target has 20× your HP | +190% | **+150% (cap)** |

### Cleansability Quick Reference
| Effect Type | Cleansable? | How |
|-------------|-------------|-----|
| Stun (dizz, group 3) | YES | CC cleanse (clear CTR) |
| Root (bound, group 3) | YES | CC cleanse |
| Knockback (throw_hit, group 3) | YES | CC cleanse |
| Ban Act (group 3) | YES | CC cleanse |
| Pause CD (group 3) | YES | CC cleanse |
| Stat debuffs (group 3) | YES | CC cleanse |
| Frozen (group 271-279) | **NO** | Only duration/break condition |
| Frozen (group 4) | **NO** | Only duration |
| Bleed (group 1) | **NO** | Only duration |
| Fragile/Vulnerability (group 200) | **NO** | Only duration |
| Reduce Heal (group 440) | **NO** | Only duration |
| Taunt (group 4) | **NO** | Only duration |
| CC (group 260) | **NO** | Enhanced uncleansable CC |
| Ban Act (group 260) | **NO** | Enhanced uncleansable CC |
