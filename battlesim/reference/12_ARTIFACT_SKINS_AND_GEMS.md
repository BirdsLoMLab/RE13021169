# 12 — Artifact Skins and Gems

> Complete artifact reference: all 43 artifacts with skin skill IDs decoded from config binaries. See also `artifacts_master.json` for structured JSON.

---

## Quick Reference — All 43 Artifacts

| # | Name | Rarity | Passive | Key Effect |
|---|------|--------|---------|------------|
| 1 | **Cryoshield Flame** | Immortal | Global ATK +10% | For the first 20s after the battle starts, targets within the range have a 30% c... |
| 2 | **Beastroar Bow** | Immortal | Global ATK +10% | Gains 20% Crit Rate. Each Crit increases Final Crit DMG by 1% until the battle e... |
| 3 | **Pixel Universe** | Immortal | Global ATK +10% | Every 14s, charges for 3s and blocks 40% damage, during which all attacks are ba... |
| 4 | **Dance of Tides** | Immortal | Global ATK +10% | Gains 6 stack(s) of Tidal Power at the start of battle, each blocking 6% of DMG ... |
| 5 | **Thunder Verdict** | Immortal | Global ATK +10% | After the battle starts, ATK SPD, Energy Regen SPD, and Pal ATK SPD increase by ... |
| 6 | **Thousandfold Pagoda** | Immortal | Global ATK +10% | After the battle starts, every 10 seconds, deal DMG equal to 6% of the maximum H... |
| 7 | **Demeter's Sickle** | Immortal | Global ATK +10% | Character ATK by 10% after the battle starts. When the Character, Pal, Avian or ... |
| 8 | **Candy Gatling** | Immortal | Global ATK +10% | Basic attacks, combos, and counters unleash an additional 1 to 5 bullets. Each b... |
| 9 | **Spring Chord** | Immortal | Global ATK +10% | Every 11 second(s), deal 1000% of current basic attack AoE DMG and confuse targe... |
| 10 | **Castle Candelabrum** | Immortal | Global ATK +10% | Increases Character ATK by 10% after the battle starts. When the Character, Pal,... |
| 11 | **Flaming Carnage** | Immortal | Global ATK +10% | Every Crit has a chance to deal extra AoE Bleed DMG equal to 50% of your Basic A... |
| 12 | **Chaotic Warlord's Hammer** | Immortal | Global Basic ATK DMG +10% | Basic attacks and combos deal an additional 30% AoE DMG. |
| 13 | **Under the Dome** | Immortal | Global ATK +10% | Summons a copy of a random enemy character or boss unit (excluding Lava Behemoth... |
| 14 | **Extreme Caution** | Immortal | Global Combo DMG +5% | Each basic attack has a 50% chance to deal extra DMG equal to 0.5% of the target... |
| 15 | **Chrono Loop** | Immortal | Global ATK +10% | After the battle starts, gain 10% extra ATK SPD, Energy Regen SPD, and Pal ATK S... |
| 16 | **Staff of Hermes** | Immortal | Global ATK +10% | Reduces all enemies' DMG RES by 8% at the start of battle. Crimson Bite triggers... |
| 17 | **Siren's Whisper** | Immortal | Global ATK +10% | Summons an Abyssal Beast with Control Immunity and 16% of the character's Max HP... |
| 18 | **Divine Champion** | Immortal | Global ATK +10% | ATK increases by 10% after the battle starts. Each basic attack hit has a 10% ch... |
| 19 | **Tear Attack** | Immortal | Global ATK +10% | Summon a Pepe with 20% of the character's Max HP every 12s. Upon its death or 4s... |
| 20 | **Unchained Staff** | Immortal | Global ATK +10% | For every 25% Max HP lost, freezes all enemies and their pals for 2s (the effect... |
| 21 | **Countdown Blast** | Immortal | Global ATK +10% | Every 11s after the battle starts, gains a shield equal to 16% of Max HP (ignore... |
| 22 | **Eye of Raven** | Immortal | Global HP +10% | Casts an equipped active skill at random every 20s. (Casts for the first time 2s... |
| 23 | **Double-edged String** | Immortal | Global ATK +10% | After battle starts, enhances the next basic attack every 1 second: basic attack... |
| 24 | **Eternal Flame** | Immortal | Global ATK +10% | After battle starts, summon an invincible Torch Bearer that exists for 2s. After... |
| 25 | **Sanguine Love** | Immortal | Global ATK +10% | The Final Energy Regen SPD of Clone Strikes increases by 10%. Become bound for 3... |
| 26 | **Lantern's Scroll** | Immortal | Global ATK +10% | Deals 1500% AoE Skill DMG, 600% current Basic ATK AoE DMG, 600% current Combo Ao... |
| 27 | **Webbed Chainsaw** | Immortal | Global ATK +10% | Each basic attack has a 15% chance to apply a stack of Tear, each dealing 20% Ba... |
| 28 | **Sovereign Dragon** | Immortal | DMG RES +10% | Every 5 second, summon a Divine Hand, dealing 1000% of current basic attack AoE ... |
| 29 | **Universe Encyclopedia** | Immortal | Global ATK +10% | After the battle starts, activate Calm World and switch between Calm World and C... |
| 30 | **Skyward Blade** | Immortal | Global ATK +10% | For every 10 (basic attack, combo, counter, skill) unleash, release a sword aura... |
| 31 | **Moment of Brilliance** | Immortal | Global ATK +10% | Every 11s, releases a big firework. Explodes once in 1.5s, dealing 3000% AoE Ski... |
| 32 | **Storm Destroyer** | Immortal | Global ATK +10% | Every 11s after the battle starts, deal 2000% AoE Skill DMG, 800% DMG current Co... |
| 33 | **Moonhunt Bow** | Immortal | Global ATK +10% | Healing Rate increases by 12%. Fires arrows every 8s, dealing DMG equal to 4% Ma... |
| 34 | **Spear of Creation** | Immortal | Global ATK +10% | Switches elements every 2s in the order of Fire, Water, Thunder and Wind and tri... |
| 35 | **Skeletal Bloom** | Immortal | Global ATK +10% | At the start of battle, immediately damage an enemy target for 30% of their max ... |
| 36 | **Fate** | Immortal | Global ATK +10% | After the battle starts, ATK, DEF, and Final DMG RES increase by 10%, 30%, and 1... |
| 37 | **Punch of Triumph** | Immortal | Global ATK +10% | Increase Final DMG RES by 10%. Charge once for every Stun triggered, 15 basic at... |
| 38 | **Thundering Hammer** | Immortal | Global ATK +10% | Every 10s, deal 5000% Skill DMG, 1000% current Basic ATK DMG (can be Crit), 1000... |
| 39 | **Fearless Stride** | Immortal | Global ATK +10% | Gains 10% Final DMG RES after the battle starts. Every 12s, deals 2000% Skill DM... |
| 40 | **Scale of Justice** | Immortal | Global ATK +10% | Judges once every 10s after battle starts. If the current HP is over 50 times th... |

---

## Artifact Skin Skill ID Reference

Decoded from `Artifact_skin.json` and `Skill.json` config binaries. Maps each artifact to its skin skill IDs used in battle simulation.

| artifact_id | Artifact Name | Base Skill ID | Skill Name | All Skin Skill IDs |
|-------------|---------------|---------------|------------|--------------------|
| 2 | Chaotic Warlord's Hammer | 5102 | Thunder Wrath | 5102 |
| 3 | Sovereign Dragon | 5103 | Sovereign Dragon | 5103 |
| 4 | Eye of Raven | 5104 | Eye of Raven | 5104, 51041, 51042 |
| 5 | Luminary Lantern | 5105 | Luminary Lantern | 5105, 51051, 51052 |
| 6 | Candy Gatling | 5106 | Candy Gatling | 5106 |
| 7 | Skyward Blade | 5107 | Skyward Blade | 5107, 51071, 51072 |
| 9 | Thousandfold Pagoda | 5110 | Snow Sprite Arrives | 5110 |
| 15 | Tear Attack | 5112 | Tear Attack | 5112, 51122, 51123 |
| 16 | Double-edged String | 5114 | Acoustic Rupture | 5114 |
| 17 | Extreme Caution | 5115 | Safe Distance | 5115 |
| 18 | Spring Chord | 5113 | Spring Chord | 5113 |
| 20 | Siren's Whisper | 5117 | Abyssal Beast | 5117, 51171, 51172 |
| 21 | Webbed Chainsaw | 5118 | Duck Swirl Strike | 5118, 51181, 51182 |
| 22 | Unchained Staff | 5124 | Time Pause | 5124, 5125, 5126, 51242, 51244, 51252, 51254, 51262, 51264 |
| 24 | Castle Candelabrum | 5129 | Spectral Chant | 5129, 51291, 51292, 51293, 51294, 51295 |
| 27 | Countdown Blast | 5132 | Chrono Reversal | 5132, 51321, 51322 |
| 28 | Lantern's Scroll | 5134 | Judgement of Flame | 5134 |
| 29 | Sanguine Love | 5135 | Binding Love | 5135 |
| 31 | Flaming Carnage | 5801 | Skyfire Wrath | 5801 |
| 32 | Fate | 5153 | Fate's Glare | 5153 |
| 108 | Pixel Universe | 5140 | Storm Slash | 5140 |
| 110 | Moment of Brilliance | 5145 | Splendid Bloom | 5145 |
| 111 | Moonhunt Bow | 5148 | Moonlight Hunt | 5148 |
| 112 | Thousand Swords | 5150 | Warblade Raid | 5150 |
| 201 | Beastroar Bow | 5120 | Piercing Squail | 5120 |
| 204 | Cryoshield Flame | 5131 | Frostflame Shield | 5131, 51311, 51312, 51313, 51314, 51315 |
| 401 | Storm Destroyer | 5147 | Shattering Slam | 5147 |
| 701 | Eternal Flame | 5121 | Invincible Torch Bearer | 5121, 5122, 5123, 51211, 51212, 51213, 51221, 51222, 51223, 51231, 51232, 51233 |
| 702 | Under the Dome | 5128 | Copy Gene | 5128, 51281, 51282 |
| 703 | Demeter's Sickle | 5130 | Demeter's Sigh | 5130, 51302, 51303, 51305, 51306, 51308 |
| 704 | Divine Champion | 5137 | Divine Champion | 5137, 51371, 51372 |
| 705 | Staff of Hermes | 5138 | Serpent Frenzy | 5138 |
| 706 | Dance of Tides | 5141 | Dancing Flows | 5141 |
| 707 | Chrono Loop | 5143 | Chrono Speed | 5143, 51431, 51432 |
| 708 | Thunder Verdict | 5144 | Lightning Storm | 5144 |
| 709 | Universe Encyclopedia | 5146 | World Flipper | 5146 |
| 710 | Spear of Creation | 5151 | Elemental Genesis | 5151 |
| 711 | Skeletal Bloom | 5152 | Sound of Reunion | 5152 |
| 712 | Punch of Triumph | 5154 | One-Punch Victory | 5154 |
| 713 | Thundering Hammer | 5155 | Hammer Smash! | 5155 |
| 714 | Fearless Stride | 5156 | Fearless Stride | 5156 |
| 715 | Scale of Justice | 5157 | Call of Justice | 5157 |
| 716 | Bear Bump | 5158 | Bullet Shock | 5158 |

---

## Full Details

### 1. Cryoshield Flame

**Rarity:** Immortal

**Effect:** For the first 20s after the battle starts, targets within the range have a 30% chance to gain a stack of Frostbite every 0.5s, each stack reducing their DMG RES by 1% until the battle ends, stacking up to 20 times. Every 10% of targets' Movement SPD lowered increases their chance of Frostbite by 1.5% (calculated independently for each target). Every 3 stacks of Frostbite reduces targets' Basic ATK DMG RES, Combo DMG RES, Counter DMG RES, Skill DMG RES and Pal DMG RES by an extra 2%. 20s after the battle starts, deals 80% of current Basic ATK AoE DMG (can be Crit), 80% of current Combo AoE DMG (can be Crit), 80% of current Counter AoE DMG (can be Crit), and 400% of Skill DMG per second for 10s, and directly defeats targets with below 4% HP. Execution DMG increases by 1% for every 5 stacks of Frostbite on targets.

**Passive:** Global ATK +10%

---

### 2. Beastroar Bow

**Rarity:** Immortal

**Effect:** Gains 20% Crit Rate. Each Crit increases Final Crit DMG by 1% until the battle ends, stacking up to 20 times. Upon reaching maximum stacks, each Crit has a 10% chance to deal an extra 750% of AoE Skill DMG, 150% of current Basic ATK AoE DMG (can be Crit), 150% of current Combo AoE DMG (can be Crit) and 150% of current Counter AoE DMG (can be Crit).

**Passive:** Global ATK +10%

---

### 3. Pixel Universe

**Rarity:** Immortal

**Effect:** Every 14s, charges for 3s and blocks 40% damage, during which all attacks are banned except for counters. After the charge, releases the Charged Slash, dealing 5000% of AoE Skill DMG, 1000% of current AoE Basic ATK DMG (can be Crit), 1000% of current AoE Combo DMG (can be Crit), and 1000% of current AoE Counter DMG (can be Crit). The Charged Slash breaks targets' Shield and ignores Immunity. Every 1% HP lost increases the Charged Slash's damage by 1%. (Triggers at the start of the battle.)

**Passive:** Global ATK +10%

---

### 4. Dance of Tides

**Rarity:** Immortal

**Effect:** Gains 6 stack(s) of Tidal Power at the start of battle, each blocking 6% of DMG but reducing ATK SPD, Energy Regen SPD and Pal ATK SPD by 6%. Dances once every 7/6/5/4/3s (every 3s afterwards), using 1 stack of Tidal Power to deal 1500% AoE Skill DMG, 300% current Combo AoE DMG (can be Crit), 300% current Counter AoE DMG (can be Crit), reduce targets' DMG RES by 2%, and increase ATK SPD, Movement SPD, Energy Regen SPD and Pal ATK SPD by 2% until the battle ends, stacking up to 10 times.

**Passive:** Global ATK +10%

---

### 5. Thunder Verdict

**Rarity:** Immortal

**Effect:** After the battle starts, ATK SPD, Energy Regen SPD, and Pal ATK SPD increase by 10%. Basic attack, combo, and counter hits have a 8% chance and pal basic attack and combo hits have a 15% chance to deal extra DMG equal to 1% of the target's Max HP (ignores Immunity).

**Passive:** Global ATK +10%

---

### 6. Thousandfold Pagoda

**Rarity:** Immortal

**Effect:** After the battle starts, every 10 seconds, deal DMG equal to 6% of the maximum HP to all targets within range, reducing their ATK SPD, Energy Regen, and Pal ATK SPD by 30% for 3 seconds.

**Passive:** Global ATK +10%

---

### 7. Demeter's Sickle

**Rarity:** Immortal

**Effect:** Character ATK by 10% after the battle starts. When the Character, Pal, Avian or Summon deals damage, for every 1% of the target's Max HP higher than the Character's (or the Summon's), increases Final DMG dealt to the target by 0.6%, up to 30%.

**Passive:** Global ATK +10%

---

### 8. Candy Gatling

**Rarity:** Immortal

**Effect:** Basic attacks, combos, and counters unleash an additional 1 to 5 bullets. Each bullet deals 10% of current basic attack DMG.

**Passive:** Global ATK +10%

---

### 9. Spring Chord

**Rarity:** Immortal

**Effect:** Every 11 second(s), deal 1000% of current basic attack AoE DMG and confuse targets: each of their own attacks (basic attacks, combos, counterstrikes, and skills) will deal an extra 20% of their current basic attack DMG to themselves. The confusion lasts 5 second(s). (Casts 1 time immediately after battle starts.)

**Passive:** Global ATK +10%

---

### 10. Castle Candelabrum

**Rarity:** Immortal

**Effect:** Increases Character ATK by 10% after the battle starts. When the Character, Pal, Avian or Summon deals damage, the Character regenerates HP equal to 15% of DMG dealt, (ignores PvP healing reduction), up to 1% of Max HP. 20s to 39s into battle, the Character loses 1% of current HP per second. 40s to 59s into battle, loses 2% of current HP per second. After 60s into battle, loses 5% of current HP per second.

**Passive:** Global ATK +10%

---

### 11. Flaming Carnage

**Rarity:** Immortal

**Effect:** Every Crit has a chance to deal extra AoE Bleed DMG equal to 50% of your Basic ATK (ignores DMG Immunity), reducing the target's Crit RES by 1% and stacking up to 20 times.

**Passive:** Global ATK +10%

---

### 12. Chaotic Warlord's Hammer

**Rarity:** Immortal

**Effect:** Basic attacks and combos deal an additional 30% AoE DMG.

**Passive:** Global Basic ATK DMG +10%

---

### 13. Under the Dome

**Rarity:** Immortal

**Effect:** Summons a copy of a random enemy character or boss unit (excluding Lava Behemoth, Spectacle Specter and Hellhound) within range every 14s, which inherits 20% of their Max HP and 40% of their ATK, all their other attributes. The copy exists for up to 5s. (Triggers once after the battle starts.)

**Passive:** Global ATK +10%

---

### 14. Extreme Caution

**Rarity:** Immortal

**Effect:** Each basic attack has a 50% chance to deal extra DMG equal to 0.5% of the target's Max HP and a 10% chance to wound all targets within the range, reducing their Regen and Healing Amount by 50% for 2 seconds.

**Passive:** Global Combo DMG +5%

---

### 15. Chrono Loop

**Rarity:** Immortal

**Effect:** After the battle starts, gain 10% extra ATK SPD, Energy Regen SPD, and Pal ATK SPD and reduce all enemies' ATK SPD, Energy Regen SPD, and Pal ATK SPD by 10%. When HP drops below 5% for the first time, recover HP over 1s to the value from 3s ago, immune to all Death and other effects and gaining Invincibility. After HP recovery, reduce all active skills' cooldowns by 3s.

**Passive:** Global ATK +10%

---

### 16. Staff of Hermes

**Rarity:** Immortal

**Effect:** Reduces all enemies' DMG RES by 8% at the start of battle. Crimson Bite triggers every 5s, making the next basic attack deal extra DMG equal to 750% of AoE Skill DMG, 150% of current AoE Combo DMG, and 150% of current AoE Counter DMG, and regenerating HP equal to 50% of the DMG dealt. (DMG can be Crit and ignores Immunity. HP Regen ignores PvP healing reduction but cannot exceed 3% of Max HP each time. Triggers at the start of the battle.) Umbra Curse triggers every 2 active skills, dealing DMG equal to 3% of the target's Max HP and reducing their HP Regen, ATK SPD, Energy Regen, and Pal ATK SPD by 10% for 5s.

**Passive:** Global ATK +10%

---

### 17. Siren's Whisper

**Rarity:** Immortal

**Effect:** Summons an Abyssal Beast with Control Immunity and 16% of the character's Max HP every 14s after battle starts, lasting up to 5s. Its attacks deal 40% DMG. (Triggers at the start of the battle.)

**Passive:** Global ATK +10%

---

### 18. Divine Champion

**Rarity:** Immortal

**Effect:** ATK increases by 10% after the battle starts. Each basic attack hit has a 10% chance to deal an extra 50% of current Basic ATK DMG and apply 1 stack of Lightning. Active Skill deals an extra 150% of Skill DMG to up to 3 targets and applies 1 stack of Lightning. Each Pal attack hit has a 10% chance to deal an extra 50% of current Pal DMG and apply 1 stack of Lightning. Each Lightning stack reduces DEF by 2%, stacking up to 7 times, cannot be Cleansed. At 7 stacks, clear all stacks to summon lightning, dealing 1000% of AoE Skill DMG, 400% of current AoE Combo DMG, and 400% of current AoE Counter DMG (Lightning DMG can be Crit and ignores immunity) and reducing target's Skill DMG RES, Combo DMG RES, Counter DMG RES, Basic ATK DMG RES and Pal DMG RES by 3%, lasting until the battle ends, stacking up to 5 times.

**Passive:** Global ATK +10%

---

### 19. Tear Attack

**Rarity:** Immortal

**Effect:** Summon a Pepe with 20% of the character's Max HP every 12s. Upon its death or 4s after it's summoned, it will explode, dealing 1000% Basic ATK DMG (triggers at the start of the battle).

**Passive:** Global ATK +10%

---

### 20. Unchained Staff

**Rarity:** Immortal

**Effect:** For every 25% Max HP lost, freezes all enemies and their pals for 2s (the effect ignores Control Immunity and Control Duration Reduction), during which they cannot use Basic ATK, Combo, Counter or skills, and their Energy Regen SPD (including Active Skills and Avian Active Skills) and Regen Attributes are reduced to 0. The skill triggers up to 3 times. When frozen targets take DMG equal to 25% of their HP at the start of the freeze, they and their pals and Avians will be unfrozen.

**Passive:** Global ATK +10%

---

### 21. Countdown Blast

**Rarity:** Immortal

**Effect:** Every 11s after the battle starts, gains a shield equal to 16% of Max HP (ignores PvP reduction and shield breaks) at the cost of 10% of current HP (ignores Immunity) for 3s, during which the character and pal cannot use Basic ATK, Combo, Counter or Active Skills.  After the shield disappears, the next Basic ATK deals 1200% of current Basic ATK DMG (can be Crit), 1200% of current Combo DMG (can be Crit), 1200% of current Counter DMG (can be Crit) and 4000% of Skill DMG to targets within the range, and increases the pal's next Basic ATK DMG by 200%. (Triggers at the start of the battle.)

**Passive:** Global ATK +10%

---

### 22. Eye of Raven

**Rarity:** Immortal

**Effect:** Casts an equipped active skill at random every 20s. (Casts for the first time 2s after battle starts.)

**Passive:** Global HP +10%

---

### 23. Double-edged String

**Rarity:** Immortal

**Effect:** After battle starts, enhances the next basic attack every 1 second: basic attacks deal 100% more Basic ATK AoE DMG. If any of the following soundwave requirements is achieved for the first time in battle, grants enhanced basic attacks its corresponding bonus effect. Bass: After 25 combos, enhanced basic attacks deal an additional 150% current Combo AoE DMG. Mediant: After 25 counterstrikes, enhanced basic attacks deal an additional 150% current Counter AoE DMG. Treble: After 10 skills, enhanced basic attacks deal an additional 400% AoE Skill DMG.

**Passive:** Global ATK +10%

---

### 24. Eternal Flame

**Rarity:** Immortal

**Effect:** After battle starts, summon an invincible Torch Bearer that exists for 2s. After it disappears, gain 5% Final Crit DMG, 5% Final Skill Crit DMG and 5% Pal Final Crit DMG until the battle ends. 8s into the battle, summon a second invincible Torch Bearer that exists for 2s. After it disappears, gain 5% ATK SPD and 5% Pal ATK SPD until the battle ends. 15s into the battle, summon a third invincible Torch Bearer that exists for 2s. After it disappears, gain 5% ATK and 10% DEF until the battle ends. 20s into the battle, summon the last invincible Torch Bearer that exists for 2s. After it disappears, double the bonuses provided by the first 3 Torch Bearers until the battle ends. (Invincible: Negates all damage, including damage that ignores damage immunity.)

**Passive:** Global ATK +10%

---

### 25. Sanguine Love

**Rarity:** Immortal

**Effect:** The Final Energy Regen SPD of Clone Strikes increases by 10%. Become bound for 3s every 10s after battle starts, during which the character cannot use Basic ATK, Combo, Counter, or Active Skill, but gains 20% of DMG RES and increases Pal, Summon and Ally Crit Rate by 10% and Final Crit DMG by 20%. (Triggers at the start of the battle.)

**Passive:** Global ATK +10%

---

### 26. Lantern's Scroll

**Rarity:** Immortal

**Effect:** Deals 1500% AoE Skill DMG, 600% current Basic ATK AoE DMG, 600% current Combo AoE DMG, and 600% current Counter AoE DMG every 10s after the battle starts. If current HP is lower than the target's, deals extra DMG equal to 4% current HP and reduces the target's Max HP by 4%, stacking up to 10 times. If current ATK is lower than the target's, reduces the target's Active Skill Duration by 4%, stacking up to 10 times. (Triggers at the start of the battle.)

**Passive:** Global ATK +10%

---

### 27. Webbed Chainsaw

**Rarity:** Immortal

**Effect:** Each basic attack has a 15% chance to apply a stack of Tear, each dealing 20% Basic ATK DMG per second to the target (can trigger Crit) and reducing their DEF by 6% until the battle ends, stacking up to 5 times. At 5 stacks, deals DMG equal to 8% of the target's Max HP once and increases their DMG received by 6% until the battle ends.

**Passive:** Global ATK +10%

---

### 28. Sovereign Dragon

**Rarity:** Immortal

**Effect:** Every 5 second, summon a Divine Hand, dealing 1000% of current basic attack AoE DMG.

**Passive:** DMG RES +10%

---

### 29. Universe Encyclopedia

**Rarity:** Immortal

**Effect:** After the battle starts, activate Calm World and switch between Calm World and Chaos World every 15s. Calm World: All enemies' ATK is reduced by 16%. Chaos World: ATK increases by 16%, and deals 1500% of AoE Skill DMG, 300% of current Combo AoE DMG (can be Crit), 300% of current Counter AoE DMG (can be Crit), and DMG equal to 3% of the target's Max HP every 5s.

**Passive:** Global ATK +10%

---

### 30. Skyward Blade

**Rarity:** Immortal

**Effect:** For every 10 (basic attack, combo, counter, skill) unleash, release a sword aura, dealing 150% of current basic attack DMG.

**Passive:** Global ATK +10%

---

### 31. Moment of Brilliance

**Rarity:** Immortal

**Effect:** Every 11s, releases a big firework. Explodes once in 1.5s, dealing 3000% AoE Skill DMG, 500% of current Combo AoE DMG (can be Crit), 500% of current Counter AoE DMG (can be Crit), and 5% of the target's Max HP DMG to enemies (ignores DMG Immunity) and reducing all active skill cooldowns by 1.2s. After 0.5s, explodes again, dealing 3000% AoE Skill DMG, 500% of current Combo AoE DMG (can be Crit), and 500% of current Counter AoE DMG (can be Crit) to enemies. (Triggers at the start of the battle.)

**Passive:** Global ATK +10%

---

### 32. Storm Destroyer

**Rarity:** Immortal

**Effect:** Every 11s after the battle starts, deal 2000% AoE Skill DMG, 800% DMG current Combo AoE DMG and 800% current Counter AoE DMG, and paralyze the target for 5s. The target's combo hits have a 20% chance to reduce their Combo Rate by 30% for 2s. Their counter hits have a 20% chance to reduce Counter Rate by 30% for 2s. Their skill crit reduces their Skill Crit Rate by 30% for 2s. Their pal crit has a 50% chance to reduce the pal's Crit Rate by 30% for 2s. The effects don't stack, but duration resets upon repeated trigger.

**Passive:** Global ATK +10%

---

### 33. Moonhunt Bow

**Rarity:** Immortal

**Effect:** Healing Rate increases by 12%. Fires arrows every 8s, dealing DMG equal to 4% Max HP to all enemies, restoring 6% Max HP and gaining 24% ATK SPD for 5s. (Triggers at the start of the battle.)

**Passive:** Global ATK +10%

---

### 34. Spear of Creation

**Rarity:** Immortal

**Effect:** Switches elements every 2s in the order of Fire, Water, Thunder and Wind and triggers elemental effects. Fire: Basic attack hits have a 40% chance to deal extra DMG equal to 2% of the target's current HP (ignores DMG Immunity) for 4s. Water: Restores 8% Max HP and increases DEF by 32% for 4s. Thunder: Reduces all active skill cooldowns by 1s and increases ATK SPD and Pal ATK SPD by 24% for 4s. Wind: Reduces all enemies' Movement SPD, ATK SPD, Energy Regen SPD, and Pal ATK SPD by 20% (cannot be cleansed) for 4s. Switches to Fire at the start of battle.

**Passive:** Global ATK +10%

---

### 35. Skeletal Bloom

**Rarity:** Immortal

**Effect:** At the start of battle, immediately damage an enemy target for 30% of their max HP (prioritizing the closest player and ignoring DMG Immunity), gain 24% increased DMG RES and DEF, and recover 8% of missing HP per second. These effects decay by 25% every 9 seconds. After 1 second, take 30% of current HP as damage, ignoring DMG Immunity.

**Passive:** Global ATK +10%

---

### 36. Fate

**Rarity:** Immortal

**Effect:** After the battle starts, ATK, DEF, and Final DMG RES increase by 10%, 30%, and 10%. Every 5s, 15 basic attacks, or 2 active skills cast grants 1 Power of Fate stack, increasing Final DMG Boost, ATK SPD, Pal ATK SPD, Energy Regen SPD, Final Crit DMG, Final Pal Crit DMG, and Final Skill Crit DMG by 1%, up to 25 stacks. Each extra Power of Fate stack after 10 stacks reduces DEF by 4%, up to 15 stacks. Each extra stack after 15 stacks reduces Final DMG RES by 2%, up to 10 stacks. Each extra stack after 20 stacks deals DMG equal to 1% of current HP per second to oneself (ignores DMG immunity), up to 5 stacks.

**Passive:** Global ATK +10%

---

### 37. Punch of Triumph

**Rarity:** Immortal

**Effect:** Increase Final DMG RES by 10%. Charge once for every Stun triggered, 15 basic attacks, or 3 active skills. After 5 charges, throw a powerful punch, dealing 4000% Skill DMG, 800% current Basic ATK DMG (can be Crit), 800% current Combo DMG (can be Crit), 800% current Counter DMG (can be Crit), and DMG equal to 2.4% Max HP to all enemies (all ignores DMG Immunity), and reducing their Crit DMG, Skill Crit DMG, and Pal Crit DMG by 24% for 5s (cannot be Cleansed).

**Passive:** Global ATK +10%

---

### 38. Thundering Hammer

**Rarity:** Immortal

**Effect:** Every 10s, deal 5000% Skill DMG, 1000% current Basic ATK DMG (can be Crit), 1000% current Combo DMG (can be Crit), and 1000% current Counter DMG (can be Crit) to all enemies, and launch them and their pals airborne for 0.8s. If a target is Invincible or Immune to DMG or death, reduce all their HP Regen, ATK SPD, Pal ATK SPD, and Energy Regen SPD by 24% for 5s; if not, reduce their DMG RES by 24% for 5s. Both effects cannot be cleansed. (Triggers at the start of the battle.)

**Passive:** Global ATK +10%

---

### 39. Fearless Stride

**Rarity:** Immortal

**Effect:** Gains 10% Final DMG RES after the battle starts. Every 12s, deals 2000% Skill DMG, 400% current Basic ATK DMG (can be Crit), 400% current Combo DMG (can be Crit), 400% current Counter DMG (can be Crit), and DMG equal to 1.6% of the target's Max HP (ignores Immunity) to all enemies after a short charge, recovers HP equal to 50% of the total DMG dealt (ignores PvP deduction, capped at 20% Max HP), and increases the target's active skill cooldown duration by 1.6s (capped at initial cooldown duration). Also, increases the next instance of Skill DMG of 'Fearless Stride' by 50%, stacking up to 4 times. (Triggers at the start of the battle.)

**Passive:** Global ATK +10%

---

### 40. Scale of Justice

**Rarity:** Immortal

**Effect:** Judges once every 10s after battle starts. If the current HP is over 50 times the current ATK, Final DMG Boost increases by 12%; otherwise, Final DMG RES increases by 12%, lasting until the next judgment. If the enemy's current HP is higher, deals DMG equal to 10% of their current HP (ignores DMG immunity) and recovers an equal amount of HP (ignores PvP reduction, capped at 30% Max HP); otherwise, reduces the enemy's ATK by 16%, lasting until the next judgement (cannot be cleansed). (Triggers at the start of the battle.)

**Passive:** Global ATK +10%

---

## Data Files

- **Source spreadsheet**: `battlesim/reference/LOM_Database-5.xlsx`
- **Structured data**: `battlesim/reference/artifacts_master.json`
- **Config binaries**: `data/tables/Artifact_skin.json`, `data/tables/Artifact.json`, `data/tables/Skill.json`, `data/tables/Language_en.json`