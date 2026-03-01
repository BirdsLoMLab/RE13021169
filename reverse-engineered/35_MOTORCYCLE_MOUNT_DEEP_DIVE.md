# 35 — Mount 404 "Life and Death Speed" (Motorcycle) Deep Dive

> **Sources:** game_script_pretty.js lines 192380-196220, 322896-322965, 429258-430116; data/tables/Mount_skin.json, Buff.json, Skill.json, Skill_level.json, Skilleffcet.json
> **Key Discovery:** Evasion/speed snowball mechanic with a 3-phase combat cycle — the most complex mount skin skill in the game

---

## 1. Mount Identity

| Field | Value |
|-------|-------|
| Mount ID | 404 |
| Internal Name | `MX_zq_shengsishisu` ("Life-Death Speed") |
| Quality | 9 (Legendary) |
| Release Date | 2025-06-20 |
| Skin Skill | 5057 (levels 1-3 via skin upgrade) |
| Base Speed | 350 |
| Skin Attribute | 2004 (ATK Speed base) — +1000 to +2500 by skin level |

---

## 2. Passive Evasion Bonus (ownEffect)

Skill 5057 provides a flat evasion bonus that scales with skin level:

| Skin Level | Skill Level | Evasion Bonus (attr 1008) |
|------------|-------------|--------------------------|
| 1-4 | 1 | +20% (2000/10000) |
| 5-9 | 2 | +25% (2500/10000) |
| 10 | 3 | +30% (3000/10000) |

This is a **permanent passive** — always active while the mount skin is equipped.

---

## 3. The Three-Phase Combat Cycle

### Phase 1: Acceleration (Speed Stacking)

**Skill 50571** (parsed via buff 50608 from skill 5057) sets up 5 parallel `STATE_TRIGER` buffs plus a `SpeedTrigger` on the owner:

| Buff ID | Trigger | Count | Effect per Trigger |
|---------|---------|-------|--------------------|
| 50610 | **Miss (Evade)** | Every 1 | +8% movement speed stack |
| 50611 | Normal Attack | Every 8 | +8% movement speed stack |
| 50612 | Double Hit (Combo) | Every 8 | +8% movement speed stack |
| 50613 | Counter Attack | Every 8 | +8% movement speed stack |
| 50614 | Skill Effect | Every 2 | +8% movement speed stack |

**Speed Stack (Buff 50609):**
- Attribute: 1009 (speed/movement)
- Mode: Multiplicative (`addMultiples`, param2=2)
- Value per stack: `skillCoefficient = 23719 ^ 24455 = 800 → 0.08` = **+8% of base speed**
- Mutex: 3 (Stack with Max)
- **Max stacks: 50**
- Bind: 1 (bound to caster)

**Speed Trigger (Buff 50615):**
- Type: SpeedTrigger (`BuffSpeedTrigger.ts`)
- Operator: 3 (≥)
- Threshold: 20000/10000 = **200% of base speed**
- When speed ≥ 200% → fires buff 50617 (parse_skill → Skill 50572)

**Math:**
- Each stack adds +8% speed multiplicatively
- 200% threshold = need `_time ≥ 2.0` (since base `_time = 1.0`)
- Need 1.0 of additional multiples = `1.0 / 0.08 = 12.5` → **13 stacks minimum to trigger**
- Maximum 50 stacks → speed = base × (1 + 50×0.08) = base × **5.0x** (500%)

**Stacking Speed by Source (assuming all active):**
- Miss stacks: 1 per evade (fastest if enemy has high ATK speed)
- Normal attack: 1 per 8 normals
- Combo: 1 per 8 combo procs
- Counter: 1 per 8 counter procs
- Skill: 1 per 2 skill uses

**Critical: The Miss-Trigger Feedback Loop**
Each miss gives +speed, but speed doesn't directly give +evasion. However, the base +30% evasion from ownEffect means misses happen regularly, which means speed stacks build quickly. The snowball comes from being alive longer (more attacks = more stacks) rather than evasion breeding more evasion.

### Phase 2: Overdrive (Speed ≥ 200%)

When the SpeedTrigger fires, it chains through:

**Step 1: Buff 50616 (Clear)** — Removes ALL Phase 1 triggers (50610-50615), stopping further stacking.

**Step 2: Buff 50618 (DMG RES)** — Adds flat DMG RES (attribute 1021):
| Level | Value |
|-------|-------|
| 1 | +9% |
| 2 | +12% |
| 3 | +15% |
Duration: 5 seconds.

**Step 3: Buff 50619 (Parse Skill 50573)** — Fires the overdrive skill after 5s base CD.

**Skill 50573 Overdrive Buffs (all 5s duration at L3):**

| Buff ID | Effect | L1 | L2 | L3 |
|---------|--------|-----|-----|-----|
| 50621 | Trap AoE (effect 754) | 12% | 15% | 18% |
| 50622 | DMG RES +X% (attr 1021) | 12% | 15% | 18% |
| 50623 | **ATK ×(1+X)** (attr 1001, multiplicative) | 12% | 16% | **20%** |
| 50624 | **DEF ×(1+X)** (attr 1024, multiplicative) | 12% | 16% | **20%** |
| 50625 | **ATK Speed ×(1+X)** (attr 1003, multiplicative) | 12% | 16% | **20%** |
| 50626 | **Power Recovery ×(1+X)** (attr 1013, multiplicative) | 12% | 16% | **20%** |
| 50627 | Trap AoE 2 (effect 755) | 32% | 40% | 48% |
| 50631 | **CC Immunity** (`not_controll`) | 5s | 5s | 5s |
| 50632 | Clear buff group 3 | — | — | — |

### Phase 3: Reset

**Buff 50629** (applied during overdrive, 5s base CD): Re-parses Skill 50571, restarting Phase 1. The cycle repeats indefinitely.

**Buff 50630** (applied during Phase 1 initialization, type=0 instant): Clears existing buff 50609 stacks from the previous cycle.

---

## 4. Complete Timeline

```
t=0     Phase 1 starts: 5 triggers active, 0 stacks
        +30% base evasion always active

t=???   13 stacks accumulated → speed ≥ 200%
        SpeedTrigger fires
        Phase 1 triggers cleared

t=???+0 DMG RES buff applied (5s)
        Phase 2 parse_skill queued (5s base CD)

t=???+5 Overdrive skill fires:
        - AoE damage burst
        - +20% ATK/DEF/ATK Speed/Power Recovery (multiplicative, 5s)
        - +18% DMG RES (5s)
        - CC Immunity (5s)
        - Phase 1 restart queued (5s base CD)

t=???+10 Phase 3: Old stacks cleared, Phase 1 restarts
         Cycle repeats
```

---

## 5. Sacred Hunter Synergy Analysis

**Why Motorcycle is S-tier on Sacred Hunter:**

| Sacred Hunter Trait | Motorcycle Synergy |
|----|-----|
| ATK Speed +15% (passive 2007) | More normal attacks per second → faster 8-attack stacking |
| Combo Rate +30% (passive 2003) | Combo procs feed 8-combo stacking |
| +30% base evasion (motorcycle) | Sacred Hunter's hit pattern (many fast attacks) makes opponents miss more |
| pause_cd (active skill) | While enemy skills are locked, you stack freely for 4s |
| 1% target current HP (passive 2126) | During overdrive's +20% ATK SPD, more hits = more HP% procs |
| Post-crit ATK +40% for 1s (passive 2031) | Overdrive's ATK multiplier stacks with post-crit bonus |

**Build Path:**
1. Open with basics to build stacks (ATK Speed + Combo feed two triggers simultaneously)
2. Use Piercing Boneforge to pause_cd when available
3. Hit overdrive threshold → CC immunity prevents interruption
4. During 5s overdrive: massive ATK burst + AoE + CC immunity
5. Cycle restarts — opponent must deal with another stacking phase

**Evasion Math (PvP):**
- Base evasion: 30% (motorcycle ownEffect at L3)
- Enemy hit stat: varies, but assume negligible Ignore Evasion
- Raw evasion formula: `(100 × 0.30)^0.9 / 100 = 30^0.9 / 100 = 24.35 / 100 = 0.2435`
- PvP cap: 80% (but 24% effective is already powerful)
- With additional evasion from equipment/gear: approaches cap quickly
- Every evade = immediate speed stack → faster overdrive

---

## 6. Martial Sage Synergy Analysis

**Why Motorcycle is S-tier on Sage:**

| Sage Trait | Motorcycle Synergy |
|----|----|
| Counter Rate +30% (passive 2001) | Every 8 counters = +speed stack; Sage gets hit and survives |
| DEF +30% (passive 2005) | Survives long enough to reach 13+ stacks |
| DMG RES +15% (passive 2008) | Stacks with overdrive's +18% DMG RES = 33% total |
| Regen 8% HP/5s (passive 2033) | Heals through stacking phase |
| Shield 8% HP/10s (passive 2022) | Additional survivability during stacking |
| Counter DMG +30% multiplier | Counters deal real damage while stacking |

**Build Path:**
1. Tank incoming attacks (shield + DEF + DMG RES)
2. Counters fire automatically (30% rate) → feed counter stacking trigger
3. Normal attacks between counters feed normal stacking trigger
4. Regen keeps HP topped off
5. Hit overdrive → CC immunity = regen continues uninterrupted
6. Overdrive's +20% DEF multiplicative makes Sage nearly unkillable for 5s
7. AoE burst during overdrive is Sage's main damage window

**Key Insight:** Sage doesn't need evasion to synergize — the motorcycle's speed stacking feeds off **all combat actions**, and Sage's survivability ensures the stacking phase completes. The overdrive's CC immunity + DEF boost + Sage's existing tankiness creates a brief window of near-invulnerability.

---

## 7. Hidden Interaction: Speed Attribute and BuffAttribCondition

At line 192412, BuffAttrib has special handling for attribute 1009 (speed):
```javascript
if (this._id == r.speed) {
    for (var i, a = this.owner.buffCtr.getBuffByType(n.ATTRIB_CONDITION), s = e(a); !(i = s()).done;) {
        i.value.updateAttrib()
    }
}
```

When speed changes, **ALL ATTRIB_CONDITION buffs re-evaluate**. This means any HP-conditional or stat-conditional buffs will re-check their conditions every time a speed stack is applied. If a build has ATTRIB_CONDITION buffs (like Sage's HP-scaling ATK buff 20028), they will re-trigger on every speed stack addition.

---

## 8. Counter-Play Analysis

**How to beat Motorcycle builds:**

| Counter | Why |
|---------|-----|
| Ignore Evasion stacking | Plume Monarch's active gives +100% Ignore Evasion for 10s — negates the 30% base evasion |
| Burst before 13 stacks | Darklord's true damage + skill rotation can kill before overdrive |
| Control chaining | Stun/suspend during Phase 1 delays stacking (but pause_cd counters this for Sacred Hunter) |
| High ATK Speed mirror | If both sides have motorcycle, the faster stacker wins |
| Ignore Counter builds | Against Sage, reducing counter rate removes a major stacking source |

**What DOESN'T work:**
- CC during Overdrive (CC Immunity active)
- Shield-breaking (overdrive buffs aren't shields — they're attribute modifiers)
- Waiting it out (cycle restarts indefinitely)

---

## 9. Data Reference

### Config Chain
```
Mount_skin (mount_id=404, skin_level≥1)
  → skin_skill: [5057, level]
    → Skill 5057 (passive, type=3)
      → ownEffect: [[1008, evasion_value]]   ← Base evasion
      → buffGroup: [50608]
        → Buff 50608 (parse_skill)
          → Skill 50571 (skillEffect1: [50571])
            → SkillEffect 50571 (buffGroup: 50610-50614, 50630)
              → Phase 1 triggers installed

Phase 2 chain:
  Buff 50615 (SpeedTrigger, ≥200%)
    → Buff 50617 (parse_skill → Skill 50572)
      → Skill 50572 (skillEffect1: [50572])
        → SkillEffect 50572 (buffGroup: 50616, 50619, 50618)
          → Clear Phase 1 + DMG RES + parse_skill 50573
            → Overdrive buffs (50621-50632)
              → Buff 50629 (parse_skill → Skill 50571) ← CYCLE RESTART
```

### XOR Decoded Coefficients (CONFIG_KEY = 24455)

| Skill | Level | Raw | Decoded | Meaning |
|-------|-------|-----|---------|---------|
| 50571 | 1-3 | 23719 | 0.08 | +8% speed per stack |
| 50572 | 1 | 23555 | 0.09 | Phase 2 DMG RES |
| 50572 | 2 | 23351 | 0.12 | Phase 2 DMG RES |
| 50572 | 3 | 23131 | 0.15 | Phase 2 DMG RES |
| 50573 | 3-1 | 22671 | 0.18 | Overdrive AoE + DMG RES |
| 50573 | 3-2 | 22615 | 0.20 | Overdrive ATK/DEF/SPD/Power |
| 50573 | 3-3 | 19783 | 0.48 | Overdrive AoE 2 + CC immunity |
