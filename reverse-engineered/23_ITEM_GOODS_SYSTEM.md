# 23 -- Item & Goods System

## Overview

The Goods system is the unified item/inventory framework for Legend of Mushroom. Every obtainable object -- currency, equipment, skills, pets, skins, mounts, artifacts, fates, spirits, and privilege tokens -- is represented as a "Goods" entry. The system handles item classification, pricing, recycling, sourcing, and shop refresh cycles.

---

## Config Tables

| Table | Source Line | Main Key | Fields | Description |
|-------|-----------|----------|--------|-------------|
| ConfigGoods | 238027 | `id` | 14 | Master item definitions |
| ConfigGoods_refresh | 237849 | `id` | 10 | Shop refresh/restock schedules |
| ConfigGoods_source | 237930 | `id` | 13 | Item acquisition source metadata |

---

## ConfigGoods Schema -- Line 238027

The central item registry. Every item in the game has a row here.

| Field | Index | Type | Description |
|-------|-------|------|-------------|
| `id` | 0 | number | Unique item ID |
| `name` | 1 | string_ref | Localized item name |
| `type` | 2 | number | GoodsType enum value (see below) |
| `subtype` | 3 | number | Sub-classification within a GoodsType |
| `quality` | 4 | number | Rarity tier (1=Common, 2=Uncommon, etc.) |
| `effect` | 5 | optional_array | Effect data applied on use |
| `desc` | 6 | string_ref | Localized item description |
| `icon` | 7 | number | Icon asset ID |
| `getItems` | 8 | optional_array | Items contained when opened (for chest/box items) |
| `icon_group` | 9 | number | Icon group classification |
| `price` | 10 | optional_array | Purchase price `[[currencyId, amount], ...]` |
| `recycle_price` | 11 | optional_array | Sell/recycle value `[[currencyId, amount], ...]` |
| `open_view` | 12 | number | UI view to open on interaction |
| `view_args` | 13 | optional_array | Arguments passed to the UI view |

---

## GoodsType Enum -- Line 184215

Classifies every item into a top-level category. The `type` field in ConfigGoods references these values.

| Name | Value | Description |
|------|-------|-------------|
| `Normal` | 1 | Generic consumable, material, currency token |
| `Equip` | 2 | Equipment (weapon, armor, accessory) |
| `Skill` | 3 | Skill scroll/book |
| `Pet` | 4 | Pet/Pal companion |
| `Skin` | 5 | Cosmetic skin |
| `Privilege` | 6 | VIP/privilege pass |
| `Fate` | 12 | Fate card |
| `Mount` | 27 | Rideable mount |
| `Artifact` | 28 | Artifact item |
| `Wing` | 32 | Wing cosmetic/stat item |
| `Spirit` | 50 | Guardian spirit |
| `SpiritClip` | 51 | Spirit shard/clip for summoning |

### Practical Notes

- **Normal (1)** is the catch-all for everything that does not have a dedicated system: gold, diamonds, EXP potions, upgrade stones, crafting materials, keys, event tokens.
- **Equip (2)** items cross-reference `ConfigEquipment` for their stat data, level progression, refinement, and suit bonuses.
- **Skill (3)** items reference `ConfigSkill` for the underlying skill definition and `ConfigSkill_level` for per-level coefficients.
- **Pet (4)** items tie into `ConfigPet`, `ConfigPetlevel`, and `ConfigPet_talent`.
- **Fate (12)** items reference `ConfigFate` and `ConfigFate_level` for the card system.

---

## ItemIdDefine -- Line 184212

Hard-coded currency constants used throughout the codebase.

| Name | Value | Description |
|------|-------|-------------|
| `Gold` | 1 | Primary soft currency |
| `Diamond` | 2 | Premium hard currency |
| `GuildExp` | 8 | Guild contribution experience |
| `FakeRechare` | 999 | Internal test/fake recharge token |

These IDs appear in `price` and `recycle_price` arrays as the `currencyId` component: `[[1, 5000]]` means "costs 5000 Gold."

---

## PropsType Enum -- Line 162825

Consumable item sub-types used for battle potions and class-specific upgrade items.

| Name | Value | Description |
|------|-------|-------------|
| `Health` | 0 | HP recovery potion |
| `WarriorUp` | 1 | Warrior class upgrade material |
| `MasterUp` | 2 | Mage/Master class upgrade material |
| `ArcherUp` | 3 | Archer class upgrade material |
| `Change` | 4 | Class change item |

---

## ConfigGoods_refresh -- Line 237849

Controls how shop inventories rotate and restock.

| Field | Index | Type | Description |
|-------|-------|------|-------------|
| `id` | 0 | number | Refresh schedule ID |
| `serv_macro` | 1 | number | Server macro / condition flag |
| `name` | 2 | string_ref | Schedule display name |
| `type` | 3 | number | Refresh type classification |
| `init` | 4 | number | Initial stock count |
| `max` | 5 | number | Maximum stock count |
| `quantity` | 6 | number | Quantity restocked per cycle |
| `time` | 7 | number | Refresh interval (in seconds or server ticks) |
| `newfuncopen_id` | 8 | number | Function unlock requirement (FK to ConfigNewFuncOpen) |
| `switch` | 9 | number | Enable/disable toggle |

### Refresh Mechanics

The shop refresh system works as follows:
```
stock = min(current_stock + quantity, max)
```
Each refresh cycle adds `quantity` items back to the pool, capped at `max`. The `init` value is the starting stock when the shop is first created for a player.

---

## ConfigGoods_source -- Line 237930

Defines where and how items can be obtained. Powers the "Source" button in the item detail UI that shows players how to farm a specific item.

| Field | Index | Type | Description |
|-------|-------|------|-------------|
| `id` | 0 | number | Source entry ID |
| `name` | 1 | string_ref | Source name (e.g., "Chapter 12-5") |
| `desc` | 2 | string_ref | Source description |
| `view` | 3 | number | UI view to navigate to |
| `show_btn` | 4 | number | Whether to show a "Go" button |
| `icon` | 5 | number | Source icon asset |
| `icon_atlas` | 6 | number | Atlas/spritesheet reference |
| `icon_scale` | 7 | number | Icon display scale factor |
| `openArgs` | 8 | optional_array | Navigation arguments for the view |
| `chapter_id` | 9 | number | Related chapter ID (if applicable) |
| `openday` | 10 | number | Day-of-week restriction (0 = always) |
| `activityType` | 11 | number | Activity type restriction |
| `newopen_func` | 12 | number | Function unlock gate |

---

## Item Flow Architecture

```
Player obtains item
    |
    v
Check GoodsType (ConfigGoods.type)
    |
    +-- Normal(1) -> Add to inventory count
    +-- Equip(2) -> Create equipment instance -> ConfigEquipment
    +-- Skill(3) -> Unlock skill -> ConfigSkill
    +-- Pet(4) -> Add pet -> ConfigPet / ConfigPetlevel
    +-- Skin(5) -> Unlock cosmetic -> ConfigSkin / ConfigFashion_skin
    +-- Privilege(6) -> Activate pass -> ConfigPrivilege
    +-- Fate(12) -> Add fate card -> ConfigFate / ConfigFate_level
    +-- Mount(27) -> Add mount -> ConfigMount / ConfigMount_level
    +-- Artifact(28) -> Add artifact -> ConfigArtifact / ConfigArtifact_level
    +-- Wing(32) -> Unlock wing -> ConfigFly (avian system)
    +-- Spirit(50) -> Add spirit -> ConfigSpirit / ConfigSpirit_level
    +-- SpiritClip(51) -> Add spirit shard -> accumulate for spirit summon
```

---

## Key Observations

1. **Unified ID Space** -- All items share a single numeric ID namespace in ConfigGoods. Cross-system references (equipment stats, skill definitions, etc.) use the same `id` value.
2. **No XOR Encoding** -- None of the Goods tables use ConfigKey XOR encoding. Item data is stored in plaintext.
3. **Price Arrays** -- Both `price` and `recycle_price` use the `[[currencyId, amount], ...]` format, allowing multi-currency costs (e.g., Gold + special tokens).
4. **Chest Items** -- The `getItems` field enables "box within a box" mechanics where opening an item yields other items, which is common for gacha/loot box implementations.
5. **View Navigation** -- The `open_view` and `view_args` fields allow items to directly open specific UI panels, enabling "use" functionality for keys, tickets, and navigation tokens.
