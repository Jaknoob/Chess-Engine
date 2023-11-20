from board import Board
import random
class ChessAI():
    def __init__(self, board, colour):
        self.board: Board = board
        self.colour = colour

    def play_best_move(self):
        self.best_move = self.random_move()
        if self.best_move != None:
            self.board.move(self.best_move)

    def random_move(self):
        if len(self.board.valid_moves_list) != 0:
            random_move_index = random.randint(0, len(self.board.valid_moves_list) -1)
            random_move = self.board.valid_moves_list[random_move_index]
            print(self.board.valid_moves_list)
            return random_move
        
