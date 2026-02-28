# 14 — Class / Job System

## Code Locations
**Config Module:** ConfigJobs.ts
**Lines:** 239943-240110 in `game_script_pretty.js`
**Config Module:** ConfigJobs_wakeup.ts
**Lines:** 239885-239940 in `game_script_pretty.js`

**Related Data:** `data/schemas/ConfigJobs.json`, `data/systems/class_system.json`

---

## Overview

The class/job system defines character archetypes (Warrior, Master, Archer), their skill loadouts, promotion chains, and determines which equipment a character can wear via the `wearable` field. Jobs also have an awakening ("wakeup") system that provides bonus stats at each awakening level.

---

## A. ConfigJobs Schema (28 Fields)

**Source:** `game_script_pretty.js` line 239943

| Field | Index | Type | Description |
|-------|-------|------|-------------|
| id | 0 | number | Unique job ID (e.g., 1001, 1141) |
| name | 1 | string_ref | Localized job name |
| type | 2 | number | Job type/class category -- equipment wearability matches this |
| job_pos | 3 | string_ref | Job position description |
| desc | 4 | string_ref | Job description |
| skill | 5 | optional_array | Active skill IDs |
| passive_skill | 6 | optional_array | Passive skill IDs |
| passive_imprint | 7 | optional_array | Passive imprint skill IDs |
| change_times | 8 | number | Promotion tier count |
| job_change | 9 | optional_array | Available promotion target job IDs |
| model | 10 | number | Unit model ID (references ConfigUnit) |
| fashion | 11 | optional_array | Fashion/appearance data |
| recommend_skill | 12 | optional_array | Recommended skills for this job |
| recommend_pet | 13 | optional_array | Recommended pets |
| transmog_list | 14 | optional_array | Transmog appearances available |
| default_transomg | 15 | optional_array | Default transmog (note: typo in source) |
| arms_icon | 16 | number | Weapon icon ID |
| arms_name | 17 | string_ref | Weapon type name |
| arms_desc | 18 | string_ref | Weapon type description |
| job_desc | 19 | string_ref | Extended job description |
| front_job | 20 | number | Pre-requisite job ID (0 = starting job) |
| unlock | 21 | number | Unlock condition/level |
| scale | 22 | number | Model scale |
| position | 23 | optional_array | Model position offsets |
| job_icon | 24 | number | Job class icon |
| skin | 25 | number | Default skin ID |
| job_sign | 26 | number | Job emblem ID |
| job_class | 27 | number | Higher-level class grouping |

---

## B. Career Types (CareerType Enum)

**Source:** `game_script_pretty.js` line 162822

```javascript
e[e.None = 0] = "None";
e[e.Warrior = 1] = "Warrior";
e[e.Master = 2] = "Master";
e[e.Archer = 3] = "Archer";
```

| Value | Career |
|-------|--------|
| 0 | None |
| 1 | Warrior |
| 2 | Master |
| 3 | Archer |

---

## C. Job Loading in Battle

**Source:** `game_script_pretty.js` lines 187359, 187423

When creating a player unit for battle, the game uses `job_figure` from the player's figure data to look up the job config and determine the unit model:

```javascript
// Line 187359: Creating player unit for battle
var f = configJobs.getDataByKey(t.figure.job_figure).model,
    c = configUnit.getDataByKey(f);
l.config = c, l.name = t.name, l.level = t.lev, l.head = t.head, l.roleId = i.id,
this.setPlayerAttrib(t, l, a),
l.idleIndex = 1,
this.setPlayerEquip(t, l, f, a),
i.units.push(l);
```

The flow is:
1. Read `player.figure.job_figure` (the current job ID)
2. Look up `configJobs.getDataByKey(job_figure)` to get the job config
3. Use `job.model` to get the unit model from `configUnit`
4. Set the unit's visual config, then load attributes, equipment, and skills

---

## D. Equipment Wearability

**Source:** `game_script_pretty.js` line 112151

Equipment items have a `wearable` field that must match the job's `type` field for the item to be equippable. A `wearable` value of 0 means any job can use the item.

```javascript
// Line 112151: Checking equipment wearability
var n = e.wearable || 0;
if (0 == n)
    this.equipItem.txtCarrer.string = "";  // any class can wear
else {
    this.equipItem.txtCarrer.string = I[n];  // show class name
    var o = IS(q).job,
        s = configJobs.getDataByKey(o).type;
    // Color red if current job type doesn't match
    this.equipItem.txtCarrer.color = s == n ? new l(77, 65, 49) : new l(191, 67, 67);
}
```

**Relationship chain:**
```
ConfigEquipment.wearable == ConfigJobs.type
```
- `wearable = 0` --> universal (any class)
- `wearable = N` --> only jobs with `type = N` can equip

---

## E. Job Promotion Chain

Jobs form a promotion chain via two fields:
- `front_job`: the prerequisite job ID (0 for base/starting jobs)
- `job_change`: array of job IDs available for promotion

```
Starting Job (front_job=0)
    |
    +--> [job_change] --> Advanced Job (front_job=starting_id)
                            |
                            +--> [job_change] --> Expert Job (front_job=advanced_id)
```

The `change_times` field indicates which promotion tier the job represents.

---

## F. Job Awakening / Wakeup System

**Config:** ConfigJobs_wakeup (line 239885)

Indexed by `(id, level)` -- the job ID and awakening level.

| Field | Type | Description |
|-------|------|-------------|
| id | number | Job ID reference |
| level | number | Awakening level |
| value_plus | optional_array | Attribute bonuses `[[attr_id, value], ...]` |
| cost | optional_array | Material costs `[[item_id, amount], ...]` |
| power | number | Combat power at this awakening level |

Each awakening level adds cumulative stats to the character. The table is indexed by `[id, level]`, meaning each job has its own set of awakening tiers.

---

## G. Passive Skill Slots

**Source:** `game_script_pretty.js` line 234509

```javascript
job_passive_skill: [1, 1, 2, 3, 4]
```

| Promotion Tier | Passive Skill Slots |
|----------------|-------------------|
| 0 | 1 |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |

---

## H. Skills Setup for Battle

**Source:** `game_script_pretty.js` line 187506

Active skills are set via `setPlayerSkill`:

```javascript
t.setPlayerSkill = function(t, e) {
    e.skillList = e.skillList || [];
    e.skillList.length = 0;
    var a = t.role_skill.active_skill;
    sort(a, function(t, e) { return t.pos_id > e.pos_id; });
    for (var s = 0; s < a.length; s++) {
        var u = a[s];
        if (u.skill_id > 0) {
            u.delay_time = u.delay_time || 0;
            addSkill(e, u.skill_id, u.skill_lv).useDelay = round(u.delay_time / 1000);
        }
    }
    e.ativeSkills = a;
};
```

Passive skills are set via `setPlayerPassiveSkill` (line 187523):

```javascript
t.setPlayerPassiveSkill = function(i, a, r, l) {
    if (i.role_skill.passive_skill) {
        for each passive in i.role_skill.passive_skill {
            if (skill_id > 0) {
                var v = configSkill.getDataByKey(c.skill_id);
                if (checkPvpChapterTypeOk(v.chapter_type, r, v.if_chapter_type)) {
                    addSkill(a, c.skill_id, c.skill_lv);
                }
            }
        }
    }
};
```

Skill types are enumerated at line 278634:
```javascript
e[e.USE = 1] = "USE";                      // Active skill
e[e.PASSIVE_ADD = 2] = "PASSIVE_ADD";      // Passive additive
e[e.PASSIVE_EFFECT = 3] = "PASSIVE_EFFECT";// Passive effect
e[e.PARTNER_SKILL = 4] = "PARTNER_SKILL";  // Pet skill
e[e.FLY_SKILL = 5] = "FLY_SKILL";          // Avian skill
```

---

## Dependencies

- **ConfigUnit** -- Unit model definitions referenced by `job.model`
- **ConfigEquipment** -- Equipment `wearable` field references `job.type`
- **ConfigSkill / ConfigSkill_level** -- Skills referenced by `job.skill`, `job.passive_skill`
- **ConfigAttribute** -- Attributes referenced in `wakeup.value_plus`
- **stat_assembly.json** -- `setPlayerList` uses job figure for initial model lookup

---

## Cross-References

- **Equipment System:** See `15_EQUIPMENT_SYSTEM.md` for how `wearable` interacts with equipment slots
- **Combat System:** See `01_BASIC_DAMAGE_CALCULATION.md` for how job-specific skills affect damage
