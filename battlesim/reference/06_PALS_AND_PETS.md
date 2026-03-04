# 06 — Pals and Pets

> Complete pal reference: all 90 pals from LOM_Database-5.xlsx with family types and DMG multipliers. See also `pals_master.json` for structured JSON.

---

## Quick Reference — All 90 Pals

| # | Name | Rarity | Family | DMG Mult | Effect |
|---|------|--------|--------|----------|--------|
| 1 | **Hatched Chick** | Normal | Chicken | 3.5 | Increase 5% Base Basic ATK Multiplier |
| 2 | **Flying Fox** | Normal | Sprite | 3.5 | Skill DMG +8% |
| 3 | **Bird Shroom** | Normal | Bird | 1.647 | Attack Speed +5% |
| 4 | **Small Yellow Snail** | Normal | Snail | 3.111 | Reduces enemy movement speed by +15% |
| 5 | **Pink Hydrosprite** | Unique | Specter | 3.5 | Active Skill Base Energy Regen +5% |
| 6 | **Panda** | Unique | Panda | 3.818 | HP Regen +10% |
| 7 | **Fawn** | Unique | Deer | 3.231 | DMG RES +5% |
| 8 | **Kitten** | Well | Cat | 4.2 | After using active skills, detonates enemies, dealing 100% DMG |
| 9 | **Snow Pudding** | Well | Snow Sprite | 6.3 | Reduce enemy attack speed by 5% |
| 10 | **Baby Cactus** | Well | — | 4.5 | Every 3 basic attacks deal an extra 15% DMG |
| 11 | **Xmas Turkey** | Well | Chicken | 3.937 | Increase 8% Base Basic ATK Multiplier |
| 12 | **Ami** | Well | — | 7.887 | Skill DMG +15% |
| 13 | **Rainshade Bird** | Well | Bird | 3.706 | Attack Speed +8% |
| 14 | **Thorn Snail** | Well | Snail | 7 | Reduces enemy movement speed by 20% |
| 15 | **Rebellious Banana** | Well | Banana | 3.316 | Combo +5% |
| 16 | **Arcane Cat** | Rare | Cat | 6.309 | After using active skills, detonates enemies, dealing 150% DMG |
| 17 | **Nature Spirit** | Rare | Specter | 7.887 | Active Skill Base Energy Regen +10% |
| 18 | **Snow Ball** | Rare | Snow Sprite | 9.464 | Reduce enemy attack speed by 8% |
| 19 | **Cub Cactus** | Rare | — | 6.76 | Every 3 basic attacks deal an extra 20% DMG |
| 20 | **Panda Mallet** | Rare | Panda | 8.604 | HP Regen +20% |
| 21 | **Stag** | Rare | Deer | 7.28 | DMG RES +8% |
| 22 | **Ultra-Clean Fighter** | Rare | — | 5.258 | Counter +8% |
| 23 | **Wizard Cat** | Mythic | Cat | 9.464 | After using active skills, detonates enemies, dealing 200% DMG |
| 24 | **Aggressive Hydrosprite** | Mythic | Specter | 11.83 | Active Skill Base Energy Regen +15% |
| 25 | **Snow Sprite** | Mythic | Snow Sprite | 14.196 | Reduce enemy attack speed by 10% |
| 26 | **Energetic Cactus** | Mythic | — | 10.14 | Every 3 basic attacks deal an extra 30% DMG |
| 27 | **Chicken Fighter** | Mythic | Chicken | 8.872 | Increase 10% Base Basic ATK Multiplier |
| 28 | **Po Kong** | Mythic | Sprite | 11.83 | Skill DMG +25% |
| 29 | **Azure Bird** | Mythic | Bird | 8.351 | Attack Speed +10% |
| 30 | **Apprentice Panda** | Mythic | Panda | 12.905 | HP Regen +30% |
| 31 | **Moss Snail** | Mythic | Snail | 15.773 | Reduces enemy movement speed by 30% |
| 32 | **Floral Deer** | Mythic | Deer | 10.92 | DMG RES +10% |
| 33 | **Fortune Dragon** | Epic | Dragon | — | Increase Basic Attack Crit DMG by 20% and Skill Crit Rate by 8% |
| 34 | **Abaddon** | Epic | Abaddon | — | Gain a 10-second shield equal to 8% of Max HP after battle starts. Increase ATK by 8% for 10 seconds after the shield is lost |
| 35 | **Davi** | Epic | Davi | — | Gain 8% Skill Crit Rate and 8% Final Skill Crit DMG for 15 seconds after battle starts |
| 36 | **Frej** | Epic | Frej | — | Gain 8% Crit Rate and 8% Final Crit DMG for 15 seconds after battle starts |
| 37 | **Tamamo** | Epic | Tamamo | — | Gain 8% Pal Crit Rate and 8% Final Pal Crit DMG for 15 seconds after battle starts |
| 38 | **Coffee Cat** | Epic | Cat | — | After using active skills, detonates enemies, dealing 250% DMG |
| 39 | **Triumphant Hydrosprite** | Epic | Specter | — | Active Skill Base Energy Regen +20% |
| 40 | **Snow Goblin** | Epic | Snow Sprite | — | Reduce enemy attack speed by 12% |
| 41 | **Floral Cactus** | Epic | — | — | Every 3 basic attacks deal an extra 35% DMG |
| 42 | **Kongfu Chicken** | Epic | Chicken | — | Increase 12% Base Basic ATK Multiplier |
| 43 | **Piercer Beast** | Epic | Sprite | — | Skill DMG +40% |
| 44 | **Caw-Caw Owl** | Epic | — | — | Attack Speed +12% |
| 45 | **Toothpick Eggplant** | Epic | Eggplant | — | Crit Rate +10% |
| 46 | **Warrior Panda** | Epic | Panda | — | HP Regen +35% |
| 47 | **Ice Cream Snail** | Epic | Snail | — | Reduces enemy movement speed by 35% |
| 48 | **Divine Deer** | Epic | Deer | — | DMG RES +12% |
| 49 | **Mecha Dragon** | Epic | — | — | Crit DMG Bonus +20% |
| 50 | **Spark Squirrel** | Epic | — | — | Pal DMG Multiplier +15% |
| 51 | **B.Duck** | Epic | B.Duck | — | Extends all shield durations by 1.5s |
| 52 | **Travel Camel** | Epic | Camel | — | Enemy Basic ATK DMG -10% |
| 53 | **Rabbids Coming** | Epic | Rabbids Coming | — | Reduce enemy Movement SPD by 15% and ATK SPD by 5% |
| 54 | **Benny** | Legendary | Rabbit | — | Increase Crit Rate by 5%. Benny's attacks have a 30% chance to launch targets for 0.5 second |
| 55 | **Mona** | Legendary | Mona | — | Increase Evasion by 10% and Boss DMG by 30% |
| 56 | **Cat Prince** | Legendary | Cat | — | After using active skills, detonates enemies, dealing 300% DMG |
| 57 | **Warlord Hydrosprite** | Legendary | Specter | — | Active Skill Base Energy Regen +25% |
| 58 | **Snow General** | Legendary | Snow Sprite | — | Reduce enemy attack speed by 15% |
| 59 | **Cowboy Cactus** | Legendary | — | — | Every 3 basic attacks deal an extra 40% DMG |
| 60 | **Chicken Hood** | Legendary | Chicken | — | Increase 15% Base Basic ATK Multiplier |
| 61 | **Fiery Tail** | Legendary | Sprite | — | Skill DMG +60% |
| 62 | **Hero Bird** | Legendary | — | — | Attack Speed +15% |
| 63 | **Kongfu Master** | Legendary | Panda | — | HP Regen +40% |
| 64 | **Tipsy Snail** | Legendary | Snail | — | Reduces enemy movement speed by 40% |
| 65 | **Angel Deer** | Legendary | Deer | — | DMG RES +15% |
| 66 | **Righteous Banana** | Legendary | Banana | — | Combo +10%, Combo DMG +100% |
| 67 | **Rainbow Guardian** | Legendary | — | — | Counter +10%, Counter DMG +100% |
| 68 | **Gingerbread** | Legendary | — | — | Boss DMG +30%, Boss DMG RES +10% |
| 69 | **Pepe** | Legendary | Pepe | — | Healing +0.1% |
| 70 | **Night Spritefox** | Legendary | — | — | Skill Crit +5%, Skill Crit DMG +10% |
| 71 | **Hellflame Feather** | Legendary | — | — | Hellflame Feather's basic attacks deal extra DMG equal to 0.5% of the target's current HP |
| 72 | **Puppy Fervor** | Legendary | — | — | Increases all shields' effects by 20% |
| 73 | **Pirate Parrot** | Legendary | Pirate Parrot | — | Pal Crit DMG +75% |
| 74 | **Floral Panda** | Legendary | Floral Panda | — | Base Regen +0.1% |
| 75 | **Moon Hare** | Legendary | — | — | Pal DMG +60% |
| 76 | **Alpaca Bell** | Legendary | Alpaca | — | Reduces all enemies' ATK by 6% |
| 77 | **Serpent Spring** | Legendary | Snake | — | Reduces all enemies' Final Crit RES by 8% |
| 78 | **Mellow Cloud** | Legendary | — | — | Increases all enemies' ATK SPD by 10%, but reduces their Final Basic ATK DMG, Combo DMG and Counter DMG by 15% |
| 79 | **Blackeye** | Legendary | Blackeye | — | Pal Ignore Evasion +20% |
| 80 | **Moonlit Lonewolf** | Legendary | Wolf | — | Enemy HP Regen -10% |
| 81 | **Mushroom Burglar** | Legendary | Mushroom Burglar | — | Every attack or combo of 7 by Mushroom Burglar increases Character ATK by 2% and reduces all enemies' ATK by 2%, stacking up to 4 times |
| 82 | **Moonspirit Hound** | Legendary | — | — | Reduce all enemies' Pal DMG RES by 8% |
| 83 | **Skeleton Minion** | Legendary | — | — | Adds 1500 Pal Inspire |
| 84 | **Treasure Dragon** | Immortal | Dragon | — | Increase Basic Attack Crit DMG by 50% and Skill Crit Rate by 20% |
| 85 | **Hipster Tortoise** | Immortal | Turtle | — | When HP is below 50%, gain a shield equal to 30% of max HP. (Cooldown: 60 seconds.) |
| 86 | **Electric Pup** | Immortal | Dog | — | Increase counter DMG by 60%, and restore 1% of lost HP on counter |
| 87 | **Alpine Fox** | Immortal | Fox | — | Extend stun duration by 30%, and reduce stunned enemies' DMG RES by 15% |
| 88 | **Pirate Octopus** | Immortal | Octopus | — | Increase Combo DMG by 60%, and with every 3 combos, deal an extra 60% current Combo DMG |
| 89 | **Wealthy Lizard** | Immortal | Lizard | — | Increase Pal DMG by 80% and Ignore Evasion by 10% |
| 90 | **Fortune Envoy** | Legendary | — | — | Increases Global Crit DMG by 15% |

---

## Normal Pals

**Hatched Chick** — Family: Chicken | DMG Mult: 3.5
- Increase 5% Base Basic ATK Multiplier

**Flying Fox** — Family: Sprite | DMG Mult: 3.5
- Skill DMG +8%

**Bird Shroom** — Family: Bird | DMG Mult: 1.647
- Attack Speed +5%

**Small Yellow Snail** — Family: Snail | DMG Mult: 3.111
- Reduces enemy movement speed by +15%

---

## Unique Pals

**Pink Hydrosprite** — Family: Specter | DMG Mult: 3.5
- Active Skill Base Energy Regen +5%

**Panda** — Family: Panda | DMG Mult: 3.818
- HP Regen +10%

**Fawn** — Family: Deer | DMG Mult: 3.231
- DMG RES +5%

---

## Well Pals

**Kitten** — Family: Cat | DMG Mult: 4.2
- After using active skills, detonates enemies, dealing 100% DMG

**Snow Pudding** — Family: Snow Sprite | DMG Mult: 6.3
- Reduce enemy attack speed by 5%

**Baby Cactus** — Family: — | DMG Mult: 4.5
- Every 3 basic attacks deal an extra 15% DMG

**Xmas Turkey** — Family: Chicken | DMG Mult: 3.937
- Increase 8% Base Basic ATK Multiplier

**Ami** — Family: — | DMG Mult: 7.887
- Skill DMG +15%

**Rainshade Bird** — Family: Bird | DMG Mult: 3.706
- Attack Speed +8%

**Thorn Snail** — Family: Snail | DMG Mult: 7
- Reduces enemy movement speed by 20%

**Rebellious Banana** — Family: Banana | DMG Mult: 3.316
- Combo +5%

---

## Rare Pals

**Arcane Cat** — Family: Cat | DMG Mult: 6.309
- After using active skills, detonates enemies, dealing 150% DMG

**Nature Spirit** — Family: Specter | DMG Mult: 7.887
- Active Skill Base Energy Regen +10%

**Snow Ball** — Family: Snow Sprite | DMG Mult: 9.464
- Reduce enemy attack speed by 8%

**Cub Cactus** — Family: — | DMG Mult: 6.76
- Every 3 basic attacks deal an extra 20% DMG

**Panda Mallet** — Family: Panda | DMG Mult: 8.604
- HP Regen +20%

**Stag** — Family: Deer | DMG Mult: 7.28
- DMG RES +8%

**Ultra-Clean Fighter** — Family: — | DMG Mult: 5.258
- Counter +8%

---

## Mythic Pals

**Wizard Cat** — Family: Cat | DMG Mult: 9.464
- After using active skills, detonates enemies, dealing 200% DMG

**Aggressive Hydrosprite** — Family: Specter | DMG Mult: 11.83
- Active Skill Base Energy Regen +15%

**Snow Sprite** — Family: Snow Sprite | DMG Mult: 14.196
- Reduce enemy attack speed by 10%

**Energetic Cactus** — Family: — | DMG Mult: 10.14
- Every 3 basic attacks deal an extra 30% DMG

**Chicken Fighter** — Family: Chicken | DMG Mult: 8.872
- Increase 10% Base Basic ATK Multiplier

**Po Kong** — Family: Sprite | DMG Mult: 11.83
- Skill DMG +25%

**Azure Bird** — Family: Bird | DMG Mult: 8.351
- Attack Speed +10%

**Apprentice Panda** — Family: Panda | DMG Mult: 12.905
- HP Regen +30%

**Moss Snail** — Family: Snail | DMG Mult: 15.773
- Reduces enemy movement speed by 30%

**Floral Deer** — Family: Deer | DMG Mult: 10.92
- DMG RES +10%

---

## Epic Pals

**Fortune Dragon** — Family: Dragon
- Increase Basic Attack Crit DMG by 20% and Skill Crit Rate by 8%

**Abaddon** — Family: Abaddon
- Gain a 10-second shield equal to 8% of Max HP after battle starts. Increase ATK by 8% for 10 seconds after the shield is lost

**Davi** — Family: Davi
- Gain 8% Skill Crit Rate and 8% Final Skill Crit DMG for 15 seconds after battle starts

**Frej** — Family: Frej
- Gain 8% Crit Rate and 8% Final Crit DMG for 15 seconds after battle starts

**Tamamo** — Family: Tamamo
- Gain 8% Pal Crit Rate and 8% Final Pal Crit DMG for 15 seconds after battle starts

**Coffee Cat** — Family: Cat
- After using active skills, detonates enemies, dealing 250% DMG

**Triumphant Hydrosprite** — Family: Specter
- Active Skill Base Energy Regen +20%

**Snow Goblin** — Family: Snow Sprite
- Reduce enemy attack speed by 12%

**Floral Cactus** — Family: —
- Every 3 basic attacks deal an extra 35% DMG

**Kongfu Chicken** — Family: Chicken
- Increase 12% Base Basic ATK Multiplier

**Piercer Beast** — Family: Sprite
- Skill DMG +40%

**Caw-Caw Owl** — Family: —
- Attack Speed +12%

**Toothpick Eggplant** — Family: Eggplant
- Crit Rate +10%

**Warrior Panda** — Family: Panda
- HP Regen +35%

**Ice Cream Snail** — Family: Snail
- Reduces enemy movement speed by 35%

**Divine Deer** — Family: Deer
- DMG RES +12%

**Mecha Dragon** — Family: —
- Crit DMG Bonus +20%

**Spark Squirrel** — Family: —
- Pal DMG Multiplier +15%

**B.Duck** — Family: B.Duck
- Extends all shield durations by 1.5s

**Travel Camel** — Family: Camel
- Enemy Basic ATK DMG -10%

**Rabbids Coming** — Family: Rabbids Coming
- Reduce enemy Movement SPD by 15% and ATK SPD by 5%

---

## Legendary Pals

**Benny** — Family: Rabbit
- Increase Crit Rate by 5%. Benny's attacks have a 30% chance to launch targets for 0.5 second

**Mona** — Family: Mona
- Increase Evasion by 10% and Boss DMG by 30%

**Cat Prince** — Family: Cat
- After using active skills, detonates enemies, dealing 300% DMG

**Warlord Hydrosprite** — Family: Specter
- Active Skill Base Energy Regen +25%

**Snow General** — Family: Snow Sprite
- Reduce enemy attack speed by 15%

**Cowboy Cactus** — Family: —
- Every 3 basic attacks deal an extra 40% DMG

**Chicken Hood** — Family: Chicken
- Increase 15% Base Basic ATK Multiplier

**Fiery Tail** — Family: Sprite
- Skill DMG +60%

**Hero Bird** — Family: —
- Attack Speed +15%

**Kongfu Master** — Family: Panda
- HP Regen +40%

**Tipsy Snail** — Family: Snail
- Reduces enemy movement speed by 40%

**Angel Deer** — Family: Deer
- DMG RES +15%

**Righteous Banana** — Family: Banana
- Combo +10%, Combo DMG +100%

**Rainbow Guardian** — Family: —
- Counter +10%, Counter DMG +100%

**Gingerbread** — Family: —
- Boss DMG +30%, Boss DMG RES +10%

**Pepe** — Family: Pepe
- Healing +0.1%

**Night Spritefox** — Family: —
- Skill Crit +5%, Skill Crit DMG +10%

**Hellflame Feather** — Family: —
- Hellflame Feather's basic attacks deal extra DMG equal to 0.5% of the target's current HP

**Puppy Fervor** — Family: —
- Increases all shields' effects by 20%

**Pirate Parrot** — Family: Pirate Parrot
- Pal Crit DMG +75%

**Floral Panda** — Family: Floral Panda
- Base Regen +0.1%

**Moon Hare** — Family: —
- Pal DMG +60%

**Alpaca Bell** — Family: Alpaca
- Reduces all enemies' ATK by 6%

**Serpent Spring** — Family: Snake
- Reduces all enemies' Final Crit RES by 8%

**Mellow Cloud** — Family: —
- Increases all enemies' ATK SPD by 10%, but reduces their Final Basic ATK DMG, Combo DMG and Counter DMG by 15%

**Blackeye** — Family: Blackeye
- Pal Ignore Evasion +20%

**Moonlit Lonewolf** — Family: Wolf
- Enemy HP Regen -10%

**Mushroom Burglar** — Family: Mushroom Burglar
- Every attack or combo of 7 by Mushroom Burglar increases Character ATK by 2% and reduces all enemies' ATK by 2%, stacking up to 4 times

**Moonspirit Hound** — Family: —
- Reduce all enemies' Pal DMG RES by 8%

**Skeleton Minion** — Family: —
- Adds 1500 Pal Inspire

**Fortune Envoy** — Family: —
- Increases Global Crit DMG by 15%

---

## Immortal Pals

**Treasure Dragon** — Family: Dragon
- Increase Basic Attack Crit DMG by 50% and Skill Crit Rate by 20%

**Hipster Tortoise** — Family: Turtle
- When HP is below 50%, gain a shield equal to 30% of max HP. (Cooldown: 60 seconds.)

**Electric Pup** — Family: Dog
- Increase counter DMG by 60%, and restore 1% of lost HP on counter

**Alpine Fox** — Family: Fox
- Extend stun duration by 30%, and reduce stunned enemies' DMG RES by 15%

**Pirate Octopus** — Family: Octopus
- Increase Combo DMG by 60%, and with every 3 combos, deal an extra 60% current Combo DMG

**Wealthy Lizard** — Family: Lizard
- Increase Pal DMG by 80% and Ignore Evasion by 10%

---

## Data Files

- **Source spreadsheet**: `battlesim/reference/LOM_Database-5.xlsx`
- **Structured data**: `battlesim/reference/pals_master.json`