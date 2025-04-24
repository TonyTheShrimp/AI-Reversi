from dlgo.gotypes import Player, Point
from dlgo import zobrist

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1),
]

class ReversiBoard:
    def __init__(self, size=8):
        self.size = size
        self._grid = {}
        self._hash = zobrist.EMPTY_BOARD
        mid = size // 2
        self._place_initial(mid, mid, Player.white)
        self._place_initial(mid + 1, mid + 1, Player.white)
        self._place_initial(mid + 1, mid, Player.black)
        self._place_initial(mid, mid + 1, Player.black)

    def _place_initial(self, row, col, player):
        pt = Point(row, col)
        self._grid[pt] = player
        self._hash ^= zobrist.HASH_CODE[(pt, player)]

    def get_hash(self):
        return self._hash

    def is_on_grid(self, point):
        return 1 <= point.row <= self.size and 1 <= point.col <= self.size

    def get(self, point):
        return self._grid.get(point)

    @property
    def num_rows(self):
        return self.size

    @property
    def num_cols(self):
        return self.size

    def place_stone(self, player, point):
        flips = self._get_flips(player, point)
        if not flips:
            return False
        self._grid[point] = player
        self._hash ^= zobrist.HASH_CODE[(point, player)]
        for pt in flips:
            old_player = self._grid[pt]
            self._hash ^= zobrist.HASH_CODE[(pt, old_player)]
            self._grid[pt] = player
            self._hash ^= zobrist.HASH_CODE[(pt, player)]
        return True

    def legal_moves(self, player):
        return [Point(r, c)
                for r in range(1, self.size + 1)
                for c in range(1, self.size + 1)
                if self._grid.get(Point(r, c)) is None and self._get_flips(player, Point(r, c))]

    def _get_flips(self, player, point):
        flips = []
        for dr, dc in DIRECTIONS:
            path = []
            r, c = point.row + dr, point.col + dc
            while self.is_on_grid(Point(r, c)):
                neighbor = self._grid.get(Point(r, c))
                if neighbor is None:
                    break
                if neighbor == player.other:
                    path.append(Point(r, c))
                elif neighbor == player:
                    flips.extend(path)
                    break
                else:
                    break
                r += dr
                c += dc
        return flips

    def count_discs(self):
        black = sum(1 for p in self._grid.values() if p == Player.black)
        white = sum(1 for p in self._grid.values() if p == Player.white)
        return black, white

    def is_full(self):
        return len(self._grid) == self.size * self.size
