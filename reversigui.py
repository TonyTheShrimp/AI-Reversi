import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import QSize, QTimer
from dlgo.gotypes import Player, Point
from reversigame import ReversiGameState
from dlgo.agent.naive import RandomBot
from dlgo.agent.minimax import MinimaxBot

class ReversiGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.bot = RandomBot()
        self.bot = MinimaxBot()

        self.setWindowTitle("Reversi - Human vs Bot")
        self.board_size = 8
        self.cell_size = 60
        self.game = ReversiGameState.new_game(self.board_size)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.grid_layout = QGridLayout()
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.status_label = QLabel("Black: 2 | White: 2")
        main_layout.addWidget(self.status_label)

        self.start_button = QPushButton("Reset Game")
        self.end_button = QPushButton("End Game")
        self.start_button.clicked.connect(self.start_game)
        self.end_button.clicked.connect(self.end_game)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.end_button)

        main_layout.addLayout(button_layout)
        main_layout.addLayout(self.grid_layout)

        self.central_widget.setLayout(main_layout)

        self.buttons = {}
        self.update_board()

    def update_board(self):
        for row in range(1, self.board_size + 1):
            for col in range(1, self.board_size + 1):
                pt = Point(row, col)
                btn = self.buttons.get(pt)

                if btn is None:
                    btn = QPushButton()
                    btn.setFixedSize(QSize(self.cell_size, self.cell_size))

                    font = btn.font()
                    font.setPointSize(24)  # Makes stone symbol large
                    font.setBold(True)
                    btn.setFont(font)
                    btn.setStyleSheet("text-align: center;")  # Ensures center alignment

                    btn.clicked.connect(lambda _, p=pt: self.handle_click(p))
                    self.grid_layout.addWidget(btn, row, col)
                    self.buttons[pt] = btn

                stone = self.game.board.get(pt)
                if stone == Player.black:
                    btn.setText("●")
                elif stone == Player.white:
                    btn.setText("○")
                elif pt in self.game.legal_moves(Player.black) and self.game.next_player == Player.black:
                    btn.setText("+")
                else:
                    btn.setText("")
        black, white = self.game.board.count_discs()
        self.status_label.setText(f"Black: {black} | White: {white}")

        if self.game.next_player == Player.black and not self.game.legal_moves(Player.black):
            QTimer.singleShot(600, self.play_bot_move)

    def handle_click(self, point):
        if self.game.is_over() or self.game.next_player != Player.black or point not in self.game.legal_moves(Player.black):
            return

        self.game = self.game.apply_move(point)
        self.update_board()

        if not self.game.is_over():
            QTimer.singleShot(600, self.play_bot_move)
            return

        self.show_game_over()

    def play_bot_move(self):
        if not self.game.is_over() and self.game.next_player == Player.white:
            bot_move = self.bot.select_move(self.game)
            if bot_move:
                self.game = self.game.apply_move(bot_move)
            else:
                self.game = ReversiGameState(
                    board=self.game.board,
                    next_player=self.game._next_player_after_move(),
                    previous_state=self.game,
                    last_move=None
                )
            self.update_board()

        if self.game.is_over():
            self.show_game_over()

    def show_game_over(self):
        black, white = self.game.board.count_discs()
        winner = self.game.winner()
        msg = f"Game Over!\nBlack: {black} | White: {white}\n"
        msg += f"{winner.name.capitalize()} wins!" if winner else "It's a tie!"
        QMessageBox.information(self, "Game Result", msg)
        self.close()

    def start_game(self):
        self.game = ReversiGameState.new_game(self.board_size)
        self.update_board()
        self.start_button.setDisabled(True)  # Optional: prevent double-start

    def end_game(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = ReversiGUI()
    gui.show()
    sys.exit(app.exec())