# 09 — Relics

> All 5 relic positions with combat effects, dual bonus system, and acquisition.

---

## Overview

Relics provide **dual bonuses**: `equip` (active when slotted) and `own` (passive from ownership). Some relics also grant `equip_effect` combat skills/buffs when equipped.

---

## ConfigRelic Schema (12 fields, keyed by [id, level])

| Field | Description |
|-------|-------------|
| id | Relic ID |
| level | Relic level |
| name | Localized name |
| type | Relic type classification |
| desc | Description template |
| desc_parm | Description format parameters |
| icon | Icon asset |
| equip | Equipped bonuses `[[attrId, value], ...]` — active only in slot |
| own | Ownership bonuses `[[attrId, value], ...]` — always active |
| equip_effect | Combat effects when equipped (skill/buff IDs) |
| cost | Level-up cost `[[itemId, count], ...]` |
| power | Combat power |

---

## Dual Bonus System

### Equip Bonuses
- **Active only** when the relic is placed in an equipment slot
- Provides direct attribute bonuses
- May include `equip_effect` for combat skills/buffs

### Own Bonuses
- **Always active** from mere ownership — no slot required
- Provides passive attribute bonuses
- Allows all relics to contribute stats even when not equipped

### equip_effect
- Combat skills/buffs triggered during battle
- Uses the standard skill/buff system (ConfigSkill → ConfigSkilleffcet → ConfigBuff)
- Only active when relic is in an equipped slot

---

## Relic Positions

### ConfigRelic_pos (3 fields)

| Field | Description |
|-------|-------------|
| id | Position slot ID |
| name | Slot name |
| icon | Slot icon |

Players have multiple relic slots. Each slot holds one relic. All 5 relics contribute `own` bonuses regardless of slot assignment.

---

## Relic Acquisition

### ConfigRelic_get (3 fields)

| Field | Description |
|-------|-------------|
| num | Draw attempt number |
| relic_pool | Available relic IDs for this pull |
| cost | Cost per attempt `[[itemId, count], ...]` |

Relics are obtained through a gacha-style draw system with escalating costs per attempt.

---

## Network Protocol

| Protocol | Description |
|----------|-------------|
| relic.relic_equip_c2s | Equip relic to slot |
| relic.relic_equip_s2c | Server confirmation |

---

## Combat Relevance

Relics feed into the stat assembly pipeline through two channels:
1. **equip bonuses** → direct attribute additions (when slotted)
2. **own bonuses** → passive attribute additions (always active)
3. **equip_effect** → runtime buff/skill activation (when slotted)

All attribute values use standard AttribDefine IDs and are additive in the MetaAttrib calculation.
