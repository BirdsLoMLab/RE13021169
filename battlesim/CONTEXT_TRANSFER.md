# LOM Battlesim — Session Context Transfer

## Project
PvP battle simulator for **Legend of Mushroom** (LOM). Single-file app at `battlesim/index.html` (~2250 lines, ~125K JS). Reference bible at `battlesim/reference/` (21 files, 00-20). Branch: `claude/investigate-session-freeze-T5xpG`.

## Architecture: index.html Modules

| Module | Lines (approx) | Purpose |
|--------|----------------|---------|
| 1: FixMath | early | `FM.round(x)` = 4-decimal round, `FM.roundInt(x)` = integer round, `FM.clamp` |
| 2: FixRandom | after FM | LCG PRNG: `(9301 * seed + 49297) % 233280`, deterministic combat |
| 3: Constants | after PRNG | `PVP_INJURY_TABLE` (220 entries), `HealthType` enum, `BG` buff group IDs, `ATTRIB_CAPS` |
| 4: Game Data | large block | `CLASS_TREE`, `T5_CLASS_PASSIVES` (8 classes), `SKILLS_DATA` (38 skills), `PALS_DATA` (90 pals), `GUARDIAN_SPIRITS` (8), `STAR_HEROES_DATA` (23), `MOUNT_DATA`, `ARTIFACT_DATA`, `BACK_DATA`, `AVIAN_DATA` |
| 5: Unit | class | Attribute storage (get/set/modify), buff list mgmt, tick method |
| 6: Buffs | classes | 13 buff types: Attrib, Shield, Dizz, Invincible, ImmuneDeath, NotControlled, ReduceHeal, ExtraDamage, GiantSlayer, FragileEffect, RecordDamage, SkillDamageAdd, DeferDamage |
| 7: DamageEngine | static | All combat math: hit/miss, double/counter act, pierce/block, inspire/suppress, calHurt, crit, normalHurt, skillHurt, hpsteal |
| 8: CombatLog | class | Per-tick event recording |
| 9: CombatEngine | class | Main loop: healthTarget, processDamageQueue, executeAttack, executeSkill, executePalAttack, tick |
| 10: BattleMain | class | Orchestrator: createPals, runToCompletion, runWithLog |
| 11: UI Controller | functions | buildPanel, getStats, onPalChange, onSpiritChange, runSim |
| 12: Self-Test | IIFE | Validates FM, PRNG, data integrity on load |

## Critical Formulas

### Damage Pipeline (11 steps)
1. **Base DMG** = `roundInt(ATK - DEF * (1 + def_coe))`, min 1
2. **Type multiplier** (normal=1.0, double_hit=skill_factor, counter=counter_dam, skill=skill%)
3. **Resistance** — Pierce/Block (random roll, ±0.5 cap) OR Inspire/Suppress (pal attacks)
4. **calHurt** = `1 + total_dam_add - total_dam_def`, floor 0.20
5. **Crit** = `max(1.5, crit_dam / max(0.5, crit_def))`
6. **Buff modifiers** (ExtraDamage, GiantSlayer, FragileEffect, SkillDamageAdd, DeferDamage)
7. **Total DMG multiplier** = `1 + total_dam_add - total_dam_def`, floor 0.20
8. **PvP division** = `damage / PVP_INJURY_TABLE[level]` (lv220 = 754.0)
9. **Absorption** (shields)
10. **HP reduction** (actual HP change)
11. **Death prevention** (ImmuneDeath buffs)

### Key Constants
- PvP shield_correct = 0.40, hp_recovery_correct = 0.30
- Miss curve: `pow(100 * raw_miss, 0.9) / 100`, PvP cap 80%
- Stun (vertigo): same 0.9 exponent
- Hidden 0.98 exponent on skill crit: `Math.pow(damage, 0.98)` — 5-13% silent reduction
- Total damage floor: 0.20x minimum multiplier
- Skill resist uses `double_hit_def` (1034) as attrib key (engine quirk, preserved)

### Pal Damage
```
rawDmg = max(roundInt(PARENT_ATK - DEF * (1 + def_coe)), 1) * round(PARTNER_DAM * PARTNER_DAM_EXTRA)
finalDmg = rawDmg * round(1 - (PARTNER_RESIST ± inspire/suppress))
```
Pal double_hit does NOT apply combo resistance (double_hit_def).

### Spirit Damage
- **vs Spirit**: `round(ATT * (spirit_dam_add - spirit_dam_def + 1) * (1 - spirit_dam_def_final))`
- **vs Normal**: Parent's normalHurt/doubleHurt/counterHurt/skillHurt scaled by att_dam weights. Counter weight always 5x highest.

### Crit Formula
`max(1.5, crit_dam / max(0.5, crit_def))` — both are raw values (e.g., 10000/5000 = 2.0x)

## Game Systems → Reference Files

| System | Ref File | Status in Engine |
|--------|----------|-----------------|
| Damage formulas | 01 | Implemented |
| PvP constants | 02 | Implemented |
| Attributes (89+) | 03 | Implemented (IDs 1001-1082, 2001-2033, 6001-6007) |
| 8 T5 Classes | 04 | Implemented (all passives + actives) |
| 38 Active Skills | 05 | Implemented |
| 90 Pals | 06 | Stat toggles implemented; **battle effects NOT implemented** |
| Avians | 07 | Data present; **battle effects NOT implemented** |
| Talents | 08 | Implemented |
| Relics | 09 | Implemented |
| Buffs (46 types) | 10 | 13 buff classes implemented; **some types missing** |
| Mount Skins | 11 | Data present; passive stats only |
| Artifact Skins | 12 | Data present; passive stats only |
| Equipment | 13 | Via stat inputs |
| Guardian Spirits | 14 | UI selection + Tenacity/TPEN; **spirit combat unit NOT spawned** |
| Star Heroes | 15 | UI selection; **battle skills NOT implemented** |
| Fate Cards | 16 | NOT implemented |
| Path to Divinity | 17 | NOT implemented |
| Rings & Badges | 18 | NOT implemented |
| Back Decorations | 19 | Data present; passive stats only |
| Special Mechanics | 20 | Partial (0.98 exp done, clones/speed cascade NOT) |

## Known Gaps (Priority Order)

### Critical
1. **Pal battle effects** — Electric Pup HP regen on counter, Hydrosprite CDR, etc. `battleDesc` field exists in PALS_DATA but effects not wired into CombatEngine
2. **Star Hero battle skills** — skill1/skill2 from ConfigAngel_star, energy cost system, formation slots
3. **Spirit combat unit** — Should spawn as actual Unit in battle with own HP/ATK/skills per ConfigSpirit_level
4. **Skill energy system** — Skills should cost energy, energy generates per attack; currently all skills fire on CD
5. **Unhandled skill effects** — Execute (kill below HP%), bleed DOT, clone spawning, scaling damage, disarm

### Moderate
6. Death prevention chain (multiple ImmuneDeath buffs, priority ordering)
7. Bleed/DOT tick system
8. Freeze/bind/taunt CC beyond stun
9. Damage sharing/reflection buffs
10. Launch mechanic (airborne + fall damage)
11. Artifact/back/avian active combat skills
12. Angel development slot passive effects

### Minor
13. Equipment suit set bonuses (via stat inputs currently)
14. Fate card passive skills from fusion
15. Path to Divinity affix caps
16. Ring base_skill combat effects
17. Badge Global Basic ATK DMG scaling
18. Back talent tree class-specific skills
19. Pet proficiency/talent stat bonuses

## Design Decisions & Quirks
- **Single HTML file** — entire app in one file, no build step, no dependencies
- **HIDDEN_ATTRIB_DEFAULTS** — attributes removed from UI but kept in engine (def_coe=0, skill_factor=10000, etc.)
- **Per-slot pal toggles** — each pal slot gets its own stat toggle checkboxes based on selected pal's `statToggles` array. `battleDesc` shown as info text but not mechanically wired
- **Guardian Spirits** split from Star Heroes — Spirits are ConfigSpirit (ref 14), Heroes are ConfigAngel (ref 15). Completely separate game systems
- **CDR** only via Hydrosprite pal or CDR on Stun talent, not a direct stat input
- **Mount/back/artifact passives** (like "+10% globals") are already reflected in stat inputs — don't double-apply
- **30 FPS frame loop** — all timers in frames. Attack speed → frames between attacks. Skill CDs in frames
- **5 buff mutex types**: 1=replace existing, 2=block if exists, 3=cap max count, 5=refresh duration
- **XOR-encoded config data** in game_script.js uses key `24455` for unit configs (77 fields)
- **ConfigFly** is the avian table (NOT ConfigBird — no ConfigBird exists)
- **Inspire/Suppress** rate names are swapped in game code (quirk preserved in engine)

## Reference File Quick Guide
- `battlesim/reference/00_INDEX.md` — master index of all 21 reference docs
- Each ref file (01-20) is self-contained with formulas, tables, config schemas, and source line references
- JSON data files in `battlesim/reference/`: `pals_master.json` (90 pals), `skills_master.json` (38 skills), `star_heroes_master.json` (23 heroes), `mounts_master.json`, `artifacts_master.json`, `avians_master.json`, `back_accessories_master.json`

## User Preferences
- Credit: "Bird → Discord @birrrd08"
- Prefers practical over theoretical — show working mechanics, not just docs
- Wants split between "stat effects" (toggleable) and "battle effects" (auto-applied) for pals
- Values accuracy over completeness — better to implement fewer systems correctly than many poorly
- Don't double-apply passives that are already in stat inputs
