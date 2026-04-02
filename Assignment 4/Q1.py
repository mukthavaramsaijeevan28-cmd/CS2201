try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def visualize_solution(solution, adjacency):
    if plt is None:
        print("\nVisualization skipped: install matplotlib to draw the map (pip install matplotlib).")
        return

    from matplotlib.patches import Polygon

    region_polygons = {
        'WA': [
            (0.00, 0.28), (0.16, 0.28), (0.32, 0.32), (0.36, 0.38), (0.36, 0.50),
            (0.28, 0.58), (0.18, 0.68), (0.08, 0.70), (0.00, 0.62)
        ],
        'NT': [
            (0.28, 0.58), (0.40, 0.60), (0.46, 0.72), (0.56, 0.78), (0.62, 0.80),
            (0.70, 0.72), (0.68, 0.62), (0.64, 0.52), (0.44, 0.52)
        ],
        'Queensland': [
            (0.64, 0.52), (0.72, 0.56), (0.80, 0.64), (0.88, 0.76), (0.95, 0.86),
            (0.98, 0.98), (0.90, 0.98), (0.80, 0.92), (0.72, 0.82), (0.68, 0.66)
        ],
        'SA': [
            (0.36, 0.38), (0.62, 0.40), (0.70, 0.44), (0.68, 0.52), (0.44, 0.52),
            (0.38, 0.48), (0.36, 0.40)
        ],
        'NSW': [
            (0.68, 0.44), (0.78, 0.38), (0.86, 0.40), (0.94, 0.46), (0.98, 0.52),
            (0.96, 0.58), (0.84, 0.56), (0.74, 0.48)
        ],
        'V': [
            (0.68, 0.20), (0.74, 0.18), (0.82, 0.16), (0.90, 0.16), (0.88, 0.10),
            (0.78, 0.06), (0.68, 0.08)
        ],
        'T': [
            (0.74, -0.10), (0.88, -0.10), (0.92, -0.04), (0.88, 0.02), (0.74, 0.02)
        ]
    }

    label_positions = {
        'WA': (0.16, 0.50),
        'NT': (0.50, 0.70),
        'Queensland': (0.84, 0.80),
        'SA': (0.50, 0.42),
        'NSW': (0.84, 0.50),
        'V': (0.80, 0.10),
        'T': (0.83, -0.05)
    }

    color_map = {
        'Red': 'red',
        'Green': 'green',
        'Blue': 'blue'
    }

    fig, ax = plt.subplots(figsize=(10, 8))
    for region, polygon in region_polygons.items():
        patch = Polygon(polygon, closed=True,
                        facecolor=color_map[solution[region]],
                        edgecolor='black', linewidth=1.5, alpha=0.8)
        ax.add_patch(patch)
        x, y = label_positions[region]
        ax.text(x, y, region, ha='center', va='center', fontsize=10,
                fontweight='bold', color='white')

    ax.set_title('Australia Map Coloring', fontsize=16)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.20, 1.05)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    plt.show()


def solve_csp(variables, domains, constraints):
    def is_consistent(var, value, assignment):
        for neighbor, constraint in constraints.get(var, []):
            if neighbor in assignment and not constraint(value, assignment[neighbor]):
                return False
        return True

    def select_unassigned_variable(assignment):
        unassigned = [v for v in variables if v not in assignment]
        unassigned.sort(key=lambda v: (len(domains[v]), -len(constraints.get(v, []))))
        return unassigned[0]

    def backtrack(assignment):
        if len(assignment) == len(variables):
            return dict(assignment)

        var = select_unassigned_variable(assignment)
        for value in domains[var]:
            if is_consistent(var, value, assignment):
                assignment[var] = value
                result = backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

    return backtrack({})


def solve_australia():
    print("=" * 60)
    print("PROBLEM 1: Australia Map Coloring (7 regions)")
    print("=" * 60)

    variables = ['WA', 'NT', 'Queensland', 'SA', 'NSW', 'V', 'T']
    colors = ['Red', 'Green', 'Blue']
    domains = {v: colors[:] for v in variables}

    # Adjacency list (undirected)
    adjacency = {
        'WA':         ['NT', 'SA'],
        'NT':         ['WA', 'SA', 'Queensland'],
        'Queensland': ['NT', 'SA', 'NSW'],
        'SA':         ['WA', 'NT', 'Queensland', 'NSW', 'V'],
        'NSW':        ['Queensland', 'SA', 'V'],
        'V':          ['SA', 'NSW'],
        'T':          []  # Tasmania is an island – no land neighbors
    }

    def diff(a, b):
        return a != b

    constraints = {}
    for var in variables:
        constraints[var] = [(nbr, diff) for nbr in adjacency[var]]

    solution = solve_csp(variables, domains, constraints)

    if solution:
        print("\nSolution found:")
        for region, color in solution.items():
            print(f"  {region:15s} -> {color}")
        # Verify
        violations = 0
        for var, neighbors in adjacency.items():
            for nbr in neighbors:
                if solution[var] == solution[nbr]:
                    violations += 1
                    print(f"  VIOLATION: {var} and {nbr} both {solution[var]}")
        if violations == 0:
            print("\n  All constraints satisfied!")
        visualize_solution(solution, adjacency)
    else:
        print("No solution found.")
    print()


if __name__ == '__main__':
    solve_australia()
