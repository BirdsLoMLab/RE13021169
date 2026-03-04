# Missing Config Data — What We Need

## Status

The `game_script_pretty.js` (24MB beautified) has been regenerated. However, the **config binary data blob** was not captured in the `uploads/20260228` HTTP archive. Without it, we cannot decode `data/tables/` and cannot map the remaining 35 mount skill IDs.

## What's Missing

The config/datas binary (~12MB) lives at:
```
bundle-firstload-res/native/c8/*.bin
```

The current capture only has:
- `bundle-firstload-res/index.5e4de.js` (bootstrap loader, ~1KB)
- `bundle-res/native/**/*.bin` (sprite/audio assets, NOT config data)

## What We Need It For

### ConfigMount_skin (mount_id → skin_skill mapping)

Schema: `[mount_id, skin_level, expend, skin_skill, attr, power]`

The `skin_skill` field contains `[[skill_id, skill_level]]` pairs — this maps each mount cosmetic to its combat skill.

**19 already mapped** (from previous code reverse-engineering):

| Mount Name (xlsx) | mount_id | skill_id |
|---|---|---|
| Hot Wheels | ? | 5003 |
| Pyrebreaker | ? | 5002 |
| White Tiger | ? | 5004 |
| Blue Ox | ? | 5005 |
| Round Frog | ? | 5007 |
| Blue Queen | ? | 5006 |
| Purple Wing | ? | 5008 |
| Cloud Drifter | ? | 5009 |
| Koi Paper Kite | ? | 5016 |
| Mini Motorcycle | ? | 5014 |
| Blazing Motorcycle | ? | 5021 |
| AdaptoSlime | ? | 5026 |
| Trembling Pepe | ? | 5029 |
| Ethereal Phoenix | 406 | 5060 |
| Speed of Death | 404 | 5057 |
| Holy Dragon | ? | 5033 |
| Vibrant Watermelon Ship | ? | 5034 |
| Silvery Crescent | ? | 5024 |
| Heart's Desire | ? | 5030 |

**35 unmapped** — need config binary to determine:
Skyshark, Boom Da Bang, Rum Barrel, Blizzard Visitor, Diving Duck, Scorpio,
Wave Cruiser, Storm Rider, Long-legged Bird, Book of the Universe, Time Machine,
Sea of Lanterns, Dimensional Wings, Gator Menace, Pumpkin Carriage, Nebular Shuttle,
Effulgent Fan, Magic Carpet, Panda Attack, Guardian Spaceship, Cheetah Zero,
Cinder Wolf, Dazzling Unicorn, Skyward Blaze, Thunder Vanguard, Sparkling Flash,
Cloud Traveler, Spectral Ride, Immortal Tyrant, Best Buddy, Soaring Shroomie,
Sanctuary Warmth, Dawn of Time, Leo, Horizon Racer

### Other Tables Needed

The config binary also contains skill coefficients, buff definitions, and attribute data for:
- `ConfigSkill` / `ConfigSkill_level` — skill parameters and level scaling
- `ConfigBuff` — buff definitions (duration, stacking, effects)
- `ConfigMount` — mount_id → name mapping (via string_ref)

## How to Capture

### Option 1: Browser Network Capture
1. Open game in browser (Chrome DevTools → Network tab)
2. Clear cache and reload
3. Filter for `bundle-firstload-res/native`
4. Find the large .bin file (~12MB) — this is config/datas
5. Save it to `uploads/YYYYMMDD/lom.joynetgame.com/assets/bundle-firstload-res/native/c8/`

### Option 2: mitmproxy / Fiddler
1. Proxy the game traffic
2. Capture `lom.joynetgame.com/assets/bundle-firstload-res/native/c8/*.bin`

### Option 3: Browser Cache
1. Navigate to `chrome://cache/` or browser cache directory
2. Search for `bundle-firstload-res` entries
3. Extract the binary blob

### After Capturing
```bash
python3 decode_config_data.py uploads/YYYYMMDD --output data/tables
```
This will decode all 908 tables into `data/tables/`, including `Mount_skin.json` with the mount_id → skill_id mappings.
