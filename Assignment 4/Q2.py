import random
import csv

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def solve_csp(variables, domains, constraints):
    def is_consistent(variable, value, assignment):
        for neighbor in constraints[variable]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True

    def backtrack(assignment):
        if len(assignment) == len(variables):
            return dict(assignment)

        for variable in variables:
            if variable not in assignment:
                current = variable
                break

        for value in domains[current]:
            if is_consistent(current, value, assignment):
                assignment[current] = value
                result = backtrack(assignment)
                if result is not None:
                    return result
                del assignment[current]
        return None

    return backtrack({})


def visualize_telangana(solution):
    if plt is None:
        print("\nVisualization skipped: install matplotlib to draw the districts (pip install matplotlib).")
        return

    positions = {
        'Adilabad': (0.10, 0.95),
        'Kumurambheem': (0.30, 0.92),
        'Mancherial': (0.35, 0.82),
        'Nirmal': (0.10, 0.82),
        'Nizamabad': (0.08, 0.65),
        'Kamareddy': (0.22, 0.58),
        'Jagtial': (0.48, 0.74),
        'Karimnagar': (0.52, 0.62),
        'Peddapalli': (0.42, 0.54),
        'Rajanna_Sircilla': (0.55, 0.46),
        'Medak': (0.20, 0.40),
        'Sangareddy': (0.10, 0.28),
        'Siddipet': (0.50, 0.34),
        'Medchal': (0.60, 0.26),
        'Hyderabad': (0.60, 0.18),
        'Rangareddy': (0.45, 0.10),
        'Vikarabad': (0.34, 0.06),
        'Nalgonda': (0.65, 0.12),
        'Yadadri': (0.72, 0.26),
        'Suryapet': (0.78, 0.42),
        'Mahabubabad': (0.72, 0.60),
        'Khammam': (0.88, 0.72),
        'Bhadradri': (0.94, 0.84),
        'Mulugu': (0.80, 0.88),
        'Warangal_Rural': (0.58, 0.58),
        'Warangal_Urban': (0.64, 0.52),
        'Hanamkonda': (0.68, 0.56),
        'Gadwal': (0.32, 0.04),
        'Wanaparthy': (0.22, 0.02),
        'Nagarkurnool': (0.30, 0.18),
        'Mahabubnagar': (0.40, 0.14),
        'Jogulamba': (0.24, 0.10),
    }

    base_colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'cyan', 'magenta']
    selected_colors = random.sample(base_colors, 4)
    color_map = {
        'Red': selected_colors[0],
        'Green': selected_colors[1],
        'Blue': selected_colors[2],
        'Yellow': selected_colors[3]
    }

    fig, ax = plt.subplots(figsize=(12, 10))
    for district in solution:
        x, y = positions.get(district, (0.5, 0.5))
        color_name = color_map[solution[district]]
        ax.scatter(x, y, color=color_name, s=300, edgecolor='black', marker='o')
        ax.text(x, y, district.replace('_', ' '), fontsize=8,
                ha='center', va='center', color='black')

    ax.set_title('Telangana District Coloring (Approximate Map)', fontsize=16)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    plt.show()


def save_solution_csv(solution, filename='telangana_district_colors.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['District', 'Color'])
        for district in sorted(solution):
            writer.writerow([district, solution[district]])
    print(f"Solution saved to {filename}")


def save_adjacency_csv(adjacency, filename='telangana_adjacency.csv'):
    seen = set()
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['District', 'AdjacentDistrict'])
        for district in sorted(adjacency):
            for neighbor in sorted(adjacency[district]):
                pair = tuple(sorted((district, neighbor)))
                if pair in seen:
                    continue
                seen.add(pair)
                writer.writerow([pair[0], pair[1]])
    print(f"Adjacency saved to {filename}")


def count_violations(solution, adjacency):
    violations = []
    for district, neighbors in adjacency.items():
        for neighbor in neighbors:
            if district < neighbor and solution.get(district) == solution.get(neighbor):
                violations.append((district, neighbor))
    return violations


def solve_telangana():
    print("=" * 60)
    print("PROBLEM 2: Telangana Map Coloring (33 districts)")
    print("=" * 60)
 
    districts = [
        'Adilabad', 'Kumurambheem', 'Mancherial', 'Nirmal', 'Nizamabad',
        'Jagtial', 'Peddapalli', 'Karimnagar', 'Rajanna_Sircilla', 'Kamareddy',
        'Medak', 'Siddipet', 'Jayashankar', 'Mulugu', 'Bhadradri',
        'Khammam', 'Suryapet', 'Nalgonda', 'Mahabubabad', 'Jangaon',
        'Warangal_Urban', 'Warangal_Rural', 'Hanamkonda', 'Yadadri', 'Medchal',
        'Hyderabad', 'Rangareddy', 'Vikarabad', 'Sangareddy', 'Mahabubnagar',
        'Nagarkurnool', 'Wanaparthy', 'Gadwal', 'Jogulamba'
    ]
 
    raw_adjacency = {
        'Adilabad':        ['Kumurambheem', 'Mancherial', 'Nirmal'],
        'Kumurambheem':    ['Adilabad', 'Mancherial', 'Jayashankar'],
        'Mancherial':      ['Adilabad', 'Kumurambheem', 'Peddapalli', 'Jagtial', 'Nirmal'],
        'Nirmal':          ['Adilabad', 'Mancherial', 'Jagtial', 'Nizamabad', 'Kamareddy'],
        'Nizamabad':       ['Nirmal', 'Kamareddy', 'Medak', 'Sangareddy'],
        'Jagtial':         ['Mancherial', 'Nirmal', 'Karimnagar', 'Peddapalli', 'Rajanna_Sircilla', 'Kamareddy'],
        'Peddapalli':      ['Mancherial', 'Jagtial', 'Karimnagar', 'Jayashankar', 'Mulugu'],
        'Karimnagar':      ['Jagtial', 'Peddapalli', 'Rajanna_Sircilla', 'Siddipet', 'Jangaon'],
        'Rajanna_Sircilla':['Jagtial', 'Karimnagar', 'Siddipet', 'Kamareddy'],
        'Kamareddy':       ['Nirmal', 'Nizamabad', 'Jagtial', 'Rajanna_Sircilla', 'Medak', 'Sangareddy'],
        'Medak':           ['Nizamabad', 'Kamareddy', 'Siddipet', 'Sangareddy', 'Medchal'],
        'Siddipet':        ['Karimnagar', 'Rajanna_Sircilla', 'Kamareddy', 'Medak', 'Jangaon', 'Yadadri', 'Medchal'],
        'Jayashankar':     ['Kumurambheem', 'Peddapalli', 'Mulugu', 'Bhadradri', 'Mahabubabad', 'Warangal_Rural'],
        'Mulugu':          ['Peddapalli', 'Jayashankar', 'Bhadradri', 'Warangal_Rural'],
        'Bhadradri':       ['Jayashankar', 'Mulugu', 'Khammam', 'Mahabubabad'],
        'Khammam':         ['Bhadradri', 'Mahabubabad', 'Suryapet', 'Nalgonda'],
        'Suryapet':        ['Khammam', 'Mahabubabad', 'Nalgonda', 'Yadadri'],
        'Nalgonda':        ['Khammam', 'Suryapet', 'Yadadri', 'Rangareddy', 'Mahabubnagar'],
        'Mahabubabad':     ['Jayashankar', 'Bhadradri', 'Khammam', 'Suryapet', 'Jangaon', 'Warangal_Rural'],
        'Jangaon':         ['Karimnagar', 'Siddipet', 'Mahabubabad', 'Warangal_Urban', 'Yadadri'],
        'Warangal_Urban':  ['Jangaon', 'Warangal_Rural', 'Hanamkonda'],
        'Warangal_Rural':  ['Jayashankar', 'Mulugu', 'Mahabubabad', 'Jangaon', 'Warangal_Urban', 'Hanamkonda'],
        'Hanamkonda':      ['Warangal_Urban', 'Warangal_Rural'],
        'Yadadri':         ['Siddipet', 'Jangaon', 'Suryapet', 'Nalgonda', 'Medchal'],
        'Medchal':         ['Medak', 'Siddipet', 'Yadadri', 'Hyderabad', 'Rangareddy'],
        'Hyderabad':       ['Medchal', 'Rangareddy'],
        'Rangareddy':      ['Medchal', 'Hyderabad', 'Nalgonda', 'Vikarabad', 'Sangareddy', 'Mahabubnagar'],
        'Vikarabad':       ['Rangareddy', 'Sangareddy', 'Mahabubnagar', 'Nagarkurnool'],
        'Sangareddy':      ['Nizamabad', 'Kamareddy', 'Medak', 'Rangareddy', 'Vikarabad'],
        'Mahabubnagar':    ['Nalgonda', 'Rangareddy', 'Vikarabad', 'Nagarkurnool', 'Wanaparthy', 'Gadwal', 'Jogulamba'],
        'Nagarkurnool':    ['Vikarabad', 'Mahabubnagar', 'Wanaparthy'],
        'Wanaparthy':      ['Nagarkurnool', 'Mahabubnagar', 'Gadwal'],
        'Gadwal':          ['Mahabubnagar', 'Wanaparthy', 'Jogulamba'],
        'Jogulamba':       ['Mahabubnagar', 'Gadwal'],
    }
    districts_set = set(districts)
    adjacency = {district: set() for district in districts}
    for district, neighbors in raw_adjacency.items():
        if district not in districts_set:
            continue
        for neighbor in neighbors:
            if neighbor in districts_set:
                adjacency[district].add(neighbor)
                adjacency[neighbor].add(district)
    adjacency = {district: sorted(neighbors) for district, neighbors in adjacency.items()}
 
    colors = ['Red', 'Green', 'Blue', 'Yellow']
    domains = {v: colors[:] for v in districts}
 
    def diff(a, b):
        return a != b
 
    constraints = adjacency
 
    solution = solve_csp(districts, domains, constraints)
 
    if solution:
        print("\nSolution found (district -> color):")
        for district in sorted(districts):
            print(f"  {district:25s} -> {solution[district]}")

        violations = 0
        violations = count_violations(solution, adjacency)
        if not violations:
            print(f"\n  All {len(solution)} districts colored. No violations!")
        else:
            print(f"\n  {len(violations)} violations found:")
            for a, b in violations:
                print(f"    {a} and {b}")

        save_solution_csv(solution)
        save_adjacency_csv(adjacency)
        visualize_telangana(solution)
    else:
        print("No solution found.")
    print()


if __name__ == '__main__':
    solve_telangana()
