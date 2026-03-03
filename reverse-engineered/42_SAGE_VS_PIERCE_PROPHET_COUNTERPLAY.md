# 42 — Counter/Regen Sage vs High-Pierce Prophet: Counterplay Guide

> **Sources:** game_script.js (HurtUtil.ts, SkillHandleNormal.ts, Unit.ts, MetaAttrib.ts), AttribDefine.json, docs 02/06/32/33/34
> **Scope:** All viable mechanics a counter/regen Martial Sage can use against a high-ATK Prophet with high pierce, **excluding** ignore_pierce and block

---

## 0. What Pierce Actually Does (And Doesn't Do)

Pierce is widely misunderstood. It is **not** a "bypass all defense" mechanic — it only modifies one specific layer in a 11-step damage pipeline.

### The damage pipeline (annotated with pierce interaction)

```
Step 1:  BASE DAMAGE = max(ATK - DEF × (1 + DEF_COE), 1)     ← PIERCE DOES NOT TOUCH THIS
Step 2:  × type multiplier (att_dam, skill_dam, etc.)
Step 3:  RESISTANCE CHECK (att_resist / skill_resist / etc.)
Step 4:  PIERCE/BLOCK ROLL (single random roll, mutually exclusive)
           If pierce: resistance -= min(0.5, (pen - ign_pen) / 10000)   ← PIERCE ACTS HERE
           If block:  resistance += min(0.5, (block - ign_block) / 10000)
Step 5:  APPLY RESISTANCE: dmg × (1 - modified_resistance)
Step 6:  DMG RES (calHurt): dmg × (1 - resist)                ← PIERCE DOES NOT TOUCH THIS
Step 7:  CRITICAL multiplier
Step 8:  BUFF MODIFIERS (FRAGILE, EXTRA_DAMAGE, GIANT_SLAYER)
Step 9:  TOTAL DMG BONUS/RES: × max(1 + dam_add - dam_def, 0.20)  ← PIERCE DOES NOT TOUCH THIS
Step 10: PVP DIVISION: ÷ injuryReduce                         ← PIERCE DOES NOT TOUCH THIS
Step 11: SHIELD → BLOCK BUFF → HP REDUCTION                   ← PIERCE DOES NOT TOUCH THIS
```

**Pierce only modifies the type-specific resistance in Step 4.** It does NOT bypass:
- **DEF** (Step 1) — flat defense subtraction
- **General DMG RES / `resist` attr 1021** (Step 6) — separate multiplicative layer
- **`total_dam_def` attr 1082** (Step 9) — final percentage reduction, floor 0.20
- **Shields** (Step 11) — absorb after all calculations
- **Counter** — fires independently, unrelated to pierce

This means there are **four independent defensive layers** the sage can stack that pierce literally cannot interact with.

### Why block fails but other defenses don't

Block and pierce share a **single random roll** inside `calArmorAndBlock`. Pierce occupies the lower range `[0, pierce_rate]` and block occupies `(pierce_rate, pierce_rate + block_rate]`. Since the loop checks index 0 (pierce) first, high pierce directly compresses block's probability window. With "really high pierce," block's effective proc rate approaches zero.

But dodge, DEF, resist, total_dam_def, and shields are all on **completely separate systems** with no roll-sharing.

---

## 1. The Proc Check Order (Critical Discovery)

The exact execution order when the prophet attacks:

```
Step 1: COUNTER CHECK — checkCounterAct(defender, attacker)     ← FIRES FIRST
Step 2: MISS/DODGE CHECK — checkHit(attacker, defender)         ← BEFORE pierce
         If Miss → skip all damage, no pierce roll happens
Step 3: DAMAGE CALC — normalHurt (includes calArmorAndBlock)    ← PIERCE ROLLS HERE
Step 4: BUFF MODIFIERS
Step 5: HP STEAL, KNOCKBACK, STUN
Step 6: DOUBLE HIT CHECK
--- DEFERRED PHASE ---
Step 7: COUNTER EXECUTES (queued from Step 1)
Step 8: SHIELD absorbs → BLOCK BUFF absorbs → HP reduced
```

**Two critical findings:**

1. **Counter is checked BEFORE dodge/miss.** The counter roll happens at Step 1, before `checkHit` at Step 2. This means **counter can proc even when the attack will be dodged.** The sage dodges the damage AND counters back. Both work simultaneously.

2. **Dodge is checked BEFORE pierce.** If dodge procs at Step 2, the entire damage pipeline (Steps 3-8) is skipped. Pierce never fires. The attack deals zero damage.

---

## 2. The Prophet's Threat Model

From `32_CLASS_SKILLS_REFERENCE.md`:

| Element | Detail |
|---------|--------|
| Active skill | **Crane's Whisper (1057):** 15157% AoE + reduce Skill DMG RES 20% for 8s + **shield-breaking on attacks for 10s** |
| Passive: Lv30 | Skill Crit +15% |
| Passive: Lv40 | ATK +12% |
| Passive: Lv50 | Active Skill Energy Regen +20% |
| Passive: Lv70 | Prolong active skills by +40%, boost DMG by +10% |
| Passive: Lv100 | Every stun trigger → all active skill CDs -0.3s |
| Playstyle | Skill-spam. Fast energy → frequent Crane's Whisper → shield-breaking uptime |

**Key prophet weaknesses to exploit:**
- Skill-focused (skills don't trigger counter, but auto-attacks between skills do)
- Shield-breaking is active-dependent (10s window, then shields regenerate)
- No inherent dodge bypass (no ignore_dodge passive)
- No inherent counter bypass (no ignore_counter passive)
- Countered by stun immunity and "fast kill before rotation" per PvP notes

---

## 3. The Strategies (Ranked by Effectiveness)

### Strategy A: Dodge Stacking — "Can't Pierce What You Can't Hit"

**Why it works:** Dodge is resolved at Step 2, before the pierce/block roll at Step 4. If dodge procs, the entire attack misses — zero damage, zero pierce, zero crit.

**The formula:**
```
effective_dodge = max(dodge_rate - hit_rate - ignore_dodge, 0)
```

**Why it's strong against prophet specifically:**
- Prophet passives grant: Skill Crit, ATK, Energy Regen, Skill Duration, CD Reduction
- Prophet passives do **NOT** grant: hit_rate, ignore_dodge
- This means the prophet has no inherent way to counter dodge stacking
- Every point of dodge_rate the sage stacks is at full value (no subtraction)

**Synergy with counter (the hidden combo):**
Since counter check (Step 1) happens BEFORE dodge (Step 2), the sage can:
1. Counter procs → queued for execution
2. Dodge procs → no damage taken
3. Counter executes → deals damage back

**Result: The sage takes zero damage AND deals counter damage.** This is the best possible outcome per incoming attack.

**How to stack dodge:**
- Equipment stats with `miss` (1008) — note: the actual attribute name is `miss`, not `dodge_rate`
- Buff effects (BuffAttribAdd targeting 1008)
- Spirit attributes

**PvP caveats:**
- Dodge has a **PvP cap** (`battle_up_limit`) — you cannot reach 100% dodge in PvP
- The miss formula applies a **power curve correction** (`miss_correct`): `corrected = pow(100 * raw_miss, miss_correct/10000) / 100`. This means diminishing returns at high dodge values.
- The effective dodge formula: `raw = max(miss - hit, 0)`, then corrected, then capped
- Despite the cap, dodge is still extremely strong because it **completely avoids the attack** — no pierce, no crit, no damage
- Pair with other layers (DEF, resist, counter) since dodge is probabilistic

---

### Strategy B: DEF + General DMG RES Layering — "Pierce-Immune Defense Stack"

**Why it works:** The sage already has two pierce-immune defense layers from passives:

| Passive | Effect | Pipeline Step | Pierce Interaction |
|---------|--------|---------------|-------------------|
| 2005 (Lv40) | DEF +30% | Step 1: `ATK - DEF×(1+def_coe)` | **None** — DEF is subtracted before pierce even rolls |
| 2008 (Lv50) | DMG RES +15% | Step 6: `dmg × (1 - resist)` | **None** — separate multiplicative layer |

**Stacking more DEF** reduces the base damage before any multipliers apply. Against a "really high ATK" prophet, DEF acts as a flat subtraction — the higher the prophet's ATK, the more absolute damage DEF removes.

**Stacking more resist (1021)** applies a percentage reduction AFTER pierce has already modified the type-specific resistance. These are multiplicative layers:
```
Step 5 output:  dmg × (1 - type_resist_after_pierce)
Step 6 output:  Step5_dmg × (1 - general_resist)
```

Even if pierce reduces `skill_resist` to 0, the sage still has `(1 - general_resist)` as a standalone multiplier.

**Sources of extra DEF/resist:**
- Equipment substats
- Gem set **Iron Wall (105):** Global Crit RES +500/+1000
- Mount **Blue Ox (5005):** DMG RES +15%
- Mount **Moon Rabbit-1 (5018):** DMG RES +15% + restore 25% lost HP every 10s

---

### Strategy C: `total_dam_def` (1082) — "The Final Wall"

**Why it works:** `total_dam_def` is applied at Step 9, the very end of the damage calculation before PvP division. It reduces ALL 13 damage types including skills, crits, combos, counters, bleeds, true damage, HP% damage, and reflect. Pierce has zero interaction with it.

**The formula:**
```
final_multiplier = max(1 + total_dam_add - total_dam_def, 0.20)
```

**The floor is 0.20×**, meaning you can reduce ALL incoming damage by up to **80%**. This is enormous and cannot be bypassed by pierce.

**How to stack it:**
- Equipment and accessories with total_dam_def
- Buffs that add to attribute 1082
- This stat is universally effective — it doesn't just counter pierce, it counters everything

---

### Strategy D: Shields — "Pierce-Proof Absorption"

**Why it works:** Shields absorb damage at Step 11, after ALL calculations (including pierce). The sage's auto-shield is a **trap buff** (undispellable by normal buff removal).

**Sage's auto-shield (passive 2022):**
- 8% Max HP shield every 10s, lasting 5s
- In PvP: shield decays to 40% → **3.2% Max HP per cycle**
- Trap buff = cannot be dispelled

**The prophet's counter-play:** Crane's Whisper enables shield-breaking on attacks for 10s. During this window, the prophet's attacks destroy shields on contact.

**How to play around it:**
- Shield-breaking is tied to the prophet's active skill (10s duration)
- With +40% duration passive, that's 14s of shield-breaking
- The sage's shield regenerates every 10s
- **During the gap when Crane's Whisper is on cooldown, shields are safe**
- Stack extra shield sources (mount skins) to have shields during the active window too:
  - **Cyclone Bamboo (5013):** Shield +3s duration, +50% effect, Counter +25% while shielded
  - **AdaptoSlime+ (5026):** Below 60% HP → shield 20% HP
  - **Trembling Pepe (5029):** Alternating 8s: shield 16% HP OR ATK +16%

---

### Strategy E: Counter Rate + counter_dam Maximization — "Punish Every Auto"

**Why it works:** Counter fires independently of pierce (it's at Step 1/7, completely outside the pierce system). Every normal attack the prophet lands (or misses!) gives the sage a free reactive strike.

**Sage's counter kit:**
```
Base counter rate:   +30% (passive 2001, attr 1017 +3000)
Base counter_dam:    +30% (passive 2001, attr 1033 +3000)
Active skill debuff: Target's counter_def -40% for 8s (effect 10532)
Active skill bonus:  Each counter deals +1% of target's current HP for 8s (effect 10531)
```

**Counter damage formula:**
```
base = max(ATK - target.DEF × (1 + target.def_coe), 1)
counter_dmg = base × counter_dam × (1 - counter_def_after_armor_check)
if crit: counter_dmg × max(1.5, crit_dam / max(0.5, crit_def))
```

**Key insight — counter can crit.** Stacking `crit_dam` benefits both the sage's normal attacks and counter strikes.

**Mount synergies for counter:**
- **Velocity Blitz (5014):** Every counter → Global Counter DMG +20% for 3s (cap +60%). Three counters in 3s = +60% counter damage.
- **Cyclone Bamboo (5013):** Counter +25% while shielded — stacks with the base +30%.

**Gem set:**
- **Heart of Resilience (101):** Global Counter DMG +500/+1000 — direct counter_dam scaling

**Important limitation: Counter only triggers on NORMAL attacks, not skills.** Since the prophet is a skill-spam class, counter won't proc from Crane's Whisper or other skills. It only procs from the prophet's auto-attacks between skill casts.

**Mitigation:** See Strategy F (Seal) and Strategy G (SKILL_COUNTER).

---

### Strategy F: Seal the Prophet — "Force Normal Attacks"

**Why it works:** This is potentially the single most devastating counter to the prophet's kit. Seal prevents skill usage but allows normal attacks.

**What seal does to the prophet:**
1. **Prevents Crane's Whisper** → no shield-breaking, no Skill DMG RES debuff, no AoE burst
2. **Forces normal attacks only** → every auto triggers the sage's counter
3. **Disables CD reduction passive** → no stun-based cooldown acceleration
4. **Kills energy economy** → +20% energy regen is useless without skills to cast

**What seal does FOR the sage:**
1. Every prophet attack is now a normal attack → counter procs on every hit
2. Shields are protected (no Crane's Whisper to break them)
3. Prophet's damage output drops dramatically (no 15157% skill multiplier)
4. The sage's regen/shield sustain can outpace normal attack damage

**Sources of seal:**
- Specific buff types (BuffSeal)
- Skill effects that apply sealed status
- Mount/artifact procs that apply seal
- Key question: which sage-accessible skills or equipment apply seal? This requires checking available seal sources in ConfigSkillEffect and buff tables.

---

### Strategy G: SKILL_COUNTER Buffs — "React to Skill Damage"

**Why it works:** Normal counter (attr 1017) only triggers on normal attacks. But there's a separate system — `BuffGroupType.SKILL_COUNTER (220)` — that triggers reactive skill casts based on accumulated HP damage or hit counts. This CAN react to skill damage.

From the code (Unit._checkSkillCounter):
```javascript
// Buff group 220 — triggers a counter SKILL when HP damage threshold is reached
// Uses skill.counterDamage as a scaling multiplier
```

**If the sage has access to SKILL_COUNTER buffs**, they can trigger reactive damage against the prophet's Crane's Whisper and other skills. This fills the gap that normal counter can't cover.

---

### Strategy H: ATK Debuffs — "Shrink the Base"

**Why it works:** Pierce modifies resistance (Step 4), but the base damage `ATK - DEF` is calculated at Step 1. Reducing the prophet's ATK directly reduces the number that gets multiplied through all subsequent steps — including the pierce-enhanced multiplier.

**The math:**
```
Without ATK debuff: base = 100000 ATK - 50000 DEF = 50000 → × pierce multiplier
With -20% ATK:      base = 80000 ATK - 50000 DEF = 30000 → × pierce multiplier
```
A 20% ATK reduction creates a 40% reduction in base damage (in this example). The effect is amplified when DEF is high relative to ATK.

**Sources of ATK debuffs:**
- `BuffAttribAdd` with negative value on attribute 1001 (ATK)
- Skill effects that reduce enemy ATK
- Mount/artifact procs that debuff ATK

---

### Strategy I: Speed Advantage — "Setup Before Burst"

**Why it works:** If the sage acts first, they can:
1. Apply Blades Reunion (active skill) → debuff counter_def by 40%, enable 1% HP counter bonus
2. Set up shields before the prophet's first attack
3. Apply control effects (stun, seal) before the prophet can cast Crane's Whisper

**The prophet's dependency on rotation:**
The prophet needs to cast Crane's Whisper to enable shield-breaking. If the sage stuns or seals before this, the prophet's entire combo falls apart. The prophet's CD reduction passive requires stuns to trigger — if the prophet can't cast skills, the passive is dead.

---

### Strategy J: Skill Reflection — "Return Crane's Whisper"

**Clarification:** There is no generic "reflect X% of damage" buff in this game. However, there IS `BuffSkillReturn` (line 2767), which can **interrupt and reflect specific skills back** at the attacker.

```javascript
// BuffSkillReturn checks if incoming skill ID is in a whitelist
// If matched: interrupts the skill AND re-casts it at the original attacker
checkSkillReturn(target, runner) {
    if (this._checkSkillList.includes(runner.useSkill.config.id)) {
        this.owner.addReturnInfo(target, skillId, level);
        runner.interrupt();  // INTERRUPTS the skill entirely
        return true;
    }
}
```

**If the sage can access a BuffSkillReturn configured for Crane's Whisper (skill 1057)**, the prophet's burst skill gets interrupted and reflected back. This would:
1. Cancel the shield-breaking window
2. Cancel the Skill DMG RES debuff
3. Deal the prophet's own 15157% AoE damage back at them

**This is niche** — it requires a buff source that specifically lists skill 1057 in its return whitelist.

**For general sustain, use lifesteal instead:**

```
Prophet attacks sage:
  → Sage takes X damage (after all reductions)
  → Counter deals sage's ATK-based damage to prophet (if normal attack)
  → att_hpsteal (1014) heals sage for % of counter damage dealt
  → skill_hpsteal (1015) heals sage for % of any skill damage dealt
```

**Lifesteal attributes:**
| Attribute | ID | Effect | Defense |
|-----------|-----|--------|---------|
| `att_hpsteal` | 1014 | Steal HP on normal/counter attacks | `att_hpsteal_def` (1027) |
| `skill_hpsteal` | 1015 | Steal HP on skill attacks | `skill_hpsteal_def` (1028) |
| VAMPIRE buff (group 380) | N/A | Buff-based lifesteal on all attacks | `treatDecay` + `REDUCE_HEAL` |

All lifesteal is subject to `treatDecay` (0.3 in PvP = 30% effectiveness) and `REDUCE_HEAL` debuffs.

---

### Strategy K: Crit Defense — "Neuter the Skill Crits"

**Why it works:** The prophet gets +15% Skill Crit Rate (+30% total with two passives stacking) and accesses crit through equipment. Their active adds Skill Crit DMG. The crit formula:

```
crit_multiplier = max(1.5, round(crit_dam / max(0.5, crit_def)))
```

If `crit_def` is high enough, the crit multiplier is clamped to 1.5× (the minimum). This removes the prophet's crit scaling entirely.

**Gem set Iron Wall (105):** Global Crit RES (2011) +500/+1000 — directly increases crit_def.

---

## 4. Recommended Build Priority

Given the sage's passives and the prophet matchup, here's the priority ordering:

### Tier 1: Build-defining (stack these first)

1. **Dodge rate** — completely avoids pierce, works with counter, prophet has no counter-play
2. **Counter rate + counter_dam** — punishes every auto-attack, synergizes with dodge
3. **DEF + general resist (1021)** — pierce-immune layers the sage already has foundations for
4. **total_dam_def (1082)** — universal damage reduction, up to 80%, pierce can't touch it

### Tier 2: Force multipliers

5. **Seal source** — transforms the matchup by disabling the prophet's entire kit
6. **Speed (att_speed)** — act first to set up or control
7. **Shield sources beyond base passive** — pierce-proof absorption, but must play around Crane's Whisper timing
8. **Crit_def** — neuters the prophet's crit scaling

### Tier 3: Sustain optimization

9. **att_hpsteal (1014)** — lifesteal on normal attack AND counter hits (subject to 30% treatDecay in PvP)
10. **VAMPIRE buff (group 380)** — buff-based lifesteal on all attack types
11. **Skill reflection (BuffSkillReturn)** — if accessible for Crane's Whisper (skill 1057), completely shuts down the prophet's burst

### Tier 4: Situational / if accessible

12. **ATK debuffs** — reduce prophet's base damage
13. **SKILL_COUNTER buffs** — react to skill damage (covers counter's normal-attack-only limitation)
14. **Stun/control** — prevent prophet from acting, but prophet's kit is stun-synergistic (CD reduction per stun)

---

## 5. Mount Skin Picks for This Matchup

| Mount | Why |
|-------|-----|
| **Velocity Blitz (5014)** | +20% global counter DMG per counter (cap 60%) = massive counter scaling |
| **Moon Rabbit-1 (5018)** | DMG RES +15% + restore 25% lost HP every 10s = pierce-immune defense + regen |
| **Neon Shadows (5033)** | 3 Guard stacks (DEF +150% each) + on expire: 4000% Skill + 1600% Counter DMG |
| **Cyclone Bamboo (5013)** | Counter +25% while shielded + shield boost (if you can keep shields up) |

---

## 6. Summary: Why This Works

The core insight is that pierce is **much narrower** than most players assume. It only modifies one of four independent defensive layers. Against a counter/regen sage:

```
Prophet's pierce reduces:    type-specific resistance (Step 4)
Sage's dodge avoids:         the entire attack (Step 2, before pierce)
Sage's DEF reduces:          base damage (Step 1, before pierce)
Sage's resist reduces:       post-calculation damage (Step 6, after pierce)
Sage's total_dam_def reduces: final damage (Step 9, after everything)
Sage's shields absorb:       remaining damage (Step 11, after everything)
Sage's counter deals:        reactive damage (independent system)
Sage's regen restores:       HP between attacks (independent system)
```

The prophet's pierce advantage is real but one-dimensional. The sage has access to **five independent defensive layers** (dodge, DEF, resist, total_dam_def, shields) plus **two reactive systems** (counter, regen) that pierce cannot interact with. Stack them correctly and the prophet's pierce advantage becomes a small fraction of the sage's total defensive profile.

**The kill condition:** The prophet runs out of time (2-minute PvP timer) while the sage sustains through counter + regen, or the sage's accumulated counter damage (amplified by Blades Reunion's 1% HP per counter) wears the prophet down.
