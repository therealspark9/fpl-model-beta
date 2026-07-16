# Fantasy Football Squad Optimizer

> A constrained optimization problem for selecting the best 15-player fantasy football squad under budget and formation rules.

---

## Problem Overview

Given a pool of football players with associated **prices**, **expected points**, and **minutes played**, select an optimal **15-player squad** (1 GK + 14 outfield) and a **starting XI** under:

- A total **budget of £100m**
- Valid **formation constraints**
- A **points-maximization objective**

---

## Decision Variables

| Variable | Description |
|----------|-------------|
| `x[i]`   | Binary — player `i` is in the **squad** (15 players) |
| `y[i]`   | Binary — player `i` is in the **starting XI** (11 players) |
| `f[k]`   | Binary — formation `k` is selected |

---

## Formations

One formation must be chosen for the starting XI. The squad always contains **1 GK + 10 outfield players** (bench included). Valid formations:

### 3-Back
| Formation | DEF | MID | ATT |
|-----------|-----|-----|-----|
| 3-4-3     | 3   | 4   | 3   |
| 3-5-2     | 3   | 5   | 2   |

### 4-Back
| Formation | DEF | MID | ATT |
|-----------|-----|-----|-----|
| 4-3-3     | 4   | 3   | 3   |
| 4-4-2     | 4   | 4   | 2   |
| 4-5-1     | 4   | 5   | 1   |

### 5-Back
| Formation | DEF | MID | ATT |
|-----------|-----|-----|-----|
| 5-4-1     | 5   | 4   | 1   |
| 5-3-2     | 5   | 3   | 2   |
| 5-2-3     | 5   | 2   | 3   |

> **Constraint:** Exactly one formation `f[k] = 1` must be active.

---

## Budget & Price Ranges

| Position | Min Price | Max Price |
|----------|-----------|-----------|
| GK       | £4.0m     | £5.5m     |
| DEF      | £4.0m     | £6.5m     |
| MID      | £4.5m     | £14.5m    |
| ATT      | £4.5m     | £14.5m    |

```
Total Budget ≤ £100m
∑ price[i] · x[i] ≤ 100
```

---

## Points System

### Playing Time
| Condition       | Points |
|-----------------|--------|
| ≥ 60 mins played | +2    |

### By Position

#### Goalkeeper
| Event        | Points |
|--------------|--------|
| Clean Sheet  | +4     |

#### Defender
| Event        | Points |
|--------------|--------|
| Clean Sheet  | +4     |
| Goal         | +6     |
| Assist       | +3     |

#### Midfielder
| Event        | Points |
|--------------|--------|
| Clean Sheet  | +1     |
| Goal         | +5     |
| Assist       | +3     |

#### Attacker
| Event        | Points |
|--------------|--------|
| Goal         | +4     |
| Assist       | +3     |

### Deductions
| Event        | Points |
|--------------|--------|
| Yellow Card  | −1     |
| Red Card     | −3     |

---

## Objective Function

Maximize total **expected points** of the starting XI:

```
maximize  ∑ points[i] · y[i]
```

Where individual player points are estimated as:

```
points[i] = max(bookmaker_odds_implied_pts[i],  xG[i] + xA[i])
```

And actual realized points follow:

```
actual_pts[i] = base_mins_pts[i] + goals[i] + assists[i] + clean_sheet[i] - card_penalty[i]
```

---

## Constraints

### Squad Composition
```
∑ x[i] = 15                        # total squad size
∑ x[i] for GK = 2                  # 2 goalkeepers in squad
∑ x[i] for DEF ∈ {5}               # 5 defenders in squad
∑ x[i] for MID ∈ {5}               # 5 midfielders in squad
∑ x[i] for ATT ∈ {3}               # 3 attackers in squad
```

### Starting XI
```
∑ y[i] = 11                        # exactly 11 starters
y[i] ≤ x[i]  for all i             # can only start if in squad
∑ y[i] for GK = 1                  # exactly 1 GK starts
```

### Formation Enforcement
```
∑ f[k] = 1                         # exactly one formation active

∑ y[i] for DEF = ∑ def_count[k] · f[k]   # DEF starters match formation
∑ y[i] for MID = ∑ mid_count[k] · f[k]   # MID starters match formation
∑ y[i] for ATT = ∑ att_count[k] · f[k]   # ATT starters match formation
```

### Budget
```
∑ price[i] · x[i] ≤ 100
```

### Minutes Priority
```
If mins[i] > mins[j]:  y[i] ≥ y[j]   (soft constraint / priority ordering)
```
Players with more expected minutes are preferred as starters over those with fewer.

---

## Problem Type

| Property         | Value |
|------------------|-------|
| Problem Class    | Mixed-Integer Linear Program (MILP) |
| Decision Vars    | Binary (`x[i]`, `y[i]`, `f[k]`) |
| Objective        | Maximize expected points |
| Key Constraints  | Budget, formation, squad structure |
| Solver Options   | `PuLP`, `OR-Tools`, `Gurobi`, `CVXPY` |

---

## Repository Structure

```
fantasy-football-optimizer/
├── data/
│   ├── players.csv          # player pool with price, position, xG, xA, mins
│   └── formations.json      # valid formations config
├── src/
│   ├── optimizer.py         # MILP model definition
│   ├── points.py            # points calculation logic
│   └── scraper.py           # data ingestion (odds, xG/xA feeds)
├── notebooks/
│   └── analysis.ipynb       # squad analysis & visualization
├── tests/
│   └── test_optimizer.py    # unit tests
├── requirements.txt
└── README.md
```

---

## Quick Start

```bash
git clone https://github.com/your-username/fantasy-football-optimizer
cd fantasy-football-optimizer
pip install -r requirements.txt
python src/optimizer.py --budget 100 --formation auto
```

---

## Dependencies

```
pulp>=2.7
pandas>=2.0
numpy>=1.24
requests>=2.31     # for data scraping
```

---

## Example Output

```
Optimal Squad (£99.2m / £100m)
Formation: 4-3-3

GK:  Flekken (£4.5m)         [bench: Flaherty £4.0m]
DEF: Alexander-Arnold (£6.5m), Pedro Porro (£5.5m), ...
MID: Salah (£13.5m), Palmer (£11.5m), ...
ATT: Haaland (£14.5m), ...

Expected Points (GW): 74.3
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
