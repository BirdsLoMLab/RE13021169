# 07 — Avians (Spirit Birds / FlyPet)

> Complete avian reference: all 35 avians (34 from LOM_Database-5.xlsx + 1 new from ConfigFly) + 102 avian affixes. See also `avians_master.json` and `avian_affixes_master.json` for structured JSON.

---

## Quick Reference — All 35 Avians

| # | Name | Rarity | fly_id | skill_id | Flags | Effect |
|---|------|--------|--------|----------|-------|--------|
| 1 | **Aggressive Lemon** | Normal | 1001 | 5101 | — | Regenerates 5% of lost HP every 5s |
| 2 | **Gleam Candle** | Normal | 1002 | 5102 | — | Deals 240% AoE Skill DMG 5 times every 11s. (Triggers at the start of the battle... |
| 3 | **Coconut Ball** | Normal | 1003 | 5103 | — | Increases ATK SPD by 5% immediately after battle starts and by 2% more for every... |
| 4 | **Sheep Balloon** | Normal | 1004 | 5104 | — | Deals 500% of current Basic ATK AoE DMG and imprisons the target for 1s every 13... |
| 5 | **Tomato Egg** | Normal | 1005 | 5105 | — | Deals 325% of current Basic ATK AoE DMG every 12s and increases Basic ATK DMG by... |
| 6 | **Smart Assistant** | Normal | 1006 | 5106 | — | Increases Pal ATK SPD by 5% every 5s after battle starts, stacking up to 5 times... |
| 7 | **Yoghurt Cocoa** | Normal | 1007 | 5107 | — | Each Pal Crit Increases its Final Crit DMG by 2%, stacking up to 5 times. |
| 8 | **Astronaut Teal** | Normal | 9001 | 5901 | Event, B.Duck Collab | Deals 450% Basic ATK AoE DMG every 16s and gains a shield equal to 10% of curren... |
| 9 | **Impulse Penguin** | Advanced | 2001 | 5201 | — | Increases Counter DMG by 4% every 10s after battle starts, stacking up to 5 time... |
| 10 | **Dense Cloud** | Advanced | 2002 | 5202 | — | Deals 1400% AoE Skill DMG every 13s after battle starts and increases Energy Reg... |
| 11 | **3-Round Shooter** | Advanced | 2003 | 5203 | — | Deals 75% extra AoE Combo DMG every 4 combos. |
| 12 | **Honeypot Warrior** | Advanced | 2004 | 5204 | — | Deals DMG equal to 2.5% Max HP every 5s after battle starts. (Triggers at the st... |
| 13 | **Pumpkin Witch** | Advanced | 2005 | 5205 | — | Every Skill Crit deals 600% extra AoE Skill DMG. |
| 14 | **Bell Ring** | Advanced | 2006 | 5206 | — | Every Crit has a 20% chance to deal 60% extra Basic ATK DMG Bleed DMG (Ignores D... |
| 15 | **Sunshine Bringer** | Advanced | 2007 | 5207 | — | Deals 560% of current Basic ATK AoE DMG every 16s after battle starts and reduce... |
| 16 | **Travelling Jellyfish** | Advanced | 2008 | 5208 | — | Deals 612.5% of current Basic ATK AoE DMG every 15s after battle starts and redu... |
| 17 | **Whirlwind Leaf** | Advanced | 2009 | 5209 | — | Deals 220% extra AoE Skill DMG every 4 Basic Attacks. |
| 18 | **Crispy Moth** | Advanced | 2010 | 5210 | — | Deals 630% of current Basic ATK AoE DMG every 17s after battle starts and stuns ... |
| 19 | **Yoghurt Champ** | Advanced | 2011 | 5211 | — | Each Pal Crit increases its Final Crit DMG by 2%, stacking up to 5 times. Each P... |
| 20 | **Astronaut Pinky** | Advanced | 9002 | 5902 | Event, B.Duck Collab | Deals 675% Basic ATK AoE DMG every 16s and gains a shield equal to 10% of Max HP... |
| 21 | **Maniac Love** | Advanced | 8001 | 5801 | Event, Rabbid Collab, LimitedBreed | Fire Cupid's Arrows at random targets every 5s (triggers at the start of the bat... |
| 22 | **Dream Moment** | Advanced | 8002 | 5802 | Event, Rabbid Collab, LimitedBreed | Gain a shield that absorbs 6% of Max HP every 12s, lasting for 6s. After a shiel... |
| 23 | **Pet - Genos** | Advanced | 8101 | 5803 | Event, One-Punch Man Collab, LimitedBreed | Every 15s after the battle starts, all enemies take 360% Skill DMG, 120% current... |
| 24 | **Anubis** | Rare | 3001 | 5301 | — | Deals 765% Skill DMG, 305% of current Combo DMG, and 305% of current Counter DMG... |
| 25 | **Midnight Firefly** | Rare | 3002 | 5302 | — | Deal 240% of current Basic ATK DMG every 16s after battle starts and reduce the ... |
| 26 | **Moonbound Spirit** | Rare | 3003 | 5303 | — | Deals 300% Skill DMG, 120% current Combo DMG, and 120% current Counter DMG every... |
| 27 | **Horus, Sky God** | Rare | 3004 | 5304 | — | Every 6s, deals 240% Skill DMG, 100% of current Combo DMG, 100% of current Count... |
| 28 | **Magic Cat** | Rare | 3005 | 5305 | — | Every 15s, deals 765% Skill DMG, 305% of current Combo DMG, and 305% of current ... |
| 29 | **Puppy Gaze** | Rare | 3006 | 5306 | — | Every 15s, deals 765% Skill DMG, 305% of current Combo DMG, and 305% of current ... |
| 30 | **Deity of Purrs** | Rare | 3007 | 5307 | — | For every 16 times healed (including HP regen, healing, active skill and healing... |
| 31 | **Michelle** | Rare | 3008 | 5308 | — | For every 50 instances of damage taken, enemies take an additional 200% AoE DMG,... |
| 32 | **Astronaut B.Duck** | Rare | 9003 | 5903 | Event, B.Duck Collab | Every 16s, deals 800% Skill DMG, 320% of current Combo DMG and 320% of current C... |
| 33 | **Lunar Sprite** | Rare | 3012 | 5312 | — | After the battle starts, the Character's DEF increases by 60% and ATK increases ... |
| 34 | **Dharma** | Advanced | 2016 | 5216 | — | Every 20s after the battle starts, gains 3 stacks of Toughness (capped at 3), ea... |

| 35 | **Daedream** | Advanced | 8201 | 82011 | Event, PLLD Collab | (ConfigFly data only - effect text pending) |

---

## Full Details

### 1. Aggressive Lemon

**Rarity:** Normal

**Effect:** Regenerates 5% of lost HP every 5s

---

### 2. Gleam Candle

**Rarity:** Normal

**Effect:** Deals 240% AoE Skill DMG 5 times every 11s. (Triggers at the start of the battle.)

---

### 3. Coconut Ball

**Rarity:** Normal

**Effect:** Increases ATK SPD by 5% immediately after battle starts and by 2% more for every 10% HP lost.

---

### 4. Sheep Balloon

**Rarity:** Normal

**Effect:** Deals 500% of current Basic ATK AoE DMG and imprisons the target for 1s every 13s. (Triggers at the start of the battle.)

---

### 5. Tomato Egg

**Rarity:** Normal

**Effect:** Deals 325% of current Basic ATK AoE DMG every 12s and increases Basic ATK DMG by 30% for 5s. (Triggers at the start of the battle.)

---

### 6. Smart Assistant

**Rarity:** Normal

**Effect:** Increases Pal ATK SPD by 5% every 5s after battle starts, stacking up to 5 times.

---

### 7. Yoghurt Cocoa

**Rarity:** Normal

**Effect:** Each Pal Crit Increases its Final Crit DMG by 2%, stacking up to 5 times.

---

### 8. Astronaut Teal

**Rarity:** Normal
**Flags:** Event Exclusive | Collab: B.Duck Collab

**Effect:** Deals 450% Basic ATK AoE DMG every 16s and gains a shield equal to 10% of current HP for 6s.

---

### 9. Impulse Penguin

**Rarity:** Advanced

**Effect:** Increases Counter DMG by 4% every 10s after battle starts, stacking up to 5 times.

---

### 10. Dense Cloud

**Rarity:** Advanced

**Effect:** Deals 1400% AoE Skill DMG every 13s after battle starts and increases Energy Regen by 25% for 5s. (Triggers at the start of the battle.)

---

### 11. 3-Round Shooter

**Rarity:** Advanced

**Effect:** Deals 75% extra AoE Combo DMG every 4 combos.

---

### 12. Honeypot Warrior

**Rarity:** Advanced

**Effect:** Deals DMG equal to 2.5% Max HP every 5s after battle starts. (Triggers at the start of the battle.)

---

### 13. Pumpkin Witch

**Rarity:** Advanced

**Effect:** Every Skill Crit deals 600% extra AoE Skill DMG.

---

### 14. Bell Ring

**Rarity:** Advanced

**Effect:** Every Crit has a 20% chance to deal 60% extra Basic ATK DMG Bleed DMG (Ignores DMG Immunity).

---

### 15. Sunshine Bringer

**Rarity:** Advanced

**Effect:** Deals 560% of current Basic ATK AoE DMG every 16s after battle starts and reduces the duration of control received by 15% for 5s. (Triggers at the start of the battle.)

---

### 16. Travelling Jellyfish

**Rarity:** Advanced

**Effect:** Deals 612.5% of current Basic ATK AoE DMG every 15s after battle starts and reduces the target's ATK SPD by 20% for 5s. (Triggers at the start of the battle.)

---

### 17. Whirlwind Leaf

**Rarity:** Advanced

**Effect:** Deals 220% extra AoE Skill DMG every 4 Basic Attacks.

---

### 18. Crispy Moth

**Rarity:** Advanced

**Effect:** Deals 630% of current Basic ATK AoE DMG every 17s after battle starts and stuns the target for 1s.

---

### 19. Yoghurt Champ

**Rarity:** Advanced

**Effect:** Each Pal Crit increases its Final Crit DMG by 2%, stacking up to 5 times. Each Pal Combo increases its Final Combo DMG by 2%, stacking up to 5 times.

---

### 20. Astronaut Pinky

**Rarity:** Advanced
**Flags:** Event Exclusive | Collab: B.Duck Collab

**Effect:** Deals 675% Basic ATK AoE DMG every 16s and gains a shield equal to 10% of Max HP for 6s.

---

### 21. Maniac Love

**Rarity:** Advanced
**Flags:** Event Exclusive | Collab: Rabbid Collab | Limited Breeding | Food Required

**Effect:** Fire Cupid's Arrows at random targets every 5s (triggers at the start of the battle). If the target is oneself, reduce DEF by 30% and convert 3 time(s) of the reduced DEF into ATK for 5s. If the target is an enemy, deal 165% of AoE Skill DMG, 70% of current AoE Combo DMG (can be Crit), and 70% of current AoE Counter DMG (can be Crit) and reduce their Final DMG RES by 10% for 5s.

---

### 22. Dream Moment

**Rarity:** Advanced
**Flags:** Event Exclusive | Collab: Rabbid Collab | Limited Breeding | Food Required

**Effect:** Gain a shield that absorbs 6% of Max HP every 12s, lasting for 6s. After a shield expires, deal 320% of AoE Skill DMG, 120% of current AoE Combo DMG, and 120% of current AoE Counter DMG and increase ATK SPD by 20% for 6s. (Triggers at the start of the battle.)

---

### 23. Pet - Genos

**Rarity:** Advanced
**Flags:** Event Exclusive | Collab: One-Punch Man Collab | Limited Breeding | Food Required

**Effect:** Every 15s after the battle starts, all enemies take 360% Skill DMG, 120% current Basic ATK DMG (can be Crit), 120% current Combo DMG (can be Crit), and 120% current Counter DMG (can be Crit) 5 times and lose 50% DEF for 5s (cannot be cleansed).

---

### 24. Anubis

**Rarity:** Rare

**Effect:** Deals 765% Skill DMG, 305% of current Combo DMG, and 305% of current Counter DMG every 15s after battle starts and reduces the target's ATK by 15% for 5s. (Triggers at the start of the battle.)

---

### 25. Midnight Firefly

**Rarity:** Rare

**Effect:** Deal 240% of current Basic ATK DMG every 16s after battle starts and reduce the target's DMG RES by 15% for 5 seconds. Deal 600% Skill DMG, 240% of current Combo DMG, and 240% of current Counter DMG again after a short delay. (Triggers at start of the battle.)

---

### 26. Moonbound Spirit

**Rarity:** Rare

**Effect:** Deals 300% Skill DMG, 120% current Combo DMG, and 120% current Counter DMG every 5s after battle starts, with a 50% chance to deal extra DMG equal to 3% of the target's Max HP. (Triggers at the start of the battle.)

---

### 27. Horus, Sky God

**Rarity:** Rare

**Effect:** Every 6s, deals 240% Skill DMG, 100% of current Combo DMG, 100% of current Counter DMG, plus an amount equal to 2% of the target's current HP. After every 3 casts, deals an additional 480% Skill DMG, 200% of current Combo DMG, and 200% of current Counter DMG and directly defeats the target if its HP is below 5%, after which dealing DMG equal to 2% of the target's Max HP per second for 3s. (Triggers at the start of the battle.)

---

### 28. Magic Cat

**Rarity:** Rare

**Effect:** Every 15s, deals 765% Skill DMG, 305% of current Combo DMG, and 305% of current Counter DMG and activates Feline Magic 5 times within 2s, each time reducing the cooldown of a random Active Skill by 2s. This prioritizes skills in cooldown and can be used on the same skill repeatedly. (Triggers 1s after the start of the battle.)

---

### 29. Puppy Gaze

**Rarity:** Rare

**Effect:** Every 15s, deals 765% Skill DMG, 305% of current Combo DMG, and 305% of current Counter DMG and increases Pal ATK SPD by 50% for 5s. (Triggers at the start of the battle.)

---

### 30. Deity of Purrs

**Rarity:** Rare

**Effect:** For every 16 times healed (including HP regen, healing, active skill and healing effects of passive skills, Lifesteal of Spectral Chant excluded), deals DMG equal to 4% of current HP to targets within the range.

---

### 31. Michelle

**Rarity:** Rare

**Effect:** For every 50 instances of damage taken, enemies take an additional 200% AoE DMG, 80% of current Combo AoE DMG, 80% of current Counter AoE DMG, and 2% of current HP AoE DMG and become stunned for 0.5s.

---

### 32. Astronaut B.Duck

**Rarity:** Rare
**Flags:** Event Exclusive | Collab: B.Duck Collab

**Effect:** Every 16s, deals 800% Skill DMG, 320% of current Combo DMG and 320% of current Counter DMG and gains a shield equal to 10% of Max HP for 6s, during which ATK increases by 15%.

---

### 33. Lunar Sprite

**Rarity:** Rare

**Effect:** After the battle starts, the Character's DEF increases by 60% and ATK increases by 10% every 15s for 5s, during which the Character restores 3% of lost HP for every 10 basic attack or combo hits taken. (Triggers at the start of the battle.)

---

### 34. Dharma

**Rarity:** Advanced

**Effect:** Every 20s after the battle starts, gains 3 stacks of Toughness (capped at 3), each of which increases DMG RES by 3.5%. For every 12% Max HP taken as DMG loses 1 stack of Toughness. (Triggers at the start of the battle.)


### 35. Daedream

**Rarity:** Advanced
**Flags:** Event Exclusive | Collab: PLLD Collab

**Effect:** (ConfigFly data only - effect text pending)

---

---

## Avian Affixes (102 total)

### Affix Rarity Tiers

| Rarity | Description |
|--------|-------------|
| gray | Negative-only debuffs |
| blue | Positive-only buffs |
| purple | Trade-off (one stat up, one stat down) |
| gold | Pure positive buffs (stronger) |
| colorful | Best-in-slot (dual buffs or HP% proc effects) |
| mutated | Breeding/progression modifiers |
| work | Farm/crafting utility effects |

---

### Gray Affixes

| ID | Name | Description |
|-----|------|-------------|
| affix_001 | Slow & Clumsy | Combo DMG -300% |
| affix_002 | Slow Reaction | Counter DMG -300% |
| affix_003 | Tickler | Basic ATK DMG -240% |
| affix_004 | Double Effort | Skill DMG -80% |
| affix_005 | Holdback | Pal DMG -80% |
| affix_006 | Squib | Crit DMG Bonus -150% |
| affix_007 | Fragile | Crit RES Bonus -150% |
| affix_008 | Bottomless Abyss | HP Regen Bonus -20% |
| affix_009 | Overtime | Avian HP -20% |
| affix_010 | Cowardly | Avian ATK -20% |
| affix_011 | Powerless | Avian DEF -20% |

---

### Blue Affixes

| ID | Name | Description |
|-----|------|-------------|
| affix_012 | Shroom Combo | Combo DMG +150% |
| affix_013 | Reflect Counter | Counter DMG -150% |
| affix_014 | Enhanced Attack | Basic Attack DMG +120% |
| affix_015 | Talent Skill | Skill DMG +40% |
| affix_016 | Enhanced. Go! | Pal DMG +40% |
| affix_017 | Rage Bonus | Crit DMG Bonus +75% |
| affix_018 | Barrel Dodge | Crit RES Bonus +75% |
| affix_019 | Regen Ability | HP Regen Bonus +10% |

---

### Purple Affixes

| ID | Name | Description |
|-----|------|-------------|
| affix_020 | Quick But Dull | Global Combo +7.5%, Skill Crit DMG -5% |
| affix_021 | Dull Blade Strike | Global Counter +7.5%, Skill Crit DMG -5% |
| affix_022 | Multi-Talented | Skill Crit DMG +15%, Global Combo -2.5% |
| affix_023 | Inert Gas | Skill Crit DMG +15%, Global Counter -2.5% |
| affix_024 | Self-Centered | Skill Crit DMG +15%, Pal Crit DMG -25% |
| affix_025 | Altruism | Pal Crit DMG +75%, Skill Crit DMG -5% |
| affix_026 | Backstabbing | Global Counter +7.5%, Global Combo -2.5% |
| affix_027 | One-Sided Attack | Global Combo +7.5%, Global Counter -2.5% |
| affix_028 | Random Match | Global Combo +7.5%, Pal Crit DMG -25% |
| affix_029 | On Standby | Global Counter +7.5%, Pal Crit DMG -25% |
| affix_030 | Same Boat | Pal Crit DMG +75%, Global Counter -2.5% |
| affix_031 | Self Sacrifice | Pal Crit DMG +75%, Global Combo -2.5% |
| affix_032 | Lifespan Match | Avian HP +15%, ATK -5% |
| affix_033 | Paper Defense | Avian HP +15%, DEF -5% |
| affix_034 | Squishy Master | Avian ATK +15%, DEF -5% |
| affix_035 | Low Endurance | Avian ATK +15%, HP -5% |
| affix_036 | Heavy Armor | Avian DEF +15%, HP -5% |
| affix_037 | Stability Focused | Avian DEF +15%, ATK -5% |
| affix_038 | Rise and Fall | Pal basic attacks have a 75% chance to boost its DMG Multiplier by 0.2% and a 25% chance to reduce its DMG Multiplier by 0.1% |
| affix_039 | The Middle Way | Counterstrikes have a 60% chance to boost Counter DMG by 0.2% and a 40% chance to reduce it by 0.1% |
| affix_040 | Dilemma | Active skills have a 75% chance to boost Skill DMG by 0.2% and a 25% chance to reduce it by 0.1% |
| affix_041 | Poisoned Arrow | Combos have a 60% chance to boost Combo DMG by 0.2% and a 40% chance to reduce it by 0.1% |

---

### Gold Affixes

| ID | Name | Description |
|-----|------|-------------|
| affix_042 | Super Crowd Combo | Global Combo +5% |
| affix_043 | Super Reflect Counter | Global Counter +5% |
| affix_044 | Super Attack | Global Basic ATK +4% |
| affix_045 | Super Boost | Skill Crit DMG +10% |
| affix_046 | Loss of Control | Pal Crit DMG +50% |
| affix_047 | Self-Defense | Basic ATK DMG RES +2.5% |
| affix_048 | Accurate Defense | Skill DMG RES +2.5% |
| affix_049 | Invalid Reflect | Counter DMG RES +2.5% |
| affix_050 | Grudge Holder | Combo DMG RES +2.5% |
| affix_051 | Shared Hatred | Pal DMG RES +2.5% |
| affix_052 | Indirect Aid | Boss DMG RES +2.5% |
| affix_053 | Against the Strong | Boss DMG +15% |
| affix_054 | Quick Healing | Healing +0.05% |
| affix_055 | Debuff Immunity | Duration of Control Effects -2.5% |
| affix_056 | Longevity | Avian HP +10% |
| affix_057 | Easy Rage | Avian ATK +10% |
| affix_058 | Iron Shield | Avian DEF +10% |

---

### Colorful Affixes

| ID | Name | Description |
|-----|------|-------------|
| affix_059 | Super League | Global Combo +5%, Pal Crit DMG +50% |
| affix_060 | All-round Hit | Global Combo +5%, Global Basic ATK +4% |
| affix_061 | All-round Control | Global Counter +5%, Pal Crit DMG +50% |
| affix_062 | Reverse Control | Global Counter +5%, Global Basic ATK +4% |
| affix_063 | Burst Impact | Skill Crit DMG +10%, Pal Crit DMG +50% |
| affix_064 | Infinite Burst Hit | Skill Crit DMG +10%, Global Basic ATK +4% |
| affix_065 | Natural Burst | Avian HP, ATK and DEF +10% |
| affix_066 | Punch Counter | Counterstrikes have a 50% chance to deal extra DMG equal to 0.5% of current HP |
| affix_067 | Wind Tear | Active skills deal extra DMG equal to 1% of the target's current HP |
| affix_068 | Multiple Shots | Combos have a 50% chance to deal extra DMG equal to 0.5% of the target's current HP |
| affix_069 | Divine Touch | Pal Crits have a 25% chance to deal extra DMG equal to 0.5% of the target's current HP |
| affix_070 | Meteor Feather | Combos have a 50% chance to restore 0.1% of Max HP |
| affix_071 | Infinite Dream | After a skill critical, the active skill deals 6% more DMG for 8s |
| affix_072 | Rage Slash | Boosts ATK by 0.4% per second when above 50% HP, stacking up to 30 times |
| affix_073 | Arcane Light | Pal Crits have a 25% chance to restore 0.1% of Character's Max HP |
| affix_074 | Terminal Strike | Each basic attack has a 8% chance to wound all targets within the range, reducing their Regen and Healing Amount by 50% for 1s |
| affix_075 | No Speeding | Reduces all enemies' active skill durations by 8% |
| affix_076 | Lightning Conductor | All enemy crit hits have a 10% chance to rebound, dealing 80% Basic ATK AoE DMG to all enemies in the area and reducing their Crit DMG by 15% for 1s |
| affix_102 | Speed Disruption | Reduce all enemies' active skill durations by 7% after the battle starts (cannot stack with 'No Speeding') |

---

### Mutated Affixes

| ID | Name | Description |
|-----|------|-------------|
| affix_077 | Mutated: Time Saving | Avian Leveling EXP -20% |
| affix_078 | Mutated: Time Wasting | Avian Advancement Cost +10% |
| affix_079 | Mutated: Super Boost | Avian Breeding Time -20% |
| affix_080 | Mutated: Speed Update | Avian Breeding Cooldown -20% |
| affix_081 | Mutated: Efficient Evolution | Avian Advancement Cost -20% |
| affix_082 | Mutated: Roundabout | Avian Leveling EXP +10% |
| affix_083 | Mutated: Long Wait | Avian Breeding Cooldown +10% |
| affix_084 | Mutated: Delayed Gratification | Avian Breeding Time +10% |
| affix_085 | Mutated: Double-Yolk Egg | Breeding this Avian has a 10% chance to get 2 magic eggs |
| affix_086 | Mutated: Power of the Giant | Avian HP, ATK and DEF +20%, but Leveling EXP and Advancement Cost +20% |
| affix_087 | Mutated: Affix Refreshing | Avian Non-Mutated Affix Level +1 |

---

### Work Affixes

| ID | Name | Description |
|-----|------|-------------|
| affix_088 | Work Light | Reduces the team's work Stamina cost by 20%. (Tiering up Avians doesn't boost the effect) |
| affix_089 | Instant Harvest | Harvest have a 5% chance to skip the process |
| affix_090 | United Effort | Reduces harvest time by 5% |
| affix_091 | Assited Irrigation | The team leader speeds up crop growth by 20% more after watering. (Tiering up Avians doesn't boost the effect) |
| affix_092 | Osmotic Fertilizer | 0.1% chance to use 1 Basic Fertilizer for free when watering |
| affix_093 | Dual Flows | 5% chance to water twice |
| affix_094 | Hawkeye Vigilance | Increases the chance of catching thieves by 5% |
| affix_095 | Quantum Baking | Pals have a 5% chance to reduce processing time by twice the amount |
| affix_096 | Production Shortcut | 1% chance to reduce processing time to 1s |
| affix_097 | Unrestricted Mining | Boosts pals' talent effect for mining Ores by 5% |
| affix_098 | Chrono Upgrade | The team leader's talent reduces 20% more research time. (Tiering up Avians doesn't boost the effect) |
| affix_099 | Free Speedup | The team leader has a 1% chance to use 1 Speedup Coupon for free when reducing research time |
| affix_100 | Research Overtime | The team leader has a 5% chance to trigger research time reduction twice |
| affix_101 | Mine Blast | 5% chance to mine twice |

---


## ConfigFly ID Reference

> Decoded from `data/tables/Fly.json` (35 records). Maps fly_id to skill_id and resolved Language_en name.

| fly_id | skill_id | Name | Quality | Type | Collab | unit_id |
|--------|----------|------|---------|------|--------|---------|
| 1001 | 5101 | Aggressive Lemon | Normal | Standard | — | fly_1001 |
| 1002 | 5102 | Gleam Candle | Normal | Standard | — | fly_1002 |
| 1003 | 5103 | Coconut Ball | Normal | Standard | — | fly_1003 |
| 1004 | 5104 | Sheep Balloon | Normal | Standard | — | fly_1004 |
| 1005 | 5105 | Tomato Egg | Normal | Standard | — | fly_1005 |
| 1006 | 5106 | Smart Assistant | Normal | Standard | — | fly_1006 |
| 1007 | 5107 | Yoghurt Cocoa | Normal | Standard | — | fly_1007 |
| 2001 | 5201 | Impulse Penguin | Advanced | Standard | — | fly_2001 |
| 2002 | 5202 | Dense Cloud | Advanced | Standard | — | fly_2002 |
| 2003 | 5203 | 3-Round Shooter | Advanced | Standard | — | fly_2003 |
| 2004 | 5204 | Honeypot Warrior | Advanced | Standard | — | fly_2004 |
| 2005 | 5205 | Pumpkin Witch | Advanced | Standard | — | fly_2005 |
| 2006 | 5206 | Bell Ring | Advanced | Standard | — | fly_2006 |
| 2007 | 5207 | Sunshine Bringer | Advanced | Standard | — | fly_2007 |
| 2008 | 5208 | Traveling Jellyfish | Advanced | Standard | — | fly_2008 |
| 2009 | 5209 | Whirlwind Leaf | Advanced | Standard | — | fly_2009 |
| 2010 | 5210 | Crispy Moth | Advanced | Standard | — | fly_2010 |
| 2011 | 5211 | Yoghurt Champ | Advanced | Standard | — | fly_2011 |
| 2016 | 5216 | Dharma | Advanced | Standard | — | fly_2016 |
| 3001 | 5301 | Anubis | Rare | Standard | — | fly_3001 |
| 3002 | 5302 | Midnight Firefly | Rare | Standard | — | fly_3002 |
| 3003 | 5303 | Moonbound Spirit | Rare | Standard | — | fly_3003 |
| 3004 | 5304 | Horus, Sky God | Rare | Standard | — | fly_3004 |
| 3005 | 5305 | Magic Cat | Rare | Standard | — | fly_3005 |
| 3006 | 5306 | Puppy Gaze | Rare | Standard | — | fly_3006 |
| 3007 | 5307 | Deity of Purrs | Rare | Standard | — | fly_3007 |
| 3008 | 5308 | Michelle | Rare | Standard | — | fly_3008 |
| 3012 | 5312 | Lunar Sprite | Rare | Standard | — | fly_3012 |
| 8001 | 5801 | Maniac Love | Advanced | Rabbid | 1 | fly_8001 |
| 8002 | 5802 | Dream Moment | Advanced | Rabbid | 1 | fly_8002 |
| 8101 | 5803 | Pet - Genos | Advanced | OPM | 2 | fly_8101 |
| 8201 | 82011 | Daedream | Advanced | PLLD | 3 | fly_8201 |
| 9001 | 5901 | Astronaut Teal | Normal | B.Duck | — | fly_9001 |
| 9002 | 5902 | Astronaut Pinky | Advanced | B.Duck | — | fly_9002 |
| 9003 | 5903 | Astronaut B.Duck | Rare | B.Duck | — | fly_9003 |

### Quality/Type Key

- **Quality**: 1=Normal, 2=Advanced, 3=Rare
- **Type**: 1-3=Standard tiers, 9=B.Duck collab series, 81=Rabbid collab, 82=One-Punch Man collab, 83=PLLD collab
- **Collab flag**: 0=standard, 1=Rabbid, 2=OPM, 3=PLLD

## Affix Entry ID Reference

> Decoded from `data/tables/Fly_entry.json` (102 affixes x 17 levels each). Maps entry_id to affix name.

| entry_id | Name | Rarity Code | xlsx Rarity | Max Lvl |
|----------|------|-------------|-------------|---------|
| 1001 | Shroom Combo | 1 | blue | 17 |
| 1002 | Reflect Counter | 1 | blue | 17 |
| 1003 | Enhanced Attack | 1 | blue | 17 |
| 1004 | Talent Skill | 1 | blue | 17 |
| 1005 | Enhanced. Go! | 1 | blue | 17 |
| 1006 | Rage Bonus | 1 | blue | 17 |
| 1007 | Barrel Dodge | 1 | blue | 17 |
| 1008 | Regen Ability | 1 | blue | 17 |
| 2001 | Super Crowd Combo | 2 | gold | 17 |
| 2002 | Super Reflect Counter | 2 | gold | 17 |
| 2003 | Super Attack | 2 | gold | 17 |
| 2004 | Super Boost | 2 | gold | 17 |
| 2005 | Loss of Control | 2 | gold | 17 |
| 2006 | Self-Defense | 2 | gold | 17 |
| 2007 | Accurate Defense | 2 | gold | 17 |
| 2008 | Invalid Reflect | 2 | gold | 17 |
| 2009 | Grudge Holder | 2 | gold | 17 |
| 2010 | Shared Hatred | 2 | gold | 17 |
| 2011 | Indirect Aid | 2 | gold | 17 |
| 2012 | Against the Strong | 2 | gold | 17 |
| 2013 | Quick Healing | 2 | gold | 17 |
| 2014 | Debuff Immunity | 2 | gold | 17 |
| 2015 | Longevity | 2 | gold | 17 |
| 2016 | Easy Rage | 2 | gold | 17 |
| 2017 | Iron Shield | 2 | gold | 17 |
| 3001 | Super League | 3 | colorful | 17 |
| 3002 | All-round Hit | 3 | colorful | 17 |
| 3003 | All-round Control | 3 | colorful | 17 |
| 3004 | Reverse Control | 3 | colorful | 17 |
| 3005 | Burst Impact | 3 | colorful | 17 |
| 3006 | Infinite Burst Hit | 3 | colorful | 17 |
| 3007 | Natural Burst | 3 | colorful | 17 |
| 3008 | Multiple Shots | 3 | colorful | 17 |
| 3009 | Meteor Feather | 3 | colorful | 17 |
| 3010 | Wind Tear | 3 | colorful | 17 |
| 3011 | Infinite Dream | 3 | colorful | 17 |
| 3012 | Punch Counter | 3 | colorful | 17 |
| 3013 | Rage Slash | 3 | colorful | 17 |
| 3014 | Divine Touch | 3 | colorful | 17 |
| 3015 | Arcane Light | 3 | colorful | 17 |
| 3101 | Terminal Strike | 3 | colorful | 17 |
| 3102 | No Speeding | 3 | colorful | 17 |
| 3103 | Lightning Conductor | 3 | colorful | 17 |
| 3104 | Speed Disruption | 3 | colorful | 17 |
| 4001 | Slow & Clumsy | 4 | gray | 17 |
| 4002 | Slow Reaction | 4 | gray | 17 |
| 4003 | Tickler | 4 | gray | 17 |
| 4004 | Double Effort | 4 | gray | 17 |
| 4005 | Holdback | 4 | gray | 17 |
| 4006 | Squib | 4 | gray | 17 |
| 4007 | Fragile | 4 | gray | 17 |
| 4008 | Bottomless Abyss | 4 | gray | 17 |
| 4009 | Overtime | 4 | gray | 17 |
| 4010 | Cowardly | 4 | gray | 17 |
| 4011 | Powerless | 4 | gray | 17 |
| 5001 | Quick But Dull | 5 | purple | 17 |
| 5002 | Dull Blade Strike | 5 | purple | 17 |
| 5003 | Multi-Talented | 5 | purple | 17 |
| 5004 | Inert Gas | 5 | purple | 17 |
| 5005 | Backstabbing | 5 | purple | 17 |
| 5006 | One-Sided Attack | 5 | purple | 17 |
| 5007 | Lifespan Match | 5 | purple | 17 |
| 5008 | Paper Defense | 5 | purple | 17 |
| 5009 | Squishy Master | 5 | purple | 17 |
| 5010 | Low Endurance | 5 | purple | 17 |
| 5011 | Heavy Armor | 5 | purple | 17 |
| 5012 | Stability Focused | 5 | purple | 17 |
| 5013 | Poisoned Arrow | 5 | purple | 17 |
| 5014 | The Middle Way | 5 | purple | 17 |
| 5015 | Dilemma | 5 | purple | 17 |
| 5016 | Rise and Fall | 5 | purple | 17 |
| 5017 | Random Match | 5 | purple | 17 |
| 5018 | On Standby | 5 | purple | 17 |
| 5019 | Self-Centered | 5 | purple | 17 |
| 5020 | Altruism | 5 | purple | 17 |
| 5021 | Same Boat | 5 | purple | 17 |
| 5022 | Self Sacrifice | 5 | purple | 17 |
| 6001 | Mutated: Super Boost | 6 | mutated | 17 |
| 6002 | Mutated: Delayed Gratification | 6 | mutated | 17 |
| 6003 | Mutated: Speed Update | 6 | mutated | 17 |
| 6004 | Mutated: Long Wait | 6 | mutated | 17 |
| 6005 | Mutated: Double-Yolk Egg | 6 | mutated | 17 |
| 6006 | Mutated: Time Saving | 6 | mutated | 17 |
| 6007 | Mutated: Roundabout | 6 | mutated | 17 |
| 6008 | Mutated: Efficient Evolution | 6 | mutated | 17 |
| 6009 | Mutated: Time Wasting | 6 | mutated | 17 |
| 6010 | Mutated: Affix Refreshing | 6 | mutated | 17 |
| 6011 | Mutated: Power of the Giant | 6 | mutated | 17 |
| 7001 | Work Light | 7 | work | 17 |
| 7003 | Instant Harvest | 7 | work | 17 |
| 7004 | United Effort | 7 | work | 17 |
| 7005 | Assited Irrigation | 7 | work | 17 |
| 7006 | Osmotic Fertilizer | 7 | work | 17 |
| 7007 | Dual Flows | 7 | work | 17 |
| 7008 | Hawkeye Vigilance | 7 | work | 17 |
| 7010 | Quantum Baking | 7 | work | 17 |
| 7011 | Production Shortcut | 7 | work | 17 |
| 7012 | Unrestricted Mining | 7 | work | 17 |
| 7013 | Chrono Upgrade | 7 | work | 17 |
| 7014 | Free Speedup | 7 | work | 17 |
| 7015 | Research Overtime | 7 | work | 17 |
| 7016 | Mine Blast | 7 | work | 17 |

### Entry Rarity Codes

- **1** = blue (positive buffs)
- **2** = gold (stronger positive)
- **3** = colorful (best-in-slot / proc effects)
- **4** = gray (negative debuffs)
- **5** = purple (trade-off)
- **6** = mutated (breeding/progression)
- **7** = work (farm/crafting)

---

## Data Files

- **Source spreadsheet**: `battlesim/reference/LOM_Database-5.xlsx`
- **ConfigFly binary decode**: `data/tables/Fly.json` (35 avians), `data/tables/Fly_entry.json` (102 affixes x 17 levels), `data/tables/Fly_advance.json` (advancement tiers)
- **Name resolution**: `data/tables/Language_en.json` (string ref -> English name)
- **Structured data**: `battlesim/reference/avians_master.json`, `battlesim/reference/avian_affixes_master.json`