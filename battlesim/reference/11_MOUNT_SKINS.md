# 11 — Mount Skins

> Complete mount reference: all 64 mounts from LOM_Database-5.xlsx (data_mounts.ts). 19 mapped to reverse-engineered code skill IDs with buff/coefficient data. See also `mounts_master.json` for structured JSON.

---

## Overview

Mount skins grant combat skills via `ConfigMount_skin.skin_skill`. Each skin has progressive levels with increasing attribute bonuses and skill unlocks. Mount stats are baked into player attributes before battle — only the cosmetic model is loaded at battle time.

**Source:** LOM_Database-5.xlsx → data_mounts.ts (Global filtered), cross-referenced with reverse-engineered game code.

---

## Quick Reference — All 64 Mounts

| # | Name | Rarity | Skill ID | Passive | Key Effect |
|---|------|--------|----------|---------|------------|
| 1 | **Lily Pad** | Rare | — | — | *(tier mount — no combat skill)* |
| 2 | **Quack Splash** | Rare | — | — | *(tier mount — no combat skill)* |
| 3 | **Surfboard** | Rare | — | — | *(tier mount — no combat skill)* |
| 4 | **Flyboard** | Rare | — | — | *(tier mount — no combat skill)* |
| 5 | **Skyglider** | Epic | — | — | *(tier mount — no combat skill)* |
| 6 | **Amethyst Gourd** | Epic | — | — | *(tier mount — no combat skill)* |
| 7 | **Magic Broom** | Legendary | — | — | *(tier mount — no combat skill)* |
| 8 | **Azure Feather** | Immortal | — | — | *(tier mount — no combat skill)* |
| 9 | **Soaring Wings** | Supreme | — | — | *(tier mount — no combat skill)* |
| 10 | **Cyan Phoenixes** | Supreme | — | — | *(tier mount — no combat skill)* |
| 11 | **Hot Wheels** | Legendary | 5003 | Ignore Stun +6% | Boost Pal Attack Speed by 2% per second (up to 40%). |
| 12 | **Pyrebreaker** | Legendary | 5002 | Ignore Evasion +10% | Increase base Crit rate by 1% and Crit DMG by 5% per second (up to 20%, 100%). |
| 13 | **Skyshark** | Legendary | — | Global DEF +10% | Launches a shark missile every 12s, dealing 1600% AoE Skill DMG and restoring... |
| 14 | **White Tiger** | Legendary | 5004 | Global Basic ATK DMG +10% | Targets with HP percentage below the caster take 15% increased DMG, while tho... |
| 15 | **Boom Da Bang** | Legendary | — | Global DEF +10% | ATK, ATK SPD, Energy Regen SPD, and Pal ATK SPD increase by 4% every 10s, sta... |
| 16 | **Blue Ox** | Legendary | 5005 | Pal Crit DMG +25% | Increase DMG RES by 10% and shorten the duration of control effects by 30%. |
| 17 | **Round Frog** | Legendary | 5007 | Crit RES Bonus +40% | Every 10 second, defeat 1 enemies, boosting ATK by 15% for 5 seconds. If the ... |
| 18 | **Blue Queen** | Legendary | 5006 | Crit DMG Bonus +40% | Distribute 10% of DMG dealt to up to 5 surrounding enemies when dealing DMG. |
| 19 | **Rum Barrel** | Legendary | — | Global DEF +10% | For every 20% Max HP missing, deal 800% Basic ATK AoE DMG within a range, gai... |
| 20 | **Blizzard Visitor** | Immortal | — | Global DEF +10% | Reduces all target's Movement SPD by 25%. For every 10% Movement SPD they los... |
| 21 | **Silvery Crescent** | Immortal | 5024 | Global HP +10% | Gain Death Immunity for 2s upon taking lethal DMG, and immediately recover 10... |
| 22 | **Diving Duck** | Immortal | — | Global DEF +10% | B.Duck creates splashes around every 11s, dealing 2000% Skill DMG, 800% Combo... |
| 23 | **Scorpio** | Immortal | — | Global DEF +10% | Inflicts 1 stack of Poison on enemies in a small area every 15s, each stack d... |
| 24 | **Wave Cruiser** | Immortal | — | Global HP +10% | Gains 5 wave stack(s) at the start of battle, each reducing enemy Final Crit ... |
| 25 | **Storm Rider** | Immortal | — | Global DEF +10% | Increase DMG RES by 5% and shorten the duration of control effects by 15%. Th... |
| 26 | **Horizon Racer** | Immortal | — | Global HP +10% | Every 10 second, summon a car, dealing 800% current basic attack AoE DMG and ... |
| 27 | **AdaptoSlime** | Immortal | 5026 | Global HP +10% | Increases ATK by 15% for 10 seconds when HP drops below 80%. Gains a shield e... |
| 28 | **Koi Paper Kite** | Immortal | 5016 | Global ATK +10% | Every 3 combo triggers an additional 500% AoE DMG. |
| 29 | **Long-legged Bird** | Immortal | — | Global DEF +10% | There is a 50% chance to gain 4% ATK, 4% DMG RES and 10% Control Duration Red... |
| 30 | **Heart's Desire** | Immortal | 5030 | Skill Crit DMG +10% | Every second for the first 20 seconds has a 60% chance to boost ATK by 1% and... |
| 31 | **Book of the Universe** | Immortal | — | Global DEF +10% | When casting an active skill, the Character has a 15% chance to cast it again... |
| 32 | **Time Machine** | Immortal | — | Global DEF +10% | For the first 20s after the battle starts, negates and stores 40% of all DMG ... |
| 33 | **Sea of Lanterns** | Immortal | — | Global DEF +10% | After 15s into battle, becomes immune to DMG for 2s and gains 15% Final Crit ... |
| 34 | **Dimensional Wings** | Immortal | — | Global DEF +10% | Gain 1 bar of Rage for every 15 basic attacks, 12 combos, 12 counters, 3 acti... |
| 35 | **Mini Motorcycle** | Immortal | 5014 | Global HP +10% | With every 1 counter, increase global counter DMG by 10% for 3 seconds, up to... |
| 36 | **Blazing Motorcycle** | Immortal | 5021 | Global DEF +10% | For every 10% lost HP, release a flame jet, dealing at least 500% of current ... |
| 37 | **Cloud Drifter** | Immortal | 5009 | Global ATK +10% | Increase Skill Crit Rate by 10%. After a skill critical, boost ATK by 20% for... |
| 38 | **Gator Menace** | Immortal | — | Global DEF +10% | After the battle starts, every 5 seconds, deal DMG equal to 4% of the maximum... |
| 39 | **Pumpkin Carriage** | Immortal | — | Global DEF +10% | Deals 2000% AoE Skill DMG, 800% current Combo AoE DMG, and 800% current Count... |
| 40 | **Ethereal Phoenix** | Immortal | 5060 | Global DEF +10% | Cleanse and ignore control effects for 1s for every 18% Max HP lost. Gain a s... |
| 41 | **Nebular Shuttle** | Immortal | — | Global DEF +10% | Grants a shield equal to 10% Max HP every 11s after battle starts, lasting 8s... |
| 42 | **Effulgent Fan** | Immortal | — | Global HP +10% | Every 11s, increases Crit Rate by 30% and Skill Crit Rate by 30% for 3s. For ... |
| 43 | **Magic Carpet** | Immortal | — | Global ATK +10% | After casting skills 6 times, restore full energy to 1 random skills. |
| 44 | **Panda Attack** | Immortal | — | Global DEF +10% | Every 10s, gains Control Immunity for 3-5s and boosts ATK by 5%-12% and DMG R... |
| 45 | **Vibrant Watermelon Ship** | Immortal | 5034 | Global DEF +10% | Increases ATK by 10% and DEF by 30% every 11s for 5s. After this, a Watermelo... |
| 46 | **Trembling Pepe** | Immortal | 5029 | Global DEF +10% | These two buffs will alternate to take effect every 8s: Gain a Shield with 8%... |
| 47 | **Guardian Spaceship** | Immortal | — | Global DEF +10% | Gain a shield equal to 6% Max HP every 9s for 6s. 6s later, reflects 20% of t... |
| 48 | **Purple Wing** | Immortal | 5008 | Global HP +10% | After the battle begins, immediately deals 5000% AoE DMG, and launches target... |
| 49 | **Thunder Vanguard** | Supreme | — | Global HP +10% | Increase DEF by 36% after the battle starts. Ram forward every 8s, dealing 10... |
| 50 | **Holy Dragon** | Supreme | 5033 | Global DEF +10% | Gain 3 stacks of Guard every 11s, each stack increasing DEF by 100% but losin... |
| 51 | **Cheetah Zero** | Supreme | — | Global HP +10% | Gain Death Immunity for 3s when taking lethal damage. For the duration, ignor... |
| 52 | **Speed of Death** | Supreme | 5057 | Global HP +10% | Gains 20% Evasion. Activates speed-up mode at the start of battle: Every 1 ev... |
| 53 | **Cinder Wolf** | Supreme | — | Global HP +10% | Gains 10% ATK and 16% Final Crit RES after the battle starts. The first time ... |
| 54 | **Dazzling Unicorn** | Supreme | — | Global DEF +10% | The unicorn spreads its wings every 12s, resisting DMG of the next active ski... |
| 55 | **Skyward Blaze** | Supreme | — | Global HP +10% | Deals 600% current Basic ATK AoE DMG to an area every 10s and burns the targe... |
| 56 | **Sparkling Flash** | Immortal | — | Global HP +10% | Every 8s after the battle starts, gain a support from Sparkling Flash (trigge... |
| 57 | **Cloud Traveler** | Immortal | — | Global DEF +10% | Healing Amount increases by 0.3%. For every 15% Max HP lost, restores 7% of l... |
| 58 | **Spectral Ride** | Immortal | — | Global HP +10% | When an opponent's HP drops below 88% for the first time, their ATK is reduce... |
| 59 | **Immortal Tyrant** | Immortal | — | Global DEF +10% | Every 11s, releases the icy breath, reducing all enemies' Movement SPD, ATK S... |
| 60 | **Best Buddy** | Immortal | — | Global DEF +10% | At the start of the battle, the Character gains 12% DMG RES, which decays by ... |
| 61 | **Soaring Shroomie** | Immortal | — | Global HP +10% | Movement SPD increases by 20% at the start of battle and by an additional 10%... |
| 62 | **Sanctuary Warmth** | Supreme | — | Global HP +10% | The first time HP drops below 70%/50%/30%, gain a Pink/Yellow/Purple Gift. Ea... |
| 63 | **Dawn of Time** | Immortal | — | Global DEF +10% | Gains 16% DMG RES after the battle starts, which is reduced by 1/4 every 12s.... |
| 64 | **Leo** | Immortal | — | Global HP +10% | Every 10s after battle starts, reduces all enemies' ATK, Crit Rate, Skill Cri... |

---

## Tier Mounts (Cosmetic Progression)

These 10 mounts are unlocked by reaching mount level milestones. They have no combat skills — purely cosmetic progression skins.

| # | Name | Rarity |
|---|------|--------|
| 1 | Lily Pad | Rare |
| 2 | Quack Splash | Rare |
| 3 | Surfboard | Rare |
| 4 | Flyboard | Rare |
| 5 | Skyglider | Epic |
| 6 | Amethyst Gourd | Epic |
| 7 | Magic Broom | Legendary |
| 8 | Azure Feather | Immortal |
| 9 | Soaring Wings | Supreme |
| 10 | Cyan Phoenixes | Supreme |

---

## Combat Skill Mounts — Full Details

### 11. Hot Wheels (Skill ID 5003)

**Rarity:** Legendary

**Effect:** Boost Pal Attack Speed by 2% per second (up to 40%).

**Passive:** Ignore Stun +6%

**Code Skill ID:** 5003

---

### 12. Pyrebreaker (Skill ID 5002)

**Rarity:** Legendary

**Effect:** Increase base Crit rate by 1% and Crit DMG by 5% per second (up to 20%, 100%).

**Passive:** Ignore Evasion +10%

**Code Skill ID:** 5002

---

### 13. Skyshark

**Rarity:** Legendary

**Effect:** Launches a shark missile every 12s, dealing 1600% AoE Skill DMG and restoring HP equal to the DMG dealt, up to 30% of Max HP, ignoring PvP reduction. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 14. White Tiger (Skill ID 5004)

**Rarity:** Legendary

**Effect:** Targets with HP percentage below the caster take 15% increased DMG, while those with HP percentage above the caster have their ATK reduced by 10%.

**Passive:** Global Basic ATK DMG +10%

**Code Skill ID:** 5004

---

### 15. Boom Da Bang

**Rarity:** Legendary

**Effect:** ATK, ATK SPD, Energy Regen SPD, and Pal ATK SPD increase by 4% every 10s, stacking up to 6 times. (Triggers at the start of the battle.) At 6 stacks or when below 40% HP, stuns all enemies for 1.5s and reduces their DMG RES by 10% until the battle ends.

**Passive:** Global DEF +10%

---

### 16. Blue Ox (Skill ID 5005)

**Rarity:** Legendary

**Effect:** Increase DMG RES by 10% and shorten the duration of control effects by 30%.

**Passive:** Pal Crit DMG +25%

**Code Skill ID:** 5005

---

### 17. Round Frog (Skill ID 5007)

**Rarity:** Legendary

**Effect:** Every 10 second, defeat 1 enemies, boosting ATK by 15% for 5 seconds. If the target is a Boss or player, stun for an additional 1 seconds.

**Passive:** Crit RES Bonus +40%

**Code Skill ID:** 5007

---

### 18. Blue Queen (Skill ID 5006)

**Rarity:** Legendary

**Effect:** Distribute 10% of DMG dealt to up to 5 surrounding enemies when dealing DMG.

**Passive:** Crit DMG Bonus +40%

**Code Skill ID:** 5006

---

### 19. Rum Barrel

**Rarity:** Legendary

**Effect:** For every 20% Max HP missing, deal 800% Basic ATK AoE DMG within a range, gain 10% ATK and take 10% less DMG for 5s (triggers at the start of the battle)

**Passive:** Global DEF +10%

---

### 20. Blizzard Visitor

**Rarity:** Immortal

**Effect:** Reduces all target's Movement SPD by 25%. For every 10% Movement SPD they lose, reduces their ATK by 2% and increases the duration of control effects on them by 2%.

**Passive:** Global DEF +10%

---

### 21. Silvery Crescent (Skill ID 5024) — Code: Immortal Ascent

**Rarity:** Immortal

**Effect:** Gain Death Immunity for 2s upon taking lethal DMG, and immediately recover 10% Max HP.

**Passive:** Global HP +10%

**Code Skill ID:** 5024

---

### 22. Diving Duck

**Rarity:** Immortal

**Effect:** B.Duck creates splashes around every 11s, dealing 2000% Skill DMG, 800% Combo DMG and 800% Counter DMG to all enemies in the area and reducing their ATK by 10% until the battle ends; the effects don't stack. The skill deals 50% more DMG when cast again. When the skill hits the same target again, reduces their ATK by 3% more, stacking up to 2 times. (Casts 1 time immediately after battle starts.)

**Passive:** Global DEF +10%

---

### 23. Scorpio

**Rarity:** Immortal

**Effect:** Inflicts 1 stack of Poison on enemies in a small area every 15s, each stack dealing Bleed DMG equal to 0.8% of the target's current HP per second (ignores Immunity) until the battle ends. Poison stacks up to 10 times. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 24. Wave Cruiser

**Rarity:** Immortal

**Effect:** Gains 5 wave stack(s) at the start of battle, each reducing enemy Final Crit DMG, Final Pal Crit DMG and Final Skill Crit DMG by 4%. Breaks 1 wave stack every 6s or after every 20 basic attacks, increasing Movement SPD by 8% and ATK by 6% until the battle ends, stacking up to 5 times.

**Passive:** Global HP +10%

---

### 25. Storm Rider

**Rarity:** Immortal

**Effect:** Increase DMG RES by 5% and shorten the duration of control effects by 15%. The first time HP drops below 80%, increase DMG RES by 8% and shorten the duration of control effects by 25% for 8s. The first time HP drops below 60%, increase DMG RES by 8% and shorten the duration of control effects by 25% for 12s. The first time HP drops below 40%, increase DMG RES by 8% and shorten the duration of control effects by 25% until the battle ends. Each effect is counted independently and stackable.

**Passive:** Global DEF +10%

---

### 26. Horizon Racer

**Rarity:** Immortal

**Effect:** Every 10 second, summon a car, dealing 800% current basic attack AoE DMG and knocking back targets.

**Passive:** Global HP +10%

---

### 27. AdaptoSlime (Skill ID 5026)

**Rarity:** Immortal

**Effect:** Increases ATK by 15% for 10 seconds when HP drops below 80%. Gains a shield equal to 10% of max HP for 10 seconds when HP drops below 60%. Reduces DMG taken by 15% for 10 seconds when HP drops below 30%.

**Passive:** Global HP +10%

**Code Skill ID:** 5026

---

### 28. Koi Paper Kite (Skill ID 5016)

**Rarity:** Immortal

**Effect:** Every 3 combo triggers an additional 500% AoE DMG.

**Passive:** Global ATK +10%

**Code Skill ID:** 5016

---

### 29. Long-legged Bird

**Rarity:** Immortal

**Effect:** There is a 50% chance to gain 4% ATK, 4% DMG RES and 10% Control Duration Reduction every 4s after the battle starts. This lasts until the battle ends and stacks up to 3 times (the chances of the 3 effects are independently calculated). There is a 100% chance to grant the Summon 4% ATK, 4% DMG RES and 10% Control Duration Reduction until the Summon disappears, stacking up to 3 times. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 30. Heart's Desire (Skill ID 5030) — Code: Unrivaled Force

**Rarity:** Immortal

**Effect:** Every second for the first 20 seconds has a 60% chance to boost ATK by 1% and DMG RES by 1% until the battle ends. After 20 seconds, deals 8000% AoE Skill DMG and launches the target airborne for 0.5 second.

**Passive:** Skill Crit DMG +10%

**Code Skill ID:** 5030

---

### 31. Book of the Universe

**Rarity:** Immortal

**Effect:** When casting an active skill, the Character has a 15% chance to cast it again (excluding those cast by Past Revisited and Eye of Raven).

**Passive:** Global DEF +10%

---

### 32. Time Machine

**Rarity:** Immortal

**Effect:** For the first 20s after the battle starts, negates and stores 40% of all DMG taken and gains 8% of ATK, 10% of Final Crit DMG, 10% of Final Skill Crit DMG and 10% of Final Pal Crit DMG. After the first 20s of the battle, receives an additional 6% of the stored DMG (ignores Immunity) per second for 10s.

**Passive:** Global DEF +10%

---

### 33. Sea of Lanterns

**Rarity:** Immortal

**Effect:** After 15s into battle, becomes immune to DMG for 2s and gains 15% Final Crit DMG, 15% Final Skill Crit DMG, and 15% Final Pal Crit DMG until the battle ends. Current HP changes into 40% Max HP during DMG immunity.

**Passive:** Global DEF +10%

---

### 34. Dimensional Wings

**Rarity:** Immortal

**Effect:** Gain 1 bar of Rage for every 15 basic attacks, 12 combos, 12 counters, 3 active skill(s), or after taking damage equal to 18% of Max HP. Each bar of Rage increases DEF by 3%. At 5 bars, uses all Rage to increase DMG RES, ATK, Crit Rate, Skill Crit Rate, Pal Crit Rate, Crit DMG, Pal Crit DMG and Skill Crit DMG by 12% for 5s.

**Passive:** Global DEF +10%

---

### 35. Mini Motorcycle (Skill ID 5014) — Code: Velocity Blitz

**Rarity:** Immortal

**Effect:** With every 1 counter, increase global counter DMG by 10% for 3 seconds, up to a maximum of 30%. The duration refreshes with each new counter trigger.

**Passive:** Global HP +10%

**Code Skill ID:** 5014

---

### 36. Blazing Motorcycle (Skill ID 5021)

**Rarity:** Immortal

**Effect:** For every 10% lost HP, release a flame jet, dealing at least 500% of current basic attack DMG (scales with lost HP).

**Passive:** Global DEF +10%

**Code Skill ID:** 5021

---

### 37. Cloud Drifter (Skill ID 5009)

**Rarity:** Immortal

**Effect:** Increase Skill Crit Rate by 10%. After a skill critical, boost ATK by 20% for 5 seconds.

**Passive:** Global ATK +10%

**Code Skill ID:** 5009

---

### 38. Gator Menace

**Rarity:** Immortal

**Effect:** After the battle starts, every 5 seconds, deal DMG equal to 4% of the maximum HP to all targets within range, reducing their DMG RES by 2% and Crit RES by 20% until the battle ends, stacking up to 5 times.

**Passive:** Global DEF +10%

---

### 39. Pumpkin Carriage

**Rarity:** Immortal

**Effect:** Deals 2000% AoE Skill DMG, 800% current Combo AoE DMG, and 800% current Counter AoE DMG every 11s after the battle starts, and the targets take DMG equal to 2% of current HP per second with ATK and DMG RES reduced by 10% for 5s. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 40. Ethereal Phoenix (Skill ID 5060) — Mount ID 406

**Rarity:** Immortal

**Effect:** Cleanse and ignore control effects for 1s for every 18% Max HP lost. Gain a shield equal to 8% Max HP, lasting 5s. After the shield expires, ATK increases by 4% until the battle ends, stacking up to 6 times.

**Passive:** Global DEF +10%

**Code Skill ID:** 5060

---

### 41. Nebular Shuttle

**Rarity:** Immortal

**Effect:** Grants a shield equal to 10% Max HP every 11s after battle starts, lasting 8s. Grants 6% DMG RES for the shield's duration; cleanses and increases Final DMG RES by 3% and ATK by 3% once the shield is lost, lasting until the end of battle. Stacks up to 3 times. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 42. Effulgent Fan

**Rarity:** Immortal

**Effect:** Every 11s, increases Crit Rate by 30% and Skill Crit Rate by 30% for 3s. For every 5 Crits or 1 Skill Crit hit during this period, fireworks deal 200% of current Basic ATK AoE DMG (can be Crit) to enemies and increase Final Crit DMG and Final Skill Crit DMG by 6% for 3s, stacking up to 5 times. (Triggers at the start of the battle.)

**Passive:** Global HP +10%

---

### 43. Magic Carpet

**Rarity:** Immortal

**Effect:** After casting skills 6 times, restore full energy to 1 random skills.

**Passive:** Global ATK +10%

---

### 44. Panda Attack

**Rarity:** Immortal

**Effect:** Every 10s, gains Control Immunity for 3-5s and boosts ATK by 5%-12% and DMG RES by 5%-12% for 10s. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 45. Vibrant Watermelon Ship (Skill ID 5034) — Code: Bite the Watermelon

**Rarity:** Immortal

**Effect:** Increases ATK by 10% and DEF by 30% every 11s for 5s. After this, a Watermelon Ship is summoned to unleash a wave that launches enemies for 0.5s, dealing 2000% Skill DMG, 800% current Combo DMG, and 800% current Counter DMG as AoE DMG. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

**Code Skill ID:** 5034

---

### 46. Trembling Pepe (Skill ID 5029)

**Rarity:** Immortal

**Effect:** These two buffs will alternate to take effect every 8s: Gain a Shield with 8% of Max HP, lasting 8s. Gain 8% ATK and reduce the time of being controlled by 30% for 8s.

**Passive:** Global DEF +10%

**Code Skill ID:** 5029

---

### 47. Guardian Spaceship

**Rarity:** Immortal

**Effect:** Gain a shield equal to 6% Max HP every 9s for 6s. 6s later, reflects 20% of the total DMG received within the 6s to all enemies. (Only DMG absorbed and blocked by the shield can be reflected, not DMG ignored by Immunity.)

**Passive:** Global DEF +10%

---

### 48. Purple Wing (Skill ID 5008)

**Rarity:** Immortal

**Effect:** After the battle begins, immediately deals 5000% AoE DMG, and launches targets within the range for 0.5 seconds. Releases every 11 seconds.

**Passive:** Global HP +10%

**Code Skill ID:** 5008

---

### 49. Thunder Vanguard

**Rarity:** Supreme

**Effect:** Increase DEF by 36% after the battle starts. Ram forward every 8s, dealing 1000% Skill DMG, 200% current Combo DMG (can be Crit), 200% current Counter DMG (can be Crit), and DMG equal to 4% Max HP to targets in the area. If targets are immune to damage or death, reduce their ATK by an additional 24% for 5s. Afterwards, DEF is reduced by 6% while ATK increases by 3%, stacking up to 6 times. (Triggers at the start of the battle.)

**Passive:** Global HP +10%

---

### 50. Holy Dragon (Skill ID 5033) — Code: Neon Shadows

**Rarity:** Supreme

**Effect:** Gain 3 stacks of Guard every 11s, each stack increasing DEF by 100% but losing 1 stack every 1s. Deal 2000% Skill DMG, 800% current Combo DMG and 800% current Counter DMG at the end of Guard (triggers at the start of the battle)

**Passive:** Global DEF +10%

**Code Skill ID:** 5033

---

### 51. Cheetah Zero

**Rarity:** Supreme

**Effect:** Gain Death Immunity for 3s when taking lethal damage. For the duration, ignore new control effects (doesn't affect existing control), gain 10% ATK, 10% Crit Rate, 10% Final Crit DMG, 10% Skill Crit Rate, 10% Final Skill Crit DMG, 10% Pal Crit Rate, and 10% Final Pal Crit DMG, and the next basic attack deals 3000% Skill DMG, 1200% Current Combo DMG (can be Crit), 1200% Current Counter DMG (can be Crit), and DMG equal to 8% Max HP to enemies in the area. The character explodes at the end of the duration.

**Passive:** Global HP +10%

---

### 52. Speed of Death (Skill ID 5057) — Code: Life and Death Speed — Mount ID 404

**Rarity:** Supreme

**Effect:** Gains 20% Evasion. Activates speed-up mode at the start of battle: Every 1 evasions, 8 basic attacks, 8 combos, 8 counters, or 2 active skills used increases Movement SPD by 8% until the burst ends. After Movement SPD reaches 200% of its initial value, activates charge mode: Increases DMG RES by 9% for 5s. After charge mode ends, activates burst mode: Cleanses and becomes immune to control effects, recovers 12% of lost HP per second, and increases DMG RES by 12%, ATK, DEF, ATK SPD, Energy Regen SPD and Pal ATK SPD by 32% for 5s. Returns to speed-up mode after the burst ends.

**Passive:** Global HP +10%

**Code Skill ID:** 5057

---

### 53. Cinder Wolf

**Rarity:** Supreme

**Effect:** Gains 10% ATK and 16% Final Crit RES after the battle starts. The first time HP drops below 39%, cleanses debuffs, becomes immune to damage for 1s, converts HP into 10% Max HP, and gains a shield equal to 45% of Max HP (ignores PvP reduction and shield breaks). For the shield's duration, reduces HP Regen by 100%, ignores control effects, but gains 10% DMG RES; the character's basic attacks deal 250% extra Skill DMG, 50% extra Combo DMG (can be Crit), 50% extra Counter DMG (can be Crit), while pals' basic attacks deal 50% extra Pal DMG (can be Crit).

**Passive:** Global HP +10%

---

### 54. Dazzling Unicorn

**Rarity:** Supreme

**Effect:** The unicorn spreads its wings every 12s, resisting DMG of the next active skill hit on the Character (excluding Class, Avian, and Summoning Skills), during which the Character gains 50% DEF and ignores all control effects. After the unicorn resists DMG, the DEF boost and control immunity effects disappear. Meanwhile, the Chracter reflects the active skill to the attacker and gains 4% ATK and 4% DMG RES until the battle ends, up to 3 stacks. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 55. Skyward Blaze

**Rarity:** Supreme

**Effect:** Deals 600% current Basic ATK AoE DMG to an area every 10s and burns the targets, who will receive 40% current Basic ATK DMG per second until the battle ends, stacking up to 3 times. Gains an additional 4% ATK and DEF and 4% DMG RES until the battle ends, stacking up to 3 times. (Casts 1 time immediately after battle starts.)

**Passive:** Global HP +10%

---

### 56. Sparkling Flash

**Rarity:** Immortal

**Effect:** Every 8s after the battle starts, gain a support from Sparkling Flash (triggers at the start of the battle). For every 10% HP over 50% Max HP, gain 2% ATK and DEF for 8s. If below 50% HP, restore 12% of lost HP and gain 10% DMG RES for 8s.

**Passive:** Global HP +10%

---

### 57. Cloud Traveler

**Rarity:** Immortal

**Effect:** Healing Amount increases by 0.3%. For every 15% Max HP lost, restores 7% of lost HP and gains 5% DMG RES for 4s, stacking up 4 times.

**Passive:** Global DEF +10%

---

### 58. Spectral Ride

**Rarity:** Immortal

**Effect:** When an opponent's HP drops below 88% for the first time, their ATK is reduced by 16%. Upon first falling below 66% HP, their DMG RES is decreased by 16%. At 44% HP, their ATK SPD, Pal ATK SPD, and Energy Regen are reduced by 16%. When HP falls below 22%, the enemy takes 1.6% of their max HP as damage per second, ignoring DMG Immunity.

**Passive:** Global HP +10%

---

### 59. Immortal Tyrant

**Rarity:** Immortal

**Effect:** Every 11s, releases the icy breath, reducing all enemies' Movement SPD, ATK SPD, Pal ATK SPD, Energy Regen SPD, and HP Regen by 60%. Loses 1/5 of the effects every 1.2s (cannot be cleansed; triggers at the start of the battle.).

**Passive:** Global DEF +10%

---

### 60. Best Buddy

**Rarity:** Immortal

**Effect:** At the start of the battle, the Character gains 12% DMG RES, which decays by 1/3 every 12s. Every 1% of the Character's Ignore Evasion grants pals 0.2% Ignore Evasion. For every 5 basic attacks or combo hits from a pal, restore the Character's HP by 1% Max HP and increase the pal's ATK SPD by 2%, stacking up to 10 times (independently counted for each pal).

**Passive:** Global DEF +10%

---

### 61. Soaring Shroomie

**Rarity:** Immortal

**Effect:** Movement SPD increases by 20% at the start of battle and by an additional 10% every 5s after that, stacking up to 10 times. For every 10% Movement SPD that the Character has higher than the base value of 10%, increase their Evasion and ATK SPD by 3.2% (up to 32%), Crit DMG and Skill Crit DMG by 2.4% (up to 24%), and Final DMG RES by 1.6% (up to 16%).

**Passive:** Global HP +10%

---

### 62. Sanctuary Warmth

**Rarity:** Supreme

**Effect:** The first time HP drops below 70%/50%/30%, gain a Pink/Yellow/Purple Gift. Each gift is gained cleanses debuffs and grants DMG and Control Immunity for 0.6s and a shield equal to 20% Max HP for 8s. While the shield persists, the Character's Final DMG RES increases by 10%. (Shields and Final DMG RES from differents gifts stack) When the shield expires, gain the following effects based on gift color: Pink: ATK increases by 10% and DEF by 30%. Yellow: Crit Rate, Pal Crit Rate, Final Crit DMG, Final Pal Crit DMG, and Final Skill Crit DMG increase by 10%. Purple: Restore 24% Max HP and deal 5000% Skill DMG, 1000% current Basic ATK DMG (can be Crit), 1000% current Combo DMG (can be Crit), and 1000% current Counter DMG (can be Crit) to all enemies. (DMG from the purple gift ignores DMG Immunity.)

**Passive:** Global HP +10%

---

### 63. Dawn of Time

**Rarity:** Immortal

**Effect:** Gains 16% DMG RES after the battle starts, which is reduced by 1/4 every 12s. Every 12s, gains a shield equal to 10% Max HP that lasts 5s, and increases Final DMG Boost by 40% and all HP Regen effects by 60% for 3s. (Triggers at the start of the battle.)

**Passive:** Global DEF +10%

---

### 64. Leo

**Rarity:** Immortal

**Effect:** Every 10s after battle starts, reduces all enemies' ATK, Crit Rate, Skill Crit Rate, Combo Rate, Counter Rate, Pal Crit Rate, and Pal Combo Rate by 20% for 6s (cannot be cleansed). Meanwhile, increases ATK, Crit Rate, Skill Crit Rate, Combo Rate, Counter Rate, Pal Crit Rate, and Pal Combo Rate by 20% for 6s. (Triggers at the start of the battle.)

**Passive:** Global HP +10%

---

## Code-Only Skill IDs (No xlsx Match)

These skill IDs were found in the reverse-engineered game code but don't have a clear match to any xlsx mount name.

| Skill ID | Code Name | Effect Pattern | Possible Match |
|----------|-----------|---------------|----------------|
| 5001 | Default Mount | Evasion scaling (+75% at lv24) | Base mount system, not a skin |
| 5010 | Kun | DEFER_DAMAGE smoothing (burst→DoT) | Storm Rider? Internal-only? |
| 5013 | Cyclone Bamboo | Shield +50%, +3s, Counter +25% | Guardian Spaceship? Nebular Shuttle? |
| 5015 | AdaptoSlime (basic) | 500% AoE per 5% HP damage | Older version of AdaptoSlime (5026) |
| 5018 | Moon Rabbit | DMG RES +15%, heal 25% lost HP/10s | Sparkling Flash? Cloud Traveler? |
| 5048 | Phoenix Nirvana | HP 50% buff chain (50482→50465-67) | Cinder Wolf? |
| 5124 | Time Pause | Freeze ALL enemies 2s/25% HP (ignores CC immunity!) | Unreleased? |

---

## Alternate Names Reference

| In-Game Name (xlsx) | Code Name | Skill ID |
|---------------------|-----------|----------|
| Speed of Death | Life and Death Speed | 5057 |
| Holy Dragon | Neon Shadows | 5033 |
| Vibrant Watermelon Ship | Bite the Watermelon | 5034 |
| Mini Motorcycle | Velocity Blitz | 5014 |
| Silvery Crescent | Immortal Ascent | 5024 |
| Heart's Desire | Unrivaled Force | 5030 |
| Diving Duck | B. Duck (web name) | — |
| Rum Barrel | Blazing Motorcycle variant? | — |

---

## Class Synergies — Best Mount Per Class

| Class | Best Mount(s) | Reason |
|-------|--------------|--------|
| Martial Sage | Speed of Death, Dazzling Unicorn, Cinder Wolf | Counter feeds speed stacks; skill reflect; death immunity + shield |
| Warbringer | Blazing Motorcycle, Mini Motorcycle, Cheetah Zero | HP-loss scaling; counter DMG stacking; death immunity burst |
| Sacred Hunter | Speed of Death, Ethereal Phoenix, Default | Evasion feeds speed stacks; CC cleanse + shield; raw evasion |
| Plume Monarch | Koi Paper Kite, Effulgent Fan | Combo rate feeds AoE; crit window synergy |
| Prophet | Cloud Drifter, Magic Carpet, Book of the Universe | Skill crit synergy; skill energy restore; 15% skill recast |
| Darklord | Cloud Drifter, Magic Carpet | Skill crit +20% stacks with +50% passive; free skill recharges |
| Beastmaster | Hot Wheels, Best Buddy, Diving Duck | Pal ATK speed; pal heal + ignore evasion sharing; AoE + ATK debuff |
| Supreme Spirit | Hot Wheels, Heart's Desire, Time Machine | Pal speed; late-game burst; stored DMG release |

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

## Data Files

- **Source spreadsheet**: `battlesim/reference/LOM_Database-5.xlsx` — Complete item database (data_mounts.ts)
- **Structured data**: `battlesim/reference/mounts_master.json` — Complete JSON with all 64 mounts
- **Config schemas**: ConfigMount (24 fields), ConfigMount_skin (6), ConfigMount_level (10), ConfigMount_ability (4), ConfigMount_abilitycost (4)