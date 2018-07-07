
from Games.GameLogic import BaseGame
import numpy as np
from Games.GameLogic import bitboard


class ConnectFour(BaseGame):

    rows = 6
    columns = 7
    num_squares = columns * rows

    def __init__(self):
        super().__init__()
        self.num_players = 2
        self.turn = 0
        self.board = np.zeros((ConnectFour.num_squares,), dtype=int)
        self.fv_size = ConnectFour.num_squares * 2
        self.num_actions = ConnectFour.columns
        self.max_game_depth = ConnectFour.num_squares
        self.in_a_row_to_win = 4

    def copy(self):
        board_copy = ConnectFour()
        board_copy.board = self.board.copy()
        board_copy.winner = self.winner
        board_copy.turn = self.turn
        return board_copy

    def get_legal_moves(self):
        """ Return a list of the possible action indexes """
        if self.is_game_over():
            return []
        return np.where(self.board[:ConnectFour.columns] == 0, 1, 0).nonzero()[0]

    def advance(self, a):
        if self.winner is not None:
            raise Exception("Cannot advance when game is over")
        if a is None:
            raise Exception("action_index can not be None")
        if self.board[a] != 0:
            raise Exception("This column is full")
        if a >= self.num_actions or a < 0:
            raise Exception("Action is not legal")

        board_value = self.player_index_to_board_value(player_index=self.turn)
        reversed_a = ConnectFour.columns - a
        while True:
            if self.board[-reversed_a] == 0:
                self.board[-reversed_a] = board_value
                break
            else:
                reversed_a += ConnectFour.columns
        self.update_game_state()

    def update_game_state(self):
        board = np.reshape(self.board, (-1, ConnectFour.columns))

        def check_in_a_row(r):
            counter = 0
            last = -1
            for c in r:
                if c == 0:
                    counter = 0
                    last = -1
                    continue
                if c == last:
                    counter += 1
                    if counter == self.in_a_row_to_win:
                        self.winner = self.board_value_to_player_index(c)
                        return
                    continue
                if c != last and c != 0:
                    last = c
                    counter = 1

        def check_horizontal(board):
            for r in board:
                check_in_a_row(r)

        # Horizontal "-"
        check_horizontal(board)

        # Vertical "|"
        board = np.transpose(board)
        check_horizontal(board)

        def check_diagonal(board, column_count, row_count):
            diagonals = [board.diagonal()]
            """ -> """
            for i in range(1, row_count - self.in_a_row_to_win + 1):
                diagonals.append(board.diagonal(offset=i))
            """ |
                V """
            for i in range(1, column_count - self.in_a_row_to_win + 1):
                diagonals.append(board.diagonal(offset=-i))

            for d in diagonals:
                check_in_a_row(d)

        # Diagonal "\"
        check_diagonal(board, column_count=ConnectFour.columns, row_count=ConnectFour.rows)

        # Diagonal "/"
        board = np.rot90(board)
        check_diagonal(board, column_count=ConnectFour.rows, row_count=ConnectFour.columns)

        self.next_turn()

        # Is the game a draw.
        if self.is_draw():
            self.winner = -1

    def get_feature_vector(self):
        return bitboard(self.board)

    def next_turn(self):
        """ Next turn is always the other player in this game """
        self.turn += 1
        if self.turn >= self.num_players:
            self.turn = 0

    def display(self):
        char_board = ""
        for x in self.board:
            if x == 0: char_board += '-'
            if x == 1: char_board += 'x'
            if x == 2: char_board += 'o'
        print("*** Print of TicTacToe game ***")
        c = ConnectFour.columns
        for r in range(c):
            print(char_board[r*c:r*c + c])
        print()
