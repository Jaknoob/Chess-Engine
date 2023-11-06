import pygame
from consts import *
from piece import Pawn, Knight, Bishop, Rook, Queen, King

class Board:
    def __init__(self, rows, columns, surface):
        self.rows = rows
        self.columns = columns              
        self.start_x = WIDTH/4              #Position on the screen from the left where chessboard should start being drawn
        self.start_y = HEIGHT/8             #Position on the screen from the top where chessboard should start being drawn
        self.square_size = HEIGHT/12        #Size of the squares on the chessboard
        self.squares = []
        self.surface = surface
        self.turn = "white"
        self.valid_moves_list = []
        self.moves_history = []
        
        
        for _ in range(rows):
            row = []
            for _ in range(columns):        #Creates a 2 dimensional array full of 0s
                row.append(0)
            self.squares.append(row)

    
    #Displays the chessboard on the screen, passes the surface to be drawn onto as a parameter

    def draw_board(self): 
        outer_border = pygame.Rect(self.start_x -5, self.start_y -5, (self.square_size*8) + 10, (self.square_size*8) + 10)        
        pygame.draw.rect(self.surface, BLACK, outer_border, 5)   #Draws the outer border around the chessboard

        temp_x = self.start_x
        temp_y = self.start_y

        for row in range(len(self.squares)):                        #Loops through rows and columns in array
            for column in range(len(self.squares[row])):
                square = pygame.Rect(temp_x, temp_y, self.square_size, self.square_size)
                
                if self.squares[row][column] == 0 or self.squares[row][column].is_selected() == False:
                    if column % 2 == row % 2:       
                        pygame.draw.rect(self.surface, DARK_SQUARE_COLOUR, square)   #Draws a dark square when rows and columns are both odd, or both even
                    else:
                        pygame.draw.rect(self.surface, LIGHT_SQUARE_COLOUR, square)
                    if self.squares[row][column] !=0:
                        self.squares[row][column].draw_piece(self.surface, temp_x, temp_y)
                else:
                    pygame.draw.rect(self.surface, SELECTED_SQUARE_COLOUR, square)
                    self.squares[row][column].draw_piece(self.surface, temp_x, temp_y)
                temp_x += self.square_size
            temp_x = self.start_x               #Reset temp_x after each row is completed.
            temp_y += self.square_size

        for row in range(len(self.squares)):                        #Loops through rows and columns in array
            for column in range(len(self.squares[row])):
                if self.squares[row][column] != 0:
                    if self.squares[row][column].is_selected():
                        self.display_valid_moves(self.squares[row][column], self.valid_moves_list)

    #Creates the pieces in the starting position

    def starting_position(self):
        self.squares[0][0] = Rook(0,0,"black")
        self.squares[0][1] = Knight(0,1,"black")
        self.squares[0][2] = Bishop(0,2,"black")
        self.squares[0][3] = Queen(0,3,"black")
        self.squares[0][4] = King(0,4,"black")
        self.squares[0][5] = Bishop(0,5,"black")
        self.squares[0][6] = Knight(0,6,"black")
        self.squares[0][7] = Rook(0,7,"black")

        for i in range(8):
            self.squares[1][i] = Pawn(1,i,"black")
            self.squares[6][i] = Pawn(6,i,"white")

        self.squares[7][0] = Rook(7,0,"white")
        self.squares[7][1] = Knight(7,1,"white")
        self.squares[7][2] = Bishop(7,2,"white")
        self.squares[7][3] = Queen(7,3,"white")
        self.squares[7][4] = King(7,4,"white")
        self.squares[7][5] = Bishop(7,5,"white")
        self.squares[7][6] = Knight(7,6,"white")
        self.squares[7][7] = Rook(7,7,"white")

        self.valid_moves_list = self.update_moves(self.squares)

    #Checks whether a piece has been clicked on and selects it

    def select(self, click: tuple):
        if (
            (click[0] >= self.start_x) and                  #If the user clicks inside the chessboard
            (click[0] <= self.start_x + self.square_size*8) and 
            (click[1] >= self.start_y) and 
            (click[1] <= self.start_y + self.square_size*8)
        ):
            click_x, click_y = click[0] - self.start_x, click[1] - self.start_y #Compares click to top left of board
            click_x, click_y = click_x / self.square_size, click_y / self.square_size #Puts difference in terms of squares
            click_x, click_y = click_x // 1, click_y // 1                       #Round down to the nearest integer

            selected_square = self.squares[int(click_y)][int(click_x)]
            selected_piece = None

            for row in range(len(self.squares)):                #Loops through all of squares and checks which piece is selected
                for column in range(len(self.squares)):         #This piece is moved on another click of a square on the board
                    if self.squares[row][column] != 0:
                        if self.squares[row][column].selected == True:    #Checks if a piece is selected
                            selected_piece = self.squares[row][column]
                            self.display_valid_moves(selected_piece, self.valid_moves_list)
                            selected_rank = row
                            selected_file = column


            if selected_piece != None:                                                   #Only if a piece is already selected
                self.move(selected_piece, selected_file, selected_rank, int(click_x), int(click_y))#Move this selected piece, to the square clicked afterwards
            
            self.unselect()
            selected_piece = None               #Resets selected piece after it has been moved

            if selected_square != 0:                    #Selects a piece if it is clicked
                if selected_square.colour == self.turn:       
                    selected_square.selected = True
                    selected_square.is_selected()
                else:
                    self.unselect()
            else:
                self.unselect()
                            

            return (int(click_y), int(click_x)), selected_square


    #Loops through all the pieces and deselects all

    def unselect(self):
        for row in range(len(self.squares)):        
                for column in range(len(self.squares)):
                    if self.squares[row][column] != 0:
                        self.squares[row][column].selected = False

    #Moves a piece in the squares array and visually, changes turn

    def move(self, piece, starting_file, starting_rank, ending_file, ending_rank):
        self.valid_moves_list = self.update_moves(self.squares)
        self.valid_moves_list = self.simulate_moves(self.valid_moves_list)
        for move in self.valid_moves_list:
            if move == (piece, starting_file, starting_rank, ending_file, ending_rank) and self.turn == piece.colour: #If the move is valid and it is your turn
                if self.turn == "white":
                    self.turn = "black"
                elif self.turn == "black":
                    self.turn = "white"
                self.squares[starting_rank][starting_file] = 0          #Clears original square
                piece.rank = ending_rank                        
                piece.file = ending_file
                self.squares[ending_rank][ending_file] = piece          #Moves piece to new position on board
            else:
                self.unselect()
        self.valid_moves_list = self.update_moves(self.squares)                      #After each move, check for new moves and checks.
        self.valid_moves_list = self.simulate_moves(self.valid_moves_list)                #After each move, detects checks and pins.
        self.is_checkmate(self.valid_moves_list)
        self.is_stalemate(self.valid_moves_list)
        self.moves_history.append(move)
            

    #Creates new list of valid moves

    def update_moves(self, board):
        valid_moves_list = []       #Clears all moves each time that it is called

        for row in range(len(board)):        
                for column in range(len(board)):             #Gets valid moves for every piece on the board
                    if board[row][column] != 0:          
                        valid_moves_list.extend(board[row][column].valid_moves(board))

        unique_moves_list = []

        for move in valid_moves_list:
            unique = True
            for unique_move in unique_moves_list:
                if move == unique_move:
                    unique = False
            if unique:
                unique_moves_list.append(move)

        self.can_castle(0, "black", 1, 3)
        self.can_castle(0, "black", 5, 6)
        self.can_castle(7, "white", 1, 3)
        self.can_castle(7, "white", 5, 6)

        return unique_moves_list
    
    def is_check(self, board, valid_moves_list):
        for move in valid_moves_list:
            if board[move[4]][move[3]] != 0:
                if board[move[4]][move[3]].__class__ == King:
                    return True
    
    def simulate_moves(self, valid_moves_list):
        escape_check_moves = []  # Valid moves to escape check
        for move in valid_moves_list:
            # Create a new board with the same dimensions
            temp_board = Board(self.rows, self.columns, self.surface)
            temp_squares = temp_board.squares

            # Copy piece positions and attributes without copying pygame.Surface objects
            for row in range(self.rows):
                for column in range(self.columns):
                    piece = self.squares[row][column]
                    if piece != 0:
                        new_piece = piece.__class__(row, column, piece.colour)  # Create a new piece of the same class
                        temp_squares[row][column] = new_piece

            # Simulate the move on the temporary board
            temp_squares[move[2]][move[1]] = 0
            temp_squares[move[4]][move[3]] = move[0]

            # Check if the king is still in check on the simulated board
            temp_moves_list = self.update_moves(temp_squares)
            if not self.is_check(temp_squares, temp_moves_list) and move[0].colour == self.turn:
                escape_check_moves.append(move)  # Move is valid and helps escape check

        return escape_check_moves
    
    #Shows valid moves on the board, called when a piece is selected.
    def display_valid_moves(self, piece, valid_moves_list):
        start_x = WIDTH/4              #Position on the screen from the left where chessboard should start being drawn
        start_y = HEIGHT/8             #Position on the screen from the top where chessboard should start being drawn    

        for move in valid_moves_list:
            if move[0] == piece:
                temp_x = start_x + (move[3]* self.square_size) + self.square_size/2 
                temp_y = start_y + (move[4]* self.square_size) + self.square_size/2 
                pygame.draw.circle(self.surface, (255,0,0), (temp_x, temp_y), 5)

    def is_checkmate(self, valid_moves_list):
        if valid_moves_list == [] and self.is_check(self.squares, valid_moves_list):
            print("Checkmate!")
            return True

    def is_stalemate(self, valid_moves_list):
        if valid_moves_list == [] and not self.is_check(self.squares, valid_moves_list):
            print("Stalemate!")
            return True
    
    def can_castle(self, rank, colour, lower_limit, upper_limit):
        temp_castle = False

        lower_limit = 1
        upper_limit = 3
        colour = "black"
        rank = 0
        #If the black king hasnt moved, and its not in check
        if self.squares[rank][4].__class__ == King and self.squares[rank][4].colour == colour and not self.is_check(self.squares, self.valid_moves_list):       
            for move in self.moves_history:
                if (move[0].__class__ == King) or (move[0].__class__ == Rook and move[0].colour == colour):    #Check if black king or rooks have moved.
                    temp_castle = False
                else:
                    temp_castle = True
            for move in self.valid_moves_list:
                for i in range(lower_limit, upper_limit):
                    if move[4] == rank and move[3] == i:   #If there is a piece targetting the squares inbetween the king and rook
                        temp_castle = False
                    else: 
                        temp_castle = True
            for i in range(lower_limit, upper_limit):
                if self.squares[0][i] == 0:
                    temp_castle = True
                else:
                    temp_castle = False

        if temp_castle:
            if upper_limit > 4: 
                self.valid_moves_list.append(((self.squares[rank][4], rank, 4, rank, upper_limit + 1), (self.squares[rank][7], rank, 7, rank, upper_limit)))
            else:
                self.valid_moves_list.append(((self.squares[rank][4], rank, 4, rank, upper_limit - 1), (self.squares[rank][0], rank, 0, rank, upper_limit)))
            
        




        
            
        if self.squares[7][4].__class__ == King and self.squares[7][4].colour == "white":
            pass







                    


