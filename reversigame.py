#3.1
import copy
from dlgo.gotypes import Player
from reversiboard import ReversiBoard
from dlgo import zobrist

#3.2 跟踪游戏状态并检查非法动作
#存储围棋的游戏状态
class ReversiGameState:
    def __init__(self, board, next_player, previous_state, last_move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous_state
        self.last_move = last_move

    @classmethod
    def new_game(cls, board_size=8):
        board = ReversiBoard(board_size)
        return ReversiGameState(board, Player.black, None, None)

    def apply_move(self, move):
        next_board = copy.deepcopy(self.board)
        valid = next_board.place_stone(self.next_player, move)
        if not valid:
            raise ValueError("Invalid move")
        return ReversiGameState(
            next_board,
            self._next_player_after_move(),
            self,
            move
        )

    def is_over(self):
        return not self.legal_moves(self.next_player) and not self.legal_moves(self.next_player.other)

    def legal_moves(self, player):
        return self.board.legal_moves(player)

    def _next_player_after_move(self):
        # If opponent has legal moves, they play next. Otherwise, current player goes again.
        if self.board.legal_moves(self.next_player.other):
            return self.next_player.other
        return self.next_player

    def winner(self):
        black, white = self.board.count_discs()
        if black > white:
            return Player.black
        elif white > black:
            return Player.white
        return None  # Tie