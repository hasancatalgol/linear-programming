# Pyomo Linear Programming Example — Product Mix

This is a minimal, self-contained **linear program (LP)** using [Pyomo](https://www.pyomo.org/) to decide how many units of two products (A and B) to produce in order to **maximize profit** subject to **machine-hour, labor-hour, and demand** constraints.

## Problem formulation

**Decision variables**
- `x_A, x_B ≥ 0` — production quantities (continuous)

**Objective**
- Maximize `40*x_A + 30*x_B`

**Constraints**
- Machine hours: `2*x_A + 1*x_B ≤ 100`
- Labor hours: `1*x_A + 1*x_B ≤ 80`
- Demand cap for B: `x_B ≤ 40`

## Quick start

### 1) Python & packages
```bash
uv add pyomo
