def print_solution(prod_levels: dict[str, float], total_profit: float) -> None:
    print("Optimal production plan:")
    for p, q in prod_levels.items():
        print(f"  {p}: {q:.2f} units")
    print(f"\nTotal profit: {total_profit:.2f}")

def print_usage(data: dict, prod_levels: dict[str, float]) -> None:
    mh_used = sum(data["hours"][p] * prod_levels[p] for p in prod_levels)
    lb_used = sum(data["labor"][p] * prod_levels[p] for p in prod_levels)

    print("\nResource usage at optimum:")
    print(f"  Machine hours: {mh_used:.2f} / {data['limits']['hours']}")
    print(f"  Labor hours:   {lb_used:.2f} / {data['limits']['labor']}")
    if "B_max" in data["limits"] and "B" in prod_levels:
        print(f"  B upper bound: {prod_levels['B']:.2f} / {data['limits']['B_max']}")
