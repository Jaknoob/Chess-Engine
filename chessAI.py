from board import Board
from heuristics import *
import random
from piece import Pawn
class ChessAI():
    def __init__(self, board, colour):
        self.board: Board = board
        self.colour = colour

    def play_best_move(self):
        best_move = None
        temp_board = self.simulate_board(self.board.squares, best_move)
        if self.colour == "white":
            best_score = -99999
        else:
            best_score = 99999
        
        if self.colour == "white":
            maximising_player = True
        else: 
            maximising_player = False

        for move in self.board.valid_moves_list:
            new_board = self.simulate_board(temp_board, move)
            evaluation = self.minimax(new_board, 0, -99999, 99999, maximising_player)

            #print(f"Move: {move}, Evaluation: {evaluation}, Colour: {move[0].colour}")

            if self.colour == "white" and evaluation > best_score:
                best_score = evaluation
                best_move = move
            elif self.colour == "black" and evaluation < best_score:
                best_score = evaluation
                best_move = move
    
        #print(f"Selected Best Move: {best_move}")
        self.board.move(best_move)


    def random_move(self):
        if len(self.board.valid_moves_list) != 0:
            random_move_index = random.randint(0, len(self.board.valid_moves_list) -1)
            random_move = self.board.valid_moves_list[random_move_index]
            return random_move
        
    

    def simulate_board(self, board, move):
        temp_board = [[0 for _ in range(8)] for _ in range(8)]

        # Copy piece positions and attributes without copying pygame.Surface objects
        for row in range(len(board)):
            for column in range(len(board[0])):
                piece = board[row][column]
                if piece != 0:
                    new_piece = piece.__class__(row, column, piece.colour)
                    temp_board[row][column] = new_piece

        if move != None:
            # Simulate the move on the temporary board
            temp_board[move[2]][move[1]] = 0
            temp_board[move[4]][move[3]] = move[0]

        return temp_board


    def material_advantage(self, board):
        centipawn_values = {
            "Pawn" : 100,
            "Bishop" : 300,
            "Knight" : 300,
            "Rook" : 500,
            "Queen" : 900,
            "King" : 99999
        }

        material_advantage = 0
        for row in range(len(board)):        
            for column in range(len(board)):             #Gets valid moves for every piece on the board
                if board[row][column] != 0:          
                    piece_type = board[row][column].__class__.__name__
                    if board[row][column].colour == "white":
                        material_advantage += centipawn_values[piece_type]
                    elif board[row][column].colour == "black":
                        material_advantage -= centipawn_values[piece_type]

        return material_advantage
    
    def evalutate_position(self, board):
        value = self.material_advantage(board) + self.add_heuristics(board)
        return value

    def add_heuristics(self, board):
        positional_advantage = 0
        for row in range(len(board)):        
            for column in range(len(board)):             #Gets valid moves for every piece on the board
                if board[row][column] != 0:
                    piece_type = (board[row][column].__class__.__name__ + "h")
                    if board[row][column].colour == "white":
                        positional_advantage += heuristics_dict[piece_type][row][column]
                    elif board[row][column].colour == "black":
                        positional_advantage -= heuristics_dict[piece_type][-(row + 1)][-(column + 1)]
        return positional_advantage
        
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_checkmate(board) or self.board.is_stalemate(board):
            return self.evalutate_position(board)

        legal_moves = self.board.simulate_moves(self.board.update_moves(board))

        if maximizing_player:
            max_eval = -99999
            for move in legal_moves:
                new_board = self.simulate_board(board, move)
                eval = self.minimax(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                if max_eval > beta:
                    #print("beta branch pruned")
                    break
                #print("branch not pruned")
                alpha = max(alpha, max_eval)
            return max_eval
        else:
            min_eval = 99999
            for move in legal_moves:
                new_board = self.simulate_board(board, move)
                eval = self.minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                if min_eval < alpha:
                    #print("alpha branch pruned")
                    break
                #print("branch not pruned")
                beta = max(beta, min_eval)
            return min_eval
