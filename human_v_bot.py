from reversigame import ReversiGameState
from reversiboard import ReversiBoard
from dlgo.gotypes import Player
from dlgo.agent.naive import RandomBot
from dlgo.utils import print_board, point_from_coords
from six.moves import input

def main():
    game = ReversiGameState.new_game(8)
    bot = RandomBot()

    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)

        if game.next_player == Player.black:
            # Human plays black
            human_input = input('-- ')
            try:
                point = point_from_coords(human_input.strip())
            except Exception:
                print("Invalid input format. Try something like D3.")
                continue

            if point not in game.legal_moves(Player.black):
                print("Invalid move. Try again.")
                continue

            game = game.apply_move(point)
        else:
            # Bot plays white
            move = bot.select_move(game)
            if move:
                print(f"Bot (White) plays at {move.row},{move.col}")
                game = game.apply_move(move)
            else:
                print("Bot has no valid moves and skips turn.")
                game = ReversiGameState(
                    board=game.board,
                    next_player=game._next_player_after_move(),
                    previous_state=game,
                    last_move=None
                )

    print(chr(27) + "[2J")
    print_board(game.board)
    black, white = game.board.count_discs()
    print(f"Game Over. Final score -> Black: {black}, White: {white}")
    winner = game.winner()
    if winner:
        print(f"{winner} wins!")
    else:
        print("It's a tie!")

if __name__ == '__main__':
    main()
