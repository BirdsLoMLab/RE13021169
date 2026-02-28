# 04 — PvP Damage Reduction

## Code Location
**BattleMain init:** Line 188200 (default values)
**ChapterArena (1v1):** Lines 197534-197544
**ChapterMultipleArena (team):** Lines 202647-202660
**ChapterRogue:** Lines 203550-203560
**ConfigLevel schema:** Lines 242991-243045
**Damage application:** Line 449285

---

## A. PvP Factor Initialization

### 1v1 Arena (ChapterArena) — Lines 197534-197544
```javascript
o.start = function() {
    var t = this.battleMain.mainCtr.player.data.level,   // Player 1's level
        e = this.arenaPlayerCtr.player.data.level,        // Player 2's level
        a = n.roundInt((t + e) / 2),                      // Average level (floor)
        i = configLevel.getDataByKey(a);                   // Lookup config by level

    this.battleMain.injuryReduce = n.round(i.pvp_injury_reduce / 1e4);
    this.battleMain.shieldDecay  = n.round(r.shield_correct / 1e4);
    this.battleMain.treatDecay   = n.round(r.hp_recovery_correct / 1e4);
}
```

### Multi-Player Arena (DoublePvP) — Lines 202647-202660
```javascript
u.start = function() {
    var r = 0;
    for (var t of battleMain.playerCtrs) {
        r = n.roundInt(r + t.player.data.level);  // Sum all player levels
    }
    var o = n.roundInt(r / e.playerCtrs.length),   // Average across all players
        u = configLevel.getDataByKey(o);

    this.battleMain.injuryReduce = n.round(u.pvp_injury_reduce / 1e4);
    this.battleMain.shieldDecay  = n.round(i.shield_correct / 1e4);
    this.battleMain.treatDecay   = n.round(i.hp_recovery_correct / 1e4);
}
```

### Default Values (Non-PvP) — Line 188200-188204
```javascript
this.injuryReduce = 1   // No reduction in PvE
this.shieldDecay = 1     // No shield decay in PvE
this.treatDecay = 1       // No heal decay in PvE
this.seasonPveDamAdd = 0  // No PvE seasonal bonus
```

---

## B. Formulas

### Average Level Calculation
```
1v1:  avg_level = roundInt((player1_level + player2_level) / 2)
Team: avg_level = roundInt(sum_of_all_player_levels / player_count)
```
Note: `roundInt` = `Math.floor(round(x))` where `round()` rounds to 4 decimal places.

### PvP Factor
```
injuryReduce = round(configLevel[avg_level].pvp_injury_reduce / 10000)
```

### Shield Decay Factor
```
shieldDecay = round(shield_correct / 10000)
```
Default `shield_correct = 4000`, so `shieldDecay = 0.4`

### Heal Decay Factor
```
treatDecay = round(hp_recovery_correct / 10000)
```
Default `hp_recovery_correct = 3000`, so `treatDecay = 0.3`

---

## C. Damage Application (how injuryReduce is used)

### At Skill/Buff Level (MULTIPLY)
Many skill effects multiply damage BY injuryReduce before sending to healthTarget:
```javascript
// Line 192776: BuffBleed HP% damage
A = n.round(B * this.skillPar);
y = A = n.round(A * t.battleMain.injuryReduce);  // multiply

// Line 195796: BuffSkillValue HP damage
l = n.roundInt(a * this.skillPar);
l = n.roundInt(l * t.battleMain.injuryReduce);  // multiply
```

### At Unit Level (DIVIDE) — Line 449285
```javascript
// Line 449285: Unit.addDamage - healthType switch
case Hurt:
case Hurt_Crit:
case Hurt_Ret:
case Hurt_Share_Damage:
case Hurt_Share_Damage_Crit:
case Hurt_Double:
case Hurt_Double_Crit:
case Real_Damage:
case Hurt_Bleed:
case Hurt_Bleed_Crit:
case Hurt_Counter:
case Hurt_Counter_Crit:
case SpiritToPlayer:
    // DIVIDE by injuryReduce (this is the main PvP reduction)
    W = Math.max(s.roundInt(W / this.battleMain.injuryReduce), 1);
    // minimum damage = 1

    // Season PvE bonus (only for team 1)
    if (this.battleMain.seasonPveDamAdd > 0 && 1 == this.teamId)
        W = s.roundInt(W * (1 + this.battleMain.seasonPveDamAdd));
```

### BuffVampire (Life Steal) — Line 196771
```javascript
// DIVIDE by injuryReduce for vampire healing
p = Math.max(r.roundInt(p / this.runner.battleMain.injuryReduce), 1);
```

---

## D. PvP Reduction Flow for HP-Based Damage

**Critical pattern for HP-based damage (BuffSkillValue._calHpHurt):**

```
Step 1: hp_dmg = roundInt(target_hp_value × skillPar)
Step 2: hp_dmg = roundInt(hp_dmg × injuryReduce)       ← MULTIPLY UP
Step 3: If _limit exists, compute base_atk_dmg and clamp
Step 4: healthTarget(target, hp_dmg, Hurt)
Step 5: At Unit.addDamage: W = max(roundInt(W / injuryReduce), 1)  ← DIVIDE BACK DOWN
```

This means HP-based damage is:
1. Multiplied UP by injuryReduce (making it larger for clamping purposes)
2. Clamped against basic ATK damage bounds
3. Then divided BACK DOWN by injuryReduce (reducing to final PvP value)
4. Min final damage = 1

This two-step process ensures the clamp operates on "raw" (pre-PvP) values.

---

## E. Shield and Heal Decay

### Shield Decay — Line 195201
```javascript
// During shield creation in BuffShield:
a = r.roundInt(a * this.skillPar);
a = r.roundInt(a * r.round(1 + t.data.getAttrib(f.shield_hp_extra)));
// Apply shield decay ONLY if _isDec == 0:
0 == this._isDec && (a = r.roundInt(a * t.battleMain.shieldDecay));
```
Formula: `shield_hp = roundInt(base_shield × round(1 + shield_hp_extra) × shieldDecay)`
With default `shieldDecay = 0.4`, shields in PvP are **40% of their PvE value**.

### Heal Decay — Lines 449335, 449242
```javascript
// During heal application:
W = s.roundInt(W * this.battleMain.treatDecay);  // Line 449335

// HP recovery per tick:
d = s.roundInt(s.round(e * u) * this.battleMain.treatDecay);  // Line 449242
```
With default `treatDecay = 0.3`, healing in PvP is **30% of its PvE value**.

---

## F. ConfigLevel Data Structure

### Schema (Lines 243004-243034)
| Index | Field | Description |
|-------|-------|-------------|
| 0 | level | Level number |
| 1 | expend | EXP cost |
| 2 | num | Count value |
| 3 | pvp_injury_reduce | PvP injury reduction factor (÷10000) |
| 4 | power_par | Power parameter |

**Note:** The actual PvP factor values per level are stored in game data (not hardcoded in the script). We only see the schema. The actual level→factor mapping would need to be extracted from the runtime data or a data file.

---

## Comparison with Known Documentation

### Expected (Yuko PDF):
```
Avg Level = floor((Player_Lv + Enemy_Lv) / 2)
Factor = configLevel[Avg Level].pvp_injury_reduce / 1e4
Final DMG = Math.max(roundInt(DMG / Factor), 1)
```

### Actual:
- **Average level: CONFIRMED** — `roundInt((lv1 + lv2) / 2)` = effectively `floor(average)`
- **Factor lookup: CONFIRMED** — `configLevel.getDataByKey(avg).pvp_injury_reduce / 1e4`
- **Division: CONFIRMED** — `Math.max(roundInt(W / injuryReduce), 1)`
- **Minimum 1: CONFIRMED** — `Math.max(..., 1)`

### Additional Findings:
1. **Shield decay and heal decay are separate PvP corrections** stored in global config, not per-level.
2. **seasonPveDamAdd** is a separate PvE seasonal damage bonus that only applies to team 1.
3. **HP-based damage uses a multiply-then-divide pattern** to properly clamp in PvP context.
4. **injuryReduce defaults to 1** (no reduction) for all non-PvP battle types.
