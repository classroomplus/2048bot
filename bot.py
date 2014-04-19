import random
import itertools
from board import Board, IllegalMoveException, ALL_TILES
from config import WIN_VALUE
import helpers
from moves import ALL_MOVES

avg = lambda values: sum(values) / len(values)

class Bot(object):
    def get_board_score(self, board):
        # return float(
        #     sum(
        #         ((1 if board[y, x] == 0 else 0) for y, x in ALL_INDICES),
        #         0
        #     )
        # )

        return float(
            sum(
                (board[y, x] ** 2 for y, x in ALL_TILES),
                0
            )
        )


    def get_next_move_simple(self, board):
        def calc_score_for_move(move):
            board_copy = Board(board)
            try:
                board_copy.move_only_swipe(move)
                return self.get_board_score(board_copy)
            except IllegalMoveException:
                return -1.0

        return max(ALL_MOVES, key=calc_score_for_move)

    def get_next_move_advanced(self, board, depth=3, agg_func=avg):
        def calc_score_for_board(board, iteration=1):
            if iteration == depth:
                return self.get_board_score(board)

            scores = []

            for tile in board.get_free_tiles():
                cur_board = Board(board)
                cur_board[tile] = 2

                if not cur_board.has_legal_moves():
                    # Things are bad if there aren't possible moves at all
                    scores += [-1]
                else:
                    for move in ALL_MOVES:
                        move_board = Board(cur_board)

                        try:
                            move_board.move_only_swipe(move)
                        except IllegalMoveException:
                            # Only counting possible moves
                            continue

                        scores.append(calc_score_for_board(move_board, iteration=iteration+1))

            if scores:
                return agg_func(scores)
            return -1

        def calc_score_for_move(move):
            cur_board = Board(board)
            try:
                cur_board.move_only_swipe(move)
                return calc_score_for_board(cur_board)
            except IllegalMoveException:
                return -10.0

        return max(ALL_MOVES, key=calc_score_for_move)

    get_next_move = get_next_move_advanced

    def play(self, board, show_steps=True):
        """
        runs the algorithm on given board and attempts to solve it.
        returns True if successfully solved and False if failed.
        """
        while board.has_legal_moves() and not board.has_tile(WIN_VALUE):
            if show_steps:
                print repr(board)

            next_move = self.get_next_move(board)

            if show_steps:
                print "Chosen move:", next_move

            board.move(next_move)

        if show_steps:
            print repr(board)

        return board.has_tile(WIN_VALUE)


if __name__ == "__main__":
    board = Board()
    success = Bot().play(board, show_steps=True)

    print "Success!" if success else "Failure!", "({})".format(board.get_max_tile())