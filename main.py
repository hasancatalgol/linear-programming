import argparse
from data import DEFAULT_DATA
from model import create_model
from solver import solve
from report import print_solution, print_usage
from plot import plot_feasible_region_and_optimum

def main():
    p = argparse.ArgumentParser(description="Product-mix LP (solve + optional plot).")
    p.add_argument("--hours", type=float, default=DEFAULT_DATA["limits"]["hours"], help="Machine-hours limit")
    p.add_argument("--labor", type=float, default=DEFAULT_DATA["limits"]["labor"], help="Labor-hours limit")
    p.add_argument("--bmax",  type=float, default=DEFAULT_DATA["limits"]["B_max"],  help="Upper bound for product B")
    p.add_argument("--plot", action="store_true", help="Show 2D plot of constraints and feasible region")
    args = p.parse_args()

    data = {
        "profit": DEFAULT_DATA["profit"],
        "hours":  DEFAULT_DATA["hours"],
        "labor":  DEFAULT_DATA["labor"],
        "limits": {"hours": args.hours, "labor": args.labor, "B_max": args.bmax},
    }

    model = create_model(data)
    prod_levels, total_profit, solver_name, status = solve(model)

    print(f"Solver: {solver_name}")
    print(f"Status: {status}\n")
    print_solution(prod_levels, total_profit)
    print_usage(data, prod_levels)

    if args.plot:
        # Pass optimal point to the plotter
        x_opt = prod_levels.get("A", 0.0)
        y_opt = prod_levels.get("B", 0.0)
        plot_feasible_region_and_optimum(data, (x_opt, y_opt), title="Product-Mix LP")

if __name__ == "__main__":
    main()
