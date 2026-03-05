from states import get_next_states

def dfs(capacity_a, capacity_b, goal):
    stack = [((0, 0), [])]
    visited = set()

    while stack:
        (a, b), path = stack.pop()
        if a == goal: return path + [(a, b)]
        
        if (a, b) in visited: continue
        visited.add((a, b))

        for state in get_next_states(a, b, capacity_a, capacity_b):
            if state not in visited:
                stack.append((state, path + [(a, b)]))
    return None