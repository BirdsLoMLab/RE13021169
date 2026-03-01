# 33 — Game Systems Reference (Decoded Config Data)

> **Sources:** `Equipment*.json`, `Mount*.json`, `Artifact*.json`, `Pet*.json`, `Petrace.json`, `Spirit*.json`, `Back_*.json`, `Badge.json`, `Title.json`, `Language_en.json`
> **Scope:** All progression systems with stat scaling, set bonuses, and combat-relevant effects

---

## Equipment System

### Overview
- **Source:** `Equipment.json` (5,357 items), `Equipment_refinement.json`, `Equipment_advancement.json`, `Equipment_resonance.json`, `Equipment_suit.json`
- **10 Slots:** Weapon (part 1), Ornaments (2), Helmet (3), Shoulder (4), Armor (5), Bracers (6), Gloves (7), Belt (8), Leggings (9), Boots (10)
- **Quality Tiers:** 1-11 (White → Green → Blue → Purple → Gold → Orange → Red → Pink → Multicolor → Gilt → Forever)

### Equipment Attributes
Each equipment piece has:
- **preAttr[0]** — Primary stats: HP (1002), ATK (1001), DEF (1024) with base values
- **preAttr[1]** — Secondary stats: Crit Rate (1004), Evasion (1008), etc.
- **multiple** — Multipliers applied at certain thresholds (e.g., `[[0, 2.5], [1002, 3.75]]` = base ×2.5, HP ×3.75)
- **gradeRange** — Random stat grade range [min, max]

### Refinement System
- **150 levels** per equipment slot
- Grants ATK (1001), HP (1002), DEF (1024) per level
- **Level 150 max:** +12,800 ATK, +12,800 HP, +12,800 DEF per slot

### Advancement System (37 Stages)
All slots must reach current max refinement to advance to next stage.

| Stage | Pierce (1068) | Ignore Pierce (1069) | Block (1071) | Ignore Block (1072) | Pal Inspire (1074) | Ignore Inspire (1075) | Pal Suppress (1077) | Ignore Suppress (1078) |
|-------|--------------|---------------------|--------------|--------------------|--------------------|---------------------|--------------------|--------------------|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 100 | 100 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2 | 100 | 100 | 100 | 100 | 0 | 0 | 0 | 0 |
| 6 | 300 | 300 | 300 | 300 | 100 | 100 | 0 | 0 |
| 10 | 780 | 780 | 780 | 780 | 780 | 780 | 780 | 780 |
| 18 | 2020 | 2020 | 2020 | 2020 | 2020 | 2020 | 2020 | 2020 |
| 36 | **6,240** | **6,240** | **6,240** | **6,240** | **6,240** | **6,240** | **6,240** | **6,240** |

### Equipment Resonance (18 Stages)
Resonance milestones grant **Final DMG Bonus (1081)** and **Final DMG RES (1082)**:

| Stage | Final DMG Bonus | Final DMG RES | Total Power |
|-------|----------------|---------------|-------------|
| 1 | 200 | 0 | — |
| 2 | 200 | 200 | — |
| 4 | 500 | 500 | — |
| 6 | 800 | 800 | — |
| 8 | 1,200 | 1,200 | — |
| 10 | 1,600 | 1,600 | — |
| 12 | 2,100 | 2,100 | — |
| 14 | 2,600 | 2,600 | — |
| 16 | 3,200 | 3,200 | — |
| **18** | **3,800** | **3,800** | — |

**PvP Significance:** Equipment resonance is the #1 source of Final DMG Bonus/RES. A fully resonated player has +3800 on both, which is the single largest source of the `total_dam_add/total_dam_def` universal multiplier.

### Equipment Suit Set — "Knight"
| Pieces | Effect |
|--------|--------|
| 3-piece | ATK +1,000 |
| 6-piece | ATK +2,000 |
| 9-piece | **ATK Bonus +50%** (multiplicative) |

---

## Mount System

### Overview
- **Source:** `Mount.json` (72 mounts), `Mount_level.json` (300 levels), `Mount_ability.json`, `Mount_skin.json`, `Mount_chapter_bufflist.json`
- **Quality range:** 4 (Green) to 9 (Multicolor)
- Speed (min_speed/max_speed) is cosmetic — always 200 in combat

### Mount Level Progression (300 levels)
All mounts share the same leveling table. Stats scale **three base attributes**:

| Level | Base HP (2003) | Base ATK (2001) | Base DEF (2005) | Power |
|-------|---------------|----------------|----------------|-------|
| 1 | 400 | 400 | 400 | 10,000 |
| 50 | — | — | — | — |
| 100 | — | — | — | — |
| 200 | — | — | — | — |
| **300** | **104,837,000** | **104,837,000** | **104,837,000** | **97,210,000** |

### Mount Ability System
3 ability branches, each with its own level track. Each branch grants 3 bonus attributes at increasing values:

**Branch 1 (Default):** Basic ATK DMG (2022), Combo DMG (2017), Counter DMG (2018)
- Level 1: +1,000 each
- Level 2: +1,200 each
- Each level increases by +200 per attribute

### Mount Skin Skills (Combat-Relevant)
Mount skins unlock powerful combat skills. Higher skin levels = higher skill levels.

| Skill ID | Mount | Max Lv | Effect |
|----------|-------|--------|--------|
| 5001 | Default | 24 | Evasion +75% |
| 5002 | Pyrebreaker | 3 | Crit Rate +2%/s (cap 40%), Crit DMG +10%/s (cap 200%) |
| 5003 | Hot Wheels | 3 | Pal ATK SPD +3%/s (cap 60%) |
| 5004 | White Tiger | 3 | Targets below your HP% take +30% DMG; above have ATK -20% |
| 5005 | Blue Ox | 3 | DMG RES +15%, Control Duration -50% |
| 5006 | Blue Queen | 1 | Distribute DMG to 5 enemies; +2.5% target max HP every 10s |
| 5007 | Round Frog | 3 | Every 10s kill 1 enemy → ATK +30% for 5s; boss/player stun 1s |
| 5008 | Purple Wing | 3 | Deals 10000% AoE DMG, launches 0.5s, every 11s |
| 5009 | Cloud Drifter | 3 | Skill Crit +20%; after skill crit ATK +40% for 5s |
| 5010 | Kun | 1 | Convert received DMG into DoT over 5s (damage smoothing) |
| 5013 | Cyclone Bamboo | 1 | Shield +3s duration, +50% effect, ATK +10%, Counter +25% under shield |
| 5014 | Velocity Blitz | 3 | Every 1 counter → Global Counter DMG +20% for 3s (cap 60%) |
| 5015 | AdaptoSlime | 1 | After cumulative 5% max HP damage → deal 500% basic ATK AoE |
| 5016 | Koi Paper Kite | 3 | Every 3 combos → additional 1000% AoE DMG |
| 5018 | Moon Rabbit-1 | 3 | DMG RES +15%, restore 25% lost HP every 10s |
| 5021 | Blazing Motorcycle | 1 | Per 10% lost HP → flame dealing 500%+ basic ATK DMG |
| 5024 | Immortal Ascent | 1 | **Death Immunity** for 2s + recover 10% max HP (once) |
| 5026 | AdaptoSlime+ | 3 | Below 80% HP: ATK +30%; below 60%: shield 20% HP; below 30%: DMG -20% |
| 5029 | Trembling Pepe | 3 | Alternating 8s buffs: shield 16% HP OR ATK +16% + Control -40% |
| 5030 | Unrivaled Force | 3 | 60% chance each second for 20s: ATK +1.5%, DMG RES +1.5%. After 20s: 16000% AoE Skill DMG + launch |
| 5033 | Neon Shadows | 3 | 3 Guard stacks/11s (DEF +150% each), on expire deal 4000% Skill + 1600% Combo + 1600% Counter DMG |
| 5034 | Bite the Watermelon | 3 | ATK +20%, DEF +50% every 11s. Summon wave: 4000% Skill + 1600% Combo + 1600% Counter |
| 5124 | Time Pause | 1 | Per 25% HP lost: **freeze all enemies for 2s** (ignores Control Immunity) + ATK +25% |

### Mount Chapter Buffs (PvE/PvP)
Random buffs gained from mount chapters. Quality-weighted drops:

**Quality 4 (Common):**
- Restore 20% max HP instantly
- ATK +10%, DEF +20%, Evasion +5%, Crit Rate +10%, Crit DMG +15%
- Counter +15%, Combo +15%, Stun +8%, Pal DMG +10%
- Energy Regen +20%, Counter DMG Taken -30%, Combo DMG Taken -30%

**Quality 5 (Rare):**
- Base ATK +20%
- Crit Rate +20%, Crit DMG +30%
- Counter +20%, Counter DMG +30%
- Combo +20%, Combo DMG +30%
- Stun Rate +15%, Pal DMG +30%
- HP Regen Bonus +1%

**Quality 7 (Legendary):**
- Base ATK +50%
- Crit Rate +30%, Crit DMG +60%
- Counter DMG +60%, each counter restores 5% lost HP
- 50% chance to deal **2% target max HP** on basic attacks
- Stun duration +50%, stunned targets take +20% DMG
- Skill DMG +50%, each skill cast reduces active CD by 0.5s
- Instant-kill normal mobs below 10% HP
- **Invincibility + ATK +50% for 5s** when HP < 30% (once)

---

## Artifact System

### Overview
- **Source:** `Artifact.json` (44 artifacts), `Artifact_level.json` (300 levels), `Artifact_skin.json`, `Artifact_gemsets.json`, `Artifact_gemattr.json`
- All quality 8 except Frostbite Spear (quality 4)

### Artifact Level Progression (300 levels)
Same triple-attribute scaling as mounts but higher base values:

| Level | Base HP (2003) | Base ATK (2001) | Base DEF (2005) | Power |
|-------|---------------|----------------|----------------|-------|
| 1 | 70,000 | 70,000 | 70,000 | 10,000 |
| **300** | **233,740,000** | **233,740,000** | **233,740,000** | **170,660,000** |

### All Artifacts
| ID | Name |
|----|------|
| 1 | Frostbite Spear |
| 2 | Chaotic Warlord's Hammer |
| 3 | Sovereign Dragon |
| 4 | Eye of Raven |
| 5 | Luminary Lantern |
| 6 | Candy Gatling |
| 7 | Skyward Blade |
| 9 | Thousandfold Pagoda |
| 15 | Tear Attack |
| 16 | Double-edged String |
| 17 | Extreme Caution |
| 18 | Spring Chord |
| 20 | Siren's Whisper |
| 21 | Webbed Chainsaw |
| 22 | Unchained Staff |
| 24 | Castle Candelabrum |
| 27 | Countdown Blast |
| 28 | Lantern's Scroll |
| 29 | Sanguine Love |
| 31 | Flaming Carnage |
| 32 | Fate |
| 108 | Pixel Universe |
| 110 | Moment of Brilliance |
| 111 | Moonhunt Bow |
| 112 | Thousand Swords |
| 201 | Beastroar Bow |
| 204 | Cryoshield Flame |
| 401 | Storm Destroyer |
| 701-716 | Eternal Flame through Bear Bump |

### Artifact Skin Skills (Combat-Relevant)

| Skill ID | Artifact | Max Lv | Effect |
|----------|---------|--------|--------|
| 5101 | Default | 10 | Ignore Evasion +50% |
| 5102 | Chaotic Warlord | 3 | Basic attacks and combos deal +60% AoE DMG |
| 5103 | Sovereign Dragon | 3 | Summon Divine Hand every 5s, dealing 2000% basic ATK AoE DMG |
| 5104 | Eye of Raven | 1 | **Auto-cast random equipped active skill** every 20s |
| 5105 | Luminary Lantern | 1 | 1000% basic ATK AoE DMG + 1s stun every 10s |
| 5106 | Candy Gatling | 3 | Basic/combo/counter unleash 1-5 extra bullets, each 20% basic ATK DMG |
| 5107 | Skyward Blade | 1 | Every 10 attacks release sword aura: 150% basic ATK DMG |
| 5110 | Snow Sprite | 3 | Deal **10% max HP** to all targets every 10s + reduce ATK SPD/Energy Regen/Pal SPD by 40% for 3s |
| 5112 | Tear Attack | 1 | Summon Pepe (20% your HP) every 12s, explodes for 1000% basic ATK DMG |
| 5113 | Spring Chord | 3 | 2000% AoE DMG every 11s + **confuse targets** (their own attacks deal 30% to themselves for 5s) |
| 5114 | Acoustic Rupture | 3 | Enhanced basic ATK: +200% AoE. Soundwave crescendo: 300%/300%/800% DMG at thresholds |
| 5115 | Safe Distance | 3 | 50% chance to deal **0.8% target max HP** + 10% chance to wound (reduce regen/healing by 50%) |
| 5117 | Abyssal Beast | 1 | Summon beast (Control Immune, 16% your HP) every 14s, 40% DMG for 5s |
| 5118 | Duck Swirl | 1 | 15% chance per basic ATK: 20% DMG/s DoT + DEF -6% per stack (cap 8 stacks = -48% DEF) |
| 5120 | Piercing Squail | 3 | +30% Crit Rate. Each crit → +2% Final Crit DMG (cap 20 stacks = +40%). At max: 10% chance for 1500% AoE Skill DMG |
| 5121-5123 | Invincible Torch | 1-3 | Summon Torch Bearer 2-3s. After disappear: +5-10% Final Crit DMG, Skill Crit DMG, Pal Crit DMG. Summons more at 2-3s intervals with increasing bonuses up to +20% |
| 5124 | Time Pause | 1 | Per 25% max HP lost: **freeze ALL enemies 2s** (ignores Control Immunity) + ATK +25% |

### Artifact Gem System
6 gem slots per artifact. Gems have quality 3-8, levels 1-20.

**Gem Attributes (per slot):**
- Slot 1: HP (1002) — 3,645 per level
- Slot 2: ATK (1001) — 160 per level
- Slot 3: DEF (1024) — 55 per level
- Slot 4: Random from Basic ATK DMG (2022), Combo DMG (2017), Counter DMG (2018), Skill DMG (2033), Pal DMG (2020)
- Additional random attributes vary by gem quality

### Artifact Gem Set Bonuses (7 Sets)

| Set ID | Name | 2-Piece Bonus | 4-Piece Bonus |
|--------|------|---------------|---------------|
| 101 | Heart of Resilience | Global Counter DMG (2031) +500 | Global Counter DMG +1,000 |
| 102 | Furious Gale | Global Combo DMG (2030) +500 | Global Combo DMG +1,000 |
| 103 | Mana Mastery | Global Basic ATK DMG (2023) +500 | Global Basic ATK DMG +1,000 |
| 104 | Blazing Roar | Global Crit DMG (2009) +500 | Global Crit DMG +1,000 |
| 105 | Iron Wall | Global Crit RES (2011) +500 | Global Crit RES +1,000 |
| 106 | Elemental Wrath | Global Skill DMG (2033) +500 | Global Skill DMG +1,000 |
| 107 | Common Foe | Pal DMG Bonus (2020) +500 | Pal DMG Bonus +1,000 |

**PvP Gem Set Recommendations by Class:**
- **Warbringer:** Heart of Resilience (Counter DMG)
- **Plume Monarch:** Furious Gale (Combo DMG)
- **Sacred Hunter/Plume Monarch:** Mana Mastery (Basic ATK DMG)
- **Darklord:** Elemental Wrath (Skill DMG)
- **Beastmaster/Supreme Spirit:** Common Foe (Pal DMG)
- **All classes:** Blazing Roar (Crit DMG) is universally strong
- **Defensive:** Iron Wall (Crit RES) to survive burst

---

## Pet/Pal System

### Overview
- **Source:** `Pet.json` (322 pets), `Petrace.json` (55 races), `Pet_talent.json`, `Pet_proficiency.json`, `Petlevel.json`
- Pals inherit player's ATK, apply their own damage multiplier (partner_dam, attr 1040)
- Player's partner_dam_extra (1047) scales all pal damage additionally

### Pet Races (55 Total)
| ID | Race | ID | Race | ID | Race |
|----|------|----|------|----|------|
| 1 | Cat | 2 | Specter | 3 | Snow Sprite |
| 4 | Cactus | 5 | Chicken | 6 | Sprite |
| 7 | Panda | 8 | Snail | 9 | Deer |
| 10 | Turtle | 11 | Octopus | 12 | Dog |
| 13 | Lizard | 14 | Dragon | 15 | Fox |
| 16 | Banana | 17 | Toothpaste | 18 | Mecha Dragon |
| 19 | Bear | 20 | Pig | 21 | Mouse |
| 22 | Bird | 23 | Eggplant | 24 | Rabbit |
| 25 | Alpaca | 26 | Snake | 1003 | Pepe |
| 1004 | Spritefox | 1005 | Hellflame Feather | 1008 | Puppy Fervor |
| 1080 | Skeleton Minion | 1081 | Camel | 1082 | Blackeye |
| 1098 | Vermillion Bird | 1099 | B.Duck | 3001-3005 | Named Pals |

### Pet Quality Distribution
| Quality | Count | Power Range | Notes |
|---------|-------|-------------|-------|
| 3 (Blue) | ~50 | 5,500 | Common |
| 4 (Purple) | ~50 | 6,000 | Uncommon |
| 5 (Gold) | ~50 | 7,000 | Rare |
| 6 (Orange) | ~60 | 8,000 | Epic |
| 7 (Red) | ~60 | 9,000 | Legendary |
| 8 (Pink) | ~50 | 9,500 | Mythic |

### Pet Talent System
Each pet has talent slots: `[[talent_group, talent_tier], ...]`
- talent_group determines which talent tree
- talent_tier determines max talent level available

### PvP Pal Mechanics
- **Pal DMG Resistance (1020):** Caps at **80%** — you cannot fully negate pal damage
- **Pal Inspire (1074):** Bonus damage from pals (like Pierce for pal attacks)
- **Pal Suppress (1077):** Counter to Pal Inspire
- **Pal DMG Multiplier (1040):** Base pal damage scaling
- **Pal DMG Extra (1047):** Additional multiplicative pal scaling

---

## Spirit System

### Overview
- **Source:** `Spirit.json` (20 spirits), `Spirit_level.json`, `Spirit_affix_group.json`, `Spirit_attrbonus_affix.json`, `Spirit_attrbonus_slot.json`
- Spirits fight other spirits in a parallel combat layer
- Spirit damage comes from weighted sum of parent's attack types

### All Spirits
| ID | Name | Quality | Base ATK (6005) | Base HP (6004) |
|----|------|---------|----------------|----------------|
| 101 | Brawl Hound | 1 | 300 | 15,000 |
| 102 | Magic Kitten | 1 | 800 | 12,000 |
| 103 | Hunter Hare | 1 | 1,600 | 8,000 |
| 104 | Deer Spirit | 1 | 500 | 10,000 |
| 201 | Minotaur | 2 | 360 | 18,000 |
| 202 | Occult Mentor | 2 | 960 | 14,400 |
| 203 | Fate Hunter | 2 | 1,920 | 9,600 |
| 204 | Commander | 2 | 600 | 12,000 |
| 301 | Combat Expert | 3 | 420 | 21,000 |
| 302 | Curse Priest | 3 | 1,120 | 16,800 |
| 303 | Bounty Hunter | 3 | 2,240 | 11,200 |
| 304 | Beast Master | 3 | 700 | 14,000 |
| 401 | Mech Master | 4 | 480 | 24,000 |
| 402 | Crazy Raider | 4 | 1,280 | 19,200 |
| 403 | Domain Hunter | 4 | 2,560 | 12,800 |
| 404 | Death Reaper | 4 | 800 | 16,000 |
| 501 | Flame Spirit | 5 | 540 | 27,000 |
| 502 | Tide Spirit | 5 | 1,440 | 21,600 |
| 503 | Zephyr Spirit | 5 | 2,880 | 14,400 |
| 504 | Litho Spirit | 5 | 900 | 18,000 |

### Spirit Damage Weights (att_dam)
Each spirit has weighted damage contributions from the parent player's attack types:

| Type ID | Attack Type | Typical Weight |
|---------|-------------|---------------|
| 1 | Normal ATK | 5,000-16,000 |
| 2 | Combo | 5,000-16,000 |
| 3 | Counter | **25,000-80,000** (always highest) |
| 4 | Skill | 5,000-16,000 |

**Key Insight:** Spirits always weight counter damage highest (5× other types), making counter-focused classes (Warbringer, Martial Sage) have the strongest spirits.

### Spirit vs Spirit Combat
```
Damage = ATT × (spirit_dam_add - spirit_dam_def + 1) × (1 - spirit_dam_def_final)
```
Where:
- ATT = spirit's attack value (6005 + bonuses)
- spirit_dam_add (6001) = attacker's spirit damage bonus
- spirit_dam_def (6002) = defender's spirit damage resistance
- spirit_dam_def_final (6003) = defender's final spirit resistance (percentage)

### Spirit Affix System
- 4 affix groups: Basic, group 2 (1000596), group 3 (1000597), group 4 (1000598)
- 22 affix slots available
- 168 possible affixes across groups
- Affixes provide: Global ATK % (2002), Crit Rate (1004), and other combat attributes
- Affix quality determines value ranges (e.g., quality 1: ATK% 50-65)

---

## Back Decoration System (Wings/Accessories)

### Overview
- **Source:** `Back_decoration.json` (48 items), `Back_level.json` (780 entries), `Back_skin.json` (495 entries), `Back_talent.json` (2,652 entries)
- All quality 7 (Red) except 3 starter items at quality 4
- Each back decoration has skin levels with skill unlocks

### Back Level Progression (260 levels)
Back items have 3 separate stat tracks:

| Track | Attribute | Max Value (Lv 260) | Power |
|-------|-----------|-------------------|-------|
| 1001 | Base ATK | 52,919,000 | 20,103,333 |
| 1002 | Base HP | 52,919,000 | 20,103,333 |
| 1003 | Base DEF | 52,919,000 | 20,103,333 |

### Notable Back Decorations
| ID | Name | Notes |
|----|------|-------|
| 70001-70003 | Raccoon/Wolf/Fox Tail | Starter (quality 4) |
| 70004 | Lustrous Plumage | — |
| 70020 | Fallen Angel | — |
| 70025 | Celestial Gemini | — |
| 70405 | Dawn Warwing | — |
| 70907 | Lord of Light | — |
| 70999 | Frostland Specter | — |

### Back Talent System
- 2,652 talent entries across multiple class types (job_type)
- Each talent has: name, icon, description, cost, connect_id (prerequisite chain)
- Talents are color-coded (color_type) and class-specific

---

## Badge System

### Overview
- **Source:** `Badge.json` (25 entries)
- Single badge: **Lightkeeper** (ID 9001), 25 levels
- Grants **Global Basic ATK DMG (2023)** at increasing values

### Badge Level Progression
| Level | Global Basic ATK DMG (2023) |
|-------|-----------------------------|
| 1 | 400 |
| 5 | 1,800 |
| 10 | 3,500 |
| 15 | 5,200 |
| 20 | 6,900 |
| **25** | **8,600** |

---

## Title System

### Overview
- **Source:** `Title.json` (120 entries)
- Titles are cosmetic with gradient color effects
- No direct stat bonuses from titles (stats come from title acquisition achievements)

### Notable Titles
| ID | Name |
|----|------|
| 1 | Best of the Best |
| 2 | Supreme Sage |
| 3 | Peak Conqueror |
| 4 | Peerless Prodigy |
| 5 | Rising Star |

---

## Cross-System Stat Sources Summary

### Final DMG Bonus (1081) Sources
| Source | Max Value |
|--------|-----------|
| Equipment Resonance Stage 18 | **+3,800** |
| Other sources (buffs, skills) | Varies |

### Final DMG RES (1082) Sources
| Source | Max Value |
|--------|-----------|
| Equipment Resonance Stage 18 | **+3,800** |
| Other sources (buffs, skills) | Varies |

### Base Stat Sources (ATK/HP/DEF)
| System | Max Per Attribute | Notes |
|--------|------------------|-------|
| Mount Level 300 | 104,837,000 | Triple attribute (2001/2003/2005) |
| Artifact Level 300 | 233,740,000 | Triple attribute (2001/2003/2005) |
| Back Level 260 | 52,919,000 | Single attribute per track |
| Equipment Refinement ×10 | 128,000 total | ATK+HP+DEF per slot |
| Equipment Advancement | Battle attrs only | Pierce/Block/Inspire/Suppress |

### Equipment Advancement Battle Attributes (Stage 36 max)
| Attribute | Value |
|-----------|-------|
| Pierce (1068) | 6,240 |
| Ignore Pierce (1069) | 6,240 |
| Block (1071) | 6,240 |
| Ignore Block (1072) | 6,240 |
| Pal Inspire (1074) | 6,240 |
| Ignore Inspire (1075) | 6,240 |
| Pal Suppress (1077) | 6,240 |
| Ignore Suppress (1078) | 6,240 |
