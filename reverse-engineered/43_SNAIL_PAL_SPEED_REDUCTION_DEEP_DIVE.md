# 43 — Snail Pal Speed Reduction Deep Dive

> **Sources:** data/tables/Buff.json (buff 10003), data/tables/Pet.json (IDs 2801-2805), battlesim/reference/06_PALS_AND_PETS.md, battlesim/reference/10_BUFFS_AND_STATUS.md, battlesim/reference/03_ATTRIBUTES.md, battlesim/reference/20_SPECIAL_MECHANICS.md, game_script_pretty.js lines 192380-192520
> **Key Discovery:** Snail speed reduction is a CTR-group control debuff (buff 10003), not a pure attribute modifier — meaning it is blocked by CC immunity (notControlled/invincible) and reduced by CONTROL_RES

---

## 1. Snail Pal Lineup — All 5 Variants

All snail pals share the primary effect: **"Reduces enemy movement speed by X%"**

| Pet ID | Name | Rarity | Quality | Skills | Speed Reduction | DMG Mult |
|--------|------|--------|---------|--------|-----------------|----------|
| 2801 | Small Yellow Snail | Normal | 1 | Detonate L1, Utility L1 | 15% | 3.111 / 50% |
| 2802 | Thorn Snail | Well | 3 | Detonate L2 | 20% | 7 / 55% |
| 2803 | Moss Snail | Mythic | 5 | Detonate L2, Slow L2 | 30% | 15.773 / 70% |
| 2804 | Ice Cream Snail | Epic | 6 | Detonate L2, Slow L3 | 35% | — / 80% |
| 2805 | Tipsy Snail | Legendary | 7 | ATK SPD L3, Slow L4 | 40% | — / 90% |

Speed reduction scales +5% per tier: 15% → 20% → 30% → 35% → 40%.

---

## 2. Target Attribute: 1009 (Movement Speed)

From `battlesim/reference/03_ATTRIBUTES.md` (line 39):

| ID | Key | Initial | num_type | Description |
|----|-----|---------|----------|-------------|
| 1009 | speed | 300 | 1 | Movement speed |

- **num_type = 1**: Raw integer (NOT /10000 percentage like ATK Speed 1003)
- **Base value: 300** for all standard units
- **No hard cap** (up_limit = 0)

---

## 3. Core Buff: 10003

From `data/tables/Buff.json`:

```json
[
  10003,        // buff_id
  0,            // name
  1,            // type: persistent (stays until expired)
  3,            // group: CTR (Control effect group)
  "",           // icon
  50110,        // effect (visual effect ID)
  0,            // effect_mirror
  1,            // mutex: replace (new instances replace old)
  0,            // add_max
  2,            // bind: bp_bottom
  "attrib",     // action: BuffAttrib class
  1009,         // param1: attribute ID (speed)
  2,            // param2: modification type (multiplicative)
  -1,           // param3: value (base multiplier)
  0,            // param4
  null          // param5
]
```

### Buff Field Breakdown

| Field | Value | Meaning |
|-------|-------|---------|
| action | `attrib` | Uses `BuffAttrib` class for attribute modification |
| param1 | 1009 | Modifies **movement speed** |
| param2 | **2** | **Multiplicative mode** (`addMultiples`) |
| param3 | **-1** | Base multiplier = -100% (scaled by skillPar) |
| group | **3 (CTR)** | **Control effect group** |
| type | 1 | Persistent — lasts for buff duration |
| mutex | 1 | Replace — new instance replaces old |

---

## 4. Speed Reduction Formula

With `param2 = 2` (multiplicative) and `param3 = -1`:

```
final_speed = base_speed × (1 + param3 × skillPar)
            = base_speed × (1 + (-1) × skillPar)
            = base_speed × (1 - skillPar)
```

The snail's **skillPar** determines the exact reduction percentage:

| Snail | skillPar | Formula | Effective Speed |
|-------|----------|---------|-----------------|
| Small Yellow Snail (2801) | 0.15 | 300 × 0.85 | 255 |
| Thorn Snail (2802) | 0.20 | 300 × 0.80 | 240 |
| Moss Snail (2803) | 0.30 | 300 × 0.70 | 210 |
| Ice Cream Snail (2804) | 0.35 | 300 × 0.65 | 195 |
| Tipsy Snail (2805) | 0.40 | 300 × 0.60 | 180 |

---

## 5. Critical Mechanic: CTR Group Classification

Buff 10003 is **group 3 (CTR)** — the **control effect group**, not group 4 (ADD/attribute). This has major implications:

### What blocks snail speed reduction

| Mechanic | Effect |
|----------|--------|
| `notControlled` buff | Target is immune to all CTR-group buffs → snail debuff is **completely blocked** |
| `invincible` buff | Target is immune to all control effects → snail debuff is **completely blocked** |
| IGNORE_BUFFIDS (group 330) | Blocked if param5 explicitly includes buff 10003 |
| **CONTROL_RES** (attr 1042) | Reduces debuff **duration**: `duration = round(duration - round(duration × CONTROL_RES))` |

### What does NOT block it

- Standard attribute cleanse (targets group 4, not group 3)
- Shield buffs
- DMG RES buffs

### Why this matters

Most players assume speed reduction is a simple stat debuff. In reality, it's classified as **crowd control** — the same category as stuns and knockups. Any build with CC immunity windows (motorcycle overdrive, certain class actives) will be **immune to snail slow during those windows**.

---

## 6. Stacking Behavior

**Mutex type 1 (replace)**: Only one instance of buff 10003 can exist on a target at a time.

- Multiple snails do **not** stack their speed reduction
- A new snail's buff replaces the previous one
- Deploying Tipsy Snail (40%) after Moss Snail (30%) overwrites to 40%
- Deploying Moss Snail (30%) after Tipsy Snail (40%) **downgrades** to 30%

---

## 7. Speed Cascade — Hidden Interaction

From `game_script_pretty.js` line 192412, `BuffAttrib` has special handling for attribute 1009:

```javascript
if (this._id == r.speed) {
    for (var i, a = this.owner.buffCtr.getBuffByType(n.ATTRIB_CONDITION), s = e(a); !(i = s()).done;) {
        i.value.updateAttrib()
    }
}
```

**When snail reduces movement speed (1009), ALL `ATTRIB_CONDITION` buffs on affected units re-evaluate.** This is unique to the speed attribute.

### Impact

- If an enemy has conditional buffs that depend on speed value, they re-trigger
- Sage's HP-scaling ATK buff (20028) re-evaluates on speed change
- Any `BuffAttribCondition` buff on the target recalculates

---

## 8. Motorcycle Mount (404) Interaction — The Key Matchup

### Why snail vs motorcycle is significant

Both systems operate on the same attribute (1009/speed) but in opposing directions:

| System | Buff ID | Mode | Effect on 1009 |
|--------|---------|------|-----------------|
| Snail pal | 10003 | Multiplicative (param2=2) | **-40%** (Tipsy) |
| Motorcycle stacking | 50609 | Multiplicative (param2=2) | **+8% per stack** |

### Phase 1 interaction (Acceleration)

The motorcycle's **SpeedTrigger** (buff 50615) fires when speed ≥ 200% of base:
- Without snail: 13 stacks needed (13 × 8% = 104% → base × 2.04)
- **With Tipsy Snail**: The -40% multiplicative debuff compounds with the stacking:
  ```
  effective_speed = base × (1 - 0.40) × (1 + stacks × 0.08)
                  = base × 0.60 × (1 + stacks × 0.08)
  ```
  Need: `0.60 × (1 + stacks × 0.08) ≥ 2.0`
  → `1 + stacks × 0.08 ≥ 3.333`
  → `stacks ≥ 29.2` → **30 stacks minimum** (vs 13 without snail)

**Snail more than doubles the stacks needed to reach overdrive.**

### Phase 2 interaction (Overdrive)

When the motorcycle hits overdrive, buff 50631 grants **CC immunity** (`not_controll`) for 5 seconds:
- During overdrive, the snail debuff **cannot be re-applied**
- Buff 50632 clears buff group 3 → **actively removes existing snail slow**
- The motorcycle rider is temporarily **immune to and cleansed of** snail speed reduction

### Phase 3 interaction (Reset)

When Phase 1 restarts (buff 50630 clears speed stacks):
- CC immunity expires
- Snail slow can be re-applied
- The stacking race begins again from 0 stacks + snail debuff

### Timeline with Tipsy Snail

```
t=0      Phase 1 starts, snail debuff active (-40%)
         Need 30 stacks instead of 13 to reach overdrive

t=???    30 stacks reached → speed ≥ 200%
         SpeedTrigger fires
         CC Immunity + Group 3 cleanse → snail debuff REMOVED

t=???+5  Overdrive: +20% ATK/DEF/SPD + CC Immunity
         Snail cannot re-apply during this window

t=???+10 Phase 3: Stacks cleared, Phase 1 restarts
         Snail debuff re-applies → back to 30-stack requirement
```

---

## 9. Beastmaster Deploy Effect Enhancement

From `battlesim/reference/04_CLASSES.md`:

**Beastmaster (Job 1542, type=9)** has a deploy enhancement passive:

| Level | Skill ID | Effect |
|-------|----------|--------|
| Lv50 | 2106 | Enhance Pal Deploy Effects by **20%** |
| Lv100 | 2108 | Extra effects based on deployed pal race count |

With Beastmaster Lv50:
- Tipsy Snail's 40% reduction × 1.20 = **48% speed reduction**
- Formula: `base × (1 - 0.48) = base × 0.52`
- Motorcycle stacks needed: `0.52 × (1 + stacks × 0.08) ≥ 2.0` → **stacks ≥ 36**

---

## 10. Counter-Play Summary

### Against snail-heavy builds

| Strategy | Why it works |
|----------|-------------|
| CC Immunity windows | Snail is CTR group → blocked by notControlled |
| Motorcycle overdrive | Phase 2 cleanses group 3 + grants CC immunity |
| CONTROL_RES stacking | Reduces snail debuff duration |
| Plume Monarch active | If build has CC immunity active skill |

### Against motorcycle with snail counter

| Strategy | Why it works |
|----------|-------------|
| Tipsy Snail (40%) | Delays overdrive from 13 to 30 stacks |
| Beastmaster + Tipsy (48%) | Delays overdrive to 36 stacks |
| Burst before overdrive | Longer Phase 1 = more time to kill |
| Stun chaining in Phase 1 | Prevent stacking entirely |

---

## 11. Key Takeaways

1. **Snail speed reduction is crowd control**, not a stat debuff. It's blocked by CC immunity and reduced by CONTROL_RES.
2. **Buff 10003 is mutex-replace** — multiple snails don't stack, latest one wins.
3. **The speed cascade** triggers ALL conditional buff re-evaluations on affected enemies when speed changes.
4. **Against motorcycle**: Tipsy Snail more than doubles the stacks needed for overdrive (13 → 30), but motorcycle's overdrive **cleanses and immunizes** against the snail debuff.
5. **Beastmaster enhancement** pushes Tipsy Snail to 48% reduction, requiring 36 stacks for motorcycle overdrive.
6. **Any future speed-boost pal** should be checked for buff group classification — if it's group 4 (ADD) instead of group 3 (CTR), it would bypass CC immunity entirely, making it mechanically distinct from snail's approach.
