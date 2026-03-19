import heapq
import math
import random

FREE = 0
OBSTACLE = 1
INF = float("inf")

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def key(s, g_rhs, g_cost, start, km):
    return (min(g_rhs[s], g_cost.get(s, INF)) + heuristic(s, start) + km,
            min(g_rhs[s], g_cost.get(s, INF)))

def successors(state, grid):
    r,c = state
    dirs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    for dr,dc in dirs:
        nr,nc = r+dr,c+dc
        if 0<=nr<len(grid) and 0<=nc<len(grid[0]):
            yield (nr,nc)

def c(u,v,grid):
    if grid[v[0]][v[1]]==OBSTACLE: return INF
    if u[0]!=v[0] and u[1]!=v[1]: return math.sqrt(2)
    return 1.0

def init(grid,start,goal):
    U=[]  # priority queue
    g_cost={}
    rhs={}
    km=0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            rhs[(r,c)] = INF
            g_cost[(r,c)] = INF
    rhs[goal]=0
    heapq.heappush(U,(key(goal,rhs,g_cost,start,km),goal))
    return U,g_cost,rhs,km

def update_vertex(u, U, g_cost, rhs, grid, start, km):
    if u != goal:
        rhs[u] = min(c(u,s,grid)+g_cost[s] for s in successors(u,grid))
    # remove old entries for u from U lazily
    heapq.heappush(U,(key(u,rhs,g_cost,start,km),u))

def compute_shortest_path(U, g_cost, rhs, grid, start, goal, km):
    while U:
        k_old, u = heapq.heappop(U)
        if k_old > key(start,rhs,g_cost,start,km) and rhs[start]==g_cost[start]:
            break
        if g_cost[u] > rhs[u]:
            g_cost[u] = rhs[u]
        else:
            g_cost[u] = INF
            update_vertex(u,U,g_cost,rhs,grid,start,km)
        for s in successors(u,grid):
            update_vertex(s,U,g_cost,rhs,grid,start,km)

def reconstruct_path(g_cost,start,goal,grid):
    if g_cost[start]==INF:
        return []
    path=[start]; u=start
    while u != goal:
        neigh = list(successors(u,grid))
        neigh.sort(key=lambda v: g_cost[v] + c(u,v,grid))
        u = neigh[0]
        if g_cost[u] == INF:
            return []
        path.append(u)
    return path

def dynamic_obstacle_step(grid,p):
    new_grid=[row[:] for row in grid]
    rng = random.Random()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if new_grid[r][c]==FREE and (r,c)!=p:
                if rng.random()<0.02:
                    new_grid[r][c]=OBSTACLE
    return new_grid

def print_grid(grid,path,start,goal):
    s=set(path)
    for r in range(len(grid)):
        line=''
        for c in range(len(grid[0])):
            if (r,c)==start: line+='A'
            elif (r,c)==goal: line+='G'
            elif (r,c) in s: line+='*'
            elif grid[r][c]==OBSTACLE: line+='#'
            else: line+='.'
        print(line)
    print()

if __name__=="__main__":
    print("UGV Dynamic D* Lite Planning")
    print("Enter settings (press Enter for defaults):")

    try:
        R = int(input("Grid rows [default 30]: ") or "30")
        C = int(input("Grid cols [default 30]: ") or "30")
        density = float(input("Obstacle density [0-1] [default 0.20]: ") or "0.20")
        dyn_prob = float(input("Dynamic obstacle probability per step [0-1] [default 0.02]: ") or "0.02")
        sr = int(input(f"Start row [0-{R-1}] [default 0]: ") or "0")
        sc = int(input(f"Start col [0-{C-1}] [default 0]: ") or "0")
        gr = int(input(f"Goal row [0-{R-1}] [default {R-1}]: ") or str(R-1))
        gc = int(input(f"Goal col [0-{C-1}] [default {C-1}]: ") or str(C-1))
        show_grid = input("Show grid each 10 steps? [y/N]: ").strip().lower() in ('y','yes')
    except ValueError as e:
        print("Invalid input; using default parameters.")
        R,C = 30,30
        density = 0.20
        dyn_prob = 0.02
        sr,sc,gr,gc = 0,0,R-1,C-1
        show_grid = False

    print("\nConfiguration:")
    print(f" Grid size            : {R} x {C}")
    print(f" Obstacle density     : {density}")
    print(f" Dynamic prob         : {dyn_prob}")
    print(f" Start                : ({sr},{sc})")
    print(f" Goal                 : ({gr},{gc})")
    print(f" Show grid            : {show_grid}\n")

    grid = [[OBSTACLE if random.random() < density else FREE for _ in range(C)] for _ in range(R)]
    start = (max(0,min(sr,R-1)), max(0,min(sc,C-1)))
    goal  = (max(0,min(gr,R-1)), max(0,min(gc,C-1)))
    grid[start[0]][start[1]] = FREE
    grid[goal[0]][goal[1]] = FREE

    U, g_cost, rhs, km = init(grid,start,goal)
    compute_shortest_path(U,g_cost,rhs,grid,start,goal,km)

    current=start
    step=0
    while current!=goal and step<1000:
        path=reconstruct_path(g_cost,current,goal,grid)
        if not path:
            print("No current path found")
            break

        next_step = path[1]
        current = next_step
        print(f"Step {step} -> {current}")

        # apply dynamic obstacles
        grid = dynamic_obstacle_step(grid,current)
        for r in range(R):
            for c in range(C):
                if random.random() < dyn_prob and (r,c)!=current and (r,c)!=goal:
                    grid[r][c] = OBSTACLE

        if grid[current[0]][current[1]]==OBSTACLE:
            print("Crashed into dynamic obstacle at current location")
            break

        km += heuristic(start,current)
        start = current
        for n in successors(current,grid):
            if grid[n[0]][n[1]] == OBSTACLE:
                rhs[n] = INF
            update_vertex(n,U,g_cost,rhs,grid,start,km)

        compute_shortest_path(U,g_cost,rhs,grid,start,goal,km)

        if show_grid:
            print_grid(grid,path,start,goal)

        step += 1

    if current == goal:
        print("Reached goal!")
    else:
        print("Stopped before goal.")