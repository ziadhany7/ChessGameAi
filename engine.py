import numpy as np


class GameState:
    def __init__(self):
        # string representation of the board
        self.board = np.array([['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                               ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                               ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                               ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                               ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                               ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
                               ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                               ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']])
        self.white_turn = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.check = False
        self.pins = []
        self.checks = []

    def make_move(self, move):
        self.board[move.starting_row][move.starting_column] = '  '  # Assign the moved from square to empty square
        if move.piece_moved != '  ':  # To prevent empty squares from being counted as moves
            self.board[move.ending_row][move.ending_column] = move.piece_moved
            self.move_log.append(move)
            self.white_turn = not self.white_turn
            if move.piece_moved == 'wK':
                self.white_king_location = (move.ending_row, move.ending_column)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.ending_row, move.ending_column)
            if move.pawn_promotion:
                promoted_to = input('Enter Q or q for Queen R or r for rock N or n for knight or B or b for bishop\n')
                self.board[move.ending_row][move.ending_column] = move.piece_moved[0] + promoted_to.upper()

    def undo(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.starting_row][move.starting_column] = move.piece_moved
            self.board[move.ending_row][move.ending_column] = move.piece_captured
            self.white_turn = not self.white_turn
            if move.piece_moved == 'wK':
                self.white_king_location = (move.starting_row, move.starting_column)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.ending_row, move.ending_column)

    def get_pawn_moves(self, row, column, moves):
        # configuring white pawn moves
        pinned = False
        pinning_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                pinned = True
                pinning_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.white_turn:
            if self.board[row - 1][column] == '  ':
                if not pinned or pinning_direction == (-1, 0):
                    moves.append(Move((row, column), (row - 1, column), self.board))
                    if row == 6 and (self.board[row - 1][column] == '  ' and self.board[row - 2][column] == '  '):
                        moves.append(Move((row, column), (row - 2, column), self.board))
            if column + 1 <= 7:
                if self.board[row-1][column+1][0] == 'b':
                    if not pinned or pinning_direction == (-1, 1):
                        moves.append(Move((row, column), (row-1, column+1), self.board))
            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0] == 'b':
                    if not pinned or pinning_direction == (-1, -1):
                        moves.append(Move((row, column), (row-1, column-1), self.board))
        # Black pawn moves
        else:
            if self.board[row + 1][column] == '  ':
                if not pinned or pinning_direction == (1, 0):
                    moves.append(Move((row, column), (row+1, column), self.board))
                    if row == 1 and (self.board[row+1][column] == '  ' and self.board[row+2][column] == '  '):
                        moves.append(Move((row, column), (row+2, column), self.board))
            if column + 1 <= 7:
                if self.board[row+1][column+1][0] == 'w':
                    if not pinned or pinning_direction == (1, 1):
                        moves.append(Move((row, column), (row+1, column+1), self.board))
            if column - 1 >= 0:
                if self.board[row+1][column-1][0] == 'w':
                    if not pinned or pinning_direction == (1, -1):
                        moves.append(Move((row, column), (row+1, column-1), self.board))

    def get_bishop_moves(self, row, column, moves):
        pinned = False
        pinning_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                pinned = True
                pinning_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][column][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        moving_right_down, moving_left_up, moving_left_down, moving_right_up = (1, 1), (-1, -1), (-1, 1), (1, -1)
        movement_directions = [moving_right_down, moving_left_up, moving_left_down, moving_right_up]
        if self.white_turn:
            enemy = 'b'
        else:
            enemy = 'w'
        for direction in movement_directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_column = column + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_column <= 7:
                    if not pinned or pinning_direction == direction or pinning_direction == (-direction[0],
                                                                                             -direction[1]):
                        piece_to_capture = self.board[end_row][end_column][0]
                        if piece_to_capture == ' ':
                            moves.append(Move((row, column), (end_row, end_column), self.board))
                        elif piece_to_capture == enemy:
                            moves.append(Move((row, column), (end_row, end_column), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_knight_moves(self, row, column, moves):
        # Knight moves
        pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                pinned = True
                self.pins.remove(self.pins[i])
                break
        movement_directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        if self.white_turn:
            enemy = 'b'
        else:
            enemy = 'w'
        for direction in movement_directions:
            end_row = row + direction[0]
            end_column = column + direction[1]
            if 0 <= end_row <= 7 and 0 <= end_column <= 7:
                if not pinned:
                    piece_to_capture = self.board[end_row][end_column]
                    if piece_to_capture[0] == enemy or piece_to_capture[0] == ' ':
                        moves.append(Move((row, column), (end_row, end_column), self.board))

    def get_rock_moves(self, row, column, moves):
        pinned = False
        pinning_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                pinned = True
                pinning_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        moving_right, moving_left, moving_up, moving_down = (0, 1), (0, -1), (-1, 0), (1, 0)
        movement_directions = [moving_right, moving_left, moving_up, moving_down]
        if self.white_turn:
            enemy = 'b'
        else:
            enemy = 'w'
        for direction in movement_directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_column = column + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_column <= 7:
                    if not pinned or pinning_direction == direction or pinning_direction == (-direction[0],
                                                                                             -direction[1]):
                        piece_to_capture = self.board[end_row][end_column][0]
                        if piece_to_capture == ' ':
                            moves.append(Move((row, column), (end_row, end_column), self.board))
                        elif piece_to_capture == enemy:
                            moves.append(Move((row, column), (end_row, end_column), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_queen_moves(self, row, column, moves):
        self.get_bishop_moves(row, column, moves)
        self.get_rock_moves(row, column, moves)

    def get_king_moves(self, row, column, moves):
        movement_directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        if self.white_turn:
            enemy = 'b'
        else:
            enemy = 'w'
        for direction in movement_directions:
            ending_row = row + direction[0]
            ending_column = column + direction[1]
            if 0 <= ending_row <= 7 and 0 <= ending_column <= 7:
                piece_to_capture = self.board[ending_row][ending_column]
                if piece_to_capture[0] == enemy or piece_to_capture[0] == ' ':
                    if enemy == 'b':
                        self.white_king_location = (ending_row, ending_column)
                    else:
                        self.black_king_location = (ending_row, ending_column)
                    check, checks, pins = self.king_states()
                    if not check:
                        moves.append(Move((row, column), (ending_row, ending_column), self.board))
                    if enemy == 'b':
                        self.white_king_location = (row, column)
                    else:
                        self.black_king_location = (row, column)

    def king_states(self):  # Getting pins and checks
        pins = []  # To store pins
        checks = []  # To store checks
        check = False  # Is the king currently checked?
        # Defining the location of the king and defining who's enemy and who's friend
        if self.white_turn:
            enemy = 'b'
            ally = 'w'
            king_row = self.white_king_location[0]
            king_column = self.white_king_location[1]
        else:
            enemy = 'w'
            ally = 'b'
            king_row = self.black_king_location[0]
            king_column = self.black_king_location[1]
        # Getting the directions that possibly contain a checking enemy or a pinned ally
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for direction_index in range(len(directions)):
            direction = directions[direction_index]
            possible_pin = ()
            for i in range(1, 8):
                # Checking all directions to get a possible piece
                piece_row = king_row + direction[0] * i
                piece_column = king_column + direction[1] * i
                if 0 <= piece_row <= 7 and 0 <= piece_column <= 7:
                    piece_to_exam = self.board[piece_row][piece_column]
                    # Getting all possible pined allies
                    if piece_to_exam[0] == ally and piece_to_exam[1] != 'K':
                        if possible_pin == ():
                            possible_pin = (piece_row, piece_column, direction[0], direction[1])
                        else:
                            break
                    # Getting all possible pinning/checking enemies(but the knight)
                    elif piece_to_exam[0] == enemy:
                        piece_type = piece_to_exam[1]
                        if (4 <= direction_index <= 7 and piece_type == 'R') or \
                                (0 <= direction_index <= 3 and piece_type == 'B') or \
                                (i == 1 and piece_type == 'p' and ((enemy == 'b' and 3 <= direction_index <= 4) or
                                                                   (enemy == 'w' and 0 <= direction_index <= 4))) or \
                                (piece_type == 'Q') or (piece_type == 'K' and i == 1):
                            if possible_pin == ():  # No ally blocking the enemy(check)
                                check = True
                                checks.append((piece_row, piece_column, direction[0], direction[1]))
                                break
                            else:  # An ally blocking the enemy(pin)
                                pins.append(possible_pin)
                                break
                        else:  # The enemy piece is no threat in that position
                            break
                else:  # Out of board
                    break
        # Enemy knight case
        knight_directions = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        for knight_direction in knight_directions:
            knight_row = king_row + knight_direction[0]
            knight_column = king_column + knight_direction[1]
            if 0 <= knight_row <= 7 and 0 <= knight_column <= 7:
                possible_knight = self.board[knight_row][knight_column]
                if possible_knight[0] == enemy and possible_knight[1] == 'N':
                    check = True
                    checks.append((knight_row, knight_column, knight_direction[0], knight_direction[1]))
        return check, checks, pins

    def get_all_moves(self):
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                piece_color = self.board[row][column][0]  # To get the first char(it's color) of the piece selected
                if (piece_color == 'w' and self.white_turn) or (piece_color == 'b' and not self.white_turn):
                    piece_type = self.board[row][column][1]  # To get the type of the piece selected
                    if piece_type == 'p':
                        self.get_pawn_moves(row, column, moves)
                    elif piece_type == 'B':
                        self.get_bishop_moves(row, column, moves)
                    elif piece_type == 'N':
                        self.get_knight_moves(row, column, moves)
                    elif piece_type == 'R':
                        self.get_rock_moves(row, column, moves)
                    elif piece_type == 'Q':
                        self.get_queen_moves(row, column, moves)
                    elif piece_type == 'K':
                        self.get_king_moves(row, column, moves)
        return moves

    def get_valid_moves(self):
        valid_moves = []
        self.check, self.checks, self.pins = self.king_states()
        if self.white_turn:
            king_row = self.white_king_location[0]
            king_column = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_column = self.black_king_location[1]
        if self.check:
            if len(self.checks) == 1:  # Just one piece checking so we can either move the king or block
                valid_squares = []
                valid_moves = self.get_all_moves()
                check_location = self.checks[0]
                check_row = check_location[0]
                check_column = check_location[1]
                piece_checking = self.board[check_row][check_column]
                if piece_checking[1] == 'N':  # If the checking piece is a knight so we can't block
                    valid_squares = [(check_row, check_column)]  # We can only capture it or move the king
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check_location[2] * i, king_column + check_location[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_column:
                            break
                for i in range(len(valid_moves)-1, -1, -1):
                    if valid_moves[i].piece_moved[1] != 'K':  # We don't check the king as the king can't be pinned
                        # Checking weather the piece move is valid or not
                        if (valid_moves[i].ending_row, valid_moves[i].ending_column) not in valid_squares:
                            valid_moves.remove(valid_moves[i])  # If not we remove that move
            else:  # Multiple checking we can just move the king
                self.get_king_moves(king_row, king_column, valid_moves)
        else:  # The king isn't checked we can move any piece in any featured direction
            valid_moves = self.get_all_moves()
        return valid_moves

    def is_check_mate(self):
        return self.check and self.get_valid_moves() == []

    def is_stale_mate(self):
        return not self.check and self.get_valid_moves() == []


# A class to make the moves
class Move:
    def __init__(self, starting_square, ending_square, board_state):
        self.starting_row = starting_square[0]
        self.starting_column = starting_square[1]
        self.ending_row = ending_square[0]
        self.ending_column = ending_square[1]
        self.piece_moved = board_state[self.starting_row, self.starting_column]
        self.piece_captured = board_state[self.ending_row, self.ending_column]
        self.id = self.starting_row * 1000 + self.starting_column * 100 + self.ending_row * 10 + self.ending_column
        self.pawn_promotion = False
        if (self.piece_moved == 'wp' and self.ending_row == 0) or (self.piece_moved == 'bp' and self.ending_row == 7):
            self.pawn_promotion = True

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.id == other.id
