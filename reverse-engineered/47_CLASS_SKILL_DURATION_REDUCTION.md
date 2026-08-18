# 47 — Class Skill Duration Reduction (Deep Dive)

> **Question that prompted this:** Does the avian affix **No Speeding** ("Reduces all
> enemies' active skill durations by X%") shorten the **Sacred Hunter's class skill
> freeze** (Piercing Boneforge's energy-regen lockout), or only "active skill" buffs?
>
> **Verdict: YES — No Speeding (and Speed Disruption) reduce the Hunter freeze.**
> The engine has no "active skill vs class skill" distinction at the attribute level.
> Every buff/debuff duration a unit's skills produce runs through the same pipeline.
>
> **Sources:** `game_script.js` (engine code), decoded config tables
> (`Skill.json`, `Skill_level.json`, `Buff.json`, `Trap.json`, `Relic.json`,
> `Fly_entry.json`, `Language_en.json`) via `decode_config_data.py`, XOR key 24455.
>
> Credit: Bird → Discord @birrrd08

---

## 1. TL;DR

| Counter | Source | Mechanism | Affects Hunter freeze? | Range |
|---|---|---|---|---|
| **No Speeding** | Avian affix 3102 → skill 23603 | Attribute debuff on **attr 1061 `skillbuff_time_all`** (aura) | **YES** | −8% (L1) → −20.8% (L17) |
| **Speed Disruption** | Avian affix 3104 → skill 23605 | **Identical buff chain** to No Speeding (hence "cannot stack") | **YES** | −7% (L1) → −18.2% (L17) |
| **Thorny Spore** | Relic 4035 → skill 4035 | **SKILL_BUFFTIME_ADD** (group 360) buff with explicit skill-ID list (permanent aura) | **YES** — 1055 is in the list | −10% (L1) → −20% (L11 = relic L100) |
| **Dawn Warwing** | Back accessory 70405 → skill 18040 | Same group-360 mechanism, applied for **60s** | **YES** | L1 −20%, L2 −25%, **L3 −30%** |

Stacking: the two avian affixes are hard-blocked from stacking with each other
(same buff, `mutex`, plus `conflict_entry: [3102]` on Speed Disruption). Everything
else stacks — attr-1061 sources add **against the base duration**, then each
group-360 buff multiplies the result.

**Worked example** (base 4.0s freeze, No Speeding L15 −19.2%, Thorny Spore max −20%,
Dawn Warwing L1 −20%):

```
(4.0 − 4.0 × 0.192) × 0.80 × 0.80 = 4.0 × 0.808 × 0.64 ≈ 2.07 s
```

Not 2.56s — that figure comes from wrongly excluding No Speeding ("Lunar Sprite's
−19.2%" is just No Speeding at level 15 on that avian; it absolutely applies).

---

## 2. The Duration Pipeline (Engine)

Every timed effect a skill produces — buffs on self, debuffs on the enemy, summon
lifetimes, trap durations, repeating-effect windows — gets its duration from **one**
code path. From `game_script.js` (deobfuscated, simplified):

```js
// Called for every buffGroup entry when a skill effect executes:
duration = cast.data.getSkillFactAttrValue(baseTime, useSkill.config.id,
                                           ATTR.active_skillbuff_time);
for (buff of cast.buffCtr.getBuffByType(SKILL_BUFFTIME_ADD)) {   // group 360
    duration = buff.getFixTime(duration, useSkill.config.id);
}
runner.addBuff(target, buffId, duration, coefficient);
```

Inside `getSkillFactAttrValue(t, skillId, attrGroup)`:

```js
var n = t;
// Step 1 — per-skill + global duration attrs in the group (multiplicative):
for (attr of attrGroup) {
    f = roundInt(getSkillAttrByAttrId(skillId, attr.id)
               + getSkillAttrByAttrId(0, attr.id));
    n = round(n * round(1 + f / 1e4));
}
// Step 2 — the global "all skill buff time" attribute (ADDITIVE vs BASE):
if (attrGroup == active_skillbuff_time) {
    n = Math.max(0, n + round(t * this.getAttrib(ATTR.skillbuff_time_all)));  // 1061
}
return n;
```

And `BuffSkillBuffTimeAdd.getFixTime` (buff group 360):

```js
getFixTime(t, skillId) {
    if (t == -1) return -1;                       // permanent buffs untouched
    if (this._skillList.includes(skillId))        // _skillList = buff.param5
        return round(t * (1 - this.skillPar));    // MULTIPLICATIVE reduction
    return t;
}
```

Three hooks, in order:

1. **Per-skill duration attributes** (e.g. Prophet's "prolong active skills by 40%",
   attr 2024) — multiplicative, keyed to specific skills.
2. **Attr 1061 `skillbuff_time_all`** — one number on the **caster**; the adjustment
   is `base × attr1061`, added to the running result. **No skill filter of any kind.**
   Negative values (debuffs) shorten everything the caster's skills produce; the
   `Math.max(0, …)` floor means it can never go below 0.
3. **Group-360 `SKILL_BUFFTIME_ADD` buffs** on the caster — each one checks its own
   skill-ID list (`param5`) and multiplies by `(1 − reduction)` on match. Multiple
   group-360 buffs compound multiplicatively.

Key consequence: the debuffs live on the **caster**. "Reduce all enemies' …
durations" items place an aura debuff on the enemy unit; when that unit then casts
*its* skills, its own (debuffed) attr 1061 / group-360 buffs scale the durations of
whatever those skills apply — including debuffs applied **to you**. That is exactly
how a duration reducer on your side shortens the freeze the enemy Hunter puts on you.

---

## 3. Anatomy of the Sacred Hunter Freeze

**Skill 1055 — Piercing Boneforge** (Sacred Hunter class active):

```
Skill 1055:  skillEffect1 = [10552, 10551]
Effect 10551: buffGroup = [[1, 20042, 1, 4]]   ← buff 20042, BASE TIME = 4 (s)
Buff 20042:  action "pause_cd", group 3 (CTR), param1 = 6, mutex 1
```

- **Base freeze = 4.0s at every skill level** (confirmed: all 220 rows of
  `Skill_level` for 1055 carry `desc_parm = […, 40, 8, 6, 4]` — the 4s never scales).
  This matches the community's "Hunter base interruption: 4.0 sec" (Mobi.gg).
- `pause_cd` with `param1 = 6` pauses energy/cooldown accumulation on 6 active-skill
  slots. It shortens nothing and slows nothing — it **stops skill regen entirely**
  for its duration. The counters below shorten the *duration of the freeze*, not the
  regen rate.
- The 4s base goes through the full pipeline of §2 because it is an ordinary
  `buffGroup` entry (`g[3] = 4`) of an ordinary skill effect. **Nothing exempts
  class skills.**

Related properties (from doc 37):
- Buff 20042 is CTR **group 3** → removable by "clear CTR" cleanse effects.
- `CONTROL_RES` does **not** reduce it (control resistance only touches
  `dizz`/`ban_act`).

---

## 4. The Four Counters, Mechanism by Mechanism

### 4.1 No Speeding (avian affix 3102)

```
Fly entry 3102 → passive skill 23603 (levels 1–17)
Skill 23603:  buffGroup = [230040], action "passive"
Buff 230040:  action "trap", param1 = 1010                (aura carrier)
Trap 1010:    duration −1 (permanent), range 10000 (whole arena),
              target [4,10,0] (all enemies), buffId [[230041, −1]]
Buff 230041:  action "attrib", param1 = 1061 (skillbuff_time_all),
              param2 = 1, param3 = −10000, mutex 2
```

So: a permanent, arena-wide aura that plants an **attr 1061 debuff on every enemy**,
scaled by the skill-level coefficient. Decoded coefficients (`value ^ 24455`):

| Skill level | Reduction | | Skill level | Reduction |
|---|---|---|---|---|
| 1 | −8.0% | | 13 | −17.6% |
| 5 | −11.2% | | 14 | −18.4% |
| 9 | −14.4% | | **15** | **−19.2%** |
| 11 | −16.0% | | 16 | −20.0% |
| 12 | −16.8% | | 17 (max) | **−20.8%** |

(+0.8%/level from 8%; the tooltip's "8%" is the level-1 value.)

**The "Lunar Sprite −19.2%" seen in the wild is No Speeding at level 15** — it is
this affix on that avian, not a separate "active skills only" effect. Because it is
an attr-1061 debuff, it applies to **every** duration the debuffed enemy's skills
produce: hero actives, pal skill buffs, and **class skills** alike.

### 4.2 Speed Disruption (avian affix 3104)

```
Skill 23605:  buffGroup = [230040]     ← the SAME buff as No Speeding
```

Identical chain (buff 230040 → trap 1010 → buff 230041), only the level
coefficients differ: −7% (L1) → −18.2% (L17). Two stacking locks:
`conflict_entry: [3102]` on the affix (can't roll both) and the shared buff with
`mutex 2` (couldn't stack even across two units). This is why the tooltip says
"cannot stack with No Speeding" — it is literally the same debuff.

### 4.3 Thorny Spore (relic 4035)

> **Correction to doc 24/09_RELICS:** relic **4035 is Thorny Spore** (Language table:
> name id 403285 = "Thorny Spore"; skill desc 403289 = "Reduces the duration of all
> enemies' Class Skills by ##1%."). The earlier guesses — 4032 = "Thorny Spore?",
> 4035 = "Nirvana Spore?" — are wrong.

```
Skill 4035:   buffGroup = [40351]
Buff 40351:   action "trap", param1 = 404
Trap 404:     duration −1 (permanent aura), all enemies, buffId [[40352, −1]]
Buff 40352:   action "skill_bufftime_add", group 360 (SKILL_BUFFTIME_ADD),
              param5 = [1016, 1017, 1018, 1053, 1054, 1055, 1056, 1057, 1058,
                        1065, 1066, 1067, 1041, 106501]
```

Reduction scales with skill level (relic level 0–100 maps to skill level 1–11 via
the `equip` field): −10% (L1) → **−20%** (L11). Multiplicative, permanent.

The target list (`param5`), with names from `Language_en`:

| ID | Skill | What it is |
|---|---|---|
| 1053 | Blades Reunion | Martial Sage class skill |
| 1054 | Shattering Axe | Warbringer class skill |
| **1055** | **Piercing Boneforge** | **Sacred Hunter class skill — the freeze** |
| 1056 | Sun Pursuit | Plume Monarch class skill |
| 1057 | Crane's Whisper | Prophet class skill |
| 1058 | Galaxy Dive | Darklord class skill |
| 1066 | Tamer of Beasts | Beastmaster class skill |
| 1067 | Wilting Souls | Supreme Spirit class skill |
| 1016 | Melon Drop | Hero active (CC) |
| 1017 | Cocklebur Dance | Hero active (CC) |
| 1018 | Meteor Blitz | Hero active (CC) |
| 1041 | Spore Shot | Hero active |
| 1065 | Spore Duo | Hero active |
| 106501 | Whip of Imprisonment | Hero active |

So "Class Skills" in the tooltip is under-descriptive: the reduction also covers six
CC/utility **hero actives**. All eight tier-5 class skills are present.

### 4.4 Dawn Warwing (back accessory 70405)

```
Skill 18040:  buffGroup = [180312]
Buff 180312:  action "trap", param1 = 757
Trap 757:     duration −1, all enemies, buffId [[180313, 60], [180314, 60]]  ← 60s!
Buff 180313:  action "skill_bufftime_add", group 360,
              param5 = same list as Thorny Spore minus 106501
```

The **60s** in the tooltip ("for 60s") is the debuff duration on trap 757's buff
application — after 60s the enemy's class-skill durations return to normal.
Level scaling (coefficients decoded, matching `desc_parm`):

| Level | Evasion/Move SPD | Class-skill duration | Debuff window |
|---|---|---|---|
| 1 | +12% | **−20%** | 60s |
| 2 | +16% | **−25%** | 60s |
| 3 (max) | +20% | **−30%** | 60s |

The commonly quoted "−20%" is **level 1**; a maxed Dawn Warwing cuts 30%.

*Open item:* trap 757 also applies buff 180314 (`attrib` on attr 1001/ATK,
param3 = 0) for 60s — likely a zero-valued placeholder or coefficient-driven; not
yet decoded. Doesn't affect the duration math.

---

## 5. Stacking Math

Combining §2's three hooks for the Hunter freeze (base **B = 4.0s**):

```
freeze = max(0,  B × Π(per-skill attrs)  +  B × attr1061 )  ×  Π(1 − r_360ᵢ)
```

- **attr 1061 sources**: additive with each other, and the adjustment is computed
  against the *base*, not the running product. In practice only one applies
  (No Speeding XOR Speed Disruption).
- **group 360 sources**: each multiplies the result. Thorny Spore and Dawn Warwing
  are separate buffs and both apply.
- The **caster's own** attr-1061 *bonuses* (e.g. relic `skillbuff_time` boosts) add
  against the same base and can partially offset the debuff.

### Worked examples

| Setup | Calculation | Freeze |
|---|---|---|
| Nothing | 4.0 | **4.00s** |
| Thorny −20% + DW −20% (the "2.56s" claim) | 4.0 × 0.8 × 0.8 | **2.56s** |
| + No Speeding L15 (−19.2%) | (4.0 − 4.0×0.192) × 0.8 × 0.8 | **≈2.07s** |
| Max everything: NS L17 −20.8%, Thorny −20%, DW L3 −30% | (4.0 − 4.0×0.208) × 0.8 × 0.7 | **≈1.77s** |

### The Discord debate, settled

- *"ChatGPT says No Speeding doesn't affect the skill."* — **Wrong.** No Speeding is
  an attr-1061 debuff and attr 1061 has no skill filter; it scales class-skill
  durations along with everything else.
- *The forwarded in-game text* ("Only the following are capable of countering this
  effect: Speed Disruption, No speeding, Thorny Spore, Dawn Warwing") — **Right**,
  and now explained: two of the four work through attr 1061 (global), two through
  group-360 skill lists that explicitly include 1055.
- *"Lunar Sprite's −19.2% is for active skill duration, so I would not apply it"* —
  **Incorrect exclusion**: that −19.2% *is* No Speeding L15, and it applies.

---

## 6. Corrections & Implications for This Repo

1. **`24_RELIC_SYSTEM.md` / `battlesim/reference/09_RELICS.md`** — relic 4035 is
   **Thorny Spore** (−10%→−20% enemy class-skill/CC-active durations, permanent
   aura), not "Nirvana Spore?"; relic 4032 is not Thorny Spore.
2. **`34_PVP_META_ANALYSIS.md`** — "No visible counter-mechanic exists in the data"
   for pause_cd is now disproven: four counters, two mechanisms, all verified in
   config data.
3. **V1 simulator (`uploads/battlesimV1.html`)** — `affixNoSpeeding` currently
   scales only active-skill buff durations. It should also scale the class-skill
   freeze/effect durations (attr-1061 semantics), and Thorny Spore / Dawn Warwing
   should apply as separate multiplicative factors after it — with Dawn Warwing
   expiring at t = 60s.
4. **Attr naming trap**: attribute **1041** is `active_skillbuff_time` while *skill*
   1041 is "Spore Shot" — same number, unrelated namespaces. Attr **1061**
   (`skillbuff_time_all`) is the one the avian affixes debuff.

## 7. Confidence & Open Questions

**High confidence (read directly from engine code + config data):** the pipeline
order, attr-1061 additivity vs base, group-360 multiplicativity and skill lists,
base 4s freeze, all level scalings, the shared No Speeding/Speed Disruption buff.

**Not yet verified in-game:** absolute frame timing of trap application at battle
start (whether a class skill cast in the first instants could precede the aura
landing), and the purpose of Dawn Warwing's companion buff 180314.
