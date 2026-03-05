def get_next_states(a, b, capacity_a, capacity_b):
    return [
        (capacity_a, b), (a, capacity_b), # Fill
        (0, b), (a, 0),   # Empty
        (a - min(a, capacity_b - b), b + min(a, capacity_b - b)), # Pour A to B
        (a + min(b, capacity_a - a), b - min(b, capacity_a - a))  # Pour B to A
    ]