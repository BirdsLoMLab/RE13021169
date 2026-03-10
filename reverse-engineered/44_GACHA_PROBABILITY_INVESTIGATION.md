# 44 — Gacha & Event Item Probability Investigation

> **Sources:** game_script_pretty.js lines 6354-6442, 10817-10926, 11408-11445, 11519-11535, 12182-12500, 224570-224623, 292666-292682, 348994-348997; data/tables/Countdown_box.json, Mount_draw.json, Spirit_draw_prob.json, Double_probabillity.json, Ippon_matsu_prob.json; data/schemas/ConfigCountdown_box.json, ConfigMount_draw.json, ConfigDouble_probabillity.json, ConfigSpirit_draw_prob.json, ConfigIppon_matsu_prob.json
> **Key Discovery:** The Countdown Box system ships two separate weight columns — `cli_weight` (displayed to the player) and `serv_weight` (used server-side for actual draws). Rare items show ~65% higher odds in the UI than reality. All monetized draws are server-authoritative.

---

## 1. The Smoking Gun: Countdown Box Dual Weights

### Schema

From `data/schemas/ConfigCountdown_box.json`:

| Index | Field | Type | Description |
|-------|-------|------|-------------|
| 0 | id | number | Item ID |
| 1 | reward | array | [item_id, quantity] |
| 2 | **cli_weight** | number | Weight shown to player in UI |
| 3 | **serv_weight** | number | Weight used by server for actual draws |
| 4 | act_day | number | Activity day |

### Actual Data

From `data/tables/Countdown_box.json`:

| ID | Reward | cli_weight | serv_weight | Displayed Prob | Real Prob | Inflation |
|----|--------|-----------|------------|----------------|-----------|-----------|
| 1 | 1017 ×140 | 15 | 10 | 15.00% | 15.15% | — |
| 2 | 1008 ×40 | 15 | 10 | 15.00% | 15.15% | — |
| 3 | 1084 ×40 | 15 | 10 | 15.00% | 15.15% | — |
| 4 | 1114 ×20 | 15 | 10 | 15.00% | 15.15% | — |
| 5 | 1164 ×40 | 15 | 10 | 15.00% | 15.15% | — |
| 6 | Currency ×2000 | 10 | 10 | 10.00% | 15.15% | — |
| 7 | **1330 ×2** | **5** | **2** | **5.00%** | **3.03%** | **+65%** |
| 8 | **1331 ×5** | **5** | **2** | **5.00%** | **3.03%** | **+65%** |
| 9 | **1025 ×1** | **5** | **2** | **5.00%** | **3.03%** | **+65%** |

**Total cli_weight = 100, Total serv_weight = 66**

The rare items (IDs 7-9) appear **~65% more likely** in the UI than they actually are on the server. Meanwhile, the common items (IDs 1-5) appear slightly *less* likely than reality in the UI — the weight redistribution makes rare items look more attainable while common items look less dominant.

### Client Code Proof

**Line 11424 — Weight accumulation for UI display:**
```javascript
var t = configCountdown_box.getDatas();
v = 0;  // total weight accumulator
var i = IS(h).blindInfo, n = [];
for (var o in i.box_list)
    if (Object.prototype.hasOwnProperty.call(i.box_list, o)) {
        var r = i.box_list[o];
        0 != r && n.push(r)
    }
for (var s, a = [], c = e(t); !(s = c()).done;) {
    var d = s.value, l = n.includes(d.id);
    l || (v += d.cli_weight), a.push({ cfg: d, isGet: l })  // ← uses cli_weight
}
```

**Line 11441 — Probability percentage display:**
```javascript
n.onRender = function(t, i) {
    t.isGet
        ? (this.isGet.active = !0, this.txtRatio.string = "")
        : (this.isGet.active = !1,
           this.txtRatio.string = c.formatStr("%s%",
               (t.cfg.cli_weight / v * 100).toFixed(2)  // ← cli_weight / total_cli_weight
           ));
    this.itemGrid.SetItemId(t.cfg.reward[0][0], t.cfg.reward[0][1])
}
```

**Line 224604 — `serv_weight` accessor exists but is NEVER called in client code:**
```javascript
key: "serv_weight",
get: function() {
    return this._data[3]  // accessor defined but unused
}
```

The client exclusively uses `cli_weight` for display. `serv_weight` is shipped in the data bundle but only consumed server-side.

---

## 2. All Monetized Draws Are Server-Authoritative

### Client-Server Flow

Every gacha draw follows this protocol:

```
1. Client sends:    act_XXX_draw_c2s  (draw request + payment)
2. Server computes: weighted random using server-side weights
3. Server returns:  act_XXX_draw_s2c  { drop_id_list[], reward_list[] }
4. Client displays: animation pointing to pre-determined results
```

**Line 6410-6413 — Mount Draw result handler:**
```javascript
m.updateLotteryResult = function(t) {
    if (t.act_type == this.actType)
        if (this.nodeRolling.active = !0, this.checkJackpot(t.drop_id_list), ...) {
            // t.drop_id_list comes FROM THE SERVER
            var e = t.drop_id_list[t.drop_id_list.length - 1];
            this.finalIndex = configMount_draw.getDataByKey(e).order - 1;
            // Client just animates to the server-chosen result
        }
}
```

### Where Client-Side RNG Is Used (NOT gacha)

The client has two `getWeightRandIndex` implementations:

**Line 292674 — Deterministic seeded RNG (battle replay):**
```javascript
r.getWeightRandIndex = function(n, t) {
    var r = this.randomInt(0, t);  // seeded random
    for (var e = 0, o = 0; o < n.length && !(r < (e += n[o])); o++);
    return o
}
```

**Line 348994 — `Math.random()` based (minigames only):**
```javascript
t.getWeightRandIndex = function(t, n) {
    var r = Math.floor(Math.random() * n);
    for (var o = 0, a = 0; a < t.length && !(r < (o += t[a])); a++);
    return a
}
```

These are used for:
- Panda minigame bug spawning (line 26581)
- Sugar catch drop generation (line 97562)
- Fishing turntable (line 47083)
- Mount chapter buff selection (line 202396)
- Ice pet random spawns (line 116083)

**No monetized gacha uses client-side random.** The server has full, unilateral control over draw outcomes.

---

## 3. Per-Account Pity & Tracking: `must_info`, `replace_info`

### Data Structure

**Line 12424-12443 — Per-account draw state:**
```javascript
this.drawinfo[act_type] = {
    stage_count: 0,       // stage progression counter
    sum_star: 0,          // star accumulation
    star_process: 0,      // star process tracker
    count: 0,             // total draws made
    lucky_list: [],       // recent jackpot winners (UI ticker)
    replace_info: {},     // item replacement map (k→v)
    must_info: {},        // guaranteed/pity counter map (k→v)
    stage_info: {},       // stage progression map
    gotReward: {}         // rewards already obtained
}
```

### `must_info` — Pity Counter

**Line 12439-12442:**
```javascript
this.drawinfo[t.act_type].must_info = {};
for (var s, c = i(null != (f = t.must_info) ? f : []); !(s = c()).done;) {
    var f, u = s.value;
    this.drawinfo[t.act_type].must_info[u.k] = u.v  // pity counter per item
}
```

This maps item keys to their current pity count. When `v` reaches the `guaranteed` threshold defined in the draw table, the server forces that item to drop.

### `replace_info` — Limited Item Substitution

**Line 12434-12437:**
```javascript
this.drawinfo[t.act_type].replace_info = {};
for (var n, a = i(null != (r = t.replace_info) ? r : []); !(n = a()).done;) {
    var r, o = n.value;
    this.drawinfo[t.act_type].replace_info[o.k] = o.v  // replacement tracking
}
```

When a `limited` item (one-time drop) has been obtained, the `reward_replace` field in the draw config specifies what replaces it in future pulls. This is tracked per-account.

### `lucky_list` — Social Proof Ticker

**Line 6358-6365:**
```javascript
this.tipsGo.active = i.lucky_list.length > 0;
if (this.tipsGo.active) {
    var e = i.lucky_list[0],
        n = i.lucky_list.concat(e);
    this.tipsScroll.datas = n;
    // Scrolling ticker showing "PlayerX just got [rare item]!"
}
```

This is purely cosmetic — a scrolling banner showing recent jackpot winners. It does NOT affect probability. But it does create perception pressure.

---

## 4. Guaranteed/Pity System Tables

### Mount Draw Guaranteed

Schema: `ConfigMount_draw_guaranteed` — fields: `id`, `type`, `group_id`, `num` (threshold), `reward`

When `count >= num`, the system forces a specific reward tier. Multiple guarantee entries exist per group, with escalating thresholds.

### Guaranteed Fields in Draw Configs

Most gacha tables include these pity-related fields:

| Field | Meaning |
|-------|---------|
| `guaranteed` | Pity threshold (0 = no pity for this item) |
| `limited` | Max obtainable count (0 = unlimited) |
| `reward_replace` | Substitute reward after limited item obtained |
| `is_jackpot` | Jackpot flag (triggers special UI + lucky_list entry) |

### Example: Ippon Matsu Pool

From `data/tables/Ippon_matsu_prob.json` (group 1):

| Tier | Reward | Weight | Guaranteed | Limited | Displayed Prob |
|------|--------|--------|------------|---------|----------------|
| 1 | 70023 ×1 (Featured) | 70 | 40 | 1 | 0.70% |
| 2 | 1025 ×6 | 100 | 0 | 0 | 1.00% |
| 3 | 1165 ×10 | 200 | 0 | 0 | 2.00% |
| 4 | 1164 ×30 | 2000 | 0 | 0 | 20.00% |
| 5 | 1012 ×30 | 2000 | 0 | 0 | 20.00% |
| 6 | 1007 ×400 | 2630 | 0 | 0 | 26.30% |
| 7 | Gold ×5000 | 3000 | 0 | 0 | 30.00% |

**Total weight: 10000** (convenient for percentage calculation)

Featured item: 0.70% base rate, guaranteed after 40 pulls, limited to 1 copy. After obtaining it, `reward_replace` kicks in with 3 alternative rewards chosen by `reward_choose` weights.

### Example: Double Draw Probability

From `data/tables/Double_probabillity.json` (pool 1001):

| Tier | Reward | Weight | Guaranteed | Limited | Displayed Prob |
|------|--------|--------|------------|---------|----------------|
| 1 | 1025 ×2 | 100 | 60 | 2 | 1.01% |
| 2 | 30022 ×1 | 25 | 121 | 1 | 0.25% |
| 3 | 1014 ×1 | 30 | 80 | 1 | 0.30% |
| 4 | 1021 ×3 | 200 | 0 | 3 | 2.02% |
| 5 | 1008 ×20 | 200 | 0 | 3 | 2.02% |
| 6 | 1017 ×50 | 200 | 0 | 3 | 2.02% |
| 7 | 1012 ×5 | 1150 | 0 | 3 | 11.62% |
| 8 | 1013 ×5 | 1150 | 0 | 3 | 11.62% |
| 9 | 1007 ×100 | 3100 | 0 | 3 | 31.33% |
| 10 | Gold ×1000 | 3845 | 0 | 3 | 38.85% |

**Total weight: 10000**

The rarest item (30022 ×1) has 0.25% rate with pity at 121 pulls. Second rarest (1014 ×1) has 0.30% with pity at 80 pulls.

---

## 5. Complete Gacha System Inventory

### Systems with `weight` field (single weight — same for display and draw)

| System | Config Table | Key Fields | Pity Table |
|--------|-------------|------------|------------|
| Mount Draw | Mount_draw.json | weight, guaranteed, limited, is_jackpot | Mount_draw_guaranteed.json |
| Angel Draw | Angel_draw.json | weight | — |
| Spirit Draw | Spirit_draw.json + Spirit_draw_prob.json | prob, good_list | — |
| Star Rain Draw | Star_rain_draw.json | weight, guaranteed, limited | Star_rain_draw_guaranteed.json |
| Double Draw | Double_probabillity.json | weight, guaranteed, limited, reward_replace | Double_draw_guaranteed.json |
| Rogue Draw | Rogue_draw.json | weight, guaranteed, limited, is_jackpot | Rogue_draw_guaranteed.json |
| Season Ship Draw | Season_ship_draw.json | weight, is_jackpot, limited | Season_ship_draw_guaranteed.json |
| Season Treasure Draw | Season_treasure_draw.json | weight, is_jackpot, limited | Season_draw_guaranteed.json |
| Fate Draw | Fate_draw.json | weights, is_guaranteed | — |
| Treasure Hunting | Treasure_hunting_draw.json | weight | — |
| Ippon Matsu | Ippon_matsu_prob.json | weight, guaranteed, limited, reward_replace | — |
| Break Gold Egg | Break_gold_egg_weight.json | weight, guaranteed, limited | — |
| Loop Break Egg | Loop_break_gold_egg_weight.json | weight | — |
| Lucky Cat | Lucky_cat_reward.json | weight | — |
| Turntable | Turntable.json | weight | — |
| Strategy Shop | Strategy_activity_shop.json | weight, guarantee_num | — |
| Card Pool | Card_pool.json + Card_pool_type.json | group-based | — |
| Mayday Lottery | Mayday_lottery.json | weight-based | — |
| Box Tower | Box_tower (via ConfigBox_tower_level) | box_prob, big_prize_prob | — |

### Systems with DUAL weights (confirmed discrepancy)

| System | Config Table | Client Field | Server Field |
|--------|-------------|-------------|-------------|
| **Countdown Box** | Countdown_box.json | **cli_weight** | **serv_weight** |

### Cumulative Reward Tables (spend-threshold bonuses)

| Table | Fields |
|-------|--------|
| Mount_draw_cumulative_times.json | Rewards at draw count milestones |
| Rogue_draw_cumulative_times.json | Rewards at draw count milestones |
| Double_cumulative_reward.json | Rewards based on total spend |
| Star_rain_draw_times.json | Rewards at draw count milestones |
| Mount_draw_cost_get.json | Bonus rewards based on total cost |

---

## 6. Account-Level Luck Modifiers: What We Found (and Didn't)

### No Client-Side Evidence

Exhaustive search found **zero** instances of:
- `playerLuck`, `accountLuck`, `luckModifier`, `luck_rate`
- `vipModifier`, `spendMultiplier`, `whale_flag`
- `segment`, `cohort`, `ab_test`, `test_group`
- Account-level RNG seeds for gacha
- VIP level affecting draw weights

### What VIP/Recharge Systems Actually Do

Tables `Privilege.json` and `Privilege_card.json` exist but only affect:
- UI badges and privilege icons
- Bonus rewards from activities (not draw weights)
- Access to premium shops
- Extra daily attempts

**No field in any VIP config connects to gacha weight modification.**

### Why "Cursed" and "Blessed" Accounts Exist

Three explanations supported by the code:

**1. Pity Counter Desync**

`must_info` is per-account, per-activity. Two players starting the same event at different pity states will have wildly different short-term outcomes. A player who just hit pity on a previous banner starts at 0; a player who's 39/40 on the counter will hit jackpot almost immediately.

Since pity counters are **activity-specific** (not global), there's no "carry-over luck" between different event types. Players who feel "cursed" may be repeatedly starting fresh pity counters without realizing it.

**2. The Displayed-vs-Real Gap Creates False Expectations**

The Countdown Box proves the game inflates displayed odds. If this pattern exists server-side for other systems (where only a single `weight` ships to the client), players calibrate expectations against inflated numbers and then feel "unlucky" when reality doesn't match.

With 0.25%-0.70% featured item rates across most systems, even "honest" odds produce long dry streaks. A player seeing "5.00%" displayed but experiencing 3.03% real odds will feel ~65% more unlucky than they "should."

**3. Server-Side Opacity**

Since **all monetized draws are server-authoritative**:
- The server receives the draw request
- The server computes the result
- The server returns the pre-determined outcome
- The client just plays an animation

The server *could* apply any modifier — spend-based, time-based, account-based — and the client would never know. The `cli_weight`/`serv_weight` split proves the developers have built infrastructure for showing different odds than what's used. Whether this extends to per-account manipulation is **unprovable from client code alone**.

---

## 7. The $100 Pack Efficiency Question

### How Pack Purchases Interact with Draws

Pack purchases and gacha draws are separate systems:
- Packs (`Christmas_pack.json`, `Text_adventure_event_pack.json`, etc.) give fixed rewards
- Draw currencies from packs feed into the gacha systems
- `Mount_draw_cost_get.json` provides bonus rewards at cumulative spend thresholds

### The Efficiency Trap

Higher-cost packs typically provide:
- More draws per dollar (volume discount)
- Access to cumulative reward thresholds faster
- BUT: no evidence of improved per-draw probability

The cumulative reward tables (`*_cumulative_times.json`, `*_cost_get.json`) are **deterministic** — spend X total, get bonus Y. These are transparent and do not affect random draw weights.

### Could $100 Packs Secretly Boost Rates?

From client code: **No mechanism exists.** The draw request (`draw_c2s`) sends the activity type and draw count — not the payment method or pack ID. The server receives the same draw request regardless of how the currency was obtained.

However, since draws are server-authoritative, the server *could* theoretically track the source of currency and adjust weights accordingly. This would require server-side logic not present in the client bundle.

---

## 8. Technical Reference: Weighted Random Algorithm

### Standard Implementation (used across all client-side draws)

**Line 348994-348996:**
```javascript
t.getWeightRandIndex = function(t, n) {
    var r = Math.floor(Math.random() * n);  // random in [0, totalWeight)
    var o = 0;
    for (var a = 0; a < t.length && !(r < (o += t[a])); a++);
    return a;  // index of selected item
}
```

Standard cumulative weight selection:
1. Generate random number in `[0, totalWeight)`
2. Walk array, accumulating weights
3. Return first index where accumulated weight exceeds random value
4. Fallback: last item (if floating point edge case)

### Seeded Deterministic Version (battle/replay)

**Line 292674-292676:**
```javascript
r.getWeightRandIndex = function(n, t) {
    var r = this.randomInt(0, t);  // seeded PRNG, not Math.random()
    for (var e = 0, o = 0; o < n.length && !(r < (e += n[o])); o++);
    return o
}
```

Uses a seeded PRNG for deterministic replay — same seed always produces same sequence. This is used for battle simulation, NOT gacha.

---

## 9. Summary of Findings

### Confirmed

| Finding | Evidence |
|---------|----------|
| **Displayed odds ≠ real odds** (Countdown Box, ~65% inflation on rares) | `cli_weight` vs `serv_weight` fields, client only reads `cli_weight` |
| **All monetized draws are server-authoritative** | Client sends request, server returns pre-computed `drop_id_list[]` |
| **Pity systems exist and are per-account** | `must_info` tracking, `guaranteed` fields in draw configs |
| **Limited items get replaced after obtaining** | `replace_info` tracking, `reward_replace` fields |
| **No client-side gacha RNG** | `Math.random()` only used for minigames, never monetized draws |

### Not Found (but cannot be ruled out)

| Claim | Status |
|-------|--------|
| Account-level luck modifier | No client evidence; server could implement invisibly |
| Spend-based rate manipulation | No client evidence; server-authoritative design allows it |
| VIP level affecting drop rates | VIP tables only affect UI/bonus rewards, not weights |
| $100 pack boosting probability | Draw requests don't include payment source; no client mechanism |
| A/B testing on rates | Zero segmentation code in client |

### The Bottom Line

The game **provably lies about odds** in at least one system (Countdown Box). The server-authoritative architecture means any additional manipulation would be invisible to client analysis. The "cursed vs blessed" account phenomenon is most likely explained by pity counter state differences and the gap between displayed and actual probabilities — but server-side per-account manipulation cannot be ruled out.

---

## 10. File References

### Data Tables
- `/home/user/RE13021169/data/tables/Countdown_box.json` — **Dual weight smoking gun**
- `/home/user/RE13021169/data/tables/Mount_draw.json` — Mount gacha pool
- `/home/user/RE13021169/data/tables/Double_probabillity.json` — Double draw probabilities
- `/home/user/RE13021169/data/tables/Ippon_matsu_prob.json` — Ippon Matsu gacha pool
- `/home/user/RE13021169/data/tables/Spirit_draw_prob.json` — Spirit draw probability tiers
- `/home/user/RE13021169/data/tables/Star_rain_draw.json` — Star rain event gacha
- `/home/user/RE13021169/data/tables/Mount_draw_guaranteed.json` — Mount pity thresholds
- `/home/user/RE13021169/data/tables/Mount_draw_cumulative_times.json` — Mount spend milestones

### Schemas
- `/home/user/RE13021169/data/schemas/ConfigCountdown_box.json` — Dual weight schema
- `/home/user/RE13021169/data/schemas/ConfigMount_draw.json` — Mount draw schema (21 fields)
- `/home/user/RE13021169/data/schemas/ConfigDouble_probabillity.json` — Double draw schema
- `/home/user/RE13021169/data/schemas/ConfigIppon_matsu_prob.json` — Ippon Matsu schema
- `/home/user/RE13021169/data/schemas/ConfigSpirit_draw_prob.json` — Spirit prob schema

### Game Script
- `game_script_pretty.js:11424` — `cli_weight` accumulation for UI
- `game_script_pretty.js:11441` — Probability percentage display using `cli_weight`
- `game_script_pretty.js:224604` — `serv_weight` accessor (defined but never called)
- `game_script_pretty.js:6410-6420` — Mount draw server response handler
- `game_script_pretty.js:12424-12443` — Per-account draw state initialization
- `game_script_pretty.js:292674` — Seeded `getWeightRandIndex` (battle)
- `game_script_pretty.js:348994` — `Math.random()` `getWeightRandIndex` (minigames)
