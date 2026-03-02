# 40 — Heroic Descent Deep Dive: The Untargetable Spirit Nobody Uses

> **Sources:** game_script_pretty.js lines 431572-431604 (addCallUnit), 450287-450306 (_addUnit1), 450273-450286 (_createUnit), 192564-192643 (BuffAttribConvert), 196638-196681 (BuffUnitCallDamageAdd), 322756-322771 (normalHurt), 429985-430048 (SkillHandleNormal.att), 449145-449149 (onLastUpdate total_dam_add inheritance), 349636-349672 (MetaAttrib); data/tables/Unit.json (unit 4001), Skill.json (1048, 10481, 4015), Skill_level.json (1048 L1-L300), Buff.json (20029, 20077, 40151), UnitType.json (type 6), Attribute.json (1039, 1045)
> **Key Discovery:** Heroic Descent's Hero Spirit is fully functional — it attacks at 3.0 ATK speed while being untargetable, with a passive that converts the caster's Skill DMG (skill_dam_extra) into basic attack multiplier (att_dam). However, its intentionally zeroed-out base att_dam means ALL damage depends on the caster's skill_dam_extra investment, making it a class-specific tool — not the general-purpose summon Clone Strike is.

---

## 1. Skill Configuration

**Skill ID:** 1048 — "Heroic Descent"
**Type:** Active (type 1), quality 7
**Action:** `effect` -> triggers skillEffect2 [10481] -> Buff 20029 (call_unit)
**Energy:** 190 initial / 190 max / 10 per second recovery -> **19s to first cast**
**Range:** [1, 100]

### Skill Scaling (L1 -> L300)

| Level | skillPar | Spirit ATK | DMG/hit (desc) | Duration |
|-------|----------|------------|----------------|----------|
| L1 | 1.48 | caster x1.48 | 148% | 10s |
| L50 | 4.46 | caster x4.46 | 446% | 10s |
| L100 | 6.97 | caster x6.97 | 697% | 10s |
| L150 | 7.02 | caster x7.02 | 702% | 10s |
| L200 | 8.88 | caster x8.88 | 888% | 10s |
| L250 | 10.76 | caster x10.76 | 1076% | 10s |
| L300 | 12.63 | caster x12.63 | 1263% | 10s |

Duration is always 10s base (from desc_parm[2]) but scales with `active_skillbuff_time` attribute.

---

## 2. Unit 4001 — The Hero Spirit

```json
{
    "id": 4001,
    "type": 6,              // CallUnit
    "model": 4001,
    "hatred_type": 21,      // Untargetable
    "ai": "common",
    "passiveSkills": [10481],
    "att_speed": 30000,     // 3.0 ATK speed (fixed)
    "crit_dam": 20000,      // 2.0x crit damage (fixed)
    "crit_def": 10000,      // 1.0 crit defense
    "att_dam": 0,           // ZERO: all damage comes from conversion
    "skill_dam_extra": 10000,  // 1.0 base (overwritten by caster value)
    "vertigo": 0,           // Cannot stun
    "vertigo_times": 1,     // Stun duration (irrelevant since vertigo = 0)
    "speed": 300,
    "att_range": 150,
    "detection_range": 2000,
    "target_num": 1
}
```

### UnitType 6 (CallUnit) Properties

```json
{
    "id": 6,
    "target": 1,            // Cannot be targeted by enemies
    "att_skill": 1,         // Generic normal attack (Skill 1)
    "counter": 0,           // No counter attacks
    "vertigo_time": 1,      // Stun buff ID (irrelevant - vertigo = 0)
    "suspend_time": [80, 0.5]
}
```

**Critical finding:** Despite Unit 4001 having `att_skill: 0` in its own config, `att_skill` comes from `UnitType`, not the Unit table. UnitType 6 has `att_skill: 1`, giving the spirit the generic normal attack skill.

---

## 3. Creation Path — How the Spirit Gets Built

```javascript
// Line 431572-431591 (addCallUnit)
addCallUnit(unitId=4001, position, time, attribs, skillPar):
    // param1 = 4001 (NOT 0) -> summon from config, NOT clone
    unit = unitMgr.addUnitCall(4001)    // -> _addUnit1 (loads passive skills!)

    // Apply param5 attribute modifications
    for mod in [[1001, 1, 1], [1045, 1, 0]]:
        // For summoned units (unitId != 0): SET baseValue from caster
        unit.attribs[mod[0]].baseValue = caster.attribs[mod[0]].baseValue
                                         * mod[1] * (mod[2]==1 ? skillPar : 1)

    // Param5 breakdown:
    // [1001, 1, 1] -> ATK.baseValue = caster.ATK * 1 * skillPar
    // [1045, 1, 0] -> skill_dam_extra.baseValue = caster.skill_dam_extra * 1

    addCopyUnit(unit, position, time)
    // -> sets lifeTime, parent, isCallType, currenHp = maxHP
```

### _addUnit1 — Loads Passive Skills

```javascript
// Line 450287-450306
_addUnit1(data, config=Unit4001):
    // Initialize ALL module-1 attributes from config
    for attr in configAttribute.getDataByList("module", 1):
        data.attribs[attr.id] = new MetaAttrib(attr)
        data.attribs[attr.id].baseValue = config[attr.key]
        // For missing keys: NaN fallback -> 10000 (percentage) or 0 (integer)

    // Load skills from config
    if config.passiveSkills != null:
        for skill in config.passiveSkills:
            addSkill(data, skill, 1)    // Adds passive 10481
```

**This is the key difference from Clone Strike.** Clone Strike (param1=0) uses `addUnitImageCall` -> `_createUnit` which gives an **empty skill list**. Heroic Descent (param1=4001) uses `addUnitCall` -> `_addUnit1` which **loads passive skills from the unit config**.

### MetaAttrib NaN Fallback

When `_addUnit1` loads attributes, it does `f.baseValue = config["att_dam"]`. Unit 4001 config has `att_dam: 0` explicitly, so baseValue = 0. This is intentional — the att_dam starts at zero.

For reference, the NaN fallback in MetaAttrib setter (line 349669):
```javascript
set baseValue(e):
    this._baseValue = null != e ? e : 0    // Handle null/undefined
    this._baseValue = Number(e)            // Convert to number
    // NaN check: if undefined was passed, Number(undefined) = NaN
    this._baseValue !== +this._baseValue && (
        this._baseValue = 2 == this.config.num_type ? 1e4 : 0
    )
    // For percentage attributes: NaN -> 10000 (1.0 = 100%)
    // For integer attributes: NaN -> 0
```

---

## 4. The Passive — skill_dam_extra to att_dam Conversion

**Passive Skill 10481** applies Buff 20077 (`attrib_convert`) with:

```json
{
    "id": 20077,
    "action": "attrib_convert",
    "param1": 0,        // calType 0: use baseValue of source
    "param2": 1045,     // source = skill_dam_extra
    "param3": 1039,     // target = att_dam
    "param5": null      // no limits
}
```

### BuffAttribConvert Code (Line 192594-192631)

```javascript
onBegin():
    value = _calValue()
    targetMeta = owner.getAttribMeta(att_dam)
    this._lastValue = value
    targetMeta.addExtraValue(value)      // Add to att_dam _addExtraValue

_calValue():
    // calType 0: get baseValue of source attribute
    a = owner.getAttribMeta(skill_dam_extra).baseValue
    a = roundInt(a * this.skillPar)      // skillPar = 1.0 (from passive 10481)
    return a

onDestroy():
    targetMeta.addExtraValue(-this._lastValue)   // Clean up on buff removal
```

### The Damage Conversion Chain

1. Caster skill_dam_extra baseValue (say 25000 = 250%) is copied to spirit via param5
2. Spirit passive fires -> `addExtraValue(25000)` to spirit att_dam
3. Spirit att_dam calculation: `((0 + 0) * 1 + 25000) / 10000 = 2.5`
4. Spirit basic attack damage: `max(ATK - DEF*(1+def_coe), 1) * 2.5 * (1-att_resist)`

**att_dam starts at zero intentionally.** The ENTIRE basic attack multiplier comes from the caster skill_dam_extra investment. Without skill_dam_extra, the spirit deals zero damage.

---

## 5. Complete Damage Formula for Hero Spirit

```
Per-hit damage:

1. normalHurt(spirit, target):
   baseDmg = max(roundInt(ATK_spirit - DEF_target * (1 + def_coe)), 1)
           * att_dam_spirit                    // = caster.skill_dam_extra / 10000
           * (1 - att_resist_target)           // After armor/block calculation

2. calHurt(baseDmg, target, spirit):
   * (1 + pve_dam_spirit)                     // PvE bonus (0 in PvP)
   * (1 - resist_target)                      // Final DMG RES
   * (1 - pve_resist_target)                  // PvE resist (0 in PvP)

3. Crit check:
   if crit: * max(1.5, crit_dam / crit_def)   // Fixed: max(1.5, 2.0/0.5) = 4.0

4. Post-normalHurt modifiers:
   + UnitCallDamageAdd from parent             // +30% with Storm Necklace talent
   * total_dam_add                             // Inherited from parent every frame
   / PvP injuryReduce                         // Same division as all damage
```

### Spirit Fixed Combat Stats (from Unit 4001 config)

| Stat | Value | Implication |
|------|-------|-------------|
| ATK speed | 3.0 (fixed) | 30 attacks in 10s, not affected by caster speed buffs |
| Crit DMG | 2.0 (fixed) | Max crit multiplier = 4.0x (vs caster potentially 16x+) |
| Crit Rate | 0 (default) | Effectively never crits without buff sources |
| Stun (vertigo) | 0 | **Cannot stun** |
| att_dam | 0 -> converted | All damage from skill_dam_extra |
| att_resist | 0 | Irrelevant — untargetable |
| resist | 0 | Irrelevant — untargetable |

---

## 6. Parent Interactions — What the Spirit Inherits (and Doesn't)

### Inherited from Parent

| Mechanic | How | Line |
|----------|-----|------|
| **total_dam_add** | Synced every frame in `onLastUpdate()` | 449149 |
| **UnitCallDamageAdd** | Checked from parent buffs on each attack | 429993 |

### NOT Inherited from Parent

| Mechanic | Why Not |
|----------|---------|
| **STATE_TRIGER effects** | Checked on `r.cast` (spirit), not parent |
| **NORMAL_ACT_NUM_TRIGGER** | Counter incremented on spirit, not parent |
| **Stun/CC effects** | Uses spirit own vertigo stat (= 0) |
| **NORMAL_ATTACK skill effects** | Uses spirit own skill effects (none) |
| **CRIT_ATTACK triggers** | Uses spirit own skill effects |
| **Mount passive skills** | Not in unit config, not loaded |
| **Artifact passive skills** | Not in unit config, not loaded |
| **Accumulated battle buffs** | Spirit is fresh unit, no buff inheritance |

### Can the Spirit Receive External Buffs?

**Partially.** CallUnit types are excluded from `CastPartner` targeting (line 450425: explicit `isCallType` check), so **pet aura buffs do NOT affect the spirit**. However, broad `Friend`-type targeting skills (ally field effects) can potentially apply buffs to the spirit.

---

## 7. Storm Necklace — The Summoned Unit Talent

**Skill 4015:** "Storm Necklace" (quality 5, passive)
**Buff 40151:** `unit_call_damage_add` (group 160)
**Description:** "Units summoned by Heroic Descent and Clone Strike inflict an additional 30% DMG when attacking."

### How It Works

```javascript
// BuffUnitCallDamageAdd.calDamage (Line 196664-196672)
calDamage(baseDamage, target):
    if calType == 0:                          // Storm Necklace uses calType 0
        return roundInt(baseDamage * skillPar)  // skillPar = 0.3 -> +30%
    if calType == 1:                          // Conditional variant
        if target.currentHP% <= threshold:
            return roundInt(baseDamage * skillPar)
    return 0
```

This adds +30% to every hit the spirit (or clone) makes. The bonus is **additive to the base damage**, calculated after normalHurt + NORMAL_ACT_NUM_TRIGGER.

---

## 8. Heroic Descent vs Clone Strike — Side by Side

| Property | Heroic Descent (1048) | Clone Strike (1052) |
|----------|----------------------|---------------------|
| **Quality** | 7 | 8 (higher) |
| **Energy Cost** | 190 (19s to charge) | 290 (29s to charge) |
| **Summon Type** | Unit 4001 (config) | Clone of caster (param1=0) |
| **Targetable?** | **NO** (untargetable) | **YES** (massive taunt) |
| **ATK Multiplier** | L300: x12.63 | L300: x17.0 |
| **att_dam** | 0 + caster skill_dam_extra | Caster full att_dam (snapshotted) |
| **Crit DMG** | 2.0 (fixed) | Caster full crit_dam |
| **ATK Speed** | 3.0 (fixed) | Caster ATK speed |
| **Passive Skills** | 10481 (skill->basic convert) | **NONE** (empty skillList) |
| **Can Stun?** | No (vertigo = 0) | Yes (inherits caster vertigo) |
| **Inherited Attributes** | Only ATK + skill_dam_extra | ALL module-1 attributes |
| **Duration** | 10s base | 10s base |
| **Role** | Untargetable DPS | Targetable tank + DPS |
| **Best With** | Skill DMG stacking classes | Any class |

### Damage Comparison at Endgame

Assumptions: caster ATK = 100M, skill_dam_extra = 25000 (250%), att_dam = 30000 (300%), crit_dam = 80000 (800%), L300 skills.

**Hero Spirit (per crit hit):**
- ATK = 100M x 12.63 = 1,263M
- att_dam = 25000/10000 = 2.5
- crit = max(1.5, 20000/max(5000, target.crit_def)) = 4.0
- Per crit = (1,263M - DEF) x 2.5 x (1-resist) x 4.0

**Clone (per crit hit):**
- ATK = 100M x 17.0 = 1,700M
- att_dam = 30000/10000 = 3.0
- crit = max(1.5, 80000/max(5000, target.crit_def)) = 16.0
- Per crit = (1,700M - DEF) x 3.0 x (1-resist) x 16.0

**Ratio (ignoring DEF):** Clone does `(1700/1263) * (3.0/2.5) * (16.0/4.0)` = **6.45x more damage per crit hit**.

But the clone can be killed. The spirit cannot.

---

## 9. The Prophet Synergy — The Overlooked Interaction

Prophet passive kit creates a unique multiplicative chain with Heroic Descent:

### Prophet Passive Bonuses (Lv70+)

| Passive | Effect on Spirit |
|---------|-----------------|
| Skill Duration +40% | **Spirit lasts 14s instead of 10s -> 42 attacks** |
| Skill DMG +10% | Adds to skill_dam_extra -> spirit att_dam increases |
| Skill Crit +15% | Does NOT transfer (spirit has its own crit stats) |
| Energy Regen +20% | Faster Heroic Descent charges -> more spirit uptime |
| ATK +12% | Increases base ATK -> spirit ATK via param5 |

### The Duration Extension

Spirit lifetime is calculated at line 431598:
```javascript
var l = this.cast.data.getSkillFactAttrValue(n, skillId, T.active_skillbuff_time);
// -> factors in skillbuff_time_all (attribute 1061)
```

Prophet Lv70 passive: `skillbuff_time_all += 4000` (40%). This extends the spirit lifetime from 10s to 14s, yielding 42 attacks instead of 30 — a **40% DPS increase** from a single passive.

### Energy Efficiency

With Prophet +20% Energy Regen:
- Base recovery: 10/s -> effective: 12/s
- Time to charge: 190/12 = **15.8s** (vs 19s without)
- In 120s PvP: ~7 casts x 14s = **98s of spirit uptime** (vs 60s for other classes)
- Spirit uptime ratio: **82%** (vs 50% for other classes)

### Why It Still Falls Short

Even with Prophet synergy:
- Spirit crit_dam is fixed at 2.0 (crit multiplier = 4.0)
- Prophet typically stacks Skill Crit DMG, not basic ATK Crit DMG — the conversion does not help crits
- Clone Strike with any class still deals ~6x more per hit from inherited crit_dam
- Prophet shield-breaking (buff 20046) only works on Prophet own skills, not the spirit attacks
- Clone Strike tanking role (massive taunt draws enemy attacks) is often worth more than raw DPS

---

## 10. The NPC Variant — Zombie Bride Ecosystem

The NPC "Zombie Bride" / "Clone" enemies use a completely different Heroic Descent ecosystem (skills 21018-21033):

### NPC Skill Chain

| Skill | Function | Key Difference from Player |
|-------|----------|---------------------------|
| 21018 | Active summon -> Buff 210018 (call_unit param1=1703602) | Summons config unit, not clone |
| 21020 | Passive -> immune_death buff | **Death immunity** — NPC summon cannot die |
| 21021 | Passive -> hpchange_trigger at 1.1% HP | Near-death triggers (not available to player) |
| 21022 | Active attack skill | NPC-specific attack |
| 21023-21027 | Passive -> periodic auto-summons of unit 1704402 | **Self-replicating** — spawns smaller units over time |

### NPC-Exclusive Buffs

| Buff ID | Effect | Why It Matters |
|---------|--------|---------------|
| 210020 | `immune_death` | The NPC summon literally cannot die |
| 210041 | Taunt value = 9999999999999990 | Extreme aggro — all enemies attack this |
| 210042 | `ignore_buff` with 24 buff IDs | Immune to specific debuffs |

**These mechanics are NOT available to the player Heroic Descent.** The NPC variant is fundamentally different — it is designed as a boss mechanic, not a player skill.

---

## 11. Could Heroic Descent Be Viable? Analysis

### Arguments FOR

1. **Untargetable DPS immunity:** In a meta where Sacred Hunter `pause_cd` locks down skill rotations and Sage trap shields absorb burst, having an untargetable source of constant pressure that cannot be CC'd, paused, or killed has unique value.

2. **Lower energy cost:** 190 vs Clone Strike 290 means 53% faster charge time. More summons per battle.

3. **Skill-damage class synergy:** For Prophet and Darklord who naturally stack skill_dam_extra, the conversion gives "free" basic attack scaling on the spirit without any opportunity cost in build choices.

4. **total_dam_add inheritance:** At endgame with high Final DMG Boost from equipment resonance, this multiplier transfers directly to every spirit hit.

5. **Anti-Sage pressure:** 30-42 attacks over 10-14s provides sustained damage that chips through regenerating shields, rather than burst that gets absorbed.

### Arguments AGAINST (Why Nobody Uses It)

1. **6.45x damage deficit per hit:** Clone Strike inherits caster full att_dam AND crit_dam, giving it dramatically higher per-hit damage. The spirit fixed 2.0 crit_dam and zero base att_dam cannot compete.

2. **Clone tactical value:** Clone Strike creates a target with maximum taunt (999999999999999 + caster.tauntValue), forcing enemies to attack the clone instead of the caster. This tanking function is often worth more than raw DPS.

3. **No buff inheritance:** The spirit gets none of the caster accumulated buffs, mount skills, artifact passives, or equipment effects. Every premium item investment is wasted on the spirit.

4. **Fixed ATK speed:** 3.0 is decent but cannot benefit from ATK speed stacking (Chrono Loop, Thunder Verdict, etc.). The clone inherits the caster ATK speed and benefits from all speed buffs.

5. **No on-hit effects:** The spirit attacks do not trigger the parent STATE_TRIGER, NORMAL_ACT_NUM_TRIGGER, or skill effects. Premium mount/artifact on-hit procs (Sacred Hunter 1% HP per basic, Empyria hit counter) do not activate.

6. **Quality 7 vs 8:** Clone Strike is quality 8, meaning it is inherently prioritized in the skill system and likely has better upgrade paths.

7. **Cannot stun:** vertigo = 0 in unit config eliminates the stun utility that 30 fast attacks could have provided.

### The Verdict

**Heroic Descent is a deliberately designed companion to skill-damage classes, not a general-purpose summon.** Its conversion mechanic (skill_dam_extra -> att_dam) is elegant but insufficient to overcome Clone Strike raw attribute inheritance. The community consensus that "nobody has found a use for it" is essentially correct — not because the skill is broken or bugged, but because Clone Strike objectively outperforms it in every metric except energy cost and untargetability.

The one scenario where Heroic Descent might edge out Clone Strike: **Prophet in a sustained fight against Sage**, where:
- The 14s untargetable spirit provides consistent pressure through Sage shields
- Prophet skill_dam_extra investment naturally feeds the conversion
- The lower energy cost allows more summon uptime (82% vs ~40% for Clone Strike)
- Clone Strike clone would get killed by Sage counter attacks anyway (Sage counter adds 1% target current HP damage)

But even in this niche, the damage output difference is so large that most players correctly choose Clone Strike for its tanking utility.

---

## 12. Summary

| Question | Answer |
|----------|--------|
| Does the Hero Spirit attack? | **Yes.** UnitType 6 provides att_skill=1 (generic normal attack). |
| What determines its damage? | **Caster skill_dam_extra**, converted to att_dam via passive buff 20077. |
| Why is att_dam = 0 in the config? | **By design.** All damage comes from the conversion — no skill_dam_extra = no damage. |
| Can the spirit be killed? | **No.** hatred_type 21 + UnitType target=1 = untargetable. |
| Can the spirit stun? | **No.** vertigo = 0 in unit config. |
| Does it trigger parent on-hit effects? | **No.** All on-hit checks use `r.cast` (spirit), not parent. |
| Does it inherit parent total_dam_add? | **Yes.** Synced every frame in onLastUpdate(). |
| Does Storm Necklace affect it? | **Yes.** +30% via UnitCallDamageAdd from parent. |
| Does Prophet skill duration extend it? | **Yes.** 10s -> 14s (+40%), yielding 42 attacks instead of 30. |
| Is it better than Clone Strike? | **No.** Clone inherits full att_dam + crit_dam -> ~6.45x more damage per hit. |
| Any viable niche? | **Marginal.** Prophet vs Sage sustained fights with high skill_dam_extra investment. |
| Why does nobody use it? | **Correct assessment.** Clone Strike is objectively superior for all practical builds. |
