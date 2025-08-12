def main():
    print("Hello from linear-programming!")

# A small linear program (product-mix) in Pyomo.
# Maximize profit from two products subject to resource limits.

from pyomo.environ import (
    ConcreteModel, Var, NonNegativeReals, Objective, Constraint, maximize,
    SolverFactory, value
)


def create_model(data):
    """
    data = {
        "profit": {"A": 40, "B": 30},
        "hours":  {"A": 2,  "B": 1},    # machine-hours per unit
        "labor":  {"A": 1,  "B": 1},    # labor-hours per unit
        "limits": {"hours": 100, "labor": 80, "B_max": 40}
    }
    """
    m = ConcreteModel()

    prods = list(data["profit"].keys())

    # Decision variables: number of units to produce (continuous, >= 0)
    m.x = Var(prods, domain=NonNegativeReals)

    # Objective: maximize total profit
    m.obj = Objective(
        expr=sum(data["profit"][p] * m.x[p] for p in prods),
        sense=maximize
    )

    # Constraints
    m.machine_hours = Constraint(
        expr=sum(data["hours"][p] * m.x[p] for p in prods) <= data["limits"]["hours"]
    )
    m.labor_hours = Constraint(
        expr=sum(data["labor"][p] * m.x[p] for p in prods) <= data["limits"]["labor"]
    )
    m.max_B = Constraint(expr=m.x["B"] <= data["limits"]["B_max"])

    return m


def choose_solver():
    """
    Try a few common LP solvers. You only need one installed.
    Priority: GLPK -> CBC
    """
    for cand in ["glpk", "cbc"]:
        try:
            solver = SolverFactory(cand)
            if solver and solver.available(exception_flag=False):
                return cand
        except Exception:
            pass
    return None


def main():
    # Problem data (tweak these to explore)
    data = {
        "profit": {"A": 40, "B": 30},
        "hours":  {"A": 2,  "B": 1},
        "labor":  {"A": 1,  "B": 1},
        "limits": {"hours": 100, "labor": 80, "B_max": 40}
    }

    model = create_model(data)

    solver_name = choose_solver()
    if solver_name is None:
        raise RuntimeError(
            "No LP solver found. Install GLPK or CBC (see README.md)."
        )

    results = SolverFactory(solver_name).solve(model, tee=False)
    status = str(results.solver.status)
    termination = str(results.solver.termination_condition)

    print(f"Solver: {solver_name}")
    print(f"Status: {status} | Termination: {termination}\n")

    # Report solution
    prod_levels = {p: value(model.x[p]) for p in model.x}
    total_profit = value(model.obj)

    print("Optimal production plan:")
    for p, q in prod_levels.items():
        print(f"  {p}: {q:.2f} units")

    print(f"\nTotal profit: {total_profit:.2f}")

    # Constraint usage (left-hand side vs. limit)
    mh_used = sum(data["hours"][p] * prod_levels[p] for p in prod_levels)
    lb_used = sum(data["labor"][p] * prod_levels[p] for p in prod_levels)

    print("\nResource usage at optimum:")
    print(f"  Machine hours: {mh_used:.2f} / {data['limits']['hours']}")
    print(f"  Labor hours:   {lb_used:.2f} / {data['limits']['labor']}")
    print(f"  B upper bound: {prod_levels['B']:.2f} / {data['limits']['B_max']}")

if __name__ == "__main__":
    main()
