from typing import Tuple, Dict
from pyomo.environ import SolverFactory, value

PREFERRED = ("glpk", "cbc")

def choose_solver() -> str | None:
    for cand in PREFERRED:
        try:
            solver = SolverFactory(cand)
            if solver and solver.available(exception_flag=False):
                return cand
        except Exception:
            continue
    return None

def solve(model) -> Tuple[Dict[str, float], float, str, str]:
    name = choose_solver()
    if name is None:
        raise RuntimeError("No LP solver found. Install GLPK or CBC.")

    results = SolverFactory(name).solve(model, tee=False)
    status = f"{results.solver.status} | {results.solver.termination_condition}"

    prod_levels = {p: float(value(model.x[p])) for p in model.x}
    total_profit = float(value(model.obj))
    return prod_levels, total_profit, name, status
