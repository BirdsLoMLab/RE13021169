# 47 — DEF Reduction Deep Dive (where "-X% DEF" actually lands)

> **Question (LordFaramire, 10/09/2026):** "Can we see in the game code where the defense reduction goes?"
> Screenshot context: battle stat panel showing **Final DEF**, a flat **DEF Total** bucket (Initial / Equip /
> Adventure Advancement / Enchant / Avian / Treasure) and a **Base DEF Total %** bucket (Pal / Skill / …),
> alongside a pal **Deploy Effect: "Reduce all enemies' DEF by 24%"** and a support reply stating there is
> **no stacking cap** on DEF reduction in PvP or PvE.
>
> **Sources (all byte offsets into `game_script.js`, the 18 MB minified bundle in this repo, 2026-02-28 capture):**
> `MetaAttrib.ts` @13543031 · `BuffAttrib.ts` @8511078 · `BuffAttribContinue.ts` @8515461 ·
> `BuffAttribCondition.ts` @8512748 · `BuffAttribConvert.ts` @8517832 · `SkillRunner.addBuff` @17059152 ·
> `BuffCtr.ts` @8540148 · `BuffClear.ts` @8535706 · `HurtUtil.normalHurt` @12441031 ·
> `setPlayerAttrib` @8294499 · `ConfigBuff.ts` @9441185

---

## TL;DR

1. **The panel buckets are not where the debuff lands.** "DEF Total" and "Base DEF Total %" are
   *out-of-battle assembly*, resolved server-side. The battle unit is handed one number per attribute.
2. In battle, a "-X% DEF" debuff goes into the **`_time` multiplier of the `def` (1024) MetaAttrib** —
   it scales the already-assembled **Final DEF**, after every panel bucket.
3. **Multiplicative DEF modifiers are additive with each other**, not compounding:
   `_time = 1 + Σ(modifiers)`. Two -24% debuffs give ×0.52, not ×0.5776.
4. **There is no lower clamp anywhere.** `MetaAttrib` caps the top (`up_limit`) and nothing caps the bottom.
   DEF can reach 0 and go **negative**.
5. Negative DEF is not a no-op — in `normalHurt` the term is `max(roundInt(ATK − DEF×(1+def_coe)), 1)`,
   so a negative DEF **adds** to the attacker's effective ATK.

---

## 1. What the battle unit actually receives

`setPlayerAttrib` (@8294499) builds every combat attribute (`module == 1`) from the server payload:

```javascript
t.setPlayerAttrib = function(t, i, a) {
    for (var f of configAttribute.getDataByList("module", 1)) {
        var c = configAttribute.getDataByKey(f.id),
            v = new MetaAttrib(c);
        // PvE-only stats zeroed out in PvP chapters, everything else straight from attr_list
        (0 != s.pve || f.id != pve_dam && f.id != pve_resist)
            ? v.baseValue = this.getAttrib(f.id, t.attr_list)
            : v.baseValue = 0;
        i.attribs[c.id] = v
    }
}
t.getAttrib = function(t, i) {            // simple k/v lookup, no assembly
    for (var s of i) if (s.k == t) return roundInt(Number(s.v));
    return 0
}
```

There is **no client-side code that combines the flat bucket with the % bucket** — `ConfigAttr_source`
(@9398753) carries only `id / name / order`, i.e. it is a label table for the panel rows. The buckets exist
purely for display; `attr_list[1024]` is already **Final DEF**, and that is what `baseValue` becomes.

Sanity check against the screenshot: `57,006 × ~318,150 ≈ 18.14 B` vs the displayed Final DEF of
**18,121.8M** — consistent with `Final DEF = flat DEF Total × (1 + Base DEF Total %)` to display precision.
(The % figure is partly covered by the markup circle, so this is an inference from the numbers, not from code.)

---

## 2. MetaAttrib — the only place an attribute value is produced

`MetaAttrib.ts` @13543031:

```javascript
function MetaAttrib(config, copy) {
    this._baseValue = 0; this._addValue = 0; this._addExtraValue = 0; this._time = 1; ...
}
_calculateValue = function(base) {
    var v = roundInt(roundInt(base + this._addValue) * this._time + this._addExtraValue);
    if (0 != this.config.up_limit) v = Math.min(v, this.config.up_limit);   // ← cap is TOP ONLY
    if (2 == this.config.num_type) v = round(v / 1e4);
    return v ?? 0
}
addValue      = function(x) { this._addValue      = round(this._addValue + x);      this._change = !0 }
addMultiples  = function(x) { this._time          = round(this._time + x);          this._change = !0 }
addExtraValue = function(x) { this._addExtraValue = round(this._addExtraValue + x); this._change = !0 }
multiple      = function(x) { this._time          = this._time * x;                 this._change = !0 }
```

So the full in-battle DEF expression is:

```
DEF = min( roundInt( roundInt(FinalDEF + Σflat) × (1 + Σpercent) + Σpost ), up_limit )
```

- `up_limit` for `def` (1024) is **0 = uncapped**. The only attribute with a battle cap in
  `data/constants/attribute_caps.json` is **1008** (`miss`, 8000 = 80%).
- **No `Math.max(0, …)` exists in this path.** Negative results pass straight through.

---

## 3. How a "-24% DEF" deploy effect is encoded

`BuffAttrib.ts` @8511078 — the `action: "attrib"` buff class:

```javascript
alloc = function(cfg) {
    buff.config = cfg;
    buff._id          = cfg.param1;      // attribute id — 1024 for DEF
    buff._isMultiples = 2 == cfg.param2; // 2 = multiplicative, else flat
    buff._value       = cfg.param3;      // base magnitude, typically -1
    return buff
}
onBegin = function() {
    var meta = this.owner.data.getAttribMeta(this._id);
    this._lastValue = round(this._value *
        this.runner.cast.data.getSkillFactAttrValue(this.skillPar, this.runner.useSkill.config.id, 1044));
    this._isMultiples ? meta.addMultiples(this._lastValue) : meta.addValue(this._lastValue)
}
onDestroy = function() {  // exact reversal when the buff ends
    this._lastValue && (this._isMultiples ? meta.addMultiples(-this._lastValue) : meta.addValue(-this._lastValue))
}
```

So a 24% pal deploy debuff is `param1=1024, param2=2, param3=-1, skillPar=0.24` → `addMultiples(-0.24)`
→ `_time: 1 → 0.76`. This is the same shape as the snail slow documented in
[43_SNAIL_PAL_SPEED_REDUCTION_DEEP_DIVE.md](43_SNAIL_PAL_SPEED_REDUCTION_DEEP_DIVE.md) (`param1=1009`).

### The `getSkillFactAttrValue(skillPar, skillId, 1044)` wrapper

@17730276. The magnitude is not raw `skillPar` — it is scaled first:

```javascript
getSkillFactAttrValue = function(par, skillId, attrGroup) {
    var n = round(par + round(skillAttr(skillId, attrGroup) + skillAttr(0, attrGroup)));  // additive
    for (var cfg of configAttribute.getDataByList("group", attrGroup))                    // then multiplicative
        n = round(n * round(1 + round(roundInt(skillAttr(skillId, cfg.id) + skillAttr(0, cfg.id)) / 1e4)));
    return n
}
```

This is the hook the Beastmaster Lv50 passive ("Enhance Pal Deploy Effects by **20%**", skill 2106 —
see [32_CLASS_SKILLS_REFERENCE.md](32_CLASS_SKILLS_REFERENCE.md)) rides on: a 24% deploy debuff becomes
**28.8%** for a Beastmaster, because the enhancement scales `skillPar` before it ever reaches `addMultiples`.

### Other channels into the same attribute

| Buff class | Offset | Channel | Notes |
|---|---|---|---|
| `BuffAttrib` | 8511078 | `addValue` / `addMultiples` | the standard flat or % modifier |
| `BuffAttribContinue` | 8515461 | same | re-applies `value × skillPar` every `param4` ms for `param5[0]` s — a ramp; accumulates in `_totaladdvalue`, **no cap**, fully reversed on expiry |
| `BuffAttribCondition` | 8512748 | same | magnitude scales off HP%/speed delta; **this one does clamp**, via `param5` `_limit` min/max |
| `BuffAttribConvert` / `BuffPetConvert` | 8517832 / 8576604 | `addExtraValue` | converts one stat into another; lands *after* the multiplier |

Nothing else in the bundle writes to a `MetaAttrib`. All of these pool into the same three accumulators,
which is why order of application is irrelevant.

---

## 4. Stacking — what the engine actually enforces

Stacking is governed per-buff by `mutex` (field 7) and `add_max` (field 8) in `ConfigBuff` (@9441185),
enforced in `SkillRunner.addBuff` (@17059152):

| `mutex` | Behaviour |
|---|---|
| 0 (or unset) | stacks freely — every application is a separate live instance |
| 1 | `stopBuffById(id)` first → **replace** any existing instance of that same buff id |
| 2 | skipped entirely if the target already has that buff id |
| 3 | stacks up to `add_max`; every application refreshes all durations; at the cap the oldest running instance is stopped |
| 4 | one per caster — a second application from the same caster is skipped |
| 5 | one per caster — a second application from the same caster only refreshes duration |

**Crucially, every one of these checks is keyed on `config.id`** (`getBuff(e)`, `getBuffListById(e)`).
Two different sources of DEF reduction are two different buff ids, so no mutex rule can ever suppress one
against the other — they coexist and both land in `_time`. That is the engine-level confirmation of the
support reply: **no global cap on DEF-reduction stacking exists**, and none could, because the sum happens
inside `MetaAttrib._time` where nothing is clamped. Same-source stacking is the only thing that can be
limited, and only by that buff's own `mutex`/`add_max`.

### What does and does not stop an attrib debuff

```javascript
var C = ["dizz", "ban_skil", "throw_hit", "bound", "ban_act"];      // SkillRunner.ts @17051640
...
if ((t.statectr.notControlled > 0 || t.statectr.invincible > 0) && C.includes(s.action)) return null;
```

- **CC immunity does not block attribute debuffs.** `"attrib"` is not in `C`. Likewise `CONTROL_RES` (1042)
  only shortens `"dizz"`/`"ban_act"` durations — it does not touch `"attrib"`.
  *(This contradicts §5 of doc 43, which states the snail slow is blocked by `notControlled`/`invincible`
  because it is group 3. The gate in the shipped code is on `action`, not `group`. Logged in 98_DISCREPANCIES.)*
- **`IGNORE_BUFFIDS`** (BuffGroupType 330) blocks a debuff only if its `param5` list names that buff id.
- **Cleanse** (`BuffClear` @8535706) has two modes: `param1 == 0` → `buffCtr.removeBuff(n)`, which matches on
  `buffType` (= `config.group`, set in `Buff.config` setter @8501296) and so can wipe a whole group;
  `param1 == 1` → `stopBuffById(n)`, which matches a specific buff id. Either way the removal reverses the
  modifier exactly (`onDestroy` subtracts `_lastValue`).
- `battle_attribute_def` (1079) and `battle_resist_def` (1080) look like they should resist this. They do not —
  both appear **only** as ConfigUnit field getters and in the `AttribDefine` enum. No battle code reads them.

### Pierce is a different system

`calArmorAndBlock` (@12441031, in the `normalHurt` tail) modifies the **resistance** term
(`att_resist` / `partner_resist` / …), capped at ±50% per hit, and never touches `def`. Armor Penetration is
not DEF reduction — see [08_PIERCE_BLOCK_INSPIRE_SUPPRESS.md](08_PIERCE_BLOCK_INSPIRE_SUPPRESS.md).

---

## 5. What happens at 0 DEF — and below

`HurtUtil.normalHurt` (@12441031):

```javascript
var f = roundInt( Math.max(roundInt(o - u * (1 + g)), 1) * round(A * round(1 - m)) );
//                         ^ATK  ^DEF    ^def_coe
```

The `max(…, 1)` floors the **whole subtraction**, not DEF itself. Walk the cases with a 24% debuff:

| Sources applied | `_time` | DEF (as fraction of Final DEF) | `ATK − DEF×(1+def_coe)` |
|---|---|---|---|
| 0 | 1.00 | 100% | ATK − DEF |
| 1 | 0.76 | 76% | ATK − 0.76·DEF |
| 2 | 0.52 | 52% | ATK − 0.52·DEF |
| 4 | 0.04 | 4% | ATK − 0.04·DEF |
| 5 | **−0.20** | **−20%** | **ATK + 0.20·DEF·(1+def_coe)** |

So "reduce them to 0 DEF" is not the ceiling of this effect — it is the halfway point. Past ~4.17 stacked
instances of −24%, the defender's DEF stat becomes a **damage bonus for the attacker**, scaled by the
attacker's own `def_coe`… which is the defender's stat, so the more DEF-amplification the target has
stacked, the worse the flip hurts them.

Same pool, opposite sign: in-battle **DEF buffs** (e.g. "increases DEF by 32%") are also
`addMultiples` on 1024, so they net out additively against debuffs — `1 + 0.32 − 0.24 = 1.08`. A defender
does not multiply their way out of a stacked debuff; they can only out-add it.

---

## 6. Practical notes / caveats

- The `max(…, 1)` floor means the ATK−DEF term is a **cliff**, not a curve. If `ATK < DEF×(1+def_coe)`, every
  hit lands on the floor of 1 before multipliers, and the first DEF debuff that pushes the target below your
  ATK is worth vastly more than the previous ones. Against a 4.72 B Final DEF wall, DEF reduction is doing
  nothing at all until your ATK is in range — then it is doing everything.
- **Unverified here:** the specific buff ids / `mutex` values for individual DEF-reduction effects. Those live
  in `data/tables/Buff.json`, which is `.gitignore`d and absent from this clone, and the config binary is not
  in `lom.joynetgame.com.zip` (assets only). Re-run `decode_config_data.py` against a capture that includes
  `bundle-firstload-res` to confirm whether any given pal/mount/artifact DEF debuff is `mutex 0` (free
  stacking from multiple copies) or `mutex 1/2/4/5` (one per id or per caster).
- Whether a given in-game line reads "DEF" or "Final DEF" (e.g. the Angel support skill "increases Final DEF
  by 8%") does not appear to correspond to a separate attribute — there is only 1024 — but confirming which
  `param2` mode each uses also needs Buff.json.
