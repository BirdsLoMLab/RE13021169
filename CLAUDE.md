# LOM Battle Simulator — Project Context

## What This Is
Reverse-engineering project for **Legend of Mushroom** (LOM) PvP battle mechanics. Single-file HTML battle simulators + 44 deep-dive docs + extracted game data.

## Key Files — READ THIS FIRST

| File | What it is | Edit? |
|------|-----------|-------|
| `uploads/battlesimV1.html` | **V1 simulator** (Alpha 6.0, 5252 lines). The standalone version the user actively develops. | YES |
| `battlesim/index.html` | Dark-themed rewrite (2396 lines). Newer architecture. | YES |
| `battlesim/battlesim_old_ref-only.html` | Archived old version for reference only. | **NO** |
| `battlesim/CONTEXT_TRANSFER.md` | Detailed engine architecture, formulas, known gaps. **Read this for technical context.** | Update as needed |

**When the user says "the battle sim" or "battlesim" without qualification, ask which one they mean.**

## Reference Materials
- `battlesim/reference/` — 21 markdown docs (00-20) + 8 JSON master files covering all game systems
- `battlesim/reference/00_INDEX.md` — master index
- Key JSON: `pals_master.json` (90 pals), `skills_master.json` (38 skills), `star_heroes_master.json` (23 heroes)

## Reverse Engineering Docs
- `reverse-engineered/` — 44 deep-dive markdown files on game mechanics
- `reverse-engineered/00_SECTION_MAP.md` — master navigation

## Game Source Code
- `game_script.js` (18MB) — original minified game code
- `game_script_pretty.js` (24MB) — prettified for analysis
- XOR config key: `24455` (77-field unit configs)

## Data & Tools
- `data/constants/` — battle_constants.json, pvp_constants.json, attribute_caps.json
- `data/tables/` — large config tables (.gitignored)
- Python utilities at repo root: `decode_config_data.py`, `extract_constants.py`, `extract_enums.py`, etc.
- `fetch_live_assets.py` — mirrors the live web client (scripts, config tables, bundles) from https://lom.joynetgame.com/ by walking the Cocos bootstrap chain (index.html → settings.json → bundle config.json). Output goes to `uploads/live_YYYYMMDD/`, then run `decode_config_data.py` on it. **Must be run from a machine with open internet** — the remote Claude sandbox egress policy blocks joynetgame.com hosts.
- `lom.joynetgame.com.zip` + `uploads/bundle-firstload-res.zip` — site capture from 2026-02-28 (hot-update manifest inside bundle-LoadingView reports client 1.0.762).

## User Preferences
- Credit: "Bird → Discord @birrrd08"
- **Accuracy over completeness** — fewer systems implemented correctly > many done poorly
- **Practical over theoretical** — show working mechanics, not just docs
- Don't double-apply passives already reflected in stat inputs
- Pal system: split "stat effects" (toggleable) vs "battle effects" (auto-applied)

## Common Pitfalls — Don't Repeat These
1. **Wrong battle sim** — Don't confuse V1 (`uploads/battlesimV1.html`) with the rewrite (`battlesim/index.html`). Always confirm which one.
2. **Context drift** — In long sessions, re-read this file and CONTEXT_TRANSFER.md if you lose track.
3. **Guardian Spirits ≠ Star Heroes** — Spirits are ConfigSpirit (ref 14), Heroes are ConfigAngel (ref 15). Completely separate systems.
4. **Inspire/Suppress names are swapped** in game code — this is a known quirk, preserve it.
5. **ConfigFly = Avians** — there is no ConfigBird.
