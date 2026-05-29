The program dynamically builds a game tree based on custom numbers provided by the user and executes the algorithms sequentially to find the optimal choices.

Implemented Algorithms
Minimax Search: A foundational decision making algorithm that computes the optimal move for a player, assuming the opponent is also playing optimally.

Alpha-Beta Pruning: An optimized variant of Minimax that cuts off branches in the game tree that cannot possibly influence the final decision, drastically reducing computation time.

Heuristic Alpha-Beta Search: A real world modification that stops searching deeper into the tree once a specified depth cutoff is reached, evaluating non terminal states using an evaluation metric.

Monte Carlo Tree Search MCTS: A simulation driven algorithm that makes choices by executing randomized games rollouts and balances exploration vs exploitation using the UCB1 formula.

How to Run the Program
Prerequisites
Python 3.x installed on your computer.

No external packages or libraries are required built purely using native Python math and random modules.

Steps to Execute
Open your terminal or command prompt.

Navigate to the directory containing the file:
cd path to your folder

Run the script using Python:
python search_algo.py

How the Interactive Interface Works
When you run the script, it will guide you through the setup of a complete binary game tree of Depth 3, which requires exactly 8 leaf values:

User Input: The program will prompt you 8 times to enter score values for each leaf node. It includes strict validation loops to ensure you enter valid numeric scores.

Execution: Once the tree is populated, it automatically runs all 4 search techniques over your custom tree.

Console Output: The system instantly prints the comparative evaluation outcomes, showing how Alpha-Beta saves work while achieving the exact same result as Minimax.

Sample execution input/putput given.
