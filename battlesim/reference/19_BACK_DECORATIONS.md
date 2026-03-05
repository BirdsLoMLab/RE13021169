# 19 — Back Decorations (Wings / Back Accessories)

> Complete back accessory reference: 45 back accessories (41 from LOM_Database-5.xlsx + 4 config-only). Enriched with `back_id` and `skill_id` from the decoded config binary. See also `back_accessories_master.json` for structured JSON.

---

## Quick Reference — All 45 Back Accessories

| # | Name | Rarity | Passive | Key Effect |
|---|------|--------|---------|------------|
| 1 | **Virtual Connection** | Legendary | Global DEF +10% | Scan the target and analyze its weaknesses after battle starts: Basic attacks ha... |
| 2 | **Ingredients for Dinner** | Legendary | Global HP +10% | Inflict Deter on an enemy every time they have dealt 15 Basic Attacks in total o... |
| 3 | **Chrono Prism** | Legendary | Global DEF +10% | When all enemies have no less than 60% HP, reduces their Basic ATK DMG RES, Skil... |
| 4 | **Dawn Warwing** | Legendary | Global HP +10% | After the battle starts, gain 12% extra Evasion and Movement SPD that lasts till... |
| 5 | **Metamorphosis** | Legendary | Global Counter DMG +5% | Every 11s, deals 1000% of current AoE DMG to the targets and reduces their ATK b... |
| 6 | **Mirror World** | Legendary | Global DEF +10% | Reduces all enemies' Energy Regen SPD, HP Regen, ATK SPD and Pal ATK SPD by 10% ... |
| 7 | **Arackar Lock** | Legendary | Global DEF +10% | Every 11s, deal 2000% Skill DMG, 800% current Combo DMG and 800% current Counter... |
| 8 | **Frostland Specter** | Legendary | Global DEF +10% | Deals DMG equal to 3% of current HP to all targets every 5s and reduces their AT... |
| 9 | **Trapped Wrath** | Legendary | Global DEF +10% | Each 5% missing HP grants a 40% chance of dealing AoE DMG equal to 400% Skill DM... |
| 10 | **Lord of Light** | Legendary | Global DEF +10% | Reduce enemy's Crit RES by 10% after the battle starts. When Character HP first ... |
| 11 | **Celestial Surprises** | Legendary | Global HP +10% | Every 11s, deals AoE Bleed DMG equal to 200% of your Basic ATK 5 times (ignores ... |
| 12 | **Iridescent Aura** | Legendary | Global ATK +10% | Gain 10% Skill Crit Rate. After every 4s, the next Skill Crit hit reduces all ac... |
| 13 | **Summer Parasol** | Legendary | Global HP +10% | Switches between the two forms every 10s: Rainshade, gains 30% DEF and a shield ... |
| 14 | **Fallen Angel** | Legendary | Global DEF +10% | Lowers ATK by 8%, ATK SPD by 12%, Energy Regen SPD by 12%, and Pal ATK SPD by 12... |
| 15 | **Emerald Embrace** | Legendary | Global HP +10% | After the battle begins, each combo increases combo DMG by 0.5%, stacking up to ... |
| 16 | **Miracle Mirage** | Legendary | Global DEF +10% | Reduces all enemies' Combo Rate, Counter Rate, Skill Crit Rate and Pal Crit Rate... |
| 17 | **Pepe-style Thruster** | Legendary | Global DEF +10% | 8s into the battle or when HP first drops below 75%, you gain 5% ATK and all ene... |
| 18 | **19th Century** | Legendary | Global DEF +10% | After 8s into battle or HP first drops below 80%, reduces all enemies' DMG RES b... |
| 19 | **Bit Gateway** | Legendary | Global HP +10% | Increases DEF by 16% after the battle starts. After 15s into battle of HP first ... |
| 20 | **Ghost Behind** | Legendary | Global ATK +10% | Evasion +20%. ATK +20% for 2s upon successful evasion. |
| 21 | **Alien Dimension** | Legendary | Global HP +10% | After battle starts, block 30% Final DMG and increases ATK SPD by 24%, Energy Re... |
| 22 | **Cosmic Rescue** | Legendary | Global HP +10% | Gain a shield equal to 4% Max HP after battle starts and increase your ATK by 5%... |
| 23 | **Till Death Apart** | Legendary | Global DEF +10% | After battle starts, gain 5% of ATK, 8% of ATK SPD, 8% of Energy Regen SPD, and ... |
| 24 | **Lustrous Plumage** | Legendary | Ignore Evasion +15% | At the start of battle, each basic attack raises DEF by 0.5%, stackable up to 40... |
| 25 | **Glory Glow** | Legendary | Global DEF +10% | Attacks with tidal waves at the start of battle, increasing Movement SPD by 20% ... |
| 26 | **Shell Shade** | Legendary | Global HP +10% | Grants a shield equal to 10% Max HP every 11s after battle starts, lasting 8s. I... |
| 27 | **Titan's Hold** | Legendary | Global DEF +10% | Every 10 basic attack hits triggers a Combo Punch, dealing 1000% AoE Skill DMG, ... |
| 28 | **Moonlit Wisp** | Legendary | Global HP +10% | After the battle begins, each releasing of an active skill increases skill DMG b... |
| 29 | **Republic of Heroes** | Legendary | Global DEF +10% | After the battle starts, every 10% Max HP lost grants a shield equal to 6% Max H... |
| 30 | **Firework Invite** | Legendary | Global DEF +10% | Every 11s, releases 7 small fireworks within 3s, each dealing 250% AoE Skill DMG... |
| 31 | **To the Clouds** | Legendary | Global DEF +10% | After 5 seconds into battle or DMG taken exceeds 20% Max HP, increase ATK by 5% ... |
| 32 | **Lunar Radiance** | Legendary | Global HP +10% | For the first 15s, increases all HP Regen efectos by 3%, ATK by 1% and DEF by 2%... |
| 33 | **Song of Frost and Flame** | Legendary | Global DEF +10% | Attacks with the flame sword and frost sword once each every 11s, dealing 1500% ... |
| 34 | **Phoenix Frost** | Legendary | Global HP +10% | Block 8% of DMG when it exceeds 1% of your Max HP, 16% when it exceeds 2%, and 3... |
| 35 | **Blade Pursuit** | Legendary | Global HP +10% | After the battle begins, each counter increases counter DMG by 0.5%, stacking up... |
| 36 | **Beastbone Breeze** | Legendary | Global DEF +10% | Each pal's basic attack increases Pal DMG Multiplier by 1.5% after the battle st... |
| 37 | **Top-Tier Bodyguard** | Legendary | Global DEF +10% | When an enemy activates an Active Skill, they take 1% of their current HP as dam... |
| 38 | **Punching Storm** | Legendary | Global DEF +10% | Increase Stun Rate by 10%. Upon triggering Stun, deal an extra 1000% Skill DMG a... |
| 39 | **Resolute Soul** | Legendary | Global DEF +10% | The first time HP drops below 60%, Pierce increases by 1000. Below 45%, DMG RES ... |
| 40 | **Frost Mirage** | Legendary | Global DEF +10% | After every 10 basic attacks, launch a snowball at a single target, dealing 200%... |
| 41 | **Repose in Time** | Legendary | Global HP +10% | Gains 6% Final DMG RES after the battle starts, which is reduced by 1/4 every 12... |

---

## Full Details

### 1. Virtual Connection

**Rarity:** Legendary

**Effect:** Scan the target and analyze its weaknesses after battle starts: Basic attacks have a 10% chance to reduce the target's Basic ATK DMG RES by 2%, stacking up to 5 times. Combos have a 15% chance to reduce the target's Combo DMG RES by 2%, stacking up to 5 times. Counterstrikes have a 15% chance to reduce the target's Counter DMG RES by 2%, stacking up to 5 times. Skills have a 50% chance to reduce the target's Skill DMG RES by 2%, stacking up to 5 times.

**Passive:** Global DEF +10%

---

### 2. Ingredients for Dinner

**Rarity:** Legendary

**Effect:** Inflict Deter on an enemy every time they have dealt 15 Basic Attacks in total or the first time their HP drops below 50%, with a 60% chance of inflicting Decay and a 60% chance of inflicting Weaken. Decay: Reduces the target's DMG RES by 4%, stacking up to 3 times. Weaken: Lowers the enemy's ATK by 4%, stacking up to 3 times.

**Passive:** Global HP +10%

---

### 3. Chrono Prism

**Rarity:** Legendary

**Effect:** When all enemies have no less than 60% HP, reduces their Basic ATK DMG RES, Skill DMG RES, Pal DMG RES, Combo DMG RES and Counter DMG RES by 10%. Otherwise, reduces their ATK by 10%. After the first 20s of the battle, all the reduction effects above are activated for all enemies.

**Passive:** Global DEF +10%

---

### 4. Dawn Warwing

**Rarity:** Legendary

**Effect:** After the battle starts, gain 12% extra Evasion and Movement SPD that lasts till the battle ends. Reduce the duration of all enemies' Class Skills by 20% for 60s.

**Passive:** Global HP +10%

---

### 5. Metamorphosis

**Rarity:** Legendary

**Effect:** Every 11s, deals 1000% of current AoE DMG to the targets and reduces their ATK by 15%. The effect lasts until they launch 35 attacks (including basic attacks, combos, counterstrikes, and active skills). (Casts 1 time immediately after battle starts.)

**Passive:** Global Counter DMG +5%

---

### 6. Mirror World

**Rarity:** Legendary

**Effect:** Reduces all enemies' Energy Regen SPD, HP Regen, ATK SPD and Pal ATK SPD by 10% after the battle starts. Allied pals have a 50% chance to become demonized. Demonized: Gains 30% Pal ATK SPD and deals extra damage equal to 1% of enemies' Current HP every 10 basic attacks.

**Passive:** Global DEF +10%

---

### 7. Arackar Lock

**Rarity:** Legendary

**Effect:** Every 11s, deal 2000% Skill DMG, 800% current Combo DMG and 800% current Counter DMG and make the target take 4% more Skill, Combo and Counter DMG, stacking up to 3 times (triggers at the start of the battle).

**Passive:** Global DEF +10%

---

### 8. Frostland Specter

**Rarity:** Legendary

**Effect:** Deals DMG equal to 3% of current HP to all targets every 5s and reduces their ATK SPD, Regen, Energy Regen SPD and Pal ATK SPD by 12% for 3s. If a target's Movement SPD drops below 80%, the DMG dealt changes to 3.5% of current HP and the same stats are reduced by 12% for 5s instead. If a target's Movement SPD drops below 40%, the DMG dealt changes to 4% of current HP and stats are reduced by 15% for 5s instead. (Triggers at the start of the battle; Cannot be Cleansed.)

**Passive:** Global DEF +10%

---

### 9. Trapped Wrath

**Rarity:** Legendary

**Effect:** Each 5% missing HP grants a 40% chance of dealing AoE DMG equal to 400% Skill DMG, 160% Current Combo DMG, 160% Current Counter DMG, and 1% of the target's Max HP. Each 10% missing HP grants a 60% chance of dealing AoE DMG equal to 600% Skill DMG, 240% Current Combo DMG, 240% Current Counter DMG, and 1% of the target's Max HP. Each 20% missing HP grants a 100% chance of dealing AoE DMG equal to 1000% Skill DMG, 400% Current Combo DMG, 400% Current Counter DMG, and 2% of the target's Max HP.

**Passive:** Global DEF +10%

---

### 10. Lord of Light

**Rarity:** Legendary

**Effect:** Reduce enemy's Crit RES by 10% after the battle starts. When Character HP first drops below 50%, trigger Avenging Light, increasing Character Crit Rate, Skill Crit Rate, and Pal Crit Rate by 6% and Final Crit DMG, Final Skill Crit DMG, and Final Pal Crit DMG by 8% for 20s.

**Passive:** Global DEF +10%

---

### 11. Celestial Surprises

**Rarity:** Legendary

**Effect:** Every 11s, deals AoE Bleed DMG equal to 200% of your Basic ATK 5 times (ignores DMG Immunity), each time having a 50% chance of dealing extra DMG equal to 1.5% of Max HP (triggers at the start of the battle)

**Passive:** Global HP +10%

---

### 12. Iridescent Aura

**Rarity:** Legendary

**Effect:** Gain 10% Skill Crit Rate. After every 4s, the next Skill Crit hit reduces all active skill cooldowns by 1s and increases Final Skill Crit DMG by 4% until the battle ends, stacking up to 5 times.

**Passive:** Global ATK +10%

---

### 13. Summer Parasol

**Rarity:** Legendary

**Effect:** Switches between the two forms every 10s: Rainshade, gains 30% DEF and a shield equal to 10% Max HP. Sunshade, gains 12% ATK, 15% ATK SPD and 15% Energy Regen (casts 1 time immediately after battle starts).

**Passive:** Global HP +10%

---

### 14. Fallen Angel

**Rarity:** Legendary

**Effect:** Lowers ATK by 8%, ATK SPD by 12%, Energy Regen SPD by 12%, and Pal ATK SPD by 12% after the battle starts, but gains 1% ATK, 1.5% ATK SPD, 1.5% Energy Regen SPD, and 1.5% Pal ATK SPD per second till the end of battle, stacking up to 20 times. Gains all the stacks the first time HP falls below 50%.

**Passive:** Global DEF +10%

---

### 15. Emerald Embrace

**Rarity:** Legendary

**Effect:** After the battle begins, each combo increases combo DMG by 0.5%, stacking up to 60 times.

**Passive:** Global HP +10%

---

### 16. Miracle Mirage

**Rarity:** Legendary

**Effect:** Reduces all enemies' Combo Rate, Counter Rate, Skill Crit Rate and Pal Crit Rate by 15% after the battle starts. The effects are halved after 20s.

**Passive:** Global DEF +10%

---

### 17. Pepe-style Thruster

**Rarity:** Legendary

**Effect:** 8s into the battle or when HP first drops below 75%, you gain 5% ATK and all enemies lose 5% ATK. 15s into the battle or when HP first drops below 50%, you gain 5% DMG RES and all enemies lose 5% DMG RES 20s into the battle or when HP first drops below 25%, you regen 8% Max HP and deal DMG equal to 8% of your Max HP to all enemies.

**Passive:** Global DEF +10%

---

### 18. 19th Century

**Rarity:** Legendary

**Effect:** After 8s into battle or HP first drops below 80%, reduces all enemies' DMG RES by 5%. After 15s into battle or HP first drops below 60%, reduces all enemies' ATK SPD, Energy Regen SPD, and Pal ATK SPD by 10%. After 20s into battle or HP first drops below 40%, reduces all enemies' Basic ATK DMG RES, Skill DMG RES, Pal DMG RES, Combo DMG RES, and Counter DMG RES by 5%. After 30s into battle or HP first drops below 20%, triggers an additional 40% of all the effects above.

**Passive:** Global DEF +10%

---

### 19. Bit Gateway

**Rarity:** Legendary

**Effect:** Increases DEF by 16% after the battle starts. After 15s into battle of HP first drops below 70%, increases ATK by 10%. After 30s into battle or HP first drops below 30%, increases DMG RES by 10% and restores 10% of lost HP second for 10s.

**Passive:** Global HP +10%

---

### 20. Ghost Behind

**Rarity:** Legendary

**Effect:** Evasion +20%. ATK +20% for 2s upon successful evasion.

**Passive:** Global ATK +10%

---

### 21. Alien Dimension

**Rarity:** Legendary

**Effect:** After battle starts, block 30% Final DMG and increases ATK SPD by 24%, Energy Regen SPD by 24% and Pal ATK SPD by 24%. The effects are reduced by 1/3 every 12 seconds.

**Passive:** Global HP +10%

---

### 22. Cosmic Rescue

**Rarity:** Legendary

**Effect:** Gain a shield equal to 4% Max HP after battle starts and increase your ATK by 5%. Gain another shield equal to 6% Max HP and increase your ATK by 5% the first time your HP falls below 75%, then a shield equal to 8% Max HP and increase your ATK by 5% the first time your HP falls below 50%.

**Passive:** Global HP +10%

---

### 23. Till Death Apart

**Rarity:** Legendary

**Effect:** After battle starts, gain 5% of ATK, 8% of ATK SPD, 8% of Energy Regen SPD, and 8% of Pal ATK SPD for 20s. In Team Dungeons, the efectos increase by 50%, last throughout the battles, and are shared with allied characters.

**Passive:** Global DEF +10%

---

### 24. Lustrous Plumage

**Rarity:** Legendary

**Effect:** At the start of battle, each basic attack raises DEF by 0.5%, stackable up to 40 times. Upon reaching maximum stacks, gain a 10% ATK Boost.

**Passive:** Ignore Evasion +15%

---

### 25. Glory Glow

**Rarity:** Legendary

**Effect:** Attacks with tidal waves at the start of battle, increasing Movement SPD by 20% and reducing enemy Movement SPD by 20%. Detects self and enemy Movement SPD every 5s (once at the start of battle): For every 10% Movement SPD increased, increases ATK SPD, Energy Regen SPD and Pal ATK SPD by 2.5%, up to 25%. For every 10% enemy Movement SPD reduced, reduces enemy ATK SPD, Energy Regen SPD and Pal ATK SPD by 2.5%, up to 25%.

**Passive:** Global DEF +10%

---

### 26. Shell Shade

**Rarity:** Legendary

**Effect:** Grants a shield equal to 10% Max HP every 11s after battle starts, lasting 8s. Increases Energy Regen by 50% for the shield's duration, and Final Skill DMG by 10% once the shield is lost, lasting until the end of battle. Stacks up to 2 times. (Triggers at the start of the battle.)

**Passive:** Global HP +10%

---

### 27. Titan's Hold

**Rarity:** Legendary

**Effect:** Every 10 basic attack hits triggers a Combo Punch, dealing 1000% AoE Skill DMG, 200% current Combo AoE DMG (can be Crit) and reducing target's ATK by 4% for 5s, stacking up to 5 times. Every 30 basic attack or combo hits taken triggers a Counter Punch, dealing 1000% AoE Skill DMG and 200% current Counter AoE DMG (can be Crit) and gaining a shield equal to 3.2% Max HP for 2s.

**Passive:** Global DEF +10%

---

### 28. Moonlit Wisp

**Rarity:** Legendary

**Effect:** After the battle begins, each releasing of an active skill increases skill DMG by 1.5%, stacking up to 10 times.

**Passive:** Global HP +10%

---

### 29. Republic of Heroes

**Rarity:** Legendary

**Effect:** After the battle starts, every 10% Max HP lost grants a shield equal to 6% Max HP that lasts 3s, triggering up to 1.5 times. Every 10 basic attack(s) restores HP equal to 400% DEF.

**Passive:** Global DEF +10%

---

### 30. Firework Invite

**Rarity:** Legendary

**Effect:** Every 11s, releases 7 small fireworks within 3s, each dealing 250% AoE Skill DMG, 50% of current Combo AoE DMG (can be Crit), and 50% of current Counter AoE DMG (can be Crit) to all enemies. After 3s, deals extra DMG equal to 30% of the DMG taken by enemies during this time (including DMG absorbed and blocked by shields, but not DMG immune; ignores DMG immunity). (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 31. To the Clouds

**Rarity:** Legendary

**Effect:** After 5 seconds into battle or DMG taken exceeds 20% Max HP, increase ATK by 5% and DEF by 10%. After 10 seconds into battle or DMG taken exceeds 40% of Max HP, reduce all enemies' ATK SPD, Energy Regen SPD and Pal ATK SPD by 10%. After 15 seconds into battle or DMG taken exceeds 60% of Max HP, increase Basic ATK DMG RES, Combo DMG RES, Counter DMG RES, Skill DMG RES and Pal DMG RES by 4%. After 20 seconds into battle or DMG taken exceeds 80% of Max HP, deal DMG equal to 8% of the target's Max HP to all enemies.

**Passive:** Global DEF +10%

---

### 32. Lunar Radiance

**Rarity:** Legendary

**Effect:** For the first 15s, increases all HP Regen efectos by 3%, ATK by 1% and DEF by 2% per second. For the next 15s, reduces all HP Regen efectos by 3%, ATK by 1% and DEF by 2% per second. Rotates every 30s.

**Passive:** Global HP +10%

---

### 33. Song of Frost and Flame

**Rarity:** Legendary

**Effect:** Attacks with the flame sword and frost sword once each every 11s, dealing 1500% AoE Skill DMG, 300% current Combo AoE DMG (can be Crit), and 300% current Counter AoE DMG (can be Crit) with additional efectos. Flame Sword: Cleanses the character's debuffs and increases Pierce by 320 until the battle ends, stacking up to 6 times. Frost Sword: Reduces the target's Movement SPD, ATK SPD, Energy Regen SPD, and Pal ATK SPD by 20% (cannot be cleansed) for 4s. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 34. Phoenix Frost

**Rarity:** Legendary

**Effect:** Block 8% of DMG when it exceeds 1% of your Max HP, 16% when it exceeds 2%, and 30% when it exceeds 5%.

**Passive:** Global HP +10%

---

### 35. Blade Pursuit

**Rarity:** Legendary

**Effect:** After the battle begins, each counter increases counter DMG by 0.5%, stacking up to 60 times.

**Passive:** Global HP +10%

---

### 36. Beastbone Breeze

**Rarity:** Legendary

**Effect:** Each pal's basic attack increases Pal DMG Multiplier by 1.5% after the battle starts, stacking up to 10 times (calculated independently for each pal).

**Passive:** Global DEF +10%

---

### 37. Top-Tier Bodyguard

**Rarity:** Legendary

**Effect:** When an enemy activates an Active Skill, they take 1% of their current HP as damage, and their Energy Regen is reduced by 16% for 2 seconds. This efecto can stack up to 3 times. (If multiple allies have the 'Power Guard' skill, only one instance will apply.)

**Passive:** Global DEF +10%

---

### 38. Punching Storm

**Rarity:** Legendary

**Effect:** Increase Stun Rate by 10%. Upon triggering Stun, deal an extra 1000% Skill DMG and 200% current Basic ATK DMG (can be Crit) to the target and reduce their Crit DMG, Pal Crit DMG, and Skill Crit DMG by 20% and Basic ATK DMG RES and Combo DMG RES by 10% for 2s.

**Passive:** Global DEF +10%

---

### 39. Resolute Soul

**Rarity:** Legendary

**Effect:** The first time HP drops below 60%, Pierce increases by 1000. Below 45%, DMG RES increases by 10%. Below 30%, Final Crit DMG, Final Skill Crit DMG, and Final Pal Crit DMG increase by 10%. Below 25%, gain Unyielding for 5s: ATK, DEF, and Final DMG RES increase by 20%; basic attacks hits deal an additional 40% current Basic ATK DMG (can be Crit); combo hits deal an additional 40% current Combo DMG (can be Crit); counter hits deal an additional 40% current Counter DMG (can be Crit); also restore HP equal to the additional DMG dealt (additional DMG ignores DMG Immunity, and healing ignores PvP reduction).

**Passive:** Global DEF +10%

---

### 40. Frost Mirage

**Rarity:** Legendary

**Effect:** After every 10 basic attacks, launch a snowball at a single target, dealing 200% current Basic ATK DMG (can be Crit). After every 10 Combo hits, launch a snowball at a single target, dealing 200% current Combo DMG (can be Crit). After every 10 Counters, launch a snowball at a single target, dealing 200% current Counter DMG (can be Crit). After every 2 active skills, launch a snowball at a single target, dealing 1000% Skill DMG. Each snowball launched increases ATK SPD by 1.2% until the battle ends, stacking up to 20 times. Snowball hits reduce the target's ATK SPD, Pal ATK SPD, Energy Regen SPD, and Movement SPD by 16% for 1.5s.

**Passive:** Global DEF +10%

---

### 41. Repose in Time

**Rarity:** Legendary

**Effect:** Gains 6% Final DMG RES after the battle starts, which is reduced by 1/4 every 12s. Every 12s, recovers 10% Max HP and uses a random active skill. Each active skill may only be used once, and the effect no longer triggers once all skills are used. (Triggers for the first time 12s into battle.).

**Passive:** Global HP +10%

---

## Config Binary ID Reference — back_id to skill_id (45 mappings)

> Decoded from the config binary. Maps each back accessory's `back_id` to its primary `skill_id` at level 1. Names resolved via `Back_decoration.json` + `Language_en.json`.

| back_id | skill_id | Name |
|---------|----------|------|
| 70004 | 18001 | Lustrous Plumage |
| 70005 | 18002 | Moonlit Wisp |
| 70006 | 18003 | Emerald Embrace |
| 70007 | 18004 | Blade Pursuit |
| 70009 | 70902 | Phoenix Frost |
| 70010 | 18011 | Virtual Connection |
| 70011 | 18008 | Celestial Surprises |
| 70013 | 18015 | Ingredients for Dinner |
| 70014 | 18012 | Metamorphosis |
| 70015 | 18021 | Shell Shade |
| 70016 | 18022 | Summer Parasol |
| 70019 | 18027 | Ghost Behind |
| 70020 | 18025 | Fallen Angel |
| 70021 | 18026 | Beastbone Breeze |
| 70022 | 18030 | Chrono Prism |
| 70023 | 18032 | Miracle Mirage |
| 70024 | 18033 | Till Death Apart |
| 70025 | 18055 | Celestial Gemini |
| 70402 | 18037 | Mirror World |
| 70403 | 18038 | Glory Glow |
| 70404 | 18039 | Titan's Hold |
| 70405 | 18040 | Dawn Warwing |
| 70406 | 18041 | Republic of Heroes |
| 70407 | 18043 | To the Clouds |
| 70409 | 18049 | Song of Frost and Flame |
| 70410 | 18050 | Top-Tier Bodyguard |
| 70411 | 18051 | Punching Storm |
| 70412 | 18052 | Resolute Soul |
| 70413 | 18053 | Frost Mirage |
| 70414 | 18054 | Repose in Time |
| 70416 | 18058 | Meow Mirage |
| 70417 | 18059 | Rollie |
| 70702 | 18036 | Bit Gateway |
| 70704 | 18042 | Firework Invite |
| 70705 | 18044 | Lunar Radiance |
| 70803 | 18023 | Iridescent Aura |
| 70902 | 18007 | Pepe-style Thruster |
| 70903 | 18014 | Arackar Lock |
| 70904 | 18904 | Trapped Wrath |
| 70905 | 18028 | 19th Century |
| 70907 | 18034 | Lord of Light |
| 70908 | 18024 | Alien Dimension |
| 70909 | 18901 | Cosmic Rescue |
| 70910 | 18056 | Cuisine Keeper |
| 70999 | 18029 | Frostland Specter |

**Notes:**
- `back_id` 70009 maps to skill_id `70902` (not in the 18xxx range -- may reference the Pepe-style Thruster back_id as a shared/alias skill)
- 4 entries are new additions not in the original xlsx: Celestial Gemini (70025), Meow Mirage (70416), Rollie (70417), Cuisine Keeper (70910)
- Some accessories have multiple sub-skills at higher skin levels (e.g., 70013 evolves 18015→18017→18018); only the level-1 primary skill_id is listed here

---

## Data Files

- **Source spreadsheet**: `battlesim/reference/LOM_Database-5.xlsx`
- **Structured data**: `battlesim/reference/back_accessories_master.json`
- **Config tables**: `data/tables/Back_skin.json`, `data/tables/Back_decoration.json`