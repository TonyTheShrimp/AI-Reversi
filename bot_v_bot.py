from reversiboard import ReversiBoard
from reversigame import ReversiGameState
from dlgo.gotypes import Player
from dlgo.agent.naive import RandomBot
from dlgo.utils import print_board  # Optional: reuse Go’s printer
import time

def main():
    game = ReversiGameState.new_game(8)
    bots = {
        Player.black: RandomBot(),
        Player.white: RandomBot()
    }

    while not game.is_over():
        time.sleep(0.5)
        print(chr(27) + "[2J")  # clear screen
        print_board(game.board)
        player = game.next_player
        bot_move = bots[player].select_move(game)

        if bot_move:
            print(f"{player} plays at {bot_move.row},{bot_move.col}")
            game = game.apply_move(bot_move)
        else:
            print(f"{player} has no valid moves and skips turn.")
            game = ReversiGameState(
                board=game.board,
                next_player=game._next_player_after_move(),
                previous_state=game,
                last_move=None
            )

    # Game over
    print(chr(27) + "[2J")
    print_board(game.board)
    black_count, white_count = game.board.count_discs()
    print(f"Game Over. Final score -> Black: {black_count}, White: {white_count}")
    winner = game.winner()
    if winner:
        print(f"{winner} wins!")
    else:
        print("It's a tie!")

if __name__ == '__main__':
    main()
