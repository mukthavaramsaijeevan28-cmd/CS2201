from DFS import dfs
from BFS import bfs
from DLS import dls
from IDDFS import iddfs

CAP_A = 4
CAP_B = 3
GOAL = 2

print(f"Goal: Measure {GOAL}L using {CAP_A}L and {CAP_B}L jugs.\n")

# BFS Results
bfs_res = bfs(CAP_A, CAP_B, GOAL)
print(f"BFS:    Steps: {len(bfs_res)-1 if bfs_res else 'N/A'} | Path: {bfs_res}")

# DFS Results
dfs_res = dfs(CAP_A, CAP_B, GOAL)
print(f"DFS:    Steps: {len(dfs_res)-1 if dfs_res else 'N/A'} | Path: {dfs_res}")

# DLS Results (Hardcoded limit of 5 - may fail if goal is deeper)
dls_limit = 5
dls_res = dls((0, 0), GOAL, CAP_A, CAP_B, dls_limit, [], set())
print(f"DLS({dls_limit}): Steps: {len(dls_res)-1 if dls_res else 'Failed (Limit too low)'}")

# IDDFS Results
iddfs_res = iddfs(CAP_A, CAP_B, GOAL, 10)
print(f"IDDFS:  Steps: {len(iddfs_res)-1 if iddfs_res else 'N/A'} | Path: {iddfs_res}")