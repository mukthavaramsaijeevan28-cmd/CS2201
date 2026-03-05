from collections import deque
from states import get_next_states

def bfs(capacity_a, capacity_b, goal):
    queue = deque([((0, 0), [])]) # (current_state, path)
    visited = set([(0, 0)])

    while queue:
        (a, b), path = queue.popleft()
        if a == goal: return path + [(a, b)]

        for state in get_next_states(a, b, capacity_a, capacity_b):
            if state not in visited:
                visited.add(state)
                queue.append((state, path + [(a, b)]))
    return None