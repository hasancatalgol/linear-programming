# plot.py
# 2-variable LP plotting utility (feasible region + constraints + optimum)

import math
from itertools import combinations
import matplotlib.pyplot as plt


def _intersect(l1, l2):
    # each line: (a, b, c, label) meaning a*x + b*y = c
    a1, b1, c1, _ = l1
    a2, b2, c2, _ = l2
    det = a1 * b2 - a2 * b1
    if abs(det) < 1e-12:
        return None
    x = (c1 * b2 - c2 * b1) / det
    y = (a1 * c2 - a2 * c1) / det
    return (x, y)


def _feasible(pt, cons):
    # cons: list of (a, b, rhs, label) for <= constraints
    x, y = pt
    if x < -1e-9 or y < -1e-9:
        return False
    for (a, b, rhs, _) in cons:
        if a * x + b * y - rhs > 1e-9:
            return False
    return True


def plot_feasible_region_and_optimum(
    data: dict,
    optimum: tuple[float, float] | None = None,
    title: str = "Product-Mix LP",
    equal_scale: bool = True,
    same_axis_max: bool = True,  # if True, use the same max for x & y
):
    """
    data: dict with keys profit, hours, labor, limits (expects products 'A' and 'B')
    optimum: (x*, y*) if you want the optimal point marked
    equal_scale: set aspect ratio so 1 unit in x equals 1 unit in y
    same_axis_max: force xlim and ylim to share the same upper bound (square plot)
    """
    # Build constraints from the same data dict used by the model
    cons = [
        (data["hours"]["A"], data["hours"]["B"], data["limits"]["hours"], "2x + y = hours"),
        (data["labor"]["A"], data["labor"]["B"], data["limits"]["labor"], "x + y = labor"),
        (0, 1, data["limits"]["B_max"], "y = B_max"),
    ]
    # Lines for intersections also include axes
    lines = cons + [(1, 0, 0.0, "x = 0"), (0, 1, 0.0, "y = 0")]

    # Enumerate feasible vertices
    verts = set()
    for l1, l2 in combinations(lines, 2):
        p = _intersect(l1, l2)
        if p and _feasible(p, cons):
            verts.add((round(p[0], 10), round(p[1], 10)))
    if _feasible((0.0, 0.0), cons):
        verts.add((0.0, 0.0))
    vertices = list(verts)

    # Order polygon for shading
    if vertices:
        cx = sum(p[0] for p in vertices) / len(vertices)
        cy = sum(p[1] for p in vertices) / len(vertices)
        vertices_sorted = sorted(vertices, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    else:
        vertices_sorted = []

    # Figure out nice limits using intercepts and vertices
    def x_intercept(a, b, c):
        return c / a if abs(a) > 1e-12 else 0.0

    def y_intercept(a, b, c):
        return c / b if abs(b) > 1e-12 else 0.0

    x_candidates = [p[0] for p in vertices] + [max(0.0, x_intercept(a, b, c)) for (a, b, c, _) in cons]
    y_candidates = [p[1] for p in vertices] + [max(0.0, y_intercept(a, b, c)) for (a, b, c, _) in cons]

    xmax = (max(x_candidates) if x_candidates else 10.0) * 1.1
    ymax = (max(y_candidates) if y_candidates else 10.0) * 1.1

    if same_axis_max:
        m = max(xmax, ymax)
        xmax = ymax = m

    # Plot
    fig, ax = plt.subplots(figsize=(7, 5))

    # Draw constraint lines
    xs = [0.0, xmax]
    def y_on_line(a, b, c, x):
        if abs(b) < 1e-12:
            return None
        return (c - a * x) / b

    for (a, b, rhs, label) in cons:
        ys = [y_on_line(a, b, rhs, xs[0]), y_on_line(a, b, rhs, xs[1])]
        ax.plot(xs, ys, label=label)

    # Axes: full x-axis (y=0) and y-axis (x=0)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    # Shade feasible region
    if vertices_sorted:
        ax.fill([p[0] for p in vertices_sorted], [p[1] for p in vertices_sorted], alpha=0.25, label="Feasible region")

    # Mark optimum, if given
    if optimum is not None:
        ax.scatter([optimum[0]], [optimum[1]], s=60, zorder=5, label=f"Optimal ({optimum[0]:.2f}, {optimum[1]:.2f})")

    # Limits and scales
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)

    if equal_scale:
        ax.set_aspect("equal", adjustable="box")

    ax.set_xlabel("x (A)")
    ax.set_ylabel("y (B)")
    ax.set_title(title)
    ax.legend(loc="best")
    plt.tight_layout()
    plt.show()
