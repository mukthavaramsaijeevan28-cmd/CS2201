import math
import random


def minimax(depth, node_index, is_max, leaves, alpha=None, beta=None, use_pruning=False):
    """
    Combines Minimax and Alpha-Beta Search based on flags.
    """
    # Base Case: Leaf node reached (Depth 3 for a binary tree with 8 leaves)
    if depth == 3:
        return leaves[node_index]
    
    if is_max:
        best = -math.inf
        for i in range(2):
            val = minimax(depth + 1, node_index * 2 + i, False, leaves, alpha, beta, use_pruning)
            best = max(best, val)
            if use_pruning:
                alpha = max(alpha, best)
                if beta <= alpha:
                    break  # Beta cutoff
        return best
    else:
        best = math.inf
        for i in range(2):
            val = minimax(depth + 1, node_index * 2 + i, True, leaves, alpha, beta, use_pruning)
            best = min(best, val)
            if use_pruning:
                beta = min(beta, best)
                if beta <= alpha:
                    break  # Alpha cutoff
        return best


def dummy_heuristic_evaluation(state, user_heuristic_avg):
    """Uses a baseline around the user's average input to simulate a heuristic evaluation"""
    return random.randint(int(user_heuristic_avg - 5), int(user_heuristic_avg + 5))

def heuristic_alpha_beta(state, depth, max_depth, alpha, beta, is_max, user_heuristic_avg):
    """Cutoff search at max_depth using a dynamic heuristic evaluation"""
    if depth == max_depth:
        return dummy_heuristic_evaluation(state, user_heuristic_avg)
        
    if is_max:
        best = -math.inf
        for move in ["left_branch", "right_branch"]:
            val = heuristic_alpha_beta(move, depth + 1, max_depth, alpha, beta, False, user_heuristic_avg)
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha: break
        return best
    else:
        best = math.inf
        for move in ["left_branch", "right_branch"]:
            val = heuristic_alpha_beta(move, depth + 1, max_depth, alpha, beta, True, user_heuristic_avg)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha: break
        return best


class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

def ucb1(node):
    if node.visits == 0:
        return math.inf
    return (node.wins / node.visits) + 1.41 * math.sqrt(math.log(node.parent.visits) / node.visits)

def monte_carlo_tree_search(root_state, iterations=100):
    root = MCTSNode(root_state)
    
    for _ in range(iterations):
        # 1. Selection
        node = root
        while node.children:
            node = max(node.children, key=ucb1)
            
        # 2. Expansion
        if node.visits > 0:
            for i in range(2):
                node.children.append(MCTSNode(state=f"{node.state}_child{i}", parent=node))
            if node.children:
                node = node.children[0]
                
        # 3. Simulation (Rollout)
        reward = random.choice([0, 1])
        
        # 4. Backpropagation
        while node is not None:
            node.visits += 1
            node.wins += reward
            node = node.parent
            
    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.state, best_child.wins / best_child.visits



print("INTERACTIVE ADVERSARIAL SEARCH TESTER")
print("To construct a complete game tree of depth 3, please enter 8 score values.\n")

user_leaves = []
for i in range(8):
    while True:
        try:
            val = float(input(f"Enter score value for Leaf Node #{i+1}: "))
            user_leaves.append(val)
            break
        except ValueError:
            print("Invalid input! Please enter a valid number.")

average_score = sum(user_leaves) / len(user_leaves)

print("\n--- PROCESSING SEARCH RESULTS BASED ON YOUR INPUTS ---")
print(f"Your Game Tree Leaves: {user_leaves}\n")

print(f"1. Minimax Value: {minimax(0, 0, True, user_leaves)}")
print(f"2. Alpha-Beta Value: {minimax(0, 0, True, user_leaves, -math.inf, math.inf, use_pruning=True)}")
print(f"3. Heuristic Alpha-Beta Value (Cutoff depth 2): {heuristic_alpha_beta('root', 0, 2, -math.inf, math.inf, True, average_score)}")
print(f"4. MCTS Simulation Decision & Projected Win Rate: {monte_carlo_tree_search('root_game_state')}")