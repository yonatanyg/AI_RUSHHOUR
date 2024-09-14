# rush_hour_game.py
import json
import argparse
import pygame
import time
from board import Board

from search_smodel import astar,null_heuristic, target_heuristic,bfs,dfs, max_distance_heuristic
from Search_Model.rush_hour_problem import Rush_Hour_Targets_Problem

from Planning_Model.planning_problem import plan_solve
from Planning_Model.rush_hour_planner import create_problem_file, create_domain_file


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [RED, GREEN, BLUE, YELLOW]


class RushHourGame:
    def __init__(self, board_size, vehicles_file, targets):
        self.board_size = board_size
        self.cell_size = 80
        self.width = self.height = board_size * self.cell_size
        self.vehicles = self.load_vehicles(vehicles_file)
        print(self.vehicles)
        self.targets = set(targets)

        # Initialize the board using the Board class
        self.board = Board(board_size, self.vehicles, self.targets)
        self.target_vehicle = next(v for v in self.vehicles if v['symbol'] == 'X')
        self.reached_targets = set()
        self.all_targets_collected = False

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rush Hour")
        self.font = pygame.font.Font(None, 36)

    def load_vehicles(self, file_name):
        """Load vehicles from a JSON file."""
        with open(file_name, 'r') as f:
            return json.load(f)

    def move_vehicle(self, symbol, direction):
        """Attempt to move a vehicle on the board."""
        if self.board.move_vehicle(symbol, direction):
            if symbol == 'X':
                self.check_target_reached(*self.board.vehicles[0]['position'])  # Assuming 'X' is the first vehicle
            return True
        return False

    def check_target_reached(self, row, col):
        """Check if a target is reached."""
        target = (row, col)
        if target in self.targets and target not in self.reached_targets:
            self.reached_targets.add(target)
        self.all_targets_collected = self.reached_targets == self.targets

    def check_win(self):
        """Check if the player has won the game."""
        x_vehicle = next(v for v in self.vehicles if v['symbol'] == 'X')
        x_row, x_col = x_vehicle['position']
        x_length = 1#x_vehicle['length']
        # Check if all targets are collected and the X vehicle is at the exit
        return self.all_targets_collected and x_row == self.board_size - 1 and x_col + x_length - 1 == self.board_size - 1

    def draw(self):
        """Draw the board and game elements."""
        self.screen.fill(WHITE)
        for row in range(self.board_size):
            for col in range(self.board_size):
                pygame.draw.rect(self.screen, BLACK,
                                 (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 1)
                if self.board.board[row][col] != '_':
                    color = COLORS[ord(self.board.board[row][col]) % len(COLORS)]
                    pygame.draw.rect(self.screen, color, (
                        col * self.cell_size + 2, row * self.cell_size + 2, self.cell_size - 4, self.cell_size - 4))
                    text = self.font.render(self.board.board[row][col], True, BLACK)
                    text_rect = text.get_rect(
                        center=(col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2))
                    self.screen.blit(text, text_rect)

        for target in self.targets:
            row, col = target
            if target not in self.reached_targets:
                pygame.draw.circle(self.screen, RED, (
                    col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2), 10)

        # Highlight exit
        exit_rect = pygame.Rect((self.board_size - 1) * self.cell_size, (self.board_size - 1) * self.cell_size,
                                self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, GREEN if self.all_targets_collected else RED, exit_rect, 3)

        pygame.display.flip()


def playgame(board_size,json_file,targets):
    game = RushHourGame(board_size, json_file, targets)

    running = True
    selected_vehicle = None
    moves = 0
    while running:
        game.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // game.cell_size
                row = event.pos[1] // game.cell_size
                if 0 <= row < game.board_size and 0 <= col < game.board_size:
                    selected_vehicle = game.board.board[row][col]
            elif event.type == pygame.KEYDOWN:
                if selected_vehicle and selected_vehicle != '_':
                    if event.key == pygame.K_LEFT:
                        if game.move_vehicle(selected_vehicle, 'left'):
                            moves += 1
                    elif event.key == pygame.K_RIGHT:
                        if game.move_vehicle(selected_vehicle, 'right'):
                            moves += 1
                    elif event.key == pygame.K_UP:
                        if game.move_vehicle(selected_vehicle, 'up'):
                            moves += 1
                    elif event.key == pygame.K_DOWN:
                        if game.move_vehicle(selected_vehicle, 'down'):
                            moves += 1

                    if game.check_win():
                        print(f"Congratulations! You've won the game! It took you {moves} moves!")
                        running = False

    pygame.quit()

def translate_action(plan_name, game):
    """
    Given a plan_name in the format "<DIR>_<i>,<j>_BLABLA" or "<DIR>_RED_<i>,<j>",
    output game.board[i][j], dir.

    Args:
        plan_name (str): A string in the format "<DIR>_<i>,<j>_BLABLA" or "<DIR>_RED_<i>,<j>".
        game (object): A game object containing a board (game.board) where board[i][j] is accessed.

    Returns:
        tuple: (board_position, dir) where board_position is game.board[i][j] and dir is the direction.
    """

    # Split the plan_name by '_'
    parts = plan_name.split('_')

    # First part is the direction (DIR)
    dir = parts[0]

    # Check if there is "RED" in the string, which means coordinates are in parts[2]
    if "RED" in plan_name:
        coords = parts[2]  # "<i>,<j>"
    else:
        coords = parts[1]  # "<i>,<j>"

    # Split the coordinates to get i and j
    i, j = map(int, coords.split(','))

    # Access the board position
    board_position = game.board.board[i][j]

    return board_position, dir.lower()


def search_model(board_size, vehicles_file, targets, algo, heuristic):
    game = RushHourGame(board_size, vehicles_file, targets)
    problem = Rush_Hour_Targets_Problem(game.board_size, game.vehicles, game.targets)

    # Map heuristics based on input
    heuristics = {
        "null": null_heuristic,
        "target": target_heuristic,
        "distance": max_distance_heuristic
    }

    # Select the heuristic function
    h = heuristics[heuristic]

    start = time.perf_counter()

    # Select the search algorithm
    if algo == "astar":
        actions, expanded_nodes = astar(problem, h)
    elif algo == "bfs":
        actions, expanded_nodes = bfs(problem)
    elif algo == "dfs":
        actions, expanded_nodes = dfs(problem)

    elapsed = time.perf_counter() - start


    # Execute the actions in the game
    moves = 0
    for action in actions:
        game.draw()
        game.move_vehicle(action[0], action[1])
        moves += 1
        time.sleep(0.4)

    if game.check_win():
        print(
            f"Congratulations! You've won the game! It took you {moves} moves, and you expanded {expanded_nodes} nodes.\n"
            f" It took {elapsed} time")
    else:
        print(f"no solution, it took {elapsed} time, and {expanded_nodes} expanded nodes")

    pygame.quit()


def plan_model(board_size, vehicles_file, targets, board_name, heuristic):
    game = RushHourGame(board_size, vehicles_file, targets)

    domain = f"domains_and_problems/{board_name}_Domain.txt"
    problem = f"domains_and_problems/{board_name}_Problem.txt"
    create_domain_file(domain, board_size)
    create_problem_file(problem, vehicles_file, board_size, targets)

    moves = 0
    plan, elapsed, nodes_expanded = plan_solve(domain, problem, heuristic)
    for action in plan:
        game.draw()
        vehicle_name, dir = translate_action(action.name, game)
        game.move_vehicle(vehicle_name, dir)
        moves += 1
        time.sleep(0.4)

    if game.check_win():
        print(
            f"Congratulations! You've won the game! It took you {moves} moves, expanded {nodes_expanded} nodes, and took {elapsed} time.")
    else:
        print(f"no solution, it took {elapsed} time, and {nodes_expanded} expanded nodes")


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Rush Hour Game")

    # Common arguments
    parser.add_argument("model", type=str, choices=["SEARCH", "PLAN","PLAY"], help="Solver Model (SEARCH or PLAN)")
    parser.add_argument("board_size", type=int, help="Size of the game board")
    parser.add_argument("vehicles_file", help="Path to the JSON file containing vehicle data")
    parser.add_argument("targets", nargs="+", type=lambda x: tuple(map(int, x.split(','))),
                        help="List of target coordinates (row,col)")

    # SEARCH model-specific arguments
    parser.add_argument("--algo", type=str, choices=["astar", "bfs", "dfs"],
                        help="Algorithm for search (astar, bfs, dfs)")
    parser.add_argument("--heuristic", type=str, choices=["null", "target","distance"],
                        help="Heuristic for search (null or target)")

    # PLAN model-specific argument
    parser.add_argument("--board_name", help="Board name for the PLAN model")
    parser.add_argument("--plan_heuristic", type=str, choices=["max", "zero", "sum"],
                        help="Heuristic for plan")

    args = parser.parse_args()

    if args.model == "SEARCH":
        if not args.algo or not args.heuristic:
            parser.error("SEARCH model requires --algo and --heuristic arguments.")
        search_model(args.board_size, args.vehicles_file, args.targets, args.algo, args.heuristic)
    elif args.model == "PLAN":
        if not args.board_name:
            parser.error("PLAN model requires --board_name argument.")
        plan_model(args.board_size, args.vehicles_file, args.targets, args.board_name, args.plan_heuristic)
    elif args.model == "PLAY":
        playgame(args.board_size, args.vehicles_file, args.targets)
