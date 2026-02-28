# 20 — Mount System (Horse / Wings / Back Decoration)

## Overview

The Mount system is split into two related subsystems:
1. **Horse/Mount** — Rideable mounts with leveling, ability branches, and skins
2. **Back/Wings** — Back decorations (wings) with leveling, talent trees, and skins

Both contribute combat stats to the player. The code internally calls mounts "Horse" (`HorseDataCache`, `HorseControl`, `HorseDefine`).

---

## Config Tables — Mount/Horse

| Table | Source Line | Main Key | Description |
|-------|-----------|----------|-------------|
| ConfigMount | 248453 | id | Base mount definitions (speed, quality, model) |
| ConfigMount_level | 248305 | level | Level progression (EXP, attrs, mount unlocks) |
| ConfigMount_ability | 247718 | id + level | Three ability branches with value_plus |
| ConfigMount_abilitycost | 247770 | total_level | Ability upgrade costs and success rates |
| ConfigMount_skin | 248389 | mount_id + skin_level | Mount skin upgrades (attrs, skills) |
| ConfigMount_chapter | — | — | Chapter/progression milestones |
| ConfigMount_draw | — | — | Mount gacha/draw system |

## Config Tables — Back/Wings

| Table | Source Line | Main Key | Description |
|-------|-----------|----------|-------------|
| ConfigBack_decoration | 220174 | id | Back decoration definitions (model, quality) |
| ConfigBack_level | 220655 | id + level | Level progression (EXP, attrs, era level) |
| ConfigBack_skin | 220827 | back_id + skin_level | Skin upgrades (attrs, skills) |
| ConfigBack_talent | 220891 | id + level | Talent tree nodes (skills, attrs, prerequisites) |

---

## A. Battle Loading — setPlayerMount

### Code (Lines 199066-199067)

```javascript
e.setPlayerMount = function(e) {
    e.mount = IS(S).use_look    // cosmetic mount ID
}
```

**Key insight:** The mount is purely cosmetic in the battle data. Mount stats (from levels, abilities, skins) are already baked into the player's attribute totals before battle begins. The `mount` field only stores which mount model to display.

### Battle Update (Line 201821)

```javascript
this.updateFlag & j.MountUpdate &&
    t.mainCtr && t.mainCtr.player && t.mainCtr.player.modelObj &&
    (IS(b).setPlayerMount(t.mainCtr.player.data),
     t.mainCtr.player.modelObj.mount = t.mainCtr.player.data.mount)
```

When the mount changes during battle, only the cosmetic model is updated.

---

## B. Mount Level System

### Config: ConfigMount_level (Line 248305)

| Field | Description |
|-------|-------------|
| level | Level number |
| name | Level name |
| order | Level tier |
| star | Star rating (1 = milestone that unlocks a mount) |
| expend_exp | EXP to reach next level |
| expend_goods | Material costs |
| attr | Attribute bonuses at this level |
| base_skill | Skills unlocked at this level |
| unlock | Mount ID unlocked (0 = none) |
| power | Combat power |

### Level-Up Logic (Lines 321241-321243)

```javascript
if (null != configMount_level.getDataByKey(IS(e).curLevel + 1)) {
    var n = configMount_level.getDataByKey(IS(e).curLevel + 1).expend_exp;
    if (t >= (n -= IS(e).curexp)) return 1   // can upgrade
}
```

**EXP Currency:** Item ID 1008

### Mount Unlocking (Lines 321224-321227)

```javascript
// Build unlock map: mount_id -> level required
for (var n = configMount_level.getDatas(), i = 0; i < n.length; i++)
    n[i].unlock > 0 && !this.normalMount[n[i].unlock] &&
    (this.normalMount[n[i].unlock] = n[i].level)

// Check state: 1=locked, 2=unlocked, 4=currently equipped
return this.normalMount[t]
    ? t == this.horse_id ? 4
    : this.curLevel >= this.normalMount[t] ? 2
    : 1
    : t == IS(e).horse_id ? 4
    : this.getSkinLevelByID(t) > 0 ? 2
    : 1
```

---

## C. Ability System (Three Branches)

### Config: ConfigMount_ability (Line 247718)

| Field | Description |
|-------|-------------|
| id | Ability branch (1, 2, or 3) |
| level | Ability level |
| value_plus | Attribute bonus array [[attr_id, value], ...] |
| power | Combat power |

### Config: ConfigMount_abilitycost (Line 247770)

| Field | Description |
|-------|-------------|
| total_level | Sum of all branch levels |
| cost | Material cost array |
| success_rate | Success rate (displayed as `rate / 100`%) |
| success_guaranteed | Guaranteed success threshold |

### Upgrade Logic (Lines 321258-321261)

```javascript
var u = configMount_abilitycost.getDatas();
// Check if at max
if (a >= u[u.length - 1].total_level) return 0;
var c = configMount_abilitycost.getDataByKey(a);
// Check if player has enough currency (item 1025)
return IS(r).getGoodsCountByGoodsGtid(1025) >= c.cost[0][1] ? 1 : 0
```

### Display Logic (Lines 321411-321417)

```javascript
var y = configMount_ability.getDataByKeys("id", n, "level", f).value_plus;
l.string = "+" + y[0][1] / 100 + "%";   // displayed as percentage
for (var p = "", b = 0; b < y.length; b++) {
    p += configAttribute.getDataByKey(y[b][0]).name;   // attribute name
    b != y.length - 1 && (p += "&")
}
h.string = p;    // "ATK&DEF" style attribute names
```

**Ability Currency:** Item ID 1025

### Ability Upgrade Process

```
1. total_level = sum(branch_1_level, branch_2_level, branch_3_level)
2. Look up ConfigMount_abilitycost(total_level) → cost, success_rate
3. Pay cost (item 1025)
4. Roll success_rate (value / 100 = percentage shown to player)
5. On success: random branch gains +1 level
6. success_guaranteed provides pity counter for guaranteed success
```

---

## D. Mount Skin System

### Config: ConfigMount_skin (Line 248389)

| Field | Description |
|-------|-------------|
| mount_id | Which mount this skin belongs to |
| skin_level | Skin upgrade level (0 = base) |
| expend | Unlock/upgrade cost array |
| skin_skill | Skills granted at this level |
| attr | Attribute bonuses |
| power | Combat power |

### Skin State Logic (Lines 321229-321231)

```javascript
n.getHorseState = function(t) {
    var n = this.getSkinLevelByID(t),
        i = configMount_skin.getDataByKeys("mount_id", t, "skin_level", n);
    // States: 1=locked, 3=maxed, 4=equipped, 5=can_unlock
    return null == i.expend || 0 == i.expend.length
        ? t == IS(e).horse_id ? 4 : 3
        : 0 == n
            ? IS(r).getGoodsCountByGoodsGtid(i.expend[0][0]) >= i.expend[0][1] ? 5 : 1
            : t == IS(e).horse_id ? 4
            : 0 != i.expend.length && 0 != i.attr.length ? 3 : void 0
}
```

---

## E. Back/Wing Level System

### Config: ConfigBack_level (Line 220655)

| Field | Description |
|-------|-------------|
| id | Back decoration type ID |
| level | Level number |
| expend_exp | EXP cost |
| expend_goods | Material cost array |
| attr | Attribute bonuses |
| power | Combat power |
| era_level | Era/epoch level requirement |
| icon_show | Icon display flag |

The back/wing system uses a separate leveling track from the mount, with its own EXP and materials. The `era_level` field gates certain levels behind overall account progression.

---

## F. Back/Wing Skin System

### Config: ConfigBack_skin (Line 220827)

| Field | Description |
|-------|-------------|
| back_id | Back decoration ID |
| skin_level | Skin upgrade level |
| expend | Upgrade cost array |
| skin_skill | Skills granted at this level |
| attr | Attribute bonuses |
| power | Combat power |

### Skin Skill Loading (Lines 114427-114428)

```javascript
h = configBack_skin.getDataByKeys("back_id", this.skinIDSel, "skin_level", c);
0 == h.skin_skill.length &&
    (h = configBack_skin.getDataByKeys("back_id", this.skinIDSel, "skin_level", c + 1));
```

If the current skin level has no skills, the system looks ahead to the next level for preview.

---

## G. Wing Talent Tree

### Config: ConfigBack_talent (Line 220891)

| Field | Description |
|-------|-------------|
| id | Talent node ID |
| level | Talent level |
| name | Talent name (string_ref) |
| icon | Icon asset |
| job_type | Job/class restriction |
| color_type | Color/rarity indicator |
| describe | Description (string_ref) |
| cost | Upgrade cost array |
| connect_id | Prerequisite talent node(s) |
| condition_1 | First unlock condition |
| condition_2 | Second unlock condition |
| attr | Attribute bonuses at this level |
| skill | Skill granted at this talent level |
| power | Combat power |

### Talent Tree Features

- **Prerequisites:** `connect_id` links talent nodes in a tree structure; a node requires its connected predecessors
- **Job Restrictions:** `job_type` limits which character classes can use certain talents
- **Dual Conditions:** Both `condition_1` and `condition_2` must be met to unlock
- **Progressive Skills:** `skill` field can grant different skills at each talent level
- **15 fields** make this the most complex talent system among companion systems

---

## H. Back Decoration Registry

### Config: ConfigBack_decoration (Line 220174)

| Field | Description |
|-------|-------------|
| id | Decoration ID |
| name | Display name |
| form | Form/shape type |
| type | Decoration category |
| path | Model asset path |
| binds | Bind point array |
| quality | Quality/rarity |
| sort | Sort order |
| back_location_adjust | Position adjustment |
| if_activity | Activity-gated |
| position | Position offset |
| scale | Model scale |

---

## I. Mount Base Config

### ConfigMount (Line 248453)

Key fields for mount behavior:

| Field | Description |
|-------|-------------|
| min_speed | Minimum movement speed |
| max_speed | Maximum movement speed |
| animation | Animation set (determines riding style) |
| mount_location_adjust | Where the rider sits |
| pk_scale | Scale in PvP mode |
| fashion | Fashion/skin variants |
| maxNum | Maximum number a player can own |
| maxTime | Duration (0 = permanent) |

---

## J. Events

### HorseDefine (Lines 321283-321290)

```javascript
E("HorseEvent", {
    TYPE_HORSE_CHANGE: "TYPE_HORSE_CHANGE",
    TYPE_HORSE_SKIN_EFFECT_SEL: "TYPE_HORSE_SKIN_SKILL_SEL",
    TYPE_HORSE_ADD_EXP: "TYPE_HORSE_ADD_EXP",
    TYPE_HORSE_USE_SKILL: "TYPE_HORSE_USE_SKILL",
    TYPE_HORSE_ENABLE_INFO: "TYPE_HORSE_ENABLE_INFO",
    TYPE_HORSE_COLLECT: "TYPE_HORSE_COLLECT"
})
```

Note: `TYPE_HORSE_SKIN_EFFECT_SEL` has value `"TYPE_HORSE_SKIN_SKILL_SEL"` (inconsistent naming in original code).

---

## K. Mount Chapter System (ChapterMount.ts)

### Line 202243

The mount has a dedicated chapter/preview mode (`ChapterMount.ts`) for previewing mount appearances and skills before unlocking them, referenced alongside Wing Preview and Artifact Skin Preview (line 190582).
