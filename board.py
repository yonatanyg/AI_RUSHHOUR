# board.py


class Board:
    def __init__(self, board_size, vehicles=None, targets=None):
        self.board_size = board_size

        self.exit_target = (self.board_size-1,self.board_size-1)

        self.board = [['_' for _ in range(board_size)] for _ in range(board_size)]
        self.vehicles = vehicles if vehicles is not None else []
        self.targets = set(targets) if targets is not None else set()
        self.targets.add(self.exit_target)

        self.reached_targets = set()

        self.place_vehicles()

    def place_vehicles(self):
        """Place all vehicles on the board."""
        for vehicle in self.vehicles:
            self.update_board(vehicle, *vehicle['position'])

    def update_board(self, vehicle, new_row, new_col):
        """Update the board with a vehicle's new position."""
        symbol = vehicle['symbol']
        if symbol == 'X':
            self.board[new_row][new_col] = symbol
            vehicle['position'] = (new_row, new_col)

            tup = (new_row,new_col) 
            if tup in self.targets and tup not in self.reached_targets:
                if tup == self.exit_target:
                    if len(self.reached_targets) + 1 != len(self.targets):
                        return
                self.reached_targets.add(tup)
            return

        length = vehicle['length']
        
        orientation = vehicle['orientation']

        if orientation == 'horizontal':
            for i in range(length):
                self.board[new_row][new_col + i] = symbol
        else:  # vertical
            for i in range(length):
                self.board[new_row + i][new_col] = symbol

        vehicle['position'] = (new_row, new_col)

    def clear_vehicle(self, vehicle):
        """Clear a vehicle from the board."""
        row, col = vehicle['position']
        length = vehicle['length']
        orientation = vehicle['orientation']

        if orientation == 'horizontal':
            for i in range(length):
                self.board[row][col + i] = '_'
        elif orientation == 'vertical':  # vertical
            for i in range(length):
                self.board[row + i][col] = '_'
        else: #both
            self.board[row][col] = '_'


    def move_vehicle(self, symbol, direction):
        """Move a vehicle in the specified direction."""
        vehicle = next((v for v in self.vehicles if v['symbol'] == symbol), None)
        if not vehicle:
            return False

        row, col = vehicle['position']
        length = vehicle['length']
        orientation = vehicle['orientation']

        new_row, new_col = row, col
        if direction == 'left':
            new_col -= 1
        elif direction == 'right':
            new_col += 1
        elif direction == 'up':
            new_row -= 1
        elif direction == 'down':
            new_row += 1

        if self.is_valid_move(new_row, new_col, length, orientation, direction):
            self.clear_vehicle(vehicle)
            self.update_board(vehicle, new_row, new_col)
            return True

        return False

    def is_valid_move(self, row, col, length, orientation, direction):
        """Check if the move is valid."""
        if orientation == 'both':
            if direction == 'left':
                return col >= 0 and self.board[row][col] == '_'
            elif direction == 'right':
                return col + length <= self.board_size and self.board[row][col + length - 1] == '_'
            elif direction == 'up':
                return row >= 0 and self.board[row][col] == '_'
            else:  # down
                return row + length <= self.board_size and self.board[row + length - 1][col] == '_'    

        if orientation == 'horizontal':
            if direction not in ['left', 'right']:
                return False
            if direction == 'left':
                return col >= 0 and self.board[row][col] == '_'
            else:  # right
                return col + length <= self.board_size and self.board[row][col + length - 1] == '_'
        elif orientation == 'vertical':
            if direction not in ['up', 'down']:
                return False
            if direction == 'up':
                return row >= 0 and self.board[row][col] == '_'
            else:  # down
                return row + length <= self.board_size and self.board[row + length - 1][col] == '_'
        return False

    def copy(self):
        """Create a copy of the board."""
        new_board = Board(self.board_size)
        new_board.board = [row[:] for row in self.board]
        new_board.vehicles = [v.copy() for v in self.vehicles]
        new_board.targets = self.targets.copy()
        new_board.reached_targets = self.reached_targets.copy()
        return new_board
