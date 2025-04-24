import random
from dlgo.gotypes import Player, Point

MAX63 = 0x7FFFFFFFFFFFFFFF
table = {}
empty_board = 0

for row in range(1, 9):
    for col in range(1, 9):
        for state in (Player.black, Player.white):
            code = random.randint(0, MAX63)
            table[Point(row, col), state] = code

print("from dlgo.gotypes import Player, Point")
print("")
print("__all__ = ['HASH_CODE', 'EMPTY_BOARD']")
print("")
print("HASH_CODE = {")
for (pt, state), hash_code in table.items():
    print(f"    ({pt!r}, {state}): {hash_code},")
print("}")
print("")
print(f"EMPTY_BOARD = {empty_board}")
