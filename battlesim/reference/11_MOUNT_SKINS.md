# 11 — Mount Skins

> Complete mount reference: all 64 mounts from LOM_Database-5.xlsx + 8 config-only mounts. All 54 combat mounts mapped to skill IDs via decoded ConfigMount_skin binary. See also `mounts_master.json` for structured JSON.

---

## Overview

Mount skins grant combat skills via `ConfigMount_skin.skin_skill`. Each skin has progressive levels with increasing attribute bonuses and skill unlocks. Mount stats are baked into player attributes before battle — only the cosmetic model is loaded at battle time.

**Source:** LOM_Database-5.xlsx + decoded ConfigMount_skin + ConfigMount + Language_en from config binary.

---

## Quick Reference — All 72 Mounts

| # | Name | Rarity | Mount ID | Skill ID | Skill Name | Passive |
|---|------|--------|----------|----------|------------|---------|
| 1 | **Lily Pad** | Rare | 1 | — | *(tier mount)* | — |
| 2 | **Quack Splash** | Rare | 2 | — | *(tier mount)* | — |
| 3 | **Surfboard** | Rare | 3 | — | *(tier mount)* | — |
| 4 | **Flyboard** | Rare | 4 | — | *(tier mount)* | — |
| 5 | **Skyglider** | Epic | 5 | — | *(tier mount)* | — |
| 6 | **Amethyst Gourd** | Epic | 6 | — | *(tier mount)* | — |
| 7 | **Magic Broom** | Legendary | 7 | — | *(tier mount)* | — |
| 8 | **Azure Feather** | Immortal | 25 | — | *(tier mount)* | — |
| 9 | **Soaring Wings** | Supreme | 16 | — | *(tier mount)* | — |
| 10 | **Cyan Phoenixes** | Supreme | 39 | — | *(tier mount)* | — |
| 11 | **Hot Wheels** | Legendary | 9 | 5003 | Hot Wheels | Ignore Stun +6% |
| 12 | **Pyrebreaker** | Legendary | 8 | 5002 | Pyrebreaker | Ignore Evasion +10% |
| 13 | **Skyshark** | Legendary | 40 | 5054 | Missile Blast | Global DEF +10% |
| 14 | **White Tiger** | Legendary | 10 | 5004 | White Tiger | Global Basic ATK DMG +10% |
| 15 | **Boom Da Bang** | Legendary | 37 | 5052 | Tempo Wave | Global DEF +10% |
| 16 | **Blue Ox** | Legendary | 11 | 5005 | Blue Ox | Pal Crit DMG +25% |
| 17 | **Round Frog** | Legendary | 13 | 5007 | Round Frog | Crit RES Bonus +40% |
| 18 | **Blue Queen** | Legendary | 12 | 5019 | Blue Queen | Crit DMG Bonus +40% |
| 19 | **Rum Barrel** | Legendary | 30 | 5031 | Wine Feast | Global DEF +10% |
| 20 | **Blizzard Visitor** | Immortal | 911 | 5046 | Wintry Jingle | Global DEF +10% |
| 21 | **Silvery Crescent** | Immortal | 24 | 5024 | Immortal Ascent | Global HP +10% |
| 22 | **Diving Duck** | Immortal | 33 | 5036 | Super Speedup | Global DEF +10% |
| 23 | **Scorpio** | Immortal | 702 | 5050 | Scorpio | Global DEF +10% |
| 24 | **Wave Cruiser** | Immortal | 403 | 5056 | Wave Commander | Global HP +10% |
| 25 | **Storm Rider** | Immortal | 701 | 5039 | Rainbow of Peace | Global DEF +10% |
| 26 | **Horizon Racer** | Immortal | 22 | 5020 | Horizon Racer | Global HP +10% |
| 27 | **AdaptoSlime** | Immortal | 26 | 5026 | AdaptoSlime | Global HP +10% |
| 28 | **Koi Paper Kite** | Immortal | 20 | 5016 | Koi Paper Kite | Global ATK +10% |
| 29 | **Long-legged Bird** | Immortal | 910 | 5045 | Thanksgiving Feast | Global DEF +10% |
| 30 | **Heart's Desire** | Immortal | 29 | 5030 | Unrivaled Force | Skill Crit DMG +10% |
| 31 | **Book of the Universe** | Immortal | 804 | 5040 | Past Revisited | Global DEF +10% |
| 32 | **Time Machine** | Immortal | 912 | 5047 | 2025 | Global DEF +10% |
| 33 | **Sea of Lanterns** | Immortal | 301 | 5048 | Phoenix Nirvana | Global DEF +10% |
| 34 | **Dimensional Wings** | Immortal | 703 | 5053 | Ultra Awakening | Global DEF +10% |
| 35 | **Mini Motorcycle** | Immortal | 21 | 5014 | Velocity Blitz | Global HP +10% |
| 36 | **Blazing Motorcycle** | Immortal | 23 | 5021 | Blazing Motorcycle | Global DEF +10% |
| 37 | **Cloud Drifter** | Immortal | 15 | 5009 | Cloud Drifter | Global ATK +10% |
| 38 | **Gator Menace** | Immortal | 909 | 5044 | Walk of Terrors | Global DEF +10% |
| 39 | **Pumpkin Carriage** | Immortal | 38 | 5043 | Halloween Express | Global DEF +10% |
| 40 | **Ethereal Phoenix** | Immortal | 406 | 5060 | Purifying Feather | Global DEF +10% |
| 41 | **Nebular Shuttle** | Immortal | 908 | 5042 | Galactic Guard | Global DEF +10% |
| 42 | **Effulgent Fan** | Immortal | 707 | 5059 | Effulgent Dream | Global HP +10% |
| 43 | **Magic Carpet** | Immortal | 19 | 5012 | Magic Carpet | Global ATK +10% |
| 44 | **Panda Attack** | Immortal | 906 | 5038 | Bamboo Muncher | Global DEF +10% |
| 45 | **Vibrant Watermelon Ship** | Immortal | 32 | 5034 | Bite the Watermelon | Global DEF +10% |
| 46 | **Trembling Pepe** | Immortal | 902 | 5029 | Trembling Pepe | Global DEF +10% |
| 47 | **Guardian Spaceship** | Immortal | 405 | 5058 | Guardian of Duty | Global DEF +10% |
| 48 | **Purple Wing** | Immortal | 14 | 5008 | Purple Wing | Global HP +10% |
| 49 | **Thunder Vanguard** | Supreme | 407 | 5061 | Thunder Rush | Global HP +10% |
| 50 | **Holy Dragon** | Supreme | 903 | 5033 | Neon Shadows | Global DEF +10% |
| 51 | **Cheetah Zero** | Supreme | 907 | 5041 | Data Remanence | Global HP +10% |
| 52 | **Speed of Death** | Supreme | 404 | 5057 | Peak of Speed | Global HP +10% |
| 53 | **Cinder Wolf** | Supreme | 402 | 5055 | Lycan Starblaze | Global HP +10% |
| 54 | **Dazzling Unicorn** | Supreme | 803 | 5037 | Spiral Strike | Global DEF +10% |
| 55 | **Skyward Blaze** | Supreme | 901 | 5901 | Skyward Blaze | Global HP +10% |
| 56 | **Sparkling Flash** | Immortal | 408 | 5062 | Flash Support | Global HP +10% |
| 57 | **Cloud Traveler** | Immortal | 708 | 5063 | Deer Leap | Global DEF +10% |
| 58 | **Spectral Ride** | Immortal | 409 | 5066 | Spectral Echoes | Global HP +10% |
| 59 | **Immortal Tyrant** | Immortal | 41 | 5067 | Hellish Breath | Global DEF +10% |
| 60 | **Best Buddy** | Immortal | 410 | 5068 | Follow Me, Pal | Global DEF +10% |
| 61 | **Soaring Shroomie** | Immortal | 411 | 5069 | Strongest Flyer | Global HP +10% |
| 62 | **Sanctuary Warmth** | Supreme | 412 | 5070 | Gift Delivery | Global HP +10% |
| 63 | **Dawn of Time** | Immortal | 413 | 5071 | Temporal Voyage | Global DEF +10% |
| 64 | **Leo** | Immortal | 414 | 5072 | Way of Conquest | Global HP +10% |

---

## Config-Only Mounts (not in xlsx)

These mounts exist in the game config but weren't in the LOM_Database-5.xlsx spreadsheet.

| Name | Mount ID | Skill ID | Skill Name |
|------|----------|----------|------------|
| Squirrel Carriage | 17 | — | — |
| Moon Rabbit-1 | 18 | 5018 | Moon Rabbit-1 |
| Capricorn | 42 | 5073 | Starry Cascade |
| Sanctuary Warmth - Premium | 41201 | — | — |
| Everfish Lantern | 415 | 5049 | Rising Carp |
| Karman | 416 | 5074 | Karmic Trial |
| Empyria | 417 | 5075 | Cosmic Conduction |
| Quivern | 418 | 5054 | Missile Blast |

---

## Tier Mounts (Cosmetic Progression)

These 10 mounts are unlocked by reaching mount level milestones. They have no combat skills — purely cosmetic progression skins.

| # | Name | Rarity | Mount ID |
|---|------|--------|----------|
| 1 | Lily Pad | Rare | 1 |
| 2 | Quack Splash | Rare | 2 |
| 3 | Surfboard | Rare | 3 |
| 4 | Flyboard | Rare | 4 |
| 5 | Skyglider | Epic | 5 |
| 6 | Amethyst Gourd | Epic | 6 |
| 7 | Magic Broom | Legendary | 7 |
| 8 | Azure Feather | Immortal | 25 |
| 9 | Soaring Wings | Supreme | 16 |
| 10 | Cyan Phoenixes | Supreme | 39 |

---

## Combat Skill Mounts — Full Details

### 11. Hot Wheels — Skill 5003: Hot Wheels

**Rarity:** Legendary | **Mount ID:** 9 | **Skill ID:** 5003

**Effect:** Boost Pal Attack Speed by 2% per second (up to 40%).

**Passive:** Ignore Stun +6%

---

### 12. Pyrebreaker — Skill 5002: Pyrebreaker

**Rarity:** Legendary | **Mount ID:** 8 | **Skill ID:** 5002

**Effect:** Increase base Crit rate by 1% and Crit DMG by 5% per second (up to 20%, 100%).

**Passive:** Ignore Evasion +10%

---

### 13. Skyshark — Skill 5054: Missile Blast

**Rarity:** Legendary | **Mount ID:** 40 | **Skill ID:** 5054

**Effect:** Launches a shark missile every 12s, dealing 1600% AoE Skill DMG and restoring HP equal to the DMG dealt, up to 30% of Max HP, ignoring PvP reduction. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 14. White Tiger — Skill 5004: White Tiger

**Rarity:** Legendary | **Mount ID:** 10 | **Skill ID:** 5004

**Effect:** Targets with HP percentage below the caster take 15% increased DMG, while those with HP percentage above the caster have their ATK reduced by 10%.

**Passive:** Global Basic ATK DMG +10%

---

### 15. Boom Da Bang — Skill 5052: Tempo Wave

**Rarity:** Legendary | **Mount ID:** 37 | **Skill ID:** 5052

**Effect:** ATK, ATK SPD, Energy Regen SPD, and Pal ATK SPD increase by 4% every 10s, stacking up to 6 times. (Triggers at the start of the battle.) At 6 stacks or when below 40% HP, stuns all enemies for 1.5s and reduces their DMG RES by 10% until the battle ends.

**Passive:** Global DEF +10%

---

### 16. Blue Ox — Skill 5005: Blue Ox

**Rarity:** Legendary | **Mount ID:** 11 | **Skill ID:** 5005

**Effect:** Increase DMG RES by 10% and shorten the duration of control effects by 30%.

**Passive:** Pal Crit DMG +25%

---

### 17. Round Frog — Skill 5007: Round Frog

**Rarity:** Legendary | **Mount ID:** 13 | **Skill ID:** 5007

**Effect:** Every 10 second, defeat 1 enemies, boosting ATK by 15% for 5 seconds. If the target is a Boss or player, stun for an additional 1 seconds.

**Passive:** Crit RES Bonus +40%

---

### 18. Blue Queen — Skill 5019: Blue Queen

**Rarity:** Legendary | **Mount ID:** 12 | **Skill ID:** 5019

**Effect:** Distribute 10% of DMG dealt to up to 5 surrounding enemies when dealing DMG.

**Passive:** Crit DMG Bonus +40%

---

### 19. Rum Barrel — Skill 5031: Wine Feast

**Rarity:** Legendary | **Mount ID:** 30 | **Skill ID:** 5031

**Effect:** For every 20% Max HP missing, deal 800% Basic ATK AoE DMG within a range, gain 10% ATK and take 10% less DMG for 5s (triggers at the start of the battle)

**Passive:** Global DEF +10%

---

### 20. Blizzard Visitor — Skill 5046: Wintry Jingle

**Rarity:** Immortal | **Mount ID:** 911 | **Skill ID:** 5046

**Effect:** Reduces all target's Movement SPD by 25%. For every 10% Movement SPD they lose, reduces their ATK by 2% and increases the duration of control effects on them by 2%.

**Passive:** Global DEF +10%

---

### 21. Silvery Crescent — Skill 5024: Immortal Ascent

**Rarity:** Immortal | **Mount ID:** 24 | **Skill ID:** 5024

**Effect:** Gain Death Immunity for 2s upon taking lethal DMG, and immediately recover 10% Max HP.

**Passive:** Global HP +10%

---

### 22. Diving Duck — Skill 5036: Super Speedup

**Rarity:** Immortal | **Mount ID:** 33 | **Skill ID:** 5036

**Effect:** B.Duck creates splashes around every 11s, dealing 2000% Skill DMG, 800% Combo DMG and 800% Counter DMG to all enemies in the area and reducing their ATK by 10% until the battle ends; the effects don't stack. The skill deals 50% more DMG when cast again. When the skill hits the same target again, reduces their ATK by 3% more, stacking up to 2 times. (Casts 1 time immediately after battle starts.)

**Passive:** Global DEF +10%

---

### 23. Scorpio — Skill 5050: Scorpio

**Rarity:** Immortal | **Mount ID:** 702 | **Skill ID:** 5050

**Effect:** Inflicts 1 stack of Poison on enemies in a small area every 15s, each stack dealing Bleed DMG equal to 0.8% of the target's current HP per second (ignores Immunity) until the battle ends. Poison stacks up to 10 times. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 24. Wave Cruiser — Skill 5056: Wave Commander

**Rarity:** Immortal | **Mount ID:** 403 | **Skill ID:** 5056

**Effect:** Gains 5 wave stack(s) at the start of battle, each reducing enemy Final Crit DMG, Final Pal Crit DMG and Final Skill Crit DMG by 4%. Breaks 1 wave stack every 6s or after every 20 basic attacks, increasing Movement SPD by 8% and ATK by 6% until the battle ends, stacking up to 5 times.

**Passive:** Global HP +10%

---

### 25. Storm Rider — Skill 5039: Rainbow of Peace

**Rarity:** Immortal | **Mount ID:** 701 | **Skill ID:** 5039

**Effect:** Increase DMG RES by 5% and shorten the duration of control effects by 15%. The first time HP drops below 80%, increase DMG RES by 8% and shorten the duration of control effects by 25% for 8s. The first time HP drops below 60%, increase DMG RES by 8% and shorten the duration of control effects by 25% for 12s. The first time HP drops below 40%, increase DMG RES by 8% and shorten the duration of control effects by 25% until the battle ends. Each effect is counted independently and stackable.

**Passive:** Global DEF +10%

---

### 26. Horizon Racer — Skill 5020: Horizon Racer

**Rarity:** Immortal | **Mount ID:** 22 | **Skill ID:** 5020

**Effect:** Every 10 second, summon a car, dealing 800% current basic attack AoE DMG and knocking back targets.

**Passive:** Global HP +10%

---

### 27. AdaptoSlime — Skill 5026: AdaptoSlime

**Rarity:** Immortal | **Mount ID:** 26 | **Skill ID:** 5026

**Effect:** Increases ATK by 15% for 10 seconds when HP drops below 80%. Gains a shield equal to 10% of max HP for 10 seconds when HP drops below 60%. Reduces DMG taken by 15% for 10 seconds when HP drops below 30%.

**Passive:** Global HP +10%

---

### 28. Koi Paper Kite — Skill 5016: Koi Paper Kite

**Rarity:** Immortal | **Mount ID:** 20 | **Skill ID:** 5016

**Effect:** Every 3 combo triggers an additional 500% AoE DMG.

**Passive:** Global ATK +10%

---

### 29. Long-legged Bird — Skill 5045: Thanksgiving Feast

**Rarity:** Immortal | **Mount ID:** 910 | **Skill ID:** 5045

**Effect:** There is a 50% chance to gain 4% ATK, 4% DMG RES and 10% Control Duration Reduction every 4s after the battle starts. This lasts until the battle ends and stacks up to 3 times (the chances of the 3 effects are independently calculated). There is a 100% chance to grant the Summon 4% ATK, 4% DMG RES and 10% Control Duration Reduction until the Summon disappears, stacking up to 3 times. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 30. Heart's Desire — Skill 5030: Unrivaled Force

**Rarity:** Immortal | **Mount ID:** 29 | **Skill ID:** 5030

**Effect:** Every second for the first 20 seconds has a 60% chance to boost ATK by 1% and DMG RES by 1% until the battle ends. After 20 seconds, deals 8000% AoE Skill DMG and launches the target airborne for 0.5 second.

**Passive:** Skill Crit DMG +10%

---

### 31. Book of the Universe — Skill 5040: Past Revisited

**Rarity:** Immortal | **Mount ID:** 804 | **Skill ID:** 5040

**Effect:** When casting an active skill, the Character has a 15% chance to cast it again (excluding those cast by Past Revisited and Eye of Raven).

**Passive:** Global DEF +10%

---

### 32. Time Machine — Skill 5047: 2025

**Rarity:** Immortal | **Mount ID:** 912 | **Skill ID:** 5047

**Effect:** For the first 20s after the battle starts, negates and stores 40% of all DMG taken and gains 8% of ATK, 10% of Final Crit DMG, 10% of Final Skill Crit DMG and 10% of Final Pal Crit DMG. After the first 20s of the battle, receives an additional 6% of the stored DMG (ignores Immunity) per second for 10s.

**Passive:** Global DEF +10%

---

### 33. Sea of Lanterns — Skill 5048: Phoenix Nirvana

**Rarity:** Immortal | **Mount ID:** 301 | **Skill ID:** 5048

**Effect:** After 15s into battle, becomes immune to DMG for 2s and gains 15% Final Crit DMG, 15% Final Skill Crit DMG, and 15% Final Pal Crit DMG until the battle ends. Current HP changes into 40% Max HP during DMG immunity.

**Passive:** Global DEF +10%

---

### 34. Dimensional Wings — Skill 5053: Ultra Awakening

**Rarity:** Immortal | **Mount ID:** 703 | **Skill ID:** 5053

**Effect:** Gain 1 bar of Rage for every 15 basic attacks, 12 combos, 12 counters, 3 active skill(s), or after taking damage equal to 18% of Max HP. Each bar of Rage increases DEF by 3%. At 5 bars, uses all Rage to increase DMG RES, ATK, Crit Rate, Skill Crit Rate, Pal Crit Rate, Crit DMG, Pal Crit DMG and Skill Crit DMG by 12% for 5s.

**Passive:** Global DEF +10%

---

### 35. Mini Motorcycle — Skill 5014: Velocity Blitz

**Rarity:** Immortal | **Mount ID:** 21 | **Skill ID:** 5014

**Effect:** With every 1 counter, increase global counter DMG by 10% for 3 seconds, up to a maximum of 30%. The duration refreshes with each new counter trigger.

**Passive:** Global HP +10%

---

### 36. Blazing Motorcycle — Skill 5021: Blazing Motorcycle

**Rarity:** Immortal | **Mount ID:** 23 | **Skill ID:** 5021

**Effect:** For every 10% lost HP, release a flame jet, dealing at least 500% of current basic attack DMG (scales with lost HP).

**Passive:** Global DEF +10%

---

### 37. Cloud Drifter — Skill 5009: Cloud Drifter

**Rarity:** Immortal | **Mount ID:** 15 | **Skill ID:** 5009

**Effect:** Increase Skill Crit Rate by 10%. After a skill critical, boost ATK by 20% for 5 seconds.

**Passive:** Global ATK +10%

---

### 38. Gator Menace — Skill 5044: Walk of Terrors

**Rarity:** Immortal | **Mount ID:** 909 | **Skill ID:** 5044

**Effect:** After the battle starts, every 5 seconds, deal DMG equal to 4% of the maximum HP to all targets within range, reducing their DMG RES by 2% and Crit RES by 20% until the battle ends, stacking up to 5 times.

**Passive:** Global DEF +10%

---

### 39. Pumpkin Carriage — Skill 5043: Halloween Express

**Rarity:** Immortal | **Mount ID:** 38 | **Skill ID:** 5043

**Effect:** Deals 2000% AoE Skill DMG, 800% current Combo AoE DMG, and 800% current Counter AoE DMG every 11s after the battle starts, and the targets take DMG equal to 2% of current HP per second with ATK and DMG RES reduced by 10% for 5s. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 40. Ethereal Phoenix — Skill 5060: Purifying Feather

**Rarity:** Immortal | **Mount ID:** 406 | **Skill ID:** 5060

**Effect:** Cleanse and ignore control effects for 1s for every 18% Max HP lost. Gain a shield equal to 8% Max HP, lasting 5s. After the shield expires, ATK increases by 4% until the battle ends, stacking up to 6 times.

**Passive:** Global DEF +10%

---

### 41. Nebular Shuttle — Skill 5042: Galactic Guard

**Rarity:** Immortal | **Mount ID:** 908 | **Skill ID:** 5042

**Effect:** Grants a shield equal to 10% Max HP every 11s after battle starts, lasting 8s. Grants 6% DMG RES for the shield's duration; cleanses and increases Final DMG RES by 3% and ATK by 3% once the shield is lost, lasting until the end of battle. Stacks up to 3 times. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 42. Effulgent Fan — Skill 5059: Effulgent Dream

**Rarity:** Immortal | **Mount ID:** 707 | **Skill ID:** 5059

**Effect:** Every 11s, increases Crit Rate by 30% and Skill Crit Rate by 30% for 3s. For every 5 Crits or 1 Skill Crit hit during this period, fireworks deal 200% of current Basic ATK AoE DMG (can be Crit) to enemies and increase Final Crit DMG and Final Skill Crit DMG by 6% for 3s, stacking up to 5 times. (Triggers at the start of the battle.)

**Passive:** Global HP +10%

---

### 43. Magic Carpet — Skill 5012: Magic Carpet

**Rarity:** Immortal | **Mount ID:** 19 | **Skill ID:** 5012

**Effect:** After casting skills 6 times, restore full energy to 1 random skills.

**Passive:** Global ATK +10%

---

### 44. Panda Attack — Skill 5038: Bamboo Muncher

**Rarity:** Immortal | **Mount ID:** 906 | **Skill ID:** 5038

**Effect:** Every 10s, gains Control Immunity for 3-5s and boosts ATK by 5%-12% and DMG RES by 5%-12% for 10s. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 45. Vibrant Watermelon Ship — Skill 5034: Bite the Watermelon

**Rarity:** Immortal | **Mount ID:** 32 | **Skill ID:** 5034

**Effect:** Increases ATK by 10% and DEF by 30% every 11s for 5s. After this, a Watermelon Ship is summoned to unleash a wave that launches enemies for 0.5s, dealing 2000% Skill DMG, 800% current Combo DMG, and 800% current Counter DMG as AoE DMG. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 46. Trembling Pepe — Skill 5029: Trembling Pepe

**Rarity:** Immortal | **Mount ID:** 902 | **Skill ID:** 5029

**Effect:** These two buffs will alternate to take effect every 8s: Gain a Shield with 8% of Max HP, lasting 8s. Gain 8% ATK and reduce the time of being controlled by 30% for 8s.

**Passive:** Global DEF +10%

---

### 47. Guardian Spaceship — Skill 5058: Guardian of Duty

**Rarity:** Immortal | **Mount ID:** 405 | **Skill ID:** 5058

**Effect:** Gain a shield equal to 6% Max HP every 9s for 6s. 6s later, reflects 20% of the total DMG received within the 6s to all enemies. (Only DMG absorbed and blocked by the shield can be reflected, not DMG ignored by Immunity.)

**Passive:** Global DEF +10%

---

### 48. Purple Wing — Skill 5008: Purple Wing

**Rarity:** Immortal | **Mount ID:** 14 | **Skill ID:** 5008

**Effect:** After the battle begins, immediately deals 5000% AoE DMG, and launches targets within the range for 0.5 seconds. Releases every 11 seconds.

**Passive:** Global HP +10%

---

### 49. Thunder Vanguard — Skill 5061: Thunder Rush

**Rarity:** Supreme | **Mount ID:** 407 | **Skill ID:** 5061

**Effect:** Increase DEF by 36% after the battle starts. Ram forward every 8s, dealing 1000% Skill DMG, 200% current Combo DMG (can be Crit), 200% current Counter DMG (can be Crit), and DMG equal to 4% Max HP to targets in the area. If targets are immune to damage or death, reduce their ATK by an additional 24% for 5s. Afterwards, DEF is reduced by 6% while ATK increases by 3%, stacking up to 6 times. (Triggers at the start of the battle.)

**Passive:** Global HP +10%

---

### 50. Holy Dragon — Skill 5033: Neon Shadows

**Rarity:** Supreme | **Mount ID:** 903 | **Skill ID:** 5033

**Effect:** Gain 3 stacks of Guard every 11s, each stack increasing DEF by 100% but losing 1 stack every 1s. Deal 2000% Skill DMG, 800% current Combo DMG and 800% current Counter DMG at the end of Guard (triggers at the start of the battle)

**Passive:** Global DEF +10%

---

### 51. Cheetah Zero — Skill 5041: Data Remanence

**Rarity:** Supreme | **Mount ID:** 907 | **Skill ID:** 5041

**Effect:** Gain Death Immunity for 3s when taking lethal damage. For the duration, ignore new control effects (doesn't affect existing control), gain 10% ATK, 10% Crit Rate, 10% Final Crit DMG, 10% Skill Crit Rate, 10% Final Skill Crit DMG, 10% Pal Crit Rate, and 10% Final Pal Crit DMG, and the next basic attack deals 3000% Skill DMG, 1200% Current Combo DMG (can be Crit), 1200% Current Counter DMG (can be Crit), and DMG equal to 8% Max HP to enemies in the area. The character explodes at the end of the duration.

**Passive:** Global HP +10%

---

### 52. Speed of Death — Skill 5057: Peak of Speed

**Rarity:** Supreme | **Mount ID:** 404 | **Skill ID:** 5057

**Effect:** Gains 20% Evasion. Activates speed-up mode at the start of battle: Every 1 evasions, 8 basic attacks, 8 combos, 8 counters, or 2 active skills used increases Movement SPD by 8% until the burst ends. After Movement SPD reaches 200% of its initial value, activates charge mode: Increases DMG RES by 9% for 5s. After charge mode ends, activates burst mode: Cleanses and becomes immune to control effects, recovers 12% of lost HP per second, and increases DMG RES by 12%, ATK, DEF, ATK SPD, Energy Regen SPD and Pal ATK SPD by 32% for 5s. Returns to speed-up mode after the burst ends.

**Passive:** Global HP +10%

---

### 53. Cinder Wolf — Skill 5055: Lycan Starblaze

**Rarity:** Supreme | **Mount ID:** 402 | **Skill ID:** 5055

**Effect:** Gains 10% ATK and 16% Final Crit RES after the battle starts. The first time HP drops below 39%, cleanses debuffs, becomes immune to damage for 1s, converts HP into 10% Max HP, and gains a shield equal to 45% of Max HP (ignores PvP reduction and shield breaks). For the shield's duration, reduces HP Regen by 100%, ignores control effects, but gains 10% DMG RES; the character's basic attacks deal 250% extra Skill DMG, 50% extra Combo DMG (can be Crit), 50% extra Counter DMG (can be Crit), while pals' basic attacks deal 50% extra Pal DMG (can be Crit).

**Passive:** Global HP +10%

---

### 54. Dazzling Unicorn — Skill 5037: Spiral Strike

**Rarity:** Supreme | **Mount ID:** 803 | **Skill ID:** 5037

**Effect:** The unicorn spreads its wings every 12s, resisting DMG of the next active skill hit on the Character (excluding Class, Avian, and Summoning Skills), during which the Character gains 50% DEF and ignores all control effects. After the unicorn resists DMG, the DEF boost and control immunity effects disappear. Meanwhile, the Chracter reflects the active skill to the attacker and gains 4% ATK and 4% DMG RES until the battle ends, up to 3 stacks. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 55. Skyward Blaze — Skill 5901: Skyward Blaze

**Rarity:** Supreme | **Mount ID:** 901 | **Skill ID:** 5901

**Effect:** Deals 600% current Basic ATK AoE DMG to an area every 10s and burns the targets, who will receive 40% current Basic ATK DMG per second until the battle ends, stacking up to 3 times. Gains an additional 4% ATK and DEF and 4% DMG RES until the battle ends, stacking up to 3 times. (Casts 1 time immediately after battle starts.)

**Passive:** Global HP +10%

---

### 56. Sparkling Flash — Skill 5062: Flash Support

**Rarity:** Immortal | **Mount ID:** 408 | **Skill ID:** 5062

**Effect:** Every 8s after the battle starts, gain a support from Sparkling Flash (triggers at the start of the battle). For every 10% HP over 50% Max HP, gain 2% ATK and DEF for 8s. If below 50% HP, restore 12% of lost HP and gain 10% DMG RES for 8s.

**Passive:** Global HP +10%

---

### 57. Cloud Traveler — Skill 5063: Deer Leap

**Rarity:** Immortal | **Mount ID:** 708 | **Skill ID:** 5063

**Effect:** Healing Amount increases by 0.3%. For every 15% Max HP lost, restores 7% of lost HP and gains 5% DMG RES for 4s, stacking up 4 times.

**Passive:** Global DEF +10%

---

### 58. Spectral Ride — Skill 5066: Spectral Echoes

**Rarity:** Immortal | **Mount ID:** 409 | **Skill ID:** 5066

**Effect:** When an opponent's HP drops below 88% for the first time, their ATK is reduced by 16%. Upon first falling below 66% HP, their DMG RES is decreased by 16%. At 44% HP, their ATK SPD, Pal ATK SPD, and Energy Regen are reduced by 16%. When HP falls below 22%, the enemy takes 1.6% of their max HP as damage per second, ignoring DMG Immunity.

**Passive:** Global HP +10%

---

### 59. Immortal Tyrant — Skill 5067: Hellish Breath

**Rarity:** Immortal | **Mount ID:** 41 | **Skill ID:** 5067

**Effect:** Every 11s, releases the icy breath, reducing all enemies' Movement SPD, ATK SPD, Pal ATK SPD, Energy Regen SPD, and HP Regen by 60%. Loses 1/5 of the effects every 1.2s (cannot be cleansed; triggers at the start of the battle.).

**Passive:** Global DEF +10%

---

### 60. Best Buddy — Skill 5068: Follow Me, Pal

**Rarity:** Immortal | **Mount ID:** 410 | **Skill ID:** 5068

**Effect:** At the start of the battle, the Character gains 12% DMG RES, which decays by 1/3 every 12s. Every 1% of the Character's Ignore Evasion grants pals 0.2% Ignore Evasion. For every 5 basic attacks or combo hits from a pal, restore the Character's HP by 1% Max HP and increase the pal's ATK SPD by 2%, stacking up to 10 times (independently counted for each pal).

**Passive:** Global DEF +10%

---

### 61. Soaring Shroomie — Skill 5069: Strongest Flyer

**Rarity:** Immortal | **Mount ID:** 411 | **Skill ID:** 5069

**Effect:** Movement SPD increases by 20% at the start of battle and by an additional 10% every 5s after that, stacking up to 10 times. For every 10% Movement SPD that the Character has higher than the base value of 10%, increase their Evasion and ATK SPD by 3.2% (up to 32%), Crit DMG and Skill Crit DMG by 2.4% (up to 24%), and Final DMG RES by 1.6% (up to 16%).

**Passive:** Global HP +10%

---

### 62. Sanctuary Warmth — Skill 5070: Gift Delivery

**Rarity:** Supreme | **Mount ID:** 412 | **Skill ID:** 5070

**Effect:** The first time HP drops below 70%/50%/30%, gain a Pink/Yellow/Purple Gift. Each gift is gained cleanses debuffs and grants DMG and Control Immunity for 0.6s and a shield equal to 20% Max HP for 8s. While the shield persists, the Character's Final DMG RES increases by 10%. (Shields and Final DMG RES from differents gifts stack) When the shield expires, gain the following effects based on gift color: Pink: ATK increases by 10% and DEF by 30%. Yellow: Crit Rate, Pal Crit Rate, Final Crit DMG, Final Pal Crit DMG, and Final Skill Crit DMG increase by 10%. Purple: Restore 24% Max HP and deal 5000% Skill DMG, 1000% current Basic ATK DMG (can be Crit), 1000% current Combo DMG (can be Crit), and 1000% current Counter DMG (can be Crit) to all enemies. (DMG from the purple gift ignores DMG Immunity.)

**Passive:** Global HP +10%

---

### 63. Dawn of Time — Skill 5071: Temporal Voyage

**Rarity:** Immortal | **Mount ID:** 413 | **Skill ID:** 5071

**Effect:** Gains 16% DMG RES after the battle starts, which is reduced by 1/4 every 12s. Every 12s, gains a shield equal to 10% Max HP that lasts 5s, and increases Final DMG Boost by 40% and all HP Regen effects by 60% for 3s. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 64. Leo — Skill 5072: Way of Conquest

**Rarity:** Immortal | **Mount ID:** 414 | **Skill ID:** 5072

**Effect:** Every 10s after battle starts, reduces all enemies' ATK, Crit Rate, Skill Crit Rate, Combo Rate, Counter Rate, Pal Crit Rate, and Pal Combo Rate by 20% for 6s (cannot be cleansed). Meanwhile, increases ATK, Crit Rate, Skill Crit Rate, Combo Rate, Counter Rate, Pal Crit Rate, and Pal Combo Rate by 20% for 6s. (Triggers at the start of the battle.)

**Passive:** Global HP +10%

---

## Skill ID → Mount Name Lookup

| Skill ID | Skill Name | Mount Name | Mount ID |
|----------|------------|------------|----------|
| 5002 | Pyrebreaker | Pyrebreaker | 8 |
| 5003 | Hot Wheels | Hot Wheels | 9 |
| 5004 | White Tiger | White Tiger | 10 |
| 5005 | Blue Ox | Blue Ox | 11 |
| 5007 | Round Frog | Round Frog | 13 |
| 5008 | Purple Wing | Purple Wing | 14 |
| 5009 | Cloud Drifter | Cloud Drifter | 15 |
| 5012 | Magic Carpet | Magic Carpet | 19 |
| 5014 | Velocity Blitz | Mini Motorcycle | 21 |
| 5016 | Koi Paper Kite | Koi Paper Kite | 20 |
| 5018 | Moon Rabbit-1 | Moon Rabbit-1 | 18 |
| 5019 | Blue Queen | Blue Queen | 12 |
| 5020 | Horizon Racer | Horizon Racer | 22 |
| 5021 | Blazing Motorcycle | Blazing Motorcycle | 23 |
| 5024 | Immortal Ascent | Silvery Crescent | 24 |
| 5026 | AdaptoSlime | AdaptoSlime | 26 |
| 5029 | Trembling Pepe | Trembling Pepe | 902 |
| 5030 | Unrivaled Force | Heart's Desire | 29 |
| 5031 | Wine Feast | Rum Barrel | 30 |
| 5033 | Neon Shadows | Holy Dragon | 903 |
| 5034 | Bite the Watermelon | Vibrant Watermelon Ship | 32 |
| 5036 | Super Speedup | Diving Duck | 33 |
| 5037 | Spiral Strike | Dazzling Unicorn | 803 |
| 5038 | Bamboo Muncher | Panda Attack | 906 |
| 5039 | Rainbow of Peace | Storm Rider | 701 |
| 5040 | Past Revisited | Book of the Universe | 804 |
| 5041 | Data Remanence | Cheetah Zero | 907 |
| 5042 | Galactic Guard | Nebular Shuttle | 908 |
| 5043 | Halloween Express | Pumpkin Carriage | 38 |
| 5044 | Walk of Terrors | Gator Menace | 909 |
| 5045 | Thanksgiving Feast | Long-legged Bird | 910 |
| 5046 | Wintry Jingle | Blizzard Visitor | 911 |
| 5047 | 2025 | Time Machine | 912 |
| 5048 | Phoenix Nirvana | Sea of Lanterns | 301 |
| 5049 | Rising Carp | Everfish Lantern | 415 |
| 5050 | Scorpio | Scorpio | 702 |
| 5052 | Tempo Wave | Boom Da Bang | 37 |
| 5053 | Ultra Awakening | Dimensional Wings | 703 |
| 5054 | Missile Blast | Quivern | 418 |
| 5054 | Missile Blast | Skyshark | 40 |
| 5055 | Lycan Starblaze | Cinder Wolf | 402 |
| 5056 | Wave Commander | Wave Cruiser | 403 |
| 5057 | Peak of Speed | Speed of Death | 404 |
| 5058 | Guardian of Duty | Guardian Spaceship | 405 |
| 5059 | Effulgent Dream | Effulgent Fan | 707 |
| 5060 | Purifying Feather | Ethereal Phoenix | 406 |
| 5061 | Thunder Rush | Thunder Vanguard | 407 |
| 5062 | Flash Support | Sparkling Flash | 408 |
| 5063 | Deer Leap | Cloud Traveler | 708 |
| 5066 | Spectral Echoes | Spectral Ride | 409 |
| 5067 | Hellish Breath | Immortal Tyrant | 41 |
| 5068 | Follow Me, Pal | Best Buddy | 410 |
| 5069 | Strongest Flyer | Soaring Shroomie | 411 |
| 5070 | Gift Delivery | Sanctuary Warmth | 412 |
| 5071 | Temporal Voyage | Dawn of Time | 413 |
| 5072 | Way of Conquest | Leo | 414 |
| 5073 | Starry Cascade | Capricorn | 42 |
| 5074 | Karmic Trial | Karman | 416 |
| 5075 | Cosmic Conduction | Empyria | 417 |
| 5901 | Skyward Blaze | Skyward Blaze | 901 |

---

## Class Synergies — Best Mount Per Class

| Class | Best Mount(s) | Reason |
|-------|--------------|--------|
| Martial Sage | Speed of Death (5057), Dazzling Unicorn (5037), Cinder Wolf (5055) | Counter feeds speed stacks; skill reflect; death immunity + shield |
| Warbringer | Blazing Motorcycle (5021), Mini Motorcycle (5014), Cheetah Zero (5041) | HP-loss scaling; counter DMG stacking; death immunity burst |
| Sacred Hunter | Speed of Death (5057), Ethereal Phoenix (5060), Default (5001) | Evasion feeds speed stacks; CC cleanse + shield; raw evasion |
| Plume Monarch | Koi Paper Kite (5016), Effulgent Fan (5059) | Combo rate feeds AoE; crit window synergy |
| Prophet | Cloud Drifter (5009), Magic Carpet (5012), Book of the Universe (5040) | Skill crit synergy; skill energy restore; skill recast |
| Darklord | Cloud Drifter (5009), Magic Carpet (5012) | Skill crit +20% stacks with +50% passive; free skill recharges |
| Beastmaster | Hot Wheels (5003), Best Buddy (5068), Diving Duck (5036) | Pal ATK speed; pal heal + ignore evasion sharing; AoE + ATK debuff |
| Supreme Spirit | Hot Wheels (5003), Heart's Desire (5030), Time Machine (5047) | Pal speed; late-game burst; stored DMG release |

---

## Data Files

- **Source spreadsheet**: `battlesim/reference/LOM_Database-5.xlsx`
- **Structured data**: `battlesim/reference/mounts_master.json` — All 64+8 mounts with complete skill mappings
- **Config binary decoded**: `data/tables/Mount_skin.json`, `data/tables/Mount.json`, `data/tables/Skill.json`
- **Localization**: `data/tables/Language_en.json` — English mount and skill names