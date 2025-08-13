from pyomo.environ import ConcreteModel, Var, NonNegativeReals, Objective, Constraint, maximize

def create_model(data: dict) -> ConcreteModel:
    m = ConcreteModel()
    prods = list(data["profit"].keys())  # expects ['A','B'] for plotting utility

    # Decision variables
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
    # Optional upper bound on B
    if "B" in prods and "B_max" in data["limits"]:
        m.max_B = Constraint(expr=m.x["B"] <= data["limits"]["B_max"])

    return m
