from states import get_next_states


def dls(state, goal, capacity_a, capacity_b, limit, path, visited):
    a, b = state
    if a == goal: return path + [state]
    if limit <= 0: return None
    
    visited.add(state)
    for next_state in get_next_states(a, b, capacity_a, capacity_b):
        if next_state not in visited:
            res = dls(next_state, goal, capacity_a, capacity_b, limit - 1, path + [state], visited.copy())
            if res: return res
    return None