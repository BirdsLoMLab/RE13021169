# 21 — Star Heroes

> Complete Star Heroes reference: all 33 heroes from LOM_Database-5.xlsx. 27 implemented, 6 not yet. See also `star_heroes_master.json` for structured JSON.

---

## Quick Reference — All 33 Star Heroes

| # | Name | Rarity | Cost | Main Type | Support Type | Limited | Impl |
|---|------|--------|------|-----------|-------------|---------|------|
| 1 | **Divine Warbringer** | SSR | 4 | Active | Active | — | Yes |
| 2 | **Storm Dominion** | SSR | 4 | Active | Active | — | Yes |
| 3 | **Barbarian Overlord** | SSR | 4 | Active | Active | — | Yes |
| 4 | **Holy Defender** | SSR | 4 | Active | Active | — | Yes |
| 5 | **Genie of Wishes** | SSR | 3 | Passive | None | — | Yes |
| 6 | **Lord of Champions** | SSR | 4 | Active | Active | Yes | Yes |
| 7 | **Spirit Harbinger** | SR | 3 | Active | Active | — | Yes |
| 8 | **Mentor of Wisdom** | SR | 3 | Passive | Passive | — | Yes |
| 9 | **Chrono Sprite** | SR | — | None | Active | — | Yes |
| 10 | **Knight of Light** | SR | 3 | Shield | Shield | — | Yes |
| 11 | **Beast Soul Guardian** | SR | 3 | Passive | Passive | — | Yes |
| 12 | **Void Guide** | SR | 3 | Active | Active | — | Yes |
| 13 | **Defender of Order** | SR | 3 | Shield | Shield | — | Yes |
| 14 | **Biosphere Guardian** | SR | 3 | Passive | Passive | — | Yes |
| 15 | **Nature's Keeper** | SR | 3 | Passive | Passive | — | Yes |
| 16 | **Goddess of Victory** | SR | 3 | None | Shield | Yes | Yes |
| 17 | **Sprite of Knowledge** | R | 2 | Active | Passive | — | Yes |
| 18 | **Intrepid Fowl** | R | 2 | Active | Shield | — | Yes |
| 19 | **Jolly Greenhorn** | R | 2 | Active | Active | — | Yes |
| 20 | **Vanguard Urchin** | R | 2 | Passive | Passive | — | Yes |
| 21 | **Faithful Guardian** | R | — | None | Passive | — | Yes |
| 22 | **Blossom Harbinger** | R | — | None | Passive | — | Yes |
| 23 | **Harvest Harbinger** | R | — | None | Passive | — | Yes |
| 24 | **Dome Watcher** | R | 2 | Passive | Shield | — | Yes |
| 25 | **Valiant Soulknight** | R | 2 | Passive | Passive | — | Yes |
| 26 | **Stoneborn Warrior** | R | 2 | Shield | Active | — | Yes |
| 27 | **Shadow Keeper** | R | 2 | Active | Shield | — | Yes |
| 28 | **Puppy Squad** | SSR | 4 | Active | Active | Yes | No |
| 29 | **Sakura Star Envoy** | SR | 3 | Shield | None | Yes | No |
| 30 | **King** | SSR | 4 | Active | Passive | Yes | No |
| 31 | **Hellish Blizzard** | SR | 3 | Active | Active | Yes | No |
| 32 | **Gold Snow Roll** | SSR | 4 | Active | Shield | Yes | No |
| 33 | **Leaf Fox** | SR | 3 | Shield | Shield | Yes | No |

---

## Full Details

### 1. Divine Warbringer

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Every 15s after the battle starts, deals AoE DMG equal to 5% of Max HP.

**Support Skill [Active]:** Releasing the main active skill increases DMG RES by 4% for 5s.

---

### 2. Storm Dominion

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Every 16s after the battle starts, deals 500% of current AoE Basic ATK DMG (can be Crit), and every Crit hit within 5s deals extra DMG equal to 0.4% of targets' current HP.

**Support Skill [Active]:** Releasing the main active skill reduces Basic ATK DMG RES by 6% for 5s.

---

### 3. Barbarian Overlord

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Every 16s after the battle starts, 3 random Pals gain 8% of Combo Multiplier and 8% of Final Crit DMG for 5s.

**Support Skill [Active]:** Releasing the main active skill reduces targets' ATK by 8% for 5s.

---

### 4. Holy Defender

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Every 14s after the battle starts, deals 1500% of AoE Skill DMG, and targets take 400% of Bleed Skill DMG per second for 5s, ignoring immunity.

**Support Skill [Active]:** Releasing the main active skill reduces targets' DMG RES by 5% for 5s.

---

### 5. Genie of Wishes

**Rarity:** SSR | **Cost:** 3

**Main Skill [Passive]:** After the battle starts, gains 4% of ATK and 12% of DEF until the battle ends.

**Support Skill [None]:** No Support Effect

---

### 6. Lord of Champions (Limited)

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** After the battle starts, summon a thunderstorm every 15s, dealing 1500% of Bleed Skill DMG and stunning the target for 1.5s, ignoring immunity.

**Support Skill [Active]:** Releasing the main active skill shortens the CD of Active Skills on cooldown by 1s and increases Final Skill DMG by 12% for 5s.

---

### 7. Spirit Harbinger

**Rarity:** SR | **Cost:** 3

**Main Skill [Active]:** Every 16s after the battle starts, all Pals gain 4% of Crit Rate and 200% of Base Crit DMG for 8s.

**Support Skill [Active]:** Releasing the main active skill grants all Pals 4% of Combo Rate for 7s.

---

### 8. Mentor of Wisdom

**Rarity:** SR | **Cost:** 3

**Main Skill [Passive]:** After the battle starts, releasing 10 active skills deals 3200% of AoE Skill DMG and increases Final Skill Crit DMG by 7.5% for 12s (triggered only once).

**Support Skill [Passive]:** Releasing the main passive skill increases Skill Crit Rate by 2.5% and Base Skill Crit DMG by 15% until the battle ends.

---

### 9. Chrono Sprite

**Rarity:** SR | **Cost:** —

**Main Skill [None]:** No Main Effect

**Support Skill [Active]:** Releasing the main active skill stuns targets for 0.5.

---

### 10. Knight of Light

**Rarity:** SR | **Cost:** 3

**Main Skill [Shield]:** Every 16s after the battle starts, gains a shield that absorbs 8% of Max HP for 5s. When taking Basic ATK DMG, the shield reduces ATK by 5% for 2s for targets within the range.

**Support Skill [Shield]:** Releasing the main shield skill regenerates 7.5% of lost HP.

---

### 11. Beast Soul Guardian

**Rarity:** SR | **Cost:** 3

**Main Skill [Passive]:** After the battle starts, all Pals gain 20% of ATK SPD, which reduces by 1/5 every 4s.

**Support Skill [Passive]:** When HP drops below 50% for the first time, releasing the main passive skill grants all Pals 8% of ATK SPD for 12s.

---

### 12. Void Guide

**Rarity:** SR | **Cost:** 3

**Main Skill [Active]:** Every 16s after the battle starts, deals 1800% of AoE Skill DMG and stuns targets for 0.5s.

**Support Skill [Active]:** Releasing the main active skill reduces targets' Base Energy Regen SPD by 8% for 5s.

---

### 13. Defender of Order

**Rarity:** SR | **Cost:** 3

**Main Skill [Shield]:** Every 14s after the battle starts, gains a shield that absorbs 8% of Max HP for 5s, during which every Basic ATK deals an additional 8% of current AoE Counter DMG (can be Crit).

**Support Skill [Shield]:** Releasing the main shield skill increases ATK by 6% for 5s.

---

### 14. Biosphere Guardian

**Rarity:** SR | **Cost:** 3

**Main Skill [Passive]:** After the battle starts, gains 20% of ATK SPD, which reduces by 1/5 every 4s.

**Support Skill [Passive]:** When HP drops below 50% for the first time, releasing the main passive skill grants 8% of ATK SPD for 12s.

---

### 15. Nature's Keeper

**Rarity:** SR | **Cost:** 3

**Main Skill [Passive]:** After the battle starts, every Crit hit has a 5% chance to reduce ATK by 5% for 3s targets within the range.

**Support Skill [Passive]:** Releasing the main passive skill increases Crit Rate by 5%.

---

### 16. Goddess of Victory (Limited)

**Rarity:** SR | **Cost:** 3

**Main Skill [None]:** No Main Effect

**Support Skill [Shield]:** Releasing the main shield skill increases ATK SPD by 10% and adds 50% of Counter DMG to Basic ATK for 5s.

---

### 17. Sprite of Knowledge

**Rarity:** R | **Cost:** 2

**Main Skill [Active]:** Every 14s after the battle starts, targets within the range take 250% of Skill DMG per second for 5s.

**Support Skill [Passive]:** Releasing the main passive skill increases Stun Rate by 3% until the battle ends.

---

### 18. Intrepid Fowl

**Rarity:** R | **Cost:** 2

**Main Skill [Active]:** Every 15s after the battle starts, deals 500% of current AoE Basic ATK DMG (can be Crit).

**Support Skill [Shield]:** Releasing the main shield skill increases Crit Rate by 4% and Base Crit DMG by 50% for 5s.

---

### 19. Jolly Greenhorn

**Rarity:** R | **Cost:** 2

**Main Skill [Active]:** Every 15s after the battle starts, deals 500% of current AoE Combo DMG (can be Crit).

**Support Skill [Active]:** Releasing the main active skill increases ATK SPD by 5% for 5s.

---

### 20. Vanguard Urchin

**Rarity:** R | **Cost:** 2

**Main Skill [Passive]:** After the battle starts, every Basic ATK deals an additional 15% of current Single-target Counter DMG.

**Support Skill [Passive]:** Releasing the main passive skill increases Base Counter DMG by 100% until the battle ends.

---

### 21. Faithful Guardian

**Rarity:** R | **Cost:** —

**Main Skill [None]:** No Main Effect

**Support Skill [Passive]:** Releasing the main passive skill increases DMG to bosses by 8% until the battle ends.

---

### 22. Blossom Harbinger

**Rarity:** R | **Cost:** —

**Main Skill [None]:** No Main Effect

**Support Skill [Passive]:** Releasing the main passive skill increases Final DEF by 8% until the battle ends.

---

### 23. Harvest Harbinger

**Rarity:** R | **Cost:** —

**Main Skill [None]:** No Main Effect

**Support Skill [Passive]:** Releasing the main passive skill increases Boss DMG RES by 4% until the battle ends.

---

### 24. Dome Watcher

**Rarity:** R | **Cost:** 2

**Main Skill [Passive]:** After the battle starts, all Pals gain 12% of Ignore Evasion.

**Support Skill [Shield]:** Releasing the main shield skill increases Base Pal DMG by 30% for 3s.

---

### 25. Valiant Soulknight

**Rarity:** R | **Cost:** 2

**Main Skill [Passive]:** After the battle starts, all Pals gain 50% of Base Crit DMG.

**Support Skill [Passive]:** Releasing the main passive skill grants all Pals 2.5% of Crit Rate until the battle ends.

---

### 26. Stoneborn Warrior

**Rarity:** R | **Cost:** 2

**Main Skill [Shield]:** Every 14s after the battle starts, gains a shield that absorbs 8% of Max HP for 5s.

**Support Skill [Active]:** Releasing the main active skill grants an extra shield that absorbs 5% of Max HP for 5s.

---

### 27. Shadow Keeper

**Rarity:** R | **Cost:** 2

**Main Skill [Active]:** Every 14s after the battle starts, deals 1400% of AoE Skill DMG.

**Support Skill [Shield]:** Releasing the main shield skill increases Base Skill DMG by 30% for 5s.

---

### 28. Puppy Squad (Limited) — No

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Every 15s after the battle starts, all pals release a phantom hound on their next basic attack, dealing 200% of their Pal DMG (can basic attack) and inflicting Bleed DMG equal to 0.65% of the target's Max HP (ignores DMG Immunity).

**Support Skill [Active]:** Releasing the main active skill reduces target's Pal DMG RES by 6% for 5s.

---

### 29. Sakura Star Envoy (Limited) — No

**Rarity:** SR | **Cost:** 3

**Main Skill [Shield]:** Every 14s after the battle starts, gain a shield that absorbs 8% of Max HP for 5s. ATK increases by 7.5% while the shield persists.

**Support Skill [None]:** No Support Effect

---

### 30. King (Limited) — No

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Every 15s after the battle starts, all enemies lose 13.5% ATK and 27% DEF for 5s (cannot be cleansed).

**Support Skill [Passive]:** Releasing the main passive skill reduces all enemies' ATK by 3.6% until the battle ends.

---

### 31. Hellish Blizzard (Limited) — No

**Rarity:** SR | **Cost:** 3

**Main Skill [Active]:** After the battle starts, casts a whirlwind every 15s, lasting 5s, dealing 450% Skill Bleed DMG per sec to all enemies (ignores DMG Immunity) and reducing their DMG RES by 2.25% for 2s. (Does not stack; duration refreshes on re-trigger.)

**Support Skill [Active]:** After casting the main active skill, deals 900% Skill DMG to all enemies and reduces their Ignore Evasion. Crit Rate, Pal Ignore Evasion, and Pal Crit Rate by 3% for 5s (cannot be cleansed).

---

### 32. Gold Snow Roll (Limited) — No

**Rarity:** SSR | **Cost:** 4

**Main Skill [Active]:** Launch a snowball every 15s after the battle starts, dealing 900% Skill DMG, 180% current Basic ATK DMG (can be Crit), 180% current Combo DMG (can be Crit), and 180% current Counter DMG (can be Crit) to all enemies, and reduce their DMG RES by 0.9% until the battle ends, stacking up to 5 times.

**Support Skill [Shield]:** Releasing the main shield skill increases Final Basic ATK DMG, Final Combo DMG, and Final Counter DMG by an additional 3% until the battle ends, stacking up to 4 times.

---

### 33. Leaf Fox (Limited) — No

**Rarity:** SR | **Cost:** 3

**Main Skill [Shield]:** Every 14s after the battle starts, gains a shield that absorbs 9% of Max HP and ignores any new control effects received. (This doesn't affect existing control.)

**Support Skill [Shield]:** Releasing the main shield skill increases Evasion by an additional 18% for 5s.

---

## Data Files

- **Source spreadsheet**: `battlesim/reference/LOM_Database-5.xlsx`
- **Structured data**: `battlesim/reference/star_heroes_master.json`