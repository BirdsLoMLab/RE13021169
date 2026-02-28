# 09 — Bleed Damage System

## Code Location
**Module:** BuffBleed.ts
**Lines:** 192750-192860 in `game_script_pretty.js`

---

## Bleed Types (_type)

The bleed system has 8 different calculation types:

| _type | Damage Source | Formula |
|-------|-------------|---------|
| 0 | Basic ATK-based bleed | (ATK-DEF×(1+DEF_COE)) × ATT_DAM × calHurt + skill crit check |
| 1 | Current HP percentage | currentHP × skillPar × injuryReduce |
| 2 | Skill-based bleed | (ATK-DEF×(1+DEF_COE)) × skill_dam_extra × skillPar × (1-skill_resist) + skill crit |
| 3 | Basic ATK with ATT_RESIST | (ATK-DEF×(1+DEF_COE)) × ATT_DAM × (1-att_resist) × calHurt + normal crit |
| 4 | Combo-based bleed | (ATK-DEF×(1+DEF_COE)) × double_hit_dam × (1-double_hit_def) × calHurt + normal crit |
| 5 | Counter-based bleed | (ATK-DEF×(1+DEF_COE)) × counter_dam × (1-counter_def) × calHurt + normal crit |
| 6 | Max HP percentage | maxHP × skillPar × injuryReduce |
| 10 | Attribute-based | target_or_caster.attrib × skillPar × injuryReduce |

---

## Raw Code (Annotated) — Key Cases

### Type 0: Basic ATK Bleed (Lines 192771-192772)
```javascript
case 0:
    // Base: (ATK - DEF×(1+DEF_COE)), min 1
    A = Math.max(n.roundInt(e - i * (1 + u)), 1);
    // × ATT_DAM multiplier
    A = n.round(A * k);
    // × active_skilldamage_par
    A = n.round(A * r.data.getSkillFactAttrValue(this.skillPar, this.runner.useSkill.config.id, d.active_skilldamage_par));
    // × (1 + boss_dam) if target is boss
    this.owner.config.type == l.Boss && v > 0 && (A = n.roundInt(A * n.round(1 + v)));
    // Apply calHurt (DMG RES)
    y = _(A, t, r);
    break;
```

### Type 1: Current HP Bleed (Lines 192774-192776)
```javascript
case 1:
    var B = this.owner.data.currenHp;  // target's current HP
    A = n.round(B * this.skillPar);     // × HP percentage
    y = A = n.round(A * t.battleMain.injuryReduce);  // × PvP factor (stays multiplied)
    break;
```
**Note:** Type 1 multiplies by injuryReduce but does NOT get divided back in the BuffBleed flow. The `healthTarget` call with the result will divide it at Unit.addDamage.

### Type 2: Skill Bleed (Lines 192778-192788)
```javascript
case 2:
    A = Math.max(n.roundInt(e - i * (1 + u)), 1);
    var M = r.data.getAttrib(d.skill_dam_extra);
    A = n.roundInt(A * M * this.skillPar);
    var x = t.data.getAttrib(d.skill_resist),
        T = g(t, r, x, d.skill_resist);  // calArmorAndBlock
    A = _(n.roundInt(A * Math.max(0, n.round(1 - T))), t, r);  // calHurt
    if (m(r)) {  // checkSkillCirt
        var S = r.data.getAttrib(d.skill_crit_dam);
        A = n.roundInt(A * n.round(1 + S));
        A = n.roundInt(Math.pow(A, .98));  // 0.98 exponent
        I = h.Hurt_Bleed_Crit;
    }
    y = A;
    break;
```

### Type 3: Basic ATK + Resistance Bleed (Lines 192790-192798)
```javascript
case 3:
    A = Math.max(n.roundInt(e - i * (1 + u)), 1);
    A = n.round(A * k);  // × ATT_DAM
    A = n.round(A * r.data.getSkillFactAttrValue(...));
    this.owner.config.type == l.Boss && v > 0 && (A = n.roundInt(A * n.round(1 + v)));
    var H = t.data.getAttrib(d.att_resist),
        C = g(t, r, H, d.skill_resist);  // calArmorAndBlock
    y = _(n.roundInt(A * Math.max(0, n.round(1 - C))), t, r);
    if (b(r, t, !0) == s.Cirt) {  // checkHit for crit
        var P = r.data.getAttrib(d.crit_dam),
            w = Math.max(.5, t.data.getAttrib(d.crit_def));
        y = n.roundInt(y * Math.max(1.5, n.round(P / w)));
        I = h.Hurt_Bleed_Crit;
    }
    break;
```

### Type 6: Max HP Bleed (Lines 192823-192824)
```javascript
case 6:
    var N = this.owner.data.getAttrib(d.hp);  // target's MAX HP
    A = n.round(N * this.skillPar);
    y = A = n.round(A * t.battleMain.injuryReduce);
    break;
```

### Type 10: Attribute-Based (Lines 192826-192827)
```javascript
case 10:
    A = this._isTarget
        ? t.data.getAttrib(this._attribId)    // target's attribute
        : r.data.getAttrib(this._attribId);   // caster's attribute
    A = n.round(A * this.skillPar);
    y = A = n.round(A * t.battleMain.injuryReduce);
    break;
```

---

## Post-Calculation Modifiers (Lines 192829-192847)

After the base damage is calculated (all types except type 1):

```javascript
// Apply EXTRA_DAMAGE buffs (multiplicative)
if (1 != this._type) {
    var q = r.buffCtr.getBuffByType(c.EXTRA_DAMAGE);
    for (var z of q) {
        y = z.calDamage(y, null, this.runner.useSkill.config.id);
    }
}

// Apply record damage bonus
var W = r.skillctr.getRecordDamage(this.runner.useSkill.config.id);
y = n.roundInt(y * n.round(1 + n.round(W / 1e4)));

// Apply GIANT_SLAYER (only for type 0)
if (0 == this._type) {
    var X = r.buffCtr.getBuffByType(c.GIANT_SLAYER);
    for (var Y of X) {
        y = Y.onCalHpDamage(t, y);
    }
}

// Apply limits and send damage
var K = this.getLimit(y);
this.runner.healthTarget(t, K, I, !1, this.config.id);

// Trigger vampire (life steal) if applicable
```

---

## Bleed DOT Execution

From the `BuffBleedDot` class (lines 193815-193825):
```javascript
// Bleed DOT: splits total damage over multiple ticks
this._totalddamagevalue = o.round(this.skillPar * this.owner.battleMain.injuryReduce);
this._damage = o.round(this._totalddamagevalue / this._effCount);

// First tick
if (this._isFirst) {
    this._totalddamagevalue = o.round(this._totalddamagevalue - this._damage);
    this.runner.healthTarget(this.owner, this._damage, u.Hurt_Bleed, !1, this.config.id);
    this._effCount = this._effCount - 1;
}
```

---

## Comparison with Known Documentation

### Key Findings:
1. **Bleed has 8 different calculation types** — much more complex than documented
2. **HP% bleed types (1, 6, 10) multiply by injuryReduce** and then get divided at Unit.addDamage
3. **Skill-based bleed (type 2) can skill-crit** with the 0.98 exponent
4. **Basic ATK bleeds (types 3, 4, 5) can normal-crit** with crit_dam/crit_def
5. **EXTRA_DAMAGE and GIANT_SLAYER buffs apply to bleed** (except type 1)
6. **Record damage bonus applies to all bleed types**
7. **Bleed DOT splits total damage over multiple ticks** evenly
