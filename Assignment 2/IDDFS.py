from DLS import dls

def iddfs(capacity_a, capacity_b, goal, max_depth):
    for limit in range(max_depth):
        result = dls((0, 0), goal, capacity_a, capacity_b, limit, [], set())
        if result: return result
    return None