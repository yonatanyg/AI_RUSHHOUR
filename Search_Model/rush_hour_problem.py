from search_smodel import SearchProblem
from board import Board

class Rush_Hour_Targets_Problem(SearchProblem):
    def __init__(self, board_size, vehicles, targets):
        """
        Initializes the search problem using the given board size, vehicles, and targets.

        Args:
            board_size (int): The size of the board.
            vehicles (list): List of vehicle dictionaries.
            targets (set): Set of target coordinates.
        """
        self.board = Board(board_size, vehicles, targets)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        return self.board

    def is_goal_state(self, state):
        """
        Returns True if and only if the state is a valid goal state.

        Args:
            state: The current state of the board.
        """
        # Goal state is reached when all targets are collected
        return len(state.reached_targets) == len(state.targets)

    def get_successors(self, state):
        """
        For a given state, returns a list of triples (successor, action, stepCost).

        Args:
            state: The current state of the board.
        """

        self.expanded = self.expanded + 1

        successors = []
        
        
        for vehicle in state.vehicles:
            for direction in ['left', 'right', 'up', 'down']:
                board_copy = state.copy()      
                if board_copy.move_vehicle(vehicle['symbol'], direction):
                    new_state = board_copy
                    action = (vehicle['symbol'], direction)
                    successors.append((new_state, action, 1))
        
        return successors

    def get_cost_of_actions(self, actions):
        """
        Returns the total cost of a particular sequence of actions.

        Args:
            actions: A list of actions to take.
        """
        return len(actions)
