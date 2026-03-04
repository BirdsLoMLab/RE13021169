# 11 — Mount Skins

> Complete mount reference: all 23 mount skin combat skills with effects, triggers, coefficients, buff IDs, and PvP notes. See also `mounts_master.json` for structured data.

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

## Complete Mount Skin Combat Skills — Master Reference

### 5001 — Default Mount
| Property | Value |
|----------|-------|
| **Skill ID** | 5001 |
| **Max Level** | 24 |
| **Trigger** | Passive (always active) |
| **Cooldown** | None |
| **Effect** | Evasion bonus (scales with level) |
| **Attribute** | miss (1008): +20% at lv1, +25% at lv2, +30% at lv3, **+75% at lv24** |
| **Duration** | Permanent |
| **PvP Notes** | At max level (+75%), approaches the 80% PvP evasion cap. Massive survivability. |

---

### 5002 — Pyrebreaker
| Property | Value |
|----------|-------|
| **Skill ID** | 5002 |
| **Max Level** | 3 |
| **Trigger** | Time-based (every 1s accumulation) |
| **Cooldown** | 1s per stack |
| **Effect 1** | Crit Rate (1004): +2%/s (200 per stack), cap +40% (4000) |
| **Effect 2** | Crit DMG (1005): +10%/s (1000 per stack), cap +200% (20000) |
| **PvP Notes** | Synergizes with Sacred Hunter (post-crit ATK +40%) and Darklord (skill crit builds). |

---

### 5003 — Hot Wheels
| Property | Value |
|----------|-------|
| **Skill ID** | 5003 |
| **Max Level** | 3 |
| **Trigger** | Time-based (every 1s accumulation) |
| **Cooldown** | 1s per stack |
| **Effect** | Pal ATK Speed (1003): +3%/s (300 per stack), cap +60% (6000) |
| **Target** | Pal only |
| **PvP Notes** | Best for Beastmaster/Supreme Spirit pal-focused builds. |

---

### 5004 — White Tiger
| Property | Value |
|----------|-------|
| **Skill ID** | 5004 |
| **Max Level** | 3 |
| **Trigger** | Combat condition (HP% comparison per hit) |
| **Cooldown** | None |
| **Buff Group** | ATTRIB_CONDITION (80) |
| **Effect 1** | Target HP% < your HP% → +30% damage to target |
| **Effect 2** | Target HP% > your HP% → -20% ATK on target |
| **PvP Notes** | Dynamic scaling. Punishes tanks (more HP than you) AND glass cannons (less HP). |

---

### 5005 — Blue Ox
| Property | Value |
|----------|-------|
| **Skill ID** | 5005 |
| **Max Level** | 3 |
| **Trigger** | Passive (always active) |
| **Cooldown** | None |
| **Effect 1** | DMG Resistance (1021): +15% (1500) |
| **Effect 2** | Control Duration: -50% (5000) |
| **PvP Notes** | Anti-CC tank mount. Strong against stun/freeze-heavy opponents. |

---

### 5006 — Blue Queen
| Property | Value |
|----------|-------|
| **Skill ID** | 5006 |
| **Max Level** | 1 |
| **Trigger** | Time-based periodic (every 10s) |
| **Cooldown** | 10s |
| **Effect 1** | Distribute damage to 5 nearby enemies |
| **Effect 2** | 2.5% target max HP damage (250) |
| **PvP Notes** | Good for PvE. In PvP, the HP% damage is useful vs high-HP tanks. |

---

### 5007 — Round Frog
| Property | Value |
|----------|-------|
| **Skill ID** | 5007 |
| **Max Level** | 3 |
| **Trigger** | Kill trigger (every 10s check) |
| **Cooldown** | Per kill |
| **Effect 1** | On kill: ATK (1001) +30% (3000) for 5s |
| **Effect 2** | On boss/player kill: Stun (dizz) 1s |
| **PvP Notes** | PvE-focused (needs kills). In PvP, only boss kill stun is relevant. |

---

### 5008 — Purple Wing
| Property | Value |
|----------|-------|
| **Skill ID** | 5008 |
| **Max Level** | 3 |
| **Trigger** | Time-based periodic (every 11s) |
| **Cooldown** | 11s |
| **Effect 1** | 10000% AoE Skill damage (coefficient: 100000 = 100x basic ATK) |
| **Effect 2** | Launch (throw_hit) 0.5s airborne |
| **PvP Notes** | Strong periodic burst. 100x basic ATK every 11s is significant sustained DPS. |

---

### 5009 — Cloud Drifter
| Property | Value |
|----------|-------|
| **Skill ID** | 5009 |
| **Max Level** | 3 |
| **Trigger** | Skill crit (after skill critical hit) |
| **Cooldown** | Per skill crit |
| **Effect 1** | Skill Crit Rate (1037): +20% (2000) passive |
| **Effect 2** | On skill crit: ATK (1001) +40% (4000) for 5s |
| **PvP Notes** | S-tier for Darklord (+50% skill crit passive stacks). Good for Prophet. |

---

### 5010 — Kun
| Property | Value |
|----------|-------|
| **Skill ID** | 5010 |
| **Max Level** | 1 |
| **Trigger** | On damage received |
| **Cooldown** | None |
| **Buff Group** | DEFER_DAMAGE (400) |
| **Effect** | Convert received burst damage into DoT over 5s (damage smoothing) |
| **PvP Notes** | DEFER_DAMAGE has NO PvP decay — very efficient. Good vs burst builds. |

---

### 5013 — Cyclone Bamboo
| Property | Value |
|----------|-------|
| **Skill ID** | 5013 |
| **Max Level** | 1 |
| **Trigger** | Conditional (while shielded) |
| **Cooldown** | None |
| **Effect 1** | Shields last +3s longer, +50% (5000) stronger |
| **Effect 2** | ATK (1001): +10% (1000) |
| **Effect 3** | Counter (1017): +25% (2500) while shielded |
| **PvP Notes** | Synergizes with Martial Sage (8% HP shield passive) and Prophet (shield-related skills). |

---

### 5014 — Velocity Blitz
| Property | Value |
|----------|-------|
| **Skill ID** | 5014 |
| **Max Level** | 3 |
| **Trigger** | Counter trigger (every counter-attack) |
| **Cooldown** | Per counter |
| **Effect** | Global Counter DMG (2031): +20% (2000) per counter, 3s duration, cap 60% (6000, 3 stacks) |
| **PvP Notes** | S-tier for Warbringer (+30% counter rate, +140% counter DMG passive). |

---

### 5015 — AdaptoSlime
| Property | Value |
|----------|-------|
| **Skill ID** | 5015 |
| **Max Level** | 1 |
| **Trigger** | HP threshold (cumulative 5% max HP damage taken) |
| **Cooldown** | Resets after trigger |
| **Effect** | 500% AoE damage (coefficient: 50000 = 5x basic ATK) |
| **PvP Notes** | Frequent proc in PvP due to constant damage. Consistent AoE output. |

---

### 5016 — Koi Paper Kite
| Property | Value |
|----------|-------|
| **Skill ID** | 5016 |
| **Max Level** | 3 |
| **Trigger** | Combo count (every 3 combo hits) |
| **Cooldown** | Per 3-combo cycle |
| **Buff Group** | DOUBLE_TRIGGER (170) |
| **Buff IDs** | 30003, 51141 |
| **Effect** | 1000% AoE damage (coefficient: 100000 = 10x basic ATK) every 3 combos |
| **PvP Notes** | S-tier for Plume Monarch (+30% combo rate, +3 extra combo bullets, +140% combo DMG). |

---

### 5018 — Moon Rabbit
| Property | Value |
|----------|-------|
| **Skill ID** | 5018 |
| **Max Level** | 3 |
| **Trigger** | Time-based periodic (every 10s) |
| **Cooldown** | 10s |
| **Effect 1** | DMG Resistance (1021): +15% (1500) passive |
| **Effect 2** | Restore 25% of lost HP every 10s (2500) |
| **PvP Notes** | Sustain mount. Good for Martial Sage. Heal affected by 30% PvP treatDecay. |

---

### 5021 — Blazing Motorcycle
| Property | Value |
|----------|-------|
| **Skill ID** | 5021 |
| **Max Level** | 1 |
| **Trigger** | HP-loss scaling (continuous) |
| **Cooldown** | None |
| **Effect** | Per 10% HP lost → 500% basic ATK damage (coefficient: 50000). At 50% HP = 2500% DMG. |
| **PvP Notes** | S-tier for Warbringer (ATK +3% per 10% HP lost stacks). Synergizes with any HP-loss scaling. |

---

### 5024 — Immortal Ascent
| Property | Value |
|----------|-------|
| **Skill ID** | 5024 |
| **Max Level** | 1 |
| **Trigger** | Death trigger (when HP would reach 0) |
| **Cooldown** | Once per combat |
| **Buff Group** | IMMUNE_DEATH (230) |
| **Effect 1** | 2s invulnerability on lethal damage |
| **Effect 2** | Recover 10% max HP (1000) |
| **PvP Notes** | Ultimate survival. 2s of invulnerability can turn fights. One-time use. |

---

### 5026 — AdaptoSlime+
| Property | Value |
|----------|-------|
| **Skill ID** | 5026 |
| **Max Level** | 3 |
| **Trigger** | Dynamic HP% thresholds (80%, 60%, 30%) |
| **Cooldown** | None |
| **Buff Group** | ATTRIB_CONDITION (80), SHIELD (20) |
| **Effect 1** | HP < 80%: ATK (1001) +30% (3000) |
| **Effect 2** | HP < 60%: Shield = 20% max HP (2000) |
| **Effect 3** | HP < 30%: Incoming DMG -20% (2000) |
| **PvP Notes** | Three-tier survival. Each tier activates as HP drops, providing layered defense. |

---

### 5029 — Trembling Pepe
| Property | Value |
|----------|-------|
| **Skill ID** | 5029 |
| **Max Level** | 3 |
| **Trigger** | Time-based alternating (every 8s) |
| **Cooldown** | 8s cycle |
| **State 1** | Shield = 16% max HP (1600) — Buff Group SHIELD (20) |
| **State 2** | ATK (1001) +16% (1600) + Control Duration -40% (4000) |
| **PvP Notes** | Flexible utility mount. Good all-around for any class. |

---

### 5030 — Unrivaled Force
| Property | Value |
|----------|-------|
| **Skill ID** | 5030 |
| **Max Level** | 3 |
| **Trigger** | Probabilistic time-based (60% chance/s for 20s, then burst) |
| **Cooldown** | 1s interval / 20s phase |
| **Phase 1** | 60% chance/s (6000): ATK (1001) +1.5% (150) + DMG RES (1021) +1.5% (150) per proc. Max 20 stacks = +30% each. |
| **Phase 2** | After 20s: 16000% AoE (coefficient: 1600000 = 160x basic ATK) + launch (throw_hit) 0.5s |
| **PvP Notes** | Massive 20s burst. If fight lasts 20s, 160x AoE can one-shot. Stacking phase provides good sustain. |

---

### 5033 — Neon Shadows
| Property | Value |
|----------|-------|
| **Skill ID** | 5033 |
| **Max Level** | 3 |
| **Trigger** | Time-based periodic (every 11s accumulation) |
| **Cooldown** | 11s cycle |
| **Phase 1** | 3 Guard stacks: DEF (1024) +150% (15000) each = +450% DEF total |
| **Phase 2** | On expire: 4000% Skill (400000) + 1600% Combo (160000) + 1600% Counter (160000) |
| **PvP Notes** | Defense-into-burst mount. Near-unkillable during Guard phase, then big damage release. |

---

### 5034 — Bite the Watermelon
| Property | Value |
|----------|-------|
| **Skill ID** | 5034 |
| **Max Level** | 3 |
| **Trigger** | Time-based periodic (every 11s) |
| **Cooldown** | 11s |
| **Effect 1** | ATK (1001) +20% (2000), DEF (1024) +50% (5000) every 11s |
| **Effect 2** | Summon wave: 4000% Skill (400000) + 1600% Combo (160000) + 1600% Counter (160000) |
| **PvP Notes** | Periodic multi-hit mount. Similar burst to Neon Shadows but with ATK/DEF buff instead of Guard stacking. |

---

### 5057 — Life and Death Speed (Motorcycle, Mount ID 404)
| Property | Value |
|----------|-------|
| **Skill ID** | 5057 |
| **Mount ID** | 404 |
| **Max Level** | 3 |
| **Trigger** | 3-phase cycle |
| **Passive** | Evasion (1008): +20/25/30% by level (2000/2500/3000) |

**Phase 1 — Speed Stacking:**

| Combat Event | Stacks Per | Every N Events | Buff ID |
|-------------|-----------|----------------|---------|
| Evade | 1 | 1 | 50610 |
| Normal Attack | 1 | 8 | 50611 |
| Combo | 1 | 8 | 50612 |
| Counter | 1 | 8 | 50613 |
| Skill | 1 | 2 | 50614 |

Speed buff (50609): +8% (800) movement speed per stack, 50 max stacks.

**Phase 2 — Overdrive (at 200% speed / buff 50615):**

| Buff ID | Effect |
|---------|--------|
| 50621 | 18% Trap AoE |
| 50622 | 18% DMG RES |
| 50623 | 20% ATK |
| 50624 | 20% DEF |
| 50625 | 20% ATK Speed |
| 50626 | 20% Power Recovery |
| 50631 | CC Immunity (5s) |

Overdrive skill: 50573. Duration: 5s.

**Phase 3 — Reset:**
Reset buff 50629, clear buff 50630. All stacks cleared, restart Phase 1.

| **PvP Notes** | S-tier mount. Synergizes extremely well with Sacred Hunter (evasion feeds speed stacks) and Martial Sage (counter feeds stacks + tankiness survives stacking phase). |
|---------------|---|

---

## Quick Reference — All Mount Skills Summary

| Skill ID | Mount | Max Lv | Trigger | Key Effect | PvP Tier |
|----------|-------|--------|---------|------------|----------|
| 5001 | Default | 24 | Passive | Evasion +75% | A |
| 5002 | Pyrebreaker | 3 | Time | Crit Rate/DMG stacking | B |
| 5003 | Hot Wheels | 3 | Time | Pal ATK SPD +60% | B (pal builds) |
| 5004 | White Tiger | 3 | Condition | HP%-based DMG/debuff | B |
| 5005 | Blue Ox | 3 | Passive | DMG RES +15%, CC -50% | A |
| 5006 | Blue Queen | 1 | 10s | AoE spread + HP% DMG | C |
| 5007 | Round Frog | 3 | Kill | ATK +30% on kill | C (PvE) |
| 5008 | Purple Wing | 3 | 11s | 10000% AoE + launch | B |
| 5009 | Cloud Drifter | 3 | Skill crit | Skill Crit +20%, ATK +40% | S (Darklord) |
| 5010 | Kun | 1 | On DMG | DEFER_DAMAGE smoothing | A |
| 5013 | Cyclone Bamboo | 1 | Shielded | Shield buff + counter | B |
| 5014 | Velocity Blitz | 3 | Counter | Counter DMG +60% cap | S (Warbringer) |
| 5015 | AdaptoSlime | 1 | HP threshold | 500% AoE on 5% HP dmg | B |
| 5016 | Koi Paper Kite | 3 | 3 combos | 1000% AoE per 3 combos | S (Plume Monarch) |
| 5018 | Moon Rabbit | 3 | 10s | DMG RES +15%, heal 25% | B |
| 5021 | Blazing Motorcycle | 1 | HP loss | 500%/10% HP lost | S (Warbringer) |
| 5024 | Immortal Ascent | 1 | Death | 2s invuln + 10% HP | A |
| 5026 | AdaptoSlime+ | 3 | HP thresholds | 3-tier ATK/shield/DR | A |
| 5029 | Trembling Pepe | 3 | 8s alt | Shield OR ATK+CC-resist | A |
| 5030 | Unrivaled Force | 3 | 20s phase | Stack → 16000% AoE burst | S |
| 5033 | Neon Shadows | 3 | 11s | DEF stack → burst release | S |
| 5034 | Bite the Watermelon | 3 | 11s | ATK/DEF + summon wave | A |
| 5057 | Motorcycle | 3 | 3-phase | Speed stack → overdrive | S |

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

### ConfigMount Key Fields (24 total)

| Field | Description |
|-------|-------------|
| id | Mount ID |
| name | Display name (string_ref) |
| type | Category |
| min_speed | Minimum movement speed |
| max_speed | Maximum movement speed |
| quality | Rarity tier |
| animation | Animation set |
| mount_location_adjust | Rider position |
| pk_scale | PvP model scale |
| maxNum | Max ownable |
| maxTime | Duration (0 = permanent) |
| fashion | Fashion/skin data |
| power | Base combat power |

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

## Class Synergies — Best Mount Per Class

| Class | Best Mount(s) | Reason |
|-------|--------------|--------|
| Martial Sage | Motorcycle, Cyclone Bamboo | Counter feeds speed stacks; shield synergy |
| Warbringer | Blazing Motorcycle, Velocity Blitz | HP-loss scaling; counter DMG stacking |
| Sacred Hunter | Motorcycle, Default | Evasion feeds speed stacks; raw evasion |
| Plume Monarch | Koi Paper Kite | Combo rate + extra bullets feed combo AoE |
| Prophet | Cloud Drifter, Cyclone Bamboo | Skill crit synergy; shield enhancement |
| Darklord | Cloud Drifter | Skill crit rate +20% stacks with +50% passive |
| Beastmaster | Hot Wheels | Pal ATK speed for pal-focused builds |
| Supreme Spirit | Hot Wheels, Unrivaled Force | Pal speed or late-game burst |

---

## Data Files

- **Structured data**: `battlesim/reference/mounts_master.json` — Complete JSON with all skill data, coefficients, buff IDs, and metadata
- **Config schemas**: ConfigMount (24 fields), ConfigMount_skin (6), ConfigMount_level (10), ConfigMount_ability (4), ConfigMount_abilitycost (4)
