# 05 — Active Skills

> Complete active skill reference: all 38 skills from LOM_Database-5.xlsx, enriched with config binary data (skill IDs, cast times, target types, effect IDs, 200–300 level scaling per skill). 8 event-exclusive skills. See also `skills_master.json` for structured JSON.

---

## Quick Reference — All 38 Skills

| # | Name | Rarity | CD | Passive | Event | Key Effect |
|---|------|--------|----|---------|-------|------------|
| 1 | **Spore Bomb** | Normal | 7s | Base HP, ATK, DEF +1% | — | Trigger an explosion on the target 2 time(s), each time dealing 68% DM... |
| 2 | **Schroom Cap** | Normal | 9s | Base HP, ATK, DEF +1% | — | Summon a Mushroom Cap, dealing 194% AoE DMG. |
| 3 | **Spore Barrage** | Normal | 7s | Base HP, ATK, DEF +1% | — | Throw 5 spore(s), each dealing 33.1% DMG. |
| 4 | **Boulder Impact** | Unique | 12s | Base HP, ATK, DEF +1.5% | — | Summon a Giant Rock, dealing 76% DMG to the target every second, lasti... |
| 5 | **Thorn Thicket** | Unique | 8s | Base HP, ATK, DEF +1.5% | — | Set up 1 trap(s), dealing 53% DMG every second and slowing the target ... |
| 6 | **Lead the Charge** | Unique | 14s | Base HP, ATK, DEF +1.5% | — | Deal 438% DMG to the nearest target and increase Basic Attack DMG by 3... |
| 7 | **Entangling Vines** | Well | 8s | Base HP, ATK, DEF +2.2% | — | Set up 1 trap(s), dealing 394% DMG to enemies triggering the trap and ... |
| 8 | **Speed Surge** | Well | 14s | Base HP, ATK, DEF +2.2% | — | Deal 656% DMG to the nearest target and increase Attack Speed by 30% f... |
| 9 | **Spider Weaver** | Well | 10s | Base HP, ATK, DEF +2.2% | — | Summon a Spider, dealing 96% AoE DMG every second, lasting for 5 secon... |
| 10 | **Pineapple Plunge** | Rare | 11s | Base HP, ATK, DEF +4% | — | Continuously summon 5 Pinneapple(s), each dealing 197% AoE DMG. |
| 11 | **Pearl Release** | Rare | 11s | Base HP, ATK, DEF +4% | — | Summon a Clam, dealing 789% AoE DMG and slowing targets within the ran... |
| 12 | **Sprawling Vine** | Rare | 11s | Base HP, ATK, DEF +4% | — | Summon vines, dealing 789% AoE DMG and imprisoning targets within the ... |
| 13 | **Batty Trace** | Mythic | 15s | Base HP, ATK, DEF +8% | — | Summon a bat, dealing 315% AoE DMG every second, lasting for 5 seconds... |
| 14 | **Nature's Renewal** | Mythic | 25s | Base HP, ATK, DEF +8% | — | Deals 1775% DMG to the target and recover 30% of max HP within 5 secon... |
| 15 | **Shroom Shield** | Mythic | 19s | Base HP, ATK, DEF +8% | — | Deal 1183% DMG to the target and gain a shield equal to 20% of max HP,... |
| 16 | **Durian Bomb** | Epic | 18s | Base HP, ATK, DEF +16% | — | Continuously summon 3 Durian(s), each dealing 888% AoE DMG and slowing... |
| 17 | **Easy Breezy** | Epic | 15s | Base HP, ATK, DEF +16% | — | Throw a Cactus, dealing 1657% AoE DMG and reducing the ATK of targets ... |
| 18 | **Take It Slow** | Epic | 12s | Base HP, ATK, DEF +16% | — | Throw a Cactus, dealing 1635% AoE DMG and reducing the ATK Speed of ta... |
| 19 | **Coin Bomb** | Epic | 13s | Base HP, ATK, DEF +16% | — | Throw coins, dealing 1450% AoE DMG and increasing Basic Attack DMG by ... |
| 20 | **Slime Bomb** | Epic | 13s | Base HP, ATK, DEF +16% | — | Summon a slime, dealing 1450% AoE DMG and increasing pals DMG by 30%, ... |
| 21 | **Meteor Fall** | Epic | 13s | Base HP, ATK, DEF +16% | — | Summon meteors, dealing 1450% AoE DMG and increasing Skill DMG by 30%,... |
| 22 | **Disarm** | Legendary | 16s | Base HP, ATK, DEF +32% | — | Jet Water Columns, dealing 2682% AoE DMG and disarming targets within ... |
| 23 | **Dazzled** | Legendary | 19s | Base HP, ATK, DEF +32% | — | Jet Poison Mist, dealing 3134% AoR DMG and stunning targets within the... |
| 24 | **Smoke Bomb** | Legendary | 13s | Base HP, ATK, DEF +32% | — | Throw a Smoke Bomb, dealing 2176% AoE DMG and increasing the DMG recei... |
| 25 | **Grim Reaper** | Legendary | 9s | Base HP, ATK, DEF +32% | — | Summon ghosts, dealing 1443% DMG. Ghosts instantly defeat targets with... |
| 26 | **Heroic Descent** | Legendary | 19s | Base HP, ATK, DEF +32% | — | Summon a Hero Spirit with 3 Attack Speed. The Spirit deals 148% DMG wi... |
| 27 | **Wild Gust** | Legendary | 16s | Base HP, ATK, DEF +32% | — | Summon a Gale, dealing 2642% AoE DMG and increasing ATK by 15% for 5 s... |
| 28 | **Blitz Assault** | Immortal | 24s | Base HP, ATK, DEF +64% | — | Summon Golden Lightning, dealing 5829% DMG and providing 3 seconds of ... |
| 29 | **Blade Pierce** | Immortal | 19s | Base HP, ATK, DEF +64% | — | Throw Sharp Blades, dealing 4663% DMG and causing the target to lose 1... |
| 30 | **Clone Strike** | Immortal | 29s | Base HP, ATK, DEF +64% | — | Generate a clone with 30% of the shroom's HP. The clone lasts for 10 s... |
| 31 | **Hundred Slashes** | Immortal | 19s | Base HP, ATK, DEF +64% | Yes | Deal 4663% DMG and gain 20% Basic ATK DMG RES and 0.5% ATK Bonus based... |
| 32 | **Windborne Arrow** | Immortal | 19s | Base HP, ATK, DEF +64% | Yes | Deal 2665% DMG and inflict vulnerability for 5 seconds. During this pe... |
| 33 | **Crimson Moonfall** | Immortal | 8s | Base HP, ATK, DEF +64% | Yes | Deal 2098% DMG. Each successive cast increases the DMG by 50%, stackin... |
| 34 | **Dragonic Resonance** | Immortal | 15s | Base HP, ATK, DEF +64% | Yes | Inflict 3731% initial DMG, followed by a 0.5 second delay, then deal 2... |
| 35 | **Worldly Snare** | Immortal | 24s | Base HP, ATK, DEF +64% | Yes | Deal 5413% DMG and increase Crit Rate by 10%. For every 1% Crit Rate, ... |
| 36 | **Star Array** | Immortal | 19s | Base HP, ATK, DEF +64% | Yes | Deal 4330% DMG and increase Skill Crit Rate by 10%. For every 1% Skill... |
| 37 | **Winged Dreams** | Immortal | 24s | Base HP, ATK, DEF +64% | Yes | Deal 5413% DMG and grant all pals a 20% Combo Rate. Every 1% Combo Rat... |
| 38 | **Ancestral Will** | Immortal | 24s | Base HP, ATK, DEF +64% | Yes | Deal 5413% DMG and grant all pals a 10% Crit Rate. Every 1% Crit Rate ... |

---

## Full Details

### 1. Spore Bomb

**Rarity:** Normal | **Cooldown:** 7s

**Effect:** Trigger an explosion on the target 2 time(s), each time dealing 68% DMG.

**Passive:** Base HP, ATK, DEF +1%

---

### 2. Schroom Cap

**Rarity:** Normal | **Cooldown:** 9s

**Effect:** Summon a Mushroom Cap, dealing 194% AoE DMG.

**Passive:** Base HP, ATK, DEF +1%

---

### 3. Spore Barrage

**Rarity:** Normal | **Cooldown:** 7s

**Effect:** Throw 5 spore(s), each dealing 33.1% DMG.

**Passive:** Base HP, ATK, DEF +1%

---

### 4. Boulder Impact

**Rarity:** Unique | **Cooldown:** 12s

**Effect:** Summon a Giant Rock, dealing 76% DMG to the target every second, lasting for 5 seconds.

**Passive:** Base HP, ATK, DEF +1.5%

---

### 5. Thorn Thicket

**Rarity:** Unique | **Cooldown:** 8s

**Effect:** Set up 1 trap(s), dealing 53% DMG every second and slowing the target by 40%, last for 5 seconds.

**Passive:** Base HP, ATK, DEF +1.5%

---

### 6. Lead the Charge

**Rarity:** Unique | **Cooldown:** 14s

**Effect:** Deal 438% DMG to the nearest target and increase Basic Attack DMG by 30% for 5 seconds.

**Passive:** Base HP, ATK, DEF +1.5%

---

### 7. Entangling Vines

**Rarity:** Well | **Cooldown:** 8s

**Effect:** Set up 1 trap(s), dealing 394% DMG to enemies triggering the trap and imprisoning them for 1 second.

**Passive:** Base HP, ATK, DEF +2.2%

---

### 8. Speed Surge

**Rarity:** Well | **Cooldown:** 14s

**Effect:** Deal 656% DMG to the nearest target and increase Attack Speed by 30% for 5 seconds.

**Passive:** Base HP, ATK, DEF +2.2%

---

### 9. Spider Weaver

**Rarity:** Well | **Cooldown:** 10s

**Effect:** Summon a Spider, dealing 96% AoE DMG every second, lasting for 5 seconds.

**Passive:** Base HP, ATK, DEF +2.2%

---

### 10. Pineapple Plunge

**Rarity:** Rare | **Cooldown:** 11s

**Effect:** Continuously summon 5 Pinneapple(s), each dealing 197% AoE DMG.

**Passive:** Base HP, ATK, DEF +4%

---

### 11. Pearl Release

**Rarity:** Rare | **Cooldown:** 11s

**Effect:** Summon a Clam, dealing 789% AoE DMG and slowing targets within the range by 40%, lasting for 5 seconds.

**Passive:** Base HP, ATK, DEF +4%

---

### 12. Sprawling Vine

**Rarity:** Rare | **Cooldown:** 11s

**Effect:** Summon vines, dealing 789% AoE DMG and imprisoning targets within the range for 1 second.

**Passive:** Base HP, ATK, DEF +4%

---

### 13. Batty Trace

**Rarity:** Mythic | **Cooldown:** 15s

**Effect:** Summon a bat, dealing 315% AoE DMG every second, lasting for 5 seconds.

**Passive:** Base HP, ATK, DEF +8%

---

### 14. Nature's Renewal

**Rarity:** Mythic | **Cooldown:** 25s

**Effect:** Deals 1775% DMG to the target and recover 30% of max HP within 5 seconds.

**Passive:** Base HP, ATK, DEF +8%

---

### 15. Shroom Shield

**Rarity:** Mythic | **Cooldown:** 19s

**Effect:** Deal 1183% DMG to the target and gain a shield equal to 20% of max HP, lasting for 10 seconds.

**Passive:** Base HP, ATK, DEF +8%

---

### 16. Durian Bomb

**Rarity:** Epic | **Cooldown:** 18s

**Effect:** Continuously summon 3 Durian(s), each dealing 888% AoE DMG and slowing targets by 40%, lasting for 5 seconds.

**Passive:** Base HP, ATK, DEF +16%

---

### 17. Easy Breezy

**Rarity:** Epic | **Cooldown:** 15s

**Effect:** Throw a Cactus, dealing 1657% AoE DMG and reducing the ATK of targets within the range by 20%, lasting for 5 seconds.

**Passive:** Base HP, ATK, DEF +16%

---

### 18. Take It Slow

**Rarity:** Epic | **Cooldown:** 12s

**Effect:** Throw a Cactus, dealing 1635% AoE DMG and reducing the ATK Speed of targets within the range by 40%, lasting for 5 seconds.

**Passive:** Base HP, ATK, DEF +16%

---

### 19. Coin Bomb

**Rarity:** Epic | **Cooldown:** 13s

**Effect:** Throw coins, dealing 1450% AoE DMG and increasing Basic Attack DMG by 35%, lasting for 5 seconds.

**Passive:** Base HP, ATK, DEF +16%

---

### 20. Slime Bomb

**Rarity:** Epic | **Cooldown:** 13s

**Effect:** Summon a slime, dealing 1450% AoE DMG and increasing pals DMG by 30%, lasting for 5 seconds.

**Passive:** Base HP, ATK, DEF +16%

---

### 21. Meteor Fall

**Rarity:** Epic | **Cooldown:** 13s

**Effect:** Summon meteors, dealing 1450% AoE DMG and increasing Skill DMG by 30%, lasting for 5 seconds.

**Passive:** Base HP, ATK, DEF +16%

---

### 22. Disarm

**Rarity:** Legendary | **Cooldown:** 16s

**Effect:** Jet Water Columns, dealing 2682% AoE DMG and disarming targets within the range for 3 seconds.

**Passive:** Base HP, ATK, DEF +32%

---

### 23. Dazzled

**Rarity:** Legendary | **Cooldown:** 19s

**Effect:** Jet Poison Mist, dealing 3134% AoR DMG and stunning targets within the range for 1.5 seconds.

**Passive:** Base HP, ATK, DEF +32%

---

### 24. Smoke Bomb

**Rarity:** Legendary | **Cooldown:** 13s

**Effect:** Throw a Smoke Bomb, dealing 2176% AoE DMG and increasing the DMG received by targets within the range by 30% for 5 seconds.

**Passive:** Base HP, ATK, DEF +32%

---

### 25. Grim Reaper

**Rarity:** Legendary | **Cooldown:** 9s

**Effect:** Summon ghosts, dealing 1443% DMG. Ghosts instantly defeat targets with less than 5% HP.

**Passive:** Base HP, ATK, DEF +32%

---

### 26. Heroic Descent

**Rarity:** Legendary | **Cooldown:** 19s

**Effect:** Summon a Hero Spirit with 3 Attack Speed. The Spirit deals 148% DMG with each basic attack, lasts for 10 seconds, and reamins untargetable by enemies.

**Passive:** Base HP, ATK, DEF +32%

---

### 27. Wild Gust

**Rarity:** Legendary | **Cooldown:** 16s

**Effect:** Summon a Gale, dealing 2642% AoE DMG and increasing ATK by 15% for 5 seconds.

**Passive:** Base HP, ATK, DEF +32%

---

### 28. Blitz Assault

**Rarity:** Immortal | **Cooldown:** 24s

**Effect:** Summon Golden Lightning, dealing 5829% DMG and providing 3 seconds of DMG immunity.

**Passive:** Base HP, ATK, DEF +64%

---

### 29. Blade Pierce

**Rarity:** Immortal | **Cooldown:** 19s

**Effect:** Throw Sharp Blades, dealing 4663% DMG and causing the target to lose 1.5% of their max HP per second for 5 seconds.

**Passive:** Base HP, ATK, DEF +64%

---

### 30. Clone Strike

**Rarity:** Immortal | **Cooldown:** 29s

**Effect:** Generate a clone with 30% of the shroom's HP. The clone lasts for 10 seconds and deals 200% DMG with each basic attack.

**Passive:** Base HP, ATK, DEF +64%

---

### 31. Hundred Slashes (Event Exclusive)

**Rarity:** Immortal | **Cooldown:** 19s

**Effect:** Deal 4663% DMG and gain 20% Basic ATK DMG RES and 0.5% ATK Bonus based on current HP for 5 seconds.

**Passive:** Base HP, ATK, DEF +64%

---

### 32. Windborne Arrow (Event Exclusive)

**Rarity:** Immortal | **Cooldown:** 19s

**Effect:** Deal 2665% DMG and inflict vulnerability for 5 seconds. During this period, any non-skill DMG dealt to the target also applies an extra 100% DMG.

**Passive:** Base HP, ATK, DEF +64%

---

### 33. Crimson Moonfall (Event Exclusive)

**Rarity:** Immortal | **Cooldown:** 8s

**Effect:** Deal 2098% DMG. Each successive cast increases the DMG by 50%, stacking up to 3 times.

**Passive:** Base HP, ATK, DEF +64%

---

### 34. Dragonic Resonance (Event Exclusive)

**Rarity:** Immortal | **Cooldown:** 15s

**Effect:** Inflict 3731% initial DMG, followed by a 0.5 second delay, then deal 2% of the target's max HP as DMG. Additionally, deal extra 1% DMG of the target's max HP for every 10% DMG.

**Passive:** Base HP, ATK, DEF +64%

---

### 35. Worldly Snare (Event Exclusive)

**Rarity:** Immortal | **Cooldown:** 24s

**Effect:** Deal 5413% DMG and increase Crit Rate by 10%. For every 1% Crit Rate, gain an additional 3% Crit DMG. This effect lasts for 5 seconds.

**Passive:** Base HP, ATK, DEF +64%

---

### 36. Star Array (Event Exclusive)

**Rarity:** Immortal | **Cooldown:** 19s

**Effect:** Deal 4330% DMG and increase Skill Crit Rate by 10%. For every 1% Skill Crit Rate, gain an additional 3% Skill Crit DMG. This effect lasts for 5 seconds.

**Passive:** Base HP, ATK, DEF +64%

---

### 37. Winged Dreams (Event Exclusive)

**Rarity:** Immortal | **Cooldown:** 24s

**Effect:** Deal 5413% DMG and grant all pals a 20% Combo Rate. Every 1% Combo Rate increases a pal's Combo Multiplier by 0.5%. This effect lasts for 5 seconds.

**Passive:** Base HP, ATK, DEF +64%

---

### 38. Ancestral Will (Event Exclusive)

**Rarity:** Immortal | **Cooldown:** 24s

**Effect:** Deal 5413% DMG and grant all pals a 10% Crit Rate. Every 1% Crit Rate increases a pal's Crit DMG by 5%. This effect lasts for 5 seconds.

**Passive:** Base HP, ATK, DEF +64%

---

## Config Binary Data — Skill IDs, Cast Times, Targeting

> Decoded from `ConfigActive_skill` binary table. Each skill maps to a `skill_id`, cast timing, targeting mode, and effect chain.

**Quality Mapping:** 1=Normal, 2=Unique, 3=Well, 4=Rare, 5=Mythic, 6=Epic, 7=Legendary, 8=Immortal

**Target Type Format:** `[team, count, mode]` — team: 4=enemy; count: 1=single; mode: 0=nearest, 1=current, 3=AoE, 4=summon

| # | Name | Skill ID | Cast | Interval | Target | Effect IDs | Event | Levels |
|---|------|----------|------|----------|--------|------------|-------|--------|
| 1 | Spore Bomb | 1001 | 0.5s | 0.4s | [4,1,1] | 10012 | — | 200 |
| 2 | Schroom Cap | 1002 | 1.0s | 1.2s | [4,1,3] | 10021 | — | 200 |
| 3 | Spore Barrage | 1003 | 1.5s | 0.3s | [4,1,3] | 10031 | — | 200 |
| 4 | Boulder Impact | 1004 | 1.0s | 1.2s | [4,1,3] | 10041 | — | 200 |
| 5 | Thorn Thicket | 1006 | 1.0s | 1.2s | [4,1,3] | 10061, 10062 | — | 200 |
| 6 | Lead the Charge | 1007 | 1.0s | 1.2s | [4,1,0] | 10072 | — | 200 |
| 7 | Entangling Vines | 1005 | 1.0s | 1.2s | [4,1,3] | 10051 | — | 200 |
| 8 | Speed Surge | 1008 | 1.0s | 1.2s | [4,1,0] | 10082 | — | 200 |
| 9 | Spider Weaver | 1009 | 1.5s | 2.0s | [4,1,1] | 10091 | — | 200 |
| 10 | Pineapple Plunge | 1011 | 4.0s | 1.0s | [4,1,3] | 10111 | — | 200 |
| 11 | Pearl Release | 1014 | 1.0s | 1.2s | [4,1,3] | 10141 | — | 200 |
| 12 | Sprawling Vine | 1015 | 1.0s | 1.2s | [4,1,3] | 10151 | — | 200 |
| 13 | Batty Trace | 1012 | 1.0s | 1.2s | [4,1,4] | 10121 | — | 300 |
| 14 | Nature's Renewal | 1019 | 5.0s | 6.0s | [4,1,0] | 10191, 10192 | — | 300 |
| 15 | Shroom Shield | 1036 | 1.0s | 1.2s | [4,1,0] | 10361, 10362 | — | 300 |
| 16 | Durian Bomb | 1020 | 2.0s | 1.0s | [4,1,3] | 10201 | — | 300 |
| 17 | Easy Breezy | 1023 | 1.0s | 1.2s | [4,1,3] | 10231 | — | 300 |
| 18 | Take It Slow | 1024 | 1.0s | 1.2s | [4,1,3] | 10241 | — | 300 |
| 19 | Coin Bomb | 1044 | 1.0s | 1.2s | [4,1,0] | 10441 | — | 300 |
| 20 | Slime Bomb | 1045 | 1.0s | 1.2s | [4,1,0] | 10451 | — | 300 |
| 21 | Meteor Fall | 1046 | 1.0s | 1.2s | [4,1,0] | 10461 | — | 300 |
| 22 | Disarm | 1021 | 1.0s | 1.2s | [4,1,3] | 10211 | — | 300 |
| 23 | Dazzled | 1022 | 1.0s | 1.2s | [4,1,3] | 10221 | — | 300 |
| 24 | Smoke Bomb | 1029 | 1.0s | 1.2s | [4,1,3] | 10291 | — | 300 |
| 25 | Grim Reaper | 1047 | 1.0s | 1.2s | [4,1,0] | 10471 | — | 300 |
| 26 | Heroic Descent | 1048 | 1.0s | 1.2s | self | 10481 | — | 300 |
| 27 | Wild Gust | 1049 | 1.0s | 1.2s | [4,1,0] | 10491 | — | 300 |
| 28 | Blitz Assault | 1050 | 1.0s | 1.2s | [4,1,0] | 10501, 10502 | — | 300 |
| 29 | Blade Pierce | 1051 | 1.0s | 1.2s | [4,1,3] | 10511, 10512 | — | 300 |
| 30 | Clone Strike | 1052 | 1.0s | 1.2s | self | 10521 | — | 300 |
| 31 | Hundred Slashes | 1060 | 1.0s | 1.2s | [4,1,0] | 10601–10603 | Yes | 300 |
| 32 | Windborne Arrow | 1062 | 1.0s | 1.2s | [4,1,0] | 10621, 10622 | Yes | 300 |
| 33 | Crimson Moonfall | 1063 | 1.0s | 1.2s | [4,1,0] | 10631, 10632 | Yes | 300 |
| 34 | Dragonic Resonance | 1059 | 1.0s | 1.2s | [4,1,0] | 10591, 10592 | Yes | 300 |
| 35 | Worldly Snare | 1061 | 1.0s | 1.2s | [4,1,0] | 10611–10613 | Yes | 300 |
| 36 | Star Array | 1064 | 1.0s | 1.2s | [4,1,0] | 10641–10643 | Yes | 300 |
| 37 | Winged Dreams | 1068 | 1.0s | 1.2s | [4,1,0] | 10681, 10682 | Yes | 300 |
| 38 | Ancestral Will | 1069 | 1.0s | 1.2s | [4,1,0] | 10691, 10692 | Yes | 300 |

**Notes:**
- Normal–Rare skills (quality 1–4) scale to 200 levels; Mythic+ (quality 5–8) scale to 300 levels.
- `release_time` = cast animation duration; `release_interval` = minimum time between consecutive casts.
- `skill_effect_ids` reference `ConfigActive_skill_effect` entries which define the actual damage coefficients, buff applications, and projectile behavior.
- Skills 26 (Heroic Descent) and 30 (Clone Strike) have no `target_type` — they target self (summon clone/spirit).

---

## Data Files

- **Source spreadsheet**: `battlesim/reference/LOM_Database-5.xlsx`
- **Structured data**: `battlesim/reference/skills_master.json`
- **Config tables**: `data/tables/Active_skill.json`, `data/tables/Active_skill_level.json`