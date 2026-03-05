# 15 — Angels / Star Heroes (Guardian Spirits)

> Complete Angel system reference: formation, battle skills, star progression, energy pool, gacha, and all 33 Star Heroes with full skill descriptions. Internally uses `ConfigAngel` tables.

---

## Overview

Angels ("Guardian Spirits" / "Star Heroes") are companion units that boost player stats, contribute battle skills, and provide passive development effects. They are organized into a typed formation with an energy budget system, star-upgraded for power growth, and acquired through a gacha draw system.

**No XOR encoding** — all Angel config tables have `usesConfigKey: false`. The only indirect XOR relevance is that angel skills chain through ConfigSkill_level -> ConfigSkilleffcet -> ConfigBuff (all also non-XOR), and stat bonuses reference AttribDefine attribute IDs.

---

## Formation System

### ConfigAngel_array
| Field | Description |
|-------|-------------|
| type | Formation type |
| pos | Slot position (1-based) |
| pos_type | Angel type allowed in this slot |

### Two Formation Groups

**Main Slots (1-3):** Contribute battle skills directly
- Slot 1: Primary slot with Skill 1 (type=1)
- Slots 2-3: Use Skill 2 from ConfigAngel_skill (type=2)

**Development Slots (1-4):** Provide passive development bonuses (type=0)

- `pos_type` must match `angel.type` for placement
- Star progression unlocks skills and development effects via `ConfigAngel_star`

### Energy Pool
All angel skills share a single energy pool:
```
all_cost1 = sum of battle_skill1_cost + battle_skill2_cost for main slots
all_cost2 = sum of develop_cost for development slots
Display: cost + "/" + maxBudget
```

---

## Config Tables

### ConfigAngel (9 fields)

| Field | Idx | Type | Description |
|-------|-----|------|-------------|
| id | 0 | number | Angel identifier |
| name | 1 | string_ref | Localized name |
| quality | 2 | number | Rarity tier (1-5) |
| type | 3 | number | Type class (formation slot matching) |
| desc | 4 | string_ref | Description |
| image | 5 | number | Primary portrait asset |
| image2 | 6 | number | Secondary portrait asset |
| image3 | 7 | number | Icon asset (used in skill display UI) |
| open_time | 8 | optional_array | Availability window |

### ConfigAngel_star (16 fields, keyed by [id, star])

| Field | Idx | Type | Description |
|-------|-----|------|-------------|
| id | 0 | number | Angel ID (FK -> ConfigAngel) |
| star | 1 | number | Star level |
| expend | 2 | optional_array | Upgrade cost `[[itemId, count], ...]` |
| frame | 3 | number | UI frame asset |
| attr | 4 | optional_array | Stat bonuses `[[attrId, value], ...]` |
| skill1_type | 5 | number | Skill 1 category (1=active, 2=passive, 3=aura) |
| battle_skill1 | 6 | optional_array | Skill 1 `[[skillId, skillLevel]]` -> ConfigSkill_level |
| battle_skill1_cost | 7 | number | Energy cost |
| skill2_type | 8 | number | Skill 2 category |
| battle_skill2 | 9 | number | Skill 2 ID -> ConfigAngel_skill |
| battle_skill2_cost | 10 | number | Energy cost |
| develop_effect | 11 | optional_array | Development passive data |
| develop_desc | 12 | string_ref | Development description template |
| develop_desc_num | 13 | optional_array | Description format parameters |
| develop_cost | 14 | number | Development energy cost |
| power | 15 | number | Combat power contribution |

### ConfigAngel_skill (6 fields)

| Field | Idx | Type | Description |
|-------|-----|------|-------------|
| id | 0 | number | Skill ID |
| skill_name | 1 | string_ref | Localized name |
| skill_effect | 2 | optional_array | Effect IDs -> ConfigSkilleffcet chain |
| skillPar | 3 | optional_array | Damage coefficients (passed to buff/effect system) |
| skill_dec | 4 | string_ref | Description template |
| desc_parm | 5 | optional_array | Description format parameters |

---

## Skill System

### Skill Slot 1
- References standard ConfigSkill + ConfigSkill_level
- Lookup: `configSkill_level.getDataByKeys("id", skillId, "level", skillLevel)`
- `skill1_type` determines visual badge (1=active, 2=passive, 3=aura)
- ConfigSkill_level.skillCoefficient contains effect IDs (pre-processed coefficients routed through the passive skill engine, not XOR-encoded)

### Skill Slot 2
- References ConfigAngel_skill directly
- Lookup: `configAngel_skill.getDataByKey(battle_skill2)`
- Description rendered as: `formatStr(skill_dec, ...desc_parm)`

```javascript
// Line ~305509: Skill 2 lookup
var r = configAngel_skill.getDataByKey(s.battle_skill2);
r ? this.skill_list[2].desc.string = formatStr(r.skill_dec, ...r.desc_parm)
  : this.skill_list[2].desc.string = "";
this.skill_list[2].cost.string = "cost " + d;
```

### Combat Integration

1. **Skill 1** enters standard skill execution pipeline (see `05_ACTIVE_SKILLS.md`)
2. **Skill 2** triggers via ConfigAngel_skill.skill_effect -> ConfigSkilleffcet chain
3. **Development effects** apply as passive modifiers
4. **Star attrs** added to player's combat attributes

---

## Gacha / Draw System

### Permanent Banners (ConfigAngel_draw, 11 fields)
| Field | Description |
|-------|-------------|
| id | Banner ID |
| name | Display name |
| type | Banner type |
| cost/cost2 | Single/multi pull costs |
| prob | Quality tier probabilities |
| must | Pity thresholds |

### Limited-Time Banners (ConfigAngel_draw_time_limit, 18 fields)
Adds rate-up mechanics:
- `is_up` — rate-up active flag
- `prob_up` — rate-up probabilities
- `up_reward` — featured angel rewards
- `special_rewards_times` — special reward trigger count

### Milestone Rewards (ConfigAngel_draw_package, 7 fields)
- `premise` — pull count threshold
- `reward` — reward items `[[itemId, count], ...]`

---

## All 33 Star Heroes

### Config ID Quick Reference

| # | Name | angel_id | Type | Skill IDs | Rarity | Limited |
|---|------|----------|------|-----------|--------|---------|
| 1 | Divine Warbringer | 30001 | 3 (Legendary) | 27021 | SSR | — |
| 2 | Storm Dominion | 30002 | 3 (Legendary) | 27022 | SSR | — |
| 3 | Barbarian Overlord | 30003 | 3 (Legendary) | 27024 | SSR | — |
| 4 | Holy Defender | 30004 | 3 (Legendary) | 27023 | SSR | — |
| 5 | Genie of Wishes | 30005 | 3 (Legendary) | 27025 | SSR | — |
| 6 | Lord of Champions | 30007 | 3 (Legendary) | 27030 | SSR | Yes |
| 7 | Spirit Harbinger | 20001 | 2 (Rare) | 27012 | SR | — |
| 8 | Mentor of Wisdom | 20002 | 2 (Rare) | 27013 | SR | — |
| 9 | Chrono Sprite | 20003 | 2 (Rare) | *(none)* | SR | — |
| 10 | Knight of Light | 20004 | 2 (Rare) | 27015 | SR | — |
| 11 | Beast Soul Guardian | 20005 | 2 (Rare) | 27016 | SR | — |
| 12 | Void Guide | 20006 | 2 (Rare) | 27017,270171-9 | SR | — |
| 13 | Defender of Order | 20007 | 2 (Rare) | 27018 | SR | — |
| 14 | Biosphere Guardian | 20008 | 2 (Rare) | 27019 | SR | — |
| 15 | Nature's Keeper | 20009 | 2 (Rare) | 27020 | SR | — |
| 16 | Goddess of Victory | 20011 | 2 (Rare) | *(none)* | SR | Yes |
| 17 | Sprite of Knowledge | 10001 | 1 (Common) | 27001 | R | — |
| 18 | Intrepid Fowl | 10002 | 1 (Common) | 27002 | R | — |
| 19 | Jolly Greenhorn | 10003 | 1 (Common) | 27003 | R | — |
| 20 | Vanguard Urchin | 10004 | 1 (Common) | 27004 | R | — |
| 21 | Faithful Guardian | 10005 | 1 (Common) | *(none)* | R | — |
| 22 | Blossom Harbinger | 10006 | 1 (Common) | *(none)* | R | — |
| 23 | Harvest Harbinger | 10007 | 1 (Common) | *(none)* | R | — |
| 24 | Dome Watcher | 10008 | 1 (Common) | 27008 | R | — |
| 25 | Valiant Soulknight | 10009 | 1 (Common) | 27009 | R | — |
| 26 | Stoneborn Warrior | 10010 | 1 (Common) | 27010 | R | — |
| 27 | Shadow Keeper | 10011 | 1 (Common) | 27011 | R | — |
| 28 | Puppy Squad | 30006 | 3 (Legendary) | 270271-270280 | SSR | Yes |
| 29 | Sakura Star Envoy | 20010 | 2 (Rare) | 27026 | SR | Yes |
| 30 | King | 30013 | 3 (Legendary) | 27041 | SSR | Yes |
| 31 | Hellish Blizzard | 20020 | 2 (Rare) | 27040 | SR | Yes |
| 32 | Gold Snow Roll | 30014 | 3 (Legendary) | 27042 | SSR | Yes |
| 33 | Leaf Fox | 20021 | 2 (Rare) | 27043 | SR | Yes |
| — | *Anubis* | 20022 | 2 (Rare) | *(config-only)* | — | Yes |
| — | *Zoe & Grizzbolt* | 30015 | 3 (Legendary) | *(config-only)* | — | Yes |

> **Angel Types**: 1=Common (R), 2=Rare (SR), 3=Legendary (SSR)
> **Skill IDs**: Reference `ConfigAngel_skill` table. Skills 27xxx are angel-specific battle skills.
> **Config-only**: Anubis and Zoe & Grizzbolt exist in ConfigAngel but not in the xlsx.

---

## Full Hero Details

### Summary Table

| # | Name | Rarity | Cost | Main Type | Support Type | Limited | Impl |
|---|------|--------|------|-----------|-------------|---------|------|
| 1 | **Divine Warbringer** | SSR | 4 | Active | Active | — | Yes |
| 2 | **Storm Dominion** | SSR | 4 | Active | Active | — | Yes |
| 3 | **Barbarian Overlord** | SSR | 4 | Active | Active | — | Yes |
| 4 | **Holy Defender** | SSR | 4 | Active | Active | — | Yes |
| 5 | **Genie of Wishes** | SSR | 3 | Passive | None | — | Yes |
| 6 | **Lord of Champions** | SSR | 4 | Active | Active | Yes | Yes |
| 7 | **Spirit Harbinger** | SR | 3 | Active | Active | — | Yes |
| 8 | **Mentor of Wisdom** | SR | 3 | Passive | Passive | — | Yes |
| 9 | **Chrono Sprite** | SR | — | None | Active | — | Yes |
| 10 | **Knight of Light** | SR | 3 | Shield | Shield | — | Yes |
| 11 | **Beast Soul Guardian** | SR | 3 | Passive | Passive | — | Yes |
| 12 | **Void Guide** | SR | 3 | Active | Active | — | Yes |
| 13 | **Defender of Order** | SR | 3 | Shield | Shield | — | Yes |
| 14 | **Biosphere Guardian** | SR | 3 | Passive | Passive | — | Yes |
| 15 | **Nature's Keeper** | SR | 3 | Passive | Passive | — | Yes |
| 16 | **Goddess of Victory** | SR | 3 | None | Shield | Yes | Yes |
| 17 | **Sprite of Knowledge** | R | 2 | Active | Passive | — | Yes |
| 18 | **Intrepid Fowl** | R | 2 | Active | Shield | — | Yes |
| 19 | **Jolly Greenhorn** | R | 2 | Active | Active | — | Yes |
| 20 | **Vanguard Urchin** | R | 2 | Passive | Passive | — | Yes |
| 21 | **Faithful Guardian** | R | — | None | Passive | — | Yes |
| 22 | **Blossom Harbinger** | R | — | None | Passive | — | Yes |
| 23 | **Harvest Harbinger** | R | — | None | Passive | — | Yes |
| 24 | **Dome Watcher** | R | 2 | Passive | Shield | — | Yes |
| 25 | **Valiant Soulknight** | R | 2 | Passive | Passive | — | Yes |
| 26 | **Stoneborn Warrior** | R | 2 | Shield | Active | — | Yes |
| 27 | **Shadow Keeper** | R | 2 | Active | Shield | — | Yes |
| 28 | **Puppy Squad** | SSR | 4 | Active | Active | Yes | No |
| 29 | **Sakura Star Envoy** | SR | 3 | Shield | None | Yes | No |
| 30 | **King** | SSR | 4 | Active | Passive | Yes | No |
| 31 | **Hellish Blizzard** | SR | 3 | Active | Active | Yes | No |
| 32 | **Gold Snow Roll** | SSR | 4 | Active | Shield | Yes | No |
| 33 | **Leaf Fox** | SR | 3 | Shield | Shield | Yes | No |

---

### 1. Divine Warbringer

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Every 15s after the battle starts, deals AoE DMG equal to 5% of Max HP.

**Support Skill [Active]:** Releasing the main active skill increases DMG RES by 4% for 5s.

---

### 2. Storm Dominion

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Every 16s after the battle starts, deals 500% of current AoE Basic ATK DMG (can be Crit), and every Crit hit within 5s deals extra DMG equal to 0.4% of targets' current HP.

**Support Skill [Active]:** Releasing the main active skill reduces Basic ATK DMG RES by 6% for 5s.

---

### 3. Barbarian Overlord

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Every 16s after the battle starts, 3 random Pals gain 8% of Combo Multiplier and 8% of Final Crit DMG for 5s.

**Support Skill [Active]:** Releasing the main active skill reduces targets' ATK by 8% for 5s.

---

### 4. Holy Defender

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Every 14s after the battle starts, deals 1500% of AoE Skill DMG, and targets take 400% of Bleed Skill DMG per second for 5s, ignoring immunity.

**Support Skill [Active]:** Releasing the main active skill reduces targets' DMG RES by 5% for 5s.

---

### 5. Genie of Wishes

**Rarity:** SSR | **Cost:** 3

**Main Skill [Passive]:** After the battle starts, gains 4% of ATK and 12% of DEF until the battle ends.

**Support Skill [None]:** No Support Effect

---

### 6. Lord of Champions (Limited)

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** After the battle starts, summon a thunderstorm every 15s, dealing 1500% of Bleed Skill DMG and stunning the target for 1.5s, ignoring immunity.

**Support Skill [Active]:** Releasing the main active skill shortens the CD of Active Skills on cooldown by 1s and increases Final Skill DMG by 12% for 5s.

---

### 7. Spirit Harbinger

**Rarity:** SR | **Cost:** 3

**Main Skill [Active]:** Every 16s after the battle starts, all Pals gain 4% of Crit Rate and 200% of Base Crit DMG for 8s.

**Support Skill [Active]:** Releasing the main active skill grants all Pals 4% of Combo Rate for 7s.

---

### 8. Mentor of Wisdom

**Rarity:** SR | **Cost:** 3

**Main Skill [Passive]:** After the battle starts, releasing 10 active skills deals 3200% of AoE Skill DMG and increases Final Skill Crit DMG by 7.5% for 12s (triggered only once).

**Support Skill [Passive]:** Releasing the main passive skill increases Skill Crit Rate by 2.5% and Base Skill Crit DMG by 15% until the battle ends.

---

### 9. Chrono Sprite

**Rarity:** SR | **Cost:** —

**Main Skill [None]:** No Main Effect

**Support Skill [Active]:** Releasing the main active skill stuns targets for 0.5.

---

### 10. Knight of Light

**Rarity:** SR | **Cost:** 3

**Main Skill [Shield]:** Every 16s after the battle starts, gains a shield that absorbs 8% of Max HP for 5s. When taking Basic ATK DMG, the shield reduces ATK by 5% for 2s for targets within the range.

**Support Skill [Shield]:** Releasing the main shield skill regenerates 7.5% of lost HP.

---

### 11. Beast Soul Guardian

**Rarity:** SR | **Cost:** 3

**Main Skill [Passive]:** After the battle starts, all Pals gain 20% of ATK SPD, which reduces by 1/5 every 4s.

**Support Skill [Passive]:** When HP drops below 50% for the first time, releasing the main passive skill grants all Pals 8% of ATK SPD for 12s.

---

### 12. Void Guide

**Rarity:** SR | **Cost:** 3

**Main Skill [Active]:** Every 16s after the battle starts, deals 1800% of AoE Skill DMG and stuns targets for 0.5s.

**Support Skill [Active]:** Releasing the main active skill reduces targets' Base Energy Regen SPD by 8% for 5s.

---

### 13. Defender of Order

**Rarity:** SR | **Cost:** 3

**Main Skill [Shield]:** Every 14s after the battle starts, gains a shield that absorbs 8% of Max HP for 5s, during which every Basic ATK deals an additional 8% of current AoE Counter DMG (can be Crit).

**Support Skill [Shield]:** Releasing the main shield skill increases ATK by 6% for 5s.

---

### 14. Biosphere Guardian

**Rarity:** SR | **Cost:** 3

**Main Skill [Passive]:** After the battle starts, gains 20% of ATK SPD, which reduces by 1/5 every 4s.

**Support Skill [Passive]:** When HP drops below 50% for the first time, releasing the main passive skill grants 8% of ATK SPD for 12s.

---

### 15. Nature's Keeper

**Rarity:** SR | **Cost:** 3

**Main Skill [Passive]:** After the battle starts, every Crit hit has a 5% chance to reduce ATK by 5% for 3s targets within the range.

**Support Skill [Passive]:** Releasing the main passive skill increases Crit Rate by 5%.

---

### 16. Goddess of Victory (Limited)

**Rarity:** SR | **Cost:** 3

**Main Skill [None]:** No Main Effect

**Support Skill [Shield]:** Releasing the main shield skill increases ATK SPD by 10% and adds 50% of Counter DMG to Basic ATK for 5s.

---

### 17. Sprite of Knowledge

**Rarity:** R | **Cost:** 2

**Main Skill [Active]:** Every 14s after the battle starts, targets within the range take 250% of Skill DMG per second for 5s.

**Support Skill [Passive]:** Releasing the main passive skill increases Stun Rate by 3% until the battle ends.

---

### 18. Intrepid Fowl

**Rarity:** R | **Cost:** 2

**Main Skill [Active]:** Every 15s after the battle starts, deals 500% of current AoE Basic ATK DMG (can be Crit).

**Support Skill [Shield]:** Releasing the main shield skill increases Crit Rate by 4% and Base Crit DMG by 50% for 5s.

---

### 19. Jolly Greenhorn

**Rarity:** R | **Cost:** 2

**Main Skill [Active]:** Every 15s after the battle starts, deals 500% of current AoE Combo DMG (can be Crit).

**Support Skill [Active]:** Releasing the main active skill increases ATK SPD by 5% for 5s.

---

### 20. Vanguard Urchin

**Rarity:** R | **Cost:** 2

**Main Skill [Passive]:** After the battle starts, every Basic ATK deals an additional 15% of current Single-target Counter DMG.

**Support Skill [Passive]:** Releasing the main passive skill increases Base Counter DMG by 100% until the battle ends.

---

### 21. Faithful Guardian

**Rarity:** R | **Cost:** —

**Main Skill [None]:** No Main Effect

**Support Skill [Passive]:** Releasing the main passive skill increases DMG to bosses by 8% until the battle ends.

---

### 22. Blossom Harbinger

**Rarity:** R | **Cost:** —

**Main Skill [None]:** No Main Effect

**Support Skill [Passive]:** Releasing the main passive skill increases Final DEF by 8% until the battle ends.

---

### 23. Harvest Harbinger

**Rarity:** R | **Cost:** —

**Main Skill [None]:** No Main Effect

**Support Skill [Passive]:** Releasing the main passive skill increases Boss DMG RES by 4% until the battle ends.

---

### 24. Dome Watcher

**Rarity:** R | **Cost:** 2

**Main Skill [Passive]:** After the battle starts, all Pals gain 12% of Ignore Evasion.

**Support Skill [Shield]:** Releasing the main shield skill increases Base Pal DMG by 30% for 3s.

---

### 25. Valiant Soulknight

**Rarity:** R | **Cost:** 2

**Main Skill [Passive]:** After the battle starts, all Pals gain 50% of Base Crit DMG.

**Support Skill [Passive]:** Releasing the main passive skill grants all Pals 2.5% of Crit Rate until the battle ends.

---

### 26. Stoneborn Warrior

**Rarity:** R | **Cost:** 2

**Main Skill [Shield]:** Every 14s after the battle starts, gains a shield that absorbs 8% of Max HP for 5s.

**Support Skill [Active]:** Releasing the main active skill grants an extra shield that absorbs 5% of Max HP for 5s.

---

### 27. Shadow Keeper

**Rarity:** R | **Cost:** 2

**Main Skill [Active]:** Every 14s after the battle starts, deals 1400% of AoE Skill DMG.

**Support Skill [Shield]:** Releasing the main shield skill increases Base Skill DMG by 30% for 5s.

---

### 28. Puppy Squad (Limited)

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Every 15s after the battle starts, all pals release a phantom hound on their next basic attack, dealing 200% of their Pal DMG (can basic attack) and inflicting Bleed DMG equal to 0.65% of the target's Max HP (ignores DMG Immunity).

**Support Skill [Active]:** Releasing the main active skill reduces target's Pal DMG RES by 6% for 5s.

---

### 29. Sakura Star Envoy (Limited)

**Rarity:** SR | **Cost:** 3

**Main Skill [Shield]:** Every 14s after the battle starts, gain a shield that absorbs 8% of Max HP for 5s. ATK increases by 7.5% while the shield persists.

**Support Skill [None]:** No Support Effect

---

### 30. King (Limited)

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Every 15s after the battle starts, all enemies lose 13.5% ATK and 27% DEF for 5s (cannot be cleansed).

**Support Skill [Passive]:** Releasing the main passive skill reduces all enemies' ATK by 3.6% until the battle ends.

---

### 31. Hellish Blizzard (Limited)

**Rarity:** SR | **Cost:** 3

**Main Skill [Active]:** After the battle starts, casts a whirlwind every 15s, lasting 5s, dealing 450% Skill Bleed DMG per sec to all enemies (ignores DMG Immunity) and reducing their DMG RES by 2.25% for 2s. (Does not stack; duration refreshes on re-trigger.)

**Support Skill [Active]:** After casting the main active skill, deals 900% Skill DMG to all enemies and reduces their Ignore Evasion. Crit Rate, Pal Ignore Evasion, and Pal Crit Rate by 3% for 5s (cannot be cleansed).

---

### 32. Gold Snow Roll (Limited)

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Launch a snowball every 15s after the battle starts, dealing 900% Skill DMG, 180% current Basic ATK DMG (can be Crit), 180% current Combo DMG (can be Crit), and 180% current Counter DMG (can be Crit) to all enemies, and reduce their DMG RES by 0.9% until the battle ends, stacking up to 5 times.

**Support Skill [Shield]:** Releasing the main shield skill increases Final Basic ATK DMG, Final Combo DMG, and Final Counter DMG by an additional 3% until the battle ends, stacking up to 4 times.

---

### 33. Leaf Fox (Limited)

**Rarity:** SR | **Cost:** 3

**Main Skill [Shield]:** Every 14s after the battle starts, gains a shield that absorbs 9% of Max HP and ignores any new control effects received. (This doesn't affect existing control.)

**Support Skill [Shield]:** Releasing the main shield skill increases Evasion by an additional 18% for 5s.

---

## Skill ID -> Angel Name Lookup

For code reference — map `ConfigAngel_skill` IDs back to their angel:

| Skill ID | Angel Name | angel_id |
|----------|------------|----------|
| 27001 | Sprite of Knowledge | 10001 |
| 27002 | Intrepid Fowl | 10002 |
| 27003 | Jolly Greenhorn | 10003 |
| 27004 | Vanguard Urchin | 10004 |
| 27008 | Dome Watcher | 10008 |
| 27009 | Valiant Soulknight | 10009 |
| 27010 | Stoneborn Warrior | 10010 |
| 27011 | Shadow Keeper | 10011 |
| 27012 | Spirit Harbinger | 20001 |
| 27013 | Mentor of Wisdom | 20002 |
| 27015 | Knight of Light | 20004 |
| 27016 | Beast Soul Guardian | 20005 |
| 27017 | Void Guide | 20006 |
| 27018 | Defender of Order | 20007 |
| 27019 | Biosphere Guardian | 20008 |
| 27020 | Nature's Keeper | 20009 |
| 27021 | Divine Warbringer | 30001 |
| 27022 | Storm Dominion | 30002 |
| 27023 | Holy Defender | 30004 |
| 27024 | Barbarian Overlord | 30003 |
| 27025 | Genie of Wishes | 30005 |
| 27026 | Sakura Star Envoy | 20010 |
| 27030 | Lord of Champions | 30007 |
| 27040 | Hellish Blizzard | 20020 |
| 27041 | King | 30013 |
| 27042 | Gold Snow Roll | 30014 |
| 27043 | Leaf Fox | 20021 |
| 270271-280 | Puppy Squad (10 skills) | 30006 |

---

## Config Tables Reference

| Table | Records | Purpose |
|-------|---------|---------|
| `ConfigAngel` | 35 | Angel definitions (id, name, type, icons) |
| `ConfigAngel_star` | 350 | Star progression (attrs, skills, develop effects) |
| `ConfigAngel_skill` | 310 | Battle skills (effects, coefficients, descriptions) |
| `ConfigAngel_array` | 5+ | Formation slot definitions |
| `ConfigAngel_develop` | — | Development slot effects |
| `ConfigAngel_draw` | — | Gacha rates (permanent banners) |
| `ConfigAngel_draw_time_limit` | — | Limited-time rate-up banners |
| `ConfigAngel_draw_package` | — | Draw milestone rewards |

---

## Code Locations

| Module | Lines | Purpose |
|--------|-------|---------|
| ConfigAngel.ts | 218577 | Base angel definitions |
| ConfigAngel_star.ts | 218461 | Per-star-level data (skills, stats, costs) |
| ConfigAngel_skill.ts | 218397 | Angel-specific skill definitions (slot 2) |
| ConfigAngel_develop.ts | 218064 | Development effect macro mappings |
| ConfigAngel_array.ts | 218018 | Formation slot layout |
| ConfigAngel_draw.ts | 218306 | Permanent gacha banners |
| ConfigAngel_draw_time_limit.ts | 218177 | Limited-time gacha banners |
| ConfigAngel_draw_package.ts | 218110 | Draw milestone rewards |
| GuardianSpiritBattleView.ts | ~305100 | Battle UI rendering for angels |
| setPlayerPassiveSkill | 187523-187534 | Passive skills with angel skill enhancements |

---

## Dependencies

- ConfigSkill / ConfigSkill_level — Skill slot 1 references
- ConfigSkilleffcet — Effect chain execution (note: typo "effcet" is in the original code)
- ConfigBuff — Buffs from angel skills
- AttribDefine — Attribute IDs for stat bonuses

## Data Files

- **Source spreadsheet**: `battlesim/reference/LOM_Database-5.xlsx`
- **Structured data**: `battlesim/reference/star_heroes_master.json`
- **Config source**: `data/tables/Angel*.json` (decoded from `bundle-firstload-res`)
