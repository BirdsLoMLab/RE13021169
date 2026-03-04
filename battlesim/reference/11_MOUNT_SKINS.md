# 11 — Mount Skins

> 21+ mount skin combat skills with effects, conditions, and damage values.

---

## Overview

Mount skins grant combat skills via `ConfigMount_skin.skin_skill`. Each skin has progressive levels with increasing attribute bonuses and skill unlocks. Mount stats are baked into player attributes before battle — only the cosmetic model is loaded at battle time.

---

## ConfigMount_skin Schema

| Field | Description |
|-------|-------------|
| mount_id | Which mount this skin belongs to |
| skin_level | Skin upgrade level (0 = base) |
| expend | Unlock/upgrade cost |
| skin_skill | Skills granted at this level |
| attr | Attribute bonuses |
| power | Combat power |

---

## Mount Skin Combat Skills

| Skill ID | Mount | Max Lv | Effect |
|----------|-------|--------|--------|
| 5001 | Default | 24 | Evasion +75% |
| 5002 | Pyrebreaker | 3 | Crit Rate +2%/s (cap 40%), Crit DMG +10%/s (cap 200%) |
| 5003 | Hot Wheels | 3 | Pal ATK SPD +3%/s (cap 60%) |
| 5004 | White Tiger | 3 | Targets below your HP% take +30% DMG; above have ATK -20% |
| 5005 | Blue Ox | 3 | DMG RES +15%, Control Duration -50% |
| 5006 | Blue Queen | 1 | Distribute DMG to 5 enemies; +2.5% target max HP every 10s |
| 5007 | Round Frog | 3 | Every 10s kill 1 enemy → ATK +30% for 5s; boss/player stun 1s |
| 5008 | Purple Wing | 3 | 10000% AoE DMG, launches 0.5s, every 11s |
| 5009 | Cloud Drifter | 3 | Skill Crit +20%; after skill crit ATK +40% for 5s |
| 5010 | Kun | 1 | Convert received DMG into DoT over 5s (damage smoothing) |
| 5013 | Cyclone Bamboo | 1 | Shield +3s duration, +50% effect, ATK +10%, Counter +25% under shield |
| 5014 | Velocity Blitz | 3 | Every 1 counter → Global Counter DMG +20% for 3s (cap 60%) |
| 5015 | AdaptoSlime | 1 | After 5% max HP cumulative damage → 500% basic ATK AoE |
| 5016 | Koi Paper Kite | 3 | Every 3 combos → 1000% AoE DMG |
| 5018 | Moon Rabbit-1 | 3 | DMG RES +15%, restore 25% lost HP every 10s |
| 5021 | Blazing Motorcycle | 1 | Per 10% lost HP → flame dealing 500%+ basic ATK DMG |
| 5024 | Immortal Ascent | 1 | **Death Immunity** for 2s + recover 10% max HP (once) |
| 5026 | AdaptoSlime+ | 3 | Below 80% HP: ATK +30%; below 60%: shield 20% HP; below 30%: DMG -20% |
| 5029 | Trembling Pepe | 3 | Alternating 8s buffs: shield 16% HP OR ATK +16% + Control -40% |
| 5030 | Unrivaled Force | 3 | 60% chance/s for 20s: ATK +1.5%, DMG RES +1.5%. After 20s: 16000% AoE + launch |
| 5033 | Neon Shadows | 3 | 3 Guard stacks/11s (DEF +150% each), on expire: 4000% Skill + 1600% Combo + 1600% Counter |
| 5034 | Bite the Watermelon | 3 | ATK +20%, DEF +50% every 11s. Summon wave: 4000% Skill + 1600% Combo + 1600% Counter |

---

## Mount Level System

### ConfigMount_level (keyed by level)

| Field | Description |
|-------|-------------|
| level | Level number |
| name | Level name |
| star | Star rating (1 = milestone unlocking a mount) |
| expend_exp | EXP cost |
| expend_goods | Material costs |
| attr | Attribute bonuses |
| base_skill | Skills unlocked |
| unlock | Mount ID unlocked (0 = none) |
| power | Combat power |

**Max stats at Level 300:** 104,837,000 per attribute (ATK/HP/DEF via 2001/2003/2005)
**EXP Currency:** Item 1008

---

## Mount Ability System (3 Branches)

### ConfigMount_ability (keyed by [id, level])

| Field | Description |
|-------|-------------|
| id | Branch (1, 2, or 3) |
| level | Branch level |
| value_plus | Attribute bonus `[[attrId, value], ...]` |
| power | Combat power |

### Upgrade Mechanics
```
total_level = sum(branch1, branch2, branch3)
cost = ConfigMount_abilitycost(total_level).cost
success_rate = ConfigMount_abilitycost(total_level).success_rate / 100
On success: random branch gains +1
```
**Currency:** Item 1025. Display: `value / 100`%.

---

## Mount Base Config

### ConfigMount Key Fields

| Field | Description |
|-------|-------------|
| min_speed | Minimum movement speed |
| max_speed | Maximum movement speed |
| animation | Animation set |
| mount_location_adjust | Rider position |
| pk_scale | PvP model scale |
| maxNum | Max ownable |
| maxTime | Duration (0 = permanent) |

---

## Battle Integration

Mount stats are **pre-baked** into player attributes:
```javascript
setPlayerMount(player) {
    player.mount = horseDataCache.use_look  // cosmetic only
}
```
Only the cosmetic model is set during battle. All stat bonuses from levels, abilities, and skins are already included in the player's total attributes.

---

## Notable PvP Mount Skills

| Skill | PvP Impact |
|-------|-----------|
| 5001 (Default) | +75% evasion — massive survivability |
| 5005 (Blue Ox) | +15% DMG RES + -50% CC duration — anti-CC tank |
| 5021 (Motorcycle) | HP-loss scaling damage — synergizes with Warbringer |
| 5024 (Immortal Ascent) | Death immunity — 2s invuln + 10% HP |
| 5029 (Pepe) | Alternating shield/ATK — flexible |
| 5030 (Unrivaled Force) | Stacking ATK/RES + massive AoE burst at 20s |
| 5033 (Neon Shadows) | DEF stacking → burst release |
