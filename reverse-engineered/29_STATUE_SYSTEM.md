# 29 — Statue System

## Overview

The Statue system is a **stat-boosting progression system** where players level up statue positions to roll attribute bonuses. Similar to Path to Divinity, it uses quality-tiered random rolls, but operates on a simpler position-based structure rather than a branching tree.

---

## Config Tables

| Table | Source Line | Main Key | Fields | Description |
|-------|-----------|----------|--------|-------------|
| ConfigStatue_attr | 263229 | id | 6 | Attribute bonus definitions: product type, attr ID, probability, value range, power |
| ConfigStatue_level | 263291 | level | 4 | Level-up requirements: cost, quality probabilities, power |
| ConfigStatue_pos | 263343 | id | 3 | Position/slot definitions: unlock level, description |
| ConfigStatue_spend | 263389 | lock_quantity | 2 | Lock spending costs based on quantity of locked slots |

---

## A. Attribute Pool (ConfigStatue_attr)

| Field | Type | Description |
|-------|------|-------------|
| id | number | Unique attribute entry ID |
| product | number | Product/statue type classification |
| attr_id | number | AttribDefine attribute ID (1001=att, 1002=hp, etc.) |
| pro | number | Probability weight for this attribute in the roll pool |
| value | array? | Value range: `[min, max]` for the rolled bonus |
| power_rate | number | Combat power contribution per unit of value |

### Roll Mechanics
When a statue position is activated:
1. Filter attributes by `product` type matching the statue
2. Use `pro` weights to randomly select an `attr_id`
3. Roll the bonus value within the `value` range
4. Apply the attribute bonus to the player's stats

---

## B. Leveling (ConfigStatue_level)

| Field | Type | Description |
|-------|------|-------------|
| level | number | Statue system level |
| expend | number | Cost to level up (currency/items) |
| pro_quality | array? | Quality probability distribution: `[[quality, probability], ...]` |
| power | number | Base combat power at this level |

Higher statue levels improve the quality distribution of rolled attributes, shifting probabilities toward rarer and more powerful bonuses.

---

## C. Position Slots (ConfigStatue_pos)

| Field | Type | Description |
|-------|------|-------------|
| id | number | Position slot ID |
| level | number | Required statue level to unlock this slot |
| desc | string_ref | Slot description |

Players unlock additional attribute slots as their statue level increases. Each slot holds one rolled attribute bonus.

---

## D. Lock System (ConfigStatue_spend)

| Field | Type | Description |
|-------|------|-------------|
| lock_quantity | number | Number of slots currently locked |
| spend | array? | Cost to reroll with this many locks: `[[currencyId, amount], ...]` |

Players can **lock** desirable attribute rolls before rerolling the rest. The cost to reroll increases with the number of locked slots, creating a risk/reward tradeoff.

### Reroll Flow
1. Player locks slots they want to keep
2. System charges based on `lock_quantity` → `spend` mapping
3. Unlocked slots are rerolled using the attribute pool
4. Locked slots retain their current values

---

## E. Combat Relevance

Statue bonuses are **additive attribute modifications** using standard AttribDefine IDs:
- Values feed into the MetaAttrib calculation during stat assembly
- Common attributes: att, hp, def, crit_rate, crit_dam, double_hit, counter
- The random roll system means optimal builds require repeated rerolling
- Lock system allows targeted optimization of specific stats

### Key Differences from Path to Divinity
| Aspect | Statue | Path to Divinity |
|--------|--------|-----------------|
| Structure | Flat position slots | Branching tree with trunks |
| Rolling | Rerollable with locks | Permanent per-node |
| Caps | No per-system caps | Per-trunk upper limits |
| Scaling | Level → quality distribution | Level → quality probability |
