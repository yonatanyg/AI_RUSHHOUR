"""
In search_smodel.py, you will implement generic search algorithms
"""

import collections
import util_smodel


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util_smodel.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util_smodel.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util_smodel.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util_smodel.raiseNotDefined()

def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    This function implements a graph search algorithm using depth-first search.
    """
    stack = [(problem.get_start_state(), [], 0)]  # (state, actions, cost)
    visited = set()
    counter = 0

    while stack:
        state, actions, cost = stack.pop()

        # Formalize the current state
        formalized_state = FormalizeBoard(state)

        # Check if the state is the goal state
        if problem.is_goal_state(state):
            return actions, counter

        # If the state has not been visited, mark it as visited
        if formalized_state not in visited:
            visited.add(formalized_state)
            counter += 1  # Increment the expanded nodes counter

            # Process each successor
            for successor, action, step_cost in problem.get_successors(state):
                formalized_successor = FormalizeBoard(successor)
                if formalized_successor not in visited:
                    new_actions = actions + [action]
                    new_cost = cost + step_cost
                    stack.append((successor, new_actions, new_cost))

    return [], counter


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    # Initialize the visited set and the queue
    visited = set()
    start_state = problem.get_start_state()
    start_state_formalized = FormalizeBoard(start_state)
    queue = collections.deque([(start_state, [], 0)])
    visited.add(start_state_formalized)

    counter = 0

    while queue:
        # Dequeue a state from the queue
        state, actions, total_cost = queue.popleft()

        # Check if the state is a goal state
        if problem.is_goal_state(state):
            return actions, counter

        # Enqueue successors if not visited
        for successor, action, step_cost in problem.get_successors(state):
            successor_formalized = FormalizeBoard(successor)
            if successor_formalized not in visited:
                counter += 1
                visited.add(successor_formalized)
                queue.append((successor, actions + [action], total_cost + step_cost))

    return [], counter


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "* YOUR CODE HERE *"
    start = problem.get_start_state()
    visited = set()
    priority_queue = util_smodel.PriorityQueue()
    counter = 0
    priority_queue.push((0, counter, [], start), 0)

    while priority_queue:
        cost, c, actions, node = priority_queue.pop()

        if node not in visited:
            visited.add(node)

            if problem.is_goal_state(node):
                return actions

            for successor, action, step_cost in problem.get_successors(node):
                if successor not in visited:
                    counter += 1
                    priority_queue.push((cost+step_cost, counter, actions+[action], successor), cost+step_cost)



def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def target_heuristic(state, problem=None):
    return len(state.targets) - len(state.reached_targets)


def distance_helper(pos_a,pos_b):
    return abs(pos_b[0] - pos_a[0]) + abs (pos_b[1] - pos_a[1])

def find_character_2d(lst, char):
    for i, row in enumerate(lst):
        for j, element in enumerate(row):
            if element == char:
                return (i, j)
    return None  # Return None if the character is not found

def max_distance_heuristic(state, problem = None):
    red_pos = find_character_2d(state.board, "X")

    furthest = (state.board_size-1,state.board_size-1)
    max1 = 0
    for target in state.targets:
        if (target in state.reached_targets):
            continue
        cur = distance_helper(red_pos,target)
        if cur > max1:
            max1 = cur
            furthest = target

    return max1 + distance_helper(furthest,(state.board_size-1, state.board_size-1))

def FormalizeBoard(board):
    return (tuple(tuple(row) for row in board.board), tuple(sorted(board.reached_targets)))

def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    start = problem.get_start_state()
    visited = set()
    priority_queue = util_smodel.PriorityQueue()
    counter = 0
    priority_queue.push((0, counter, [], start), 0)

    while not priority_queue.isEmpty():
        cost, c, actions, node = priority_queue.pop()
        formalized_node = FormalizeBoard(node)

        if formalized_node not in visited:
            visited.add(formalized_node)

            if problem.is_goal_state(node):
                return actions,counter

            for successor, action, step_cost in problem.get_successors(node):
                formalized_successor = FormalizeBoard(successor)
                if formalized_successor not in visited:
                    counter += 1
                    new_cost = cost + step_cost
                    priority_queue.push((new_cost, counter, actions + [action], successor), new_cost + heuristic(successor, problem))

    return [],counter  # Return an empty list if no solution is found


"""
def target_heuristic(state,problem=None):
    return 4 * (len(state.targets) - len(state.reached_targets))

def FormalizeBoard(board):
    return (tuple(tuple(row) for row in board.board),tuple(sorted(board.reached_targets)))

def a_star_search(problem, heuristic=null_heuristic):
    "*** YOUR CODE HERE ***"

    start = problem.get_start_state()
    visited = set()
    priority_queue = util.PriorityQueue()
    counter = 0
    priority_queue.push((0, counter, [], start), 0)

    while priority_queue:

        cost, c, actions, node = priority_queue.pop()

        for i in range(len(node.board)):
            print(node.board[i])

        if FormalizeBoard(node) not in visited:
            visited.add(FormalizeBoard(node))

            if problem.is_goal_state(node):
                return actions

            for successor, action, step_cost in problem.get_successors(node):
                if FormalizeBoard(successor) not in visited:
                    counter += 1
                    priority_queue.push((cost + step_cost, counter, actions + [action], successor), cost + step_cost
                                        + heuristic(successor, problem) )
"""


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
