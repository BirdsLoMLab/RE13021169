# Draconic Resonance — Pierce/Block Inversion on Caster's DMG RES

## The Question

> Does the caster's pierce value affect Draconic Resonance damage?

**Answer: Yes — and it's inverted. The caster's own pierce can REDUCE their Draconic Resonance damage.**

This contradicts the general rule that pierce doesn't affect DMG RES (resist, attr 1021). That rule is correct for all normal combat — but BuffSkillHpHurt is a special case where the caster's DMG RES is used offensively, and the code erroneously passes it through `calArmorAndBlock`.

---

## Background: Pierce Does NOT Affect General DMG RES in Normal Combat

The community understanding is correct for standard damage. Here's why:

### calHurt() — Where General DMG RES Is Applied

**Source:** `game_script.js` line 5439 (`HurtUtil.ts`, sourceLine 322831)

```javascript
calHurt(damage, defender, attacker) {
    resist    = defender.getAttrib(resist);       // defender's DMG RES (1021)
    pve_resist = defender.getAttrib(pve_resist);
    pve_dam    = attacker.getAttrib(pve_dam);

    damage = roundInt(damage * round(1 + pve_dam));
    damage = roundInt(roundInt(damage * round(1 - resist)) * round(1 - pve_resist));
    return max(1, damage);
}
```

General DMG RES (`resist`, 1021) is applied directly: `damage × (1 - resist)`. **No `calArmorAndBlock` call. No pierce/block interaction.** This is the final damage reduction layer used by all standard damage types (BuffSkillValue, BuffBleed, etc.).

### calArmorAndBlock() — Only Used on Type-Specific Resistances

Every call to `calArmorAndBlock` in normal combat uses a **type-specific** defensive resistance from the **defender**:

| Call site | Resistance passed | Attribute | Who's resist |
|-----------|------------------|-----------|-------------|
| `normalHurt` (basic attacks) | `att_resist` | 1026 | Defender's |
| `normalDoubleHurt` (combo hits) | `double_hit_def` | 1030 | Defender's |
| `normalCounterHurt` (counters) | `counter_def` | 1032 | Defender's |
| `BuffSkillValue._calResistPar` (skills) | `skill_resist` | 1024 | Defender's |
| `SkillHurt` (skill damage) | `skill_resist` | 1024 | Defender's |

In all these cases:
- The resistance belongs to the **defender** (the unit taking damage)
- Pierce from the **attacker** reduces the defender's resistance → attacker deals more damage
- Block from the **defender** increases their resistance → defender takes less damage
- Everything works as intended

### The Exception: BuffSkillHpHurt

| Call site | Resistance passed | Attribute | Who's resist |
|-----------|------------------|-----------|-------------|
| **BuffSkillHpHurt** (Draconic Resonance) | `resist` | **1021** | **Caster's** (offensive) |

This is the ONLY place where:
1. General DMG RES (1021) is passed through `calArmorAndBlock`
2. The resistance belongs to the **caster**, not the defender
3. The resistance is used **offensively** (higher resist = more damage)

---

## The BuffSkillHpHurt Damage Formula

**Source:** `game_script.js` line 2761 (`BuffSkillHpHurt.ts`, sourceLine 195500)

```javascript
e.onBegin = function() {
    var t = this.owner;                        // t = target (defender, receives damage)
    var i = this.runner.cast;                  // i = caster (attacker, deals damage)

    var n = t.data.getAttrib(u.hp);            // target's MAX HP
    var e = i.data.getAttrib(u.resist);        // CASTER's own DMG RES (attr 1021) — used OFFENSIVELY
    var o = f(t, i, e, u.resist);              // calArmorAndBlock(target, caster, CASTER_RESIST, resist)
    //      ^  ^  ^                              defender=target, attacker=CASTER, resistance=CASTER's resist

    // Two-component damage formula:
    n = a.roundInt(n * this.skillPar)          // Component 1: fixed HP% (unaffected by pierce)
      + a.roundInt(n * this._resistPar * o);   // Component 2: resist-scaled HP% (affected by pierce)

    n = a.roundInt(n * t.battleMain.injuryReduce);   // PvP reduction

    // ... clamping (if _limit defined) ...

    this.runner.healthTarget(t, n, s.Hurt, false, this.config.id);
}
```

### Formula Breakdown

```
damage = roundInt(targetMaxHP × skillPar) + roundInt(targetMaxHP × resistPar × modifiedResist)
damage = roundInt(damage × injuryReduce)
if (limit): damage = clamp(damage, roundInt(refDmg × limit[0]), roundInt(refDmg × limit[1]))
```

| Parameter | Source | Description |
|-----------|--------|-------------|
| `targetMaxHP` | `defender.getAttrib(hp)` | Target's max HP — the base for HP% damage |
| `skillPar` | Skill config | Base HP% multiplier (fixed per skill level) |
| `resistPar` | `round(config.param1 / 10000)` | Resist scaling coefficient |
| `modifiedResist` | `calArmorAndBlock(target, caster, caster_resist, resist)` | Caster's DMG RES after pierce/block |
| `injuryReduce` | `configLevel.pvp_injury_reduce / 10000` | PvP factor (1.0 in PvE) |
| `refDmg` | `roundInt(max(roundInt(ATK - DEF × (1 + DEF_COE)), 1) × att_dam)` | For clamping only |

**Component 1** (`targetMaxHP × skillPar`) is a flat HP% hit. Always the same. Not affected by this bug.

**Component 2** (`targetMaxHP × resistPar × modifiedResist`) scales with the caster's DMG RES. This is where higher caster resist = more damage. And this is where `calArmorAndBlock` creates the inversion.

---

## How the Inversion Works

### Inside calArmorAndBlock for This Call

```javascript
calArmorAndBlock(
    t,          // param 1: "defender" = TARGET    → reads: block, block_rate, ignore_armor_pen
    i,          // param 2: "attacker" = CASTER    → reads: armor_pen, armor_pen_rate, ignore_block
    e,          // param 3: resistance  = CASTER's resist (being used offensively)
    u.resist    // param 4: attrib key for up_limit lookup (resist: 8000 = 80% cap)
)
```

**Source:** `game_script.js` line 5439 (`HurtUtil.ts`, sourceLine 322773)

```javascript
calArmorAndBlock(defender, attacker, resistance, attrib_key) {
    pen       = attacker.armor_penetration;          // CASTER's pierce
    ignore_pen = defender.ignore_armor_penetration;   // TARGET's ignore-pierce
    ignore_blk = attacker.ignore_block;               // CASTER's ignore-block
    block     = defender.block;                        // TARGET's block

    // Build probability ranges
    if (pen > ignore_pen):   pierce_range = roundInt(10000 × attacker.armor_penetration_rate)
    if (block > ignore_blk): block_range  = pierce_range + roundInt(10000 × defender.block_rate)

    // RNG roll 0-10000
    rand = randomInt(0, 10000)

    if (rand <= pierce_range):  // PIERCE: reduce resistance
        resistance = round(resistance - min(0.5, (pen - ignore_pen) / 10000))

    elif (rand <= block_range):  // BLOCK: increase resistance
        resistance = round(resistance + min(0.5, (block - ignore_blk) / 10000))

    // Cap by attribute up_limit
    resistance = min(resistance, up_limit)   // resist up_limit = 0.80

    return resistance
}
```

### The Inversion Table

| Event | In Normal Combat (defensive resist) | In Draconic Resonance (offensive resist) |
|-------|-------|-------|
| **Pierce triggers** | Defender's resist goes DOWN → more damage taken (good for attacker) | Caster's resist goes DOWN → **LESS damage dealt (bad for caster)** |
| **Block triggers** | Defender's resist goes UP → less damage taken (good for defender) | Caster's resist goes UP → **MORE damage dealt (bad for target)** |
| **Neither** | No change | No change |

**Who provides what in this call:**
- **Caster** (attacker slot) provides: `armor_penetration`, `armor_penetration_rate`, `ignore_block`
- **Target** (defender slot) provides: `ignore_armor_penetration`, `block`, `block_rate`

So the **caster's own pierce stats** are what trigger the self-nerf. And the **target's own block stats** are what trigger the backfire.

---

## Quantified Impact

### Example: Caster with 80% DMG RES, High Pierce

**Setup:**
- Caster `resist` = 0.80 (80%, at cap)
- Caster `armor_penetration` = 5000, target `ignore_armor_penetration` = 0
- Pierce amount = `min(0.5, (5000 - 0) / 10000)` = **0.50** (maximum reduction)
- Target maxHP = 50B, resistPar = 0.50, skillPar = 0.05

**No proc (Neither — expected behavior):**
```
damage = roundInt(50B × 0.05) + roundInt(50B × 0.50 × 0.80)
       = 2.5B + 20.0B = 22.5B
```

**Caster's pierce procs (self-nerf):**
```
modifiedResist = round(0.80 - 0.50) = 0.30
damage = roundInt(50B × 0.05) + roundInt(50B × 0.50 × 0.30)
       = 2.5B + 7.5B = 10.0B

Loss: 12.5B → 55.6% of expected damage destroyed
```

**Target's block procs (backfire — helps caster):**
```
modifiedResist = round(0.80 + 0.50) = 1.30 → capped at 0.80 by up_limit
damage = 22.5B (no change — already at cap)
```

Note: If caster resist is below cap (e.g., 50%), target's block WOULD increase the caster's resist toward cap, increasing Draconic Resonance damage. The target's own block helps the attacker.

### Impact by Caster Resist Level

Assumes: resistPar = 0.50, skillPar = 0.05, pierce reduces resist by full 50pp.

| Caster Resist | No Proc (total dmg) | Pierce Procs (total dmg) | Resist Component Loss |
|---------------|---------|-------------|------|
| 80% (cap) | HP × 0.45 | HP × 0.20 | -62.5% of resist component |
| 70% | HP × 0.40 | HP × 0.15 | -71.4% of resist component |
| 60% | HP × 0.35 | HP × 0.10 | -83.3% of resist component |
| 50% | HP × 0.30 | HP × 0.05 | -90.0% of resist component |

The resist-scaled component is devastated. At 50% DMG RES with max pierce, the resist component drops by 90%. Only the fixed `skillPar` component survives untouched.

---

## When Does This Actually Trigger?

This is **RNG-based**, not guaranteed per hit. Requirements for pierce to self-nerf:

1. **Caster's `armor_penetration` (1068) must exceed target's `ignore_armor_penetration` (1069)**
   - Equipment Advancement provides up to **6,240** armor_penetration at stage 36
   - If target has 0 ignore_pen, ANY pierce value enables the proc
   - This condition is met by virtually every endgame character

2. **RNG roll must land in the pierce range**
   - Probability = `roundInt(10000 × caster.armor_penetration_rate)`
   - If armor_pen_rate = 0.50 (50%), there's a 50% chance per hit

3. **The call must be for BuffSkillHpHurt specifically** — no other damage type has this issue

For block to backfire (help the caster):

1. **Target's `block` (1071) must exceed caster's `ignore_block` (1072)**
2. **RNG roll must land in the block range** (checked after pierce range)
3. **Caster's resist must be below 80% cap** — otherwise the increase is capped and wasted

Pierce and block are **mutually exclusive** per hit — only one can trigger.

---

## Full Damage Pipeline for BuffSkillHpHurt

```
1. Read target maxHP and caster's resist (1021)
2. calArmorAndBlock modifies caster's resist via pierce/block  ← BUG: inverted semantics
3. damage = roundInt(maxHP × skillPar) + roundInt(maxHP × resistPar × modifiedResist)
4. damage × injuryReduce (PvP factor)
5. Clamp to [refDmg × limit[0], refDmg × limit[1]]  (if _limit defined)
6. healthTarget() applies total_dam_add / total_dam_def    ← this layer works correctly
7. Final damage dealt
```

Note: The `healthTarget()` call at step 6 applies the Total DMG Bonus/RES system (attrs 1081/1082) as a final multiplier, which is unrelated to this bug and works correctly.

---

## Related: BuffVampire total_dam_def Issue (Discrepancies C6)

A separate but thematically similar issue exists in **BuffVampire** (life steal), documented in `98_DISCREPANCIES.md` section C6:

> BuffVampire reads `this.owner.data.getAttrib(total_dam_def)` where owner is the **target** receiving the buff (which is the caster's own unit for life steal).

**Source:** `data/formulas/buffs/vampire.json`

```javascript
// In BuffVampire.calDamage():
total_dam_add = caster.getAttrib(total_dam_add);   // 1081
total_dam_def = this.owner.getAttrib(total_dam_def); // 1082 — owner = caster (self-referencing)
totalDamMultiplier = max(1 + total_dam_add - total_dam_def, 0.20);  // floor at 20%
```

When the caster has a vampire buff on themselves, `this.owner` is the caster. The caster's own Final DMG RES reduces their own life steal healing. This is the same pattern: a defensive stat penalizing its holder in a context where it shouldn't.

---

## Why This Contradicts Community Understanding

The community correctly states: **"Pierce doesn't affect DMG RES, just type-specific resistances like counter/combo res."**

This is true for **all standard damage paths**:

| Damage type | Resistance | Pierce applies? | How resist is used |
|-------------|-----------|----------------|-------------------|
| Basic attack | `att_resist` (1026) | Yes, via `calArmorAndBlock` | Defender's, defensively |
| Combo hit | `double_hit_def` (1030) | Yes, via `calArmorAndBlock` | Defender's, defensively |
| Counter | `counter_def` (1032) | Yes, via `calArmorAndBlock` | Defender's, defensively |
| Skill damage | `skill_resist` (1024) | Yes, via `calArmorAndBlock` | Defender's, defensively |
| **All of the above** (final layer) | **`resist` (1021)** | **No** — `calHurt()` applies directly | Defender's, defensively |
| **Draconic Resonance HP% dmg** | **`resist` (1021)** | **Yes** — via `calArmorAndBlock` | **Caster's, offensively** |

BuffSkillHpHurt is the sole exception. It passes the caster's `resist` (1021) through `calArmorAndBlock`, which is never done anywhere else in the codebase. The result is that general DMG RES — the one stat the community knows pierce doesn't touch — IS affected by pierce in this one specific case, and in the wrong direction.

---

## Code References

| Component | File | Line | Doc |
|-----------|------|------|-----|
| BuffSkillHpHurt.onBegin | game_script.js | 2761 | data/formulas/buffs/hp_hurt.json |
| calArmorAndBlock | game_script.js | 5439 | data/formulas/combat/cal_armor_and_block.json |
| calHurt (general resist, NO pierce) | game_script.js | 5439 | data/formulas/combat/cal_hurt.json |
| BuffVampire.calDamage | game_script.js | 196745 | data/formulas/buffs/vampire.json |
| healthTarget (total_dam_add/def) | game_script.js | 7229 | reverse-engineered/07_TOTAL_DMG_BONUS_RES.md |
| Pierce/block system | game_script.js | 5439 | reverse-engineered/08_PIERCE_BLOCK_INSPIRE_SUPPRESS.md |
| Resist attr cap (8000/80%) | — | — | reverse-engineered/LOM_MASTER_FORMULA_REFERENCE.md:131 |
| Discrepancy C6 (Vampire) | — | — | reverse-engineered/98_DISCREPANCIES.md:108 |

---

## Summary

1. **The community is right**: Pierce does not affect general DMG RES (`resist`, 1021) in normal combat. `calHurt()` applies it directly without `calArmorAndBlock`.

2. **BuffSkillHpHurt is the sole exception**: It uniquely passes the caster's own `resist` through `calArmorAndBlock`, enabling pierce/block interactions on an attribute that normally never sees them.

3. **The interaction is inverted**: Because `resist` is used offensively here (more caster resist = more damage), pierce reducing it hurts the caster, and block increasing it hurts the target. Both are backwards from player expectations.

4. **This is probabilistic**: Depends on caster's pierce rate and target's block rate. Creates unpredictable damage variance (up to 55-90% loss on the resist component) on a skill that should deal consistent HP%-based damage.

5. **Endgame characters are most affected**: Equipment Advancement gives up to 6,240 pierce — more than enough to enable the proc. The higher your pierce investment, the more likely you self-nerf your own Draconic Resonance.
