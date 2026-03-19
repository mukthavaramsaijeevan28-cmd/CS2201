import heapq
import random
import time
import math

# Constants
GRID_SIZE   = 70          # 70 × 70 km grid (1 cell = 1 km)
FREE        = 0
OBSTACLE    = 1
DENSITY     = {"LOW": 0.10, "MEDIUM": 0.25, "HIGH": 0.40}

# Grid generation
def generate_grid(size: int, density: float, seed: int = 42):
    """Create a random obstacle grid; start (0,0) and goal (size-1,size-1) always free."""
    rng = random.Random(seed)
    grid = [[OBSTACLE if rng.random() < density else FREE for _ in range(size)] for _ in range(size)]
    grid[0][0] = FREE
    grid[size - 1][size - 1] = FREE
    return grid


#Heuristic function for A* search
def heuristic(a, b, mode="euclidean"):
    
    if mode == "euclidean":
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# A* Search
def astar(grid, start: tuple, goal: tuple):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    DIRS = [(-1,0),(1,0),(0,-1),(0,1),          # cardinal  cost 1.0
            (-1,-1),(-1,1),(1,-1),(1,1)]          # diagonal  cost √2
    MOVE_COST = [1.0]*4 + [math.sqrt(2)]*4

    g = {start: 0.0}
    prev = {start: None}
    visited = set()
    nodes_expanded  = 0
    nodes_generated = 1

    # (f, g, node)
    pq = [(heuristic(start, goal), 0.0, start)]

    t0 = time.perf_counter()

    while pq:
        f, cost, u = heapq.heappop(pq)

        if u in visited:
            continue
        visited.add(u)
        nodes_expanded += 1

        if u == goal:
            break

        r, c = u
        for (dr, dc), move_cost in zip(DIRS, MOVE_COST):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == FREE:
                v = (nr, nc)
                new_g = cost + move_cost
                if new_g < g.get(v, float('inf')):
                    g[v] = new_g
                    prev[v] = u
                    nodes_generated += 1
                    heapq.heappush(pq, (new_g + heuristic(v, goal), new_g, v))

    elapsed_ms = (time.perf_counter() - t0) * 1000

    # Reconstruct path
    if goal not in visited:
        return [], nodes_expanded, nodes_generated, elapsed_ms, visited

    path, node = [], goal
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path, nodes_expanded, nodes_generated, elapsed_ms, visited


#Measures of Effectiveness 
def measures_of_effectiveness(grid, path, nodes_expanded, nodes_generated,
                               elapsed_ms, density_label):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    total_cells  = rows * cols
    obstacle_cnt = sum(cell == OBSTACLE for row in grid for cell in row)
    path_len     = len(path)
    path_cost    = 0.0
    for i in range(1, path_len):
        dr = abs(path[i][0] - path[i-1][0])
        dc = abs(path[i][1] - path[i-1][1])
        path_cost += math.sqrt(2) if (dr + dc == 2) else 1.0

    straight_line = math.sqrt((rows-1)**2 + (cols-1)**2)
    optimality_ratio = path_cost / straight_line if straight_line > 0 else float('inf')
    branching_factor = nodes_generated / max(nodes_expanded, 1)

    print("\n" + "═"*55)
    print(f"  MEASURES OF EFFECTIVENESS  [{density_label} density]")
    print("═"*55)
    print(f"  Grid size              : {rows} × {cols} = {total_cells} cells")
    print(f"  Obstacle count         : {obstacle_cnt} ({100*obstacle_cnt/total_cells:.1f}%)")
    print(f"  Path found             : {'Yes' if path_len > 0 else 'No'}")
    if path_len:
        print(f"  Path length (hops)     : {path_len - 1}")
        print(f"  Path cost (km)         : {path_cost:.2f}")
        print(f"  Straight-line dist     : {straight_line:.2f} km")
        print(f"  Optimality ratio       : {optimality_ratio:.4f}  (1.0 = perfect)")
    print(f"  Nodes expanded         : {nodes_expanded}")
    print(f"  Nodes generated        : {nodes_generated}")
    print(f"  Effective branch factor: {branching_factor:.2f}")
    print(f"  Time elapsed           : {elapsed_ms:.2f} ms")
    print("═"*55)


#Visualisation 
def visualize(grid, path, visited, start, goal, density_label, filename):
    # Matplotlib removed; this is now a no-op placeholder.
    print(f"  [INFO] Visualization skipped (matplotlib not used) for {filename}")


def display_grid(grid, path, start, goal):
    path_set = set(path)
    for r in range(len(grid)):
        row_chars = []
        for c in range(len(grid[0])):
            if (r, c) == start:
                row_chars.append('S')
            elif (r, c) == goal:
                row_chars.append('G')
            elif (r, c) in path_set:
                row_chars.append('*')
            elif grid[r][c] == OBSTACLE:
                row_chars.append('#')
            else:
                row_chars.append('.')
        print(''.join(row_chars))


if __name__ == "__main__":
    print("=" * 55)
    print("  UGV PATH PLANNING  —  70×70 km Battlefield Grid")
    print("  Algorithm : A* Search (8-directional movement)")
    print("=" * 55)

    try:
        sr = int(input("  Start row   (0-69): ") or 0)
        sc = int(input("  Start col   (0-69): ") or 0)
        gr = int(input("  Goal row    (0-69): ") or 69)
        gc = int(input("  Goal col    (0-69): ") or 69)
    except ValueError:
        print("Invalid start/goal coordinates. Using defaults 0,0 -> 69,69.")
        sr, sc, gr, gc = 0, 0, GRID_SIZE - 1, GRID_SIZE - 1

    dens_str = input("Density [LOW/MEDIUM/HIGH] (default MEDIUM): ").strip().upper() or "MEDIUM"
    dens = DENSITY.get(dens_str, 0.25)
    label = dens_str if dens_str in DENSITY else "CUSTOM"

    show_grid = input("Show grid in console? [y/N]: ").strip().lower() in ('y', 'yes')

    grid = generate_grid(GRID_SIZE, dens)
    grid[sr][sc] = FREE
    grid[gr][gc] = FREE

    path, n_exp, n_gen, elapsed, visited = astar(grid, (sr, sc), (gr, gc))

    if show_grid:
        print("\nGrid visualization (S=start, G=goal, *=path, #=obstacle, .=free):")
        display_grid(grid, path, (sr, sc), (gr, gc))

    if path:
        measures_of_effectiveness(grid, path, n_exp, n_gen, elapsed, label)
        visualize(grid, path, visited, (sr, sc), (gr, gc), label, "ugv_static.png")
    else:
        print(f"  ✗ No path found for density {label} ({elapsed:.2f} ms, {n_exp} nodes expanded)")