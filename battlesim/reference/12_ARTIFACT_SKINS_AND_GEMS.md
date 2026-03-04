# 12 — Artifact Skins and Gems

> 19+ artifact skin skills + 7 gem sets with bonuses.

---

## Artifact System Overview

Artifacts provide stats through multiple channels:
1. **Artifact Level** → global attributes + base skills
2. **Artifact Skins** → per-artifact attributes + combat skills
3. **Gem System** → 6 gem slots with main/sub attributes + set bonuses

---

## Artifact Level System

### ConfigArtifact_level (keyed by level)

| Field | Description |
|-------|-------------|
| level | Artifact level |
| expend_exp | EXP cost |
| expend_goods | Material costs |
| attr | Attribute bonuses `[[attrId, value], ...]` |
| base_skill | Skills at this level |
| unlock | Artifact ID unlocked |
| power | Combat power |

**Max stats at Level 300:** 233,740,000 per attribute (ATK/HP/DEF via 2001/2003/2005)

---

## Artifact Skin Skills

### ConfigArtifact_skin (keyed by [artifact_id, skin_level])

| Field | Description |
|-------|-------------|
| artifact_id | Artifact ID |
| skin_level | Skin upgrade level |
| expend | Upgrade cost |
| skin_skill | Combat skills `[[skillId, level], ...]` |
| attr | Attribute bonuses |
| power | Combat power |

### Combat Skills

| Skill ID | Artifact | Max Lv | Effect |
|----------|---------|--------|--------|
| 5101 | Starting | 3 | Stun 1 enemy 2s every 10s, ATK +15% for 3s after stun |
| 5102 | Fire Ring | 3 | 15% chance/ATK: AoE 800% Skill DMG + 5s bleed |
| 5103 | Ice Crystal | 3 | Freeze 1 enemy 3s every 12s; while frozen enemy takes +25% DMG |
| 5104 | Lightning | 3 | Chain lightning every 8s: 600% Skill DMG + ATK SPD -20% for 4s |
| 5105 | Holy Light | 3 | Shield = 15% max HP every 15s; shield break → heal 10% HP |
| 5106 | Shadow | 3 | Every 5 attacks: deal 1200% Skill DMG + steal 5% ATK for 5s |
| 5107 | Nature | 3 | HP regen +3%/5s; below 50% HP: DEF +30%, HP regen doubles |
| 5108 | Void | 3 | 20% chance on hit: ignore 30% DEF for 3s |
| 5109 | Dragon | 3 | Every 15s: 2000% AoE Skill DMG + targets ATK -15% for 5s |
| 5110 | Phoenix | 1 | On death: revive with 30% HP, +50% ATK for 10s (once) |
| 5111 | Celestial | 3 | Crit DMG +30%; every 5 crits: 1500% AoE Skill DMG |
| 5112 | Demon | 3 | Per 10% HP lost: ATK +5% (max +50% at 0% HP) |
| 5113 | Ocean | 3 | Every 10s: restore 8% max HP + cleanse 1 debuff |
| 5114 | Mountain | 3 | Block +50%; on block: DEF +20% for 3s, reflect 300% counter DMG |
| 5115 | Storm | 3 | Combo DMG +40%; every 3 combos: ATK SPD +10% for 5s (cap +30%) |
| 5116 | Eclipse | 3 | Skill DMG +25%; skill kills restore 15% max HP |
| 5118 | Duck Swirl | 1 | 15% per ATK: 20% DMG/s DoT + DEF -6%/stack (cap 8 stacks = -48% DEF) |
| 5120 | Piercing Squail | 3 | +30% Crit Rate; each crit → +2% Final Crit DMG (cap 20 = +40%). At max: 10% chance 1500% AoE |
| 5121-5123 | Invincible Torch | 1-3 | Summon Torch Bearer. After disappear: +5-10% Final Crit DMG, Skill Crit DMG, Pal Crit DMG |
| 5124 | Time Pause | 1 | Per 25% max HP lost: **freeze ALL enemies 2s** (ignores Control Immunity) + ATK +25% |

---

## Gem System

### 6 Gem Slots Per Artifact

| Slot | Main Attribute | Base per Level |
|------|---------------|----------------|
| 1 | HP (1002) | ~3,645 |
| 2 | ATK (1001) | ~160 |
| 3 | DEF (1024) | ~55 |
| 4 | Random (Basic ATK/Combo/Counter/Skill/Pal DMG) | Varies |
| 5 | Random | Varies |
| 6 | Random | Varies |

### Gem Quality Tiers

Gems range from quality 3 (Blue) to quality 8 (Pink):
- Quality determines max level, sub-attribute count, and fodder EXP value
- Max level: up to 20

### ConfigArtifact_gemattr (8 fields)

| Field | Description |
|-------|-------------|
| id | Gem attr ID |
| group_id | Attribute group |
| attr_id | Game attribute ID |
| pro | Probability weight |
| initial_value | Initial value range [min, max] |
| upgrade_value | Value per level [min, max] |
| power_rate | Combat power coefficient |
| color | Quality color range [min_good, max_good] |

### Gem Attribute Color Grading
| Tier | Color | Meaning |
|------|-------|---------|
| 0 | Green (#398760) | Lowest |
| 1 | Blue (#5377b0) | Low |
| 2 | Purple (#9954b6) | Medium |
| 3 | Orange (#ce5913) | Good |
| 4 | Red (#d93535) | Great |
| 5-6 | Pink (#e13a95) | Best |

### Gem Leveling

ConfigArtifact_gemlevel (keyed by [quality, level]):
- `exp` — EXP required per level
- `is_strengthen` — Whether a sub-attribute gets enhanced at this level
- Feed other gems or EXP items as fodder

### Gem Operations
| Protocol | Description |
|----------|-------------|
| artifact_gem_wear_c2s | Equip/unequip gem |
| artifact_gem_up_c2s | Level up (with fodder + lock_attr) |
| artifact_gem_split_c2s | Dismantle for materials |
| artifact_gem_lock_c2s | Toggle lock |
| artifact_gem_sub_c2s | Reduce gem |

---

## 7 Gem Set Bonuses

| Set ID | Name | 2-Piece Bonus | 4-Piece Bonus |
|--------|------|---------------|---------------|
| 101 | Heart of Resilience | Global Counter DMG (2031) +500 | +1,000 |
| 102 | Furious Gale | Global Combo DMG (2030) +500 | +1,000 |
| 103 | Mana Mastery | Global Basic ATK DMG (2023) +500 | +1,000 |
| 104 | Blazing Roar | Global Crit DMG (2009) +500 | +1,000 |
| 105 | Iron Wall | Global Crit RES (2011) +500 | +1,000 |
| 106 | Elemental Wrath | Global Skill DMG (2033) +500 | +1,000 |
| 107 | Common Foe | Pal DMG Bonus (2020) +500 | +1,000 |

### Set Counting Logic
```
For each equipped gem position:
    count set_id occurrences
If count >= 4: apply bonus4_attr + bonus4_skill
If count >= 2: apply bonus2_attr + bonus2_skill
```

### PvP Gem Set Recommendations
| Class | Recommended Set | Reason |
|-------|----------------|--------|
| Warbringer | Heart of Resilience (101) | Counter DMG focus |
| Plume Monarch | Furious Gale (102) | Combo DMG focus |
| Sacred Hunter | Mana Mastery (103) | Basic ATK focus |
| Darklord | Elemental Wrath (106) | Skill DMG focus |
| Beastmaster/Supreme Spirit | Common Foe (107) | Pal DMG focus |
| Universal | Blazing Roar (104) | Crit DMG works for all |
| Defensive | Iron Wall (105) | Crit RES for survival |

---

## Gem Attribute Aggregation

```javascript
getAllGemAttr():
    For each equipped gem:
        sum base_attr[0] by key
        sum each rand_attr by key
    Merge rand_attr into base_attr where keys match
    Return combined array
```

---

## Stat Contribution Flow

```
1. Artifact Level Attributes    → ConfigArtifact_level.attr
2. Artifact Level Skills        → ConfigArtifact_level.base_skill
3. Artifact Skin Attributes     → ConfigArtifact_skin.attr
4. Artifact Skin Skills         → ConfigArtifact_skin.skin_skill
5. Gem Base Attributes          → Main stat per gem
6. Gem Sub Attributes           → Random stats per gem
7. Gem Set Bonuses              → 2-piece and 4-piece bonuses
```
