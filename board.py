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
        self.highlighted_moves = []
        self.turn = "white"
        
        
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
                        self.squares[row][column].move_validation(self.surface, self.squares)

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

        self.update_moves()

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
        valid_moves_list = self.update_moves()                                     #Before each move, reset moves list
        for move in valid_moves_list:
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

    #Creates new list of valid moves

    def update_moves(self):
        valid_moves_list = []       #Clears all moves each time that it is called

        for row in range(len(self.squares)):        
                for column in range(len(self.squares)):             #Gets valid moves for every piece on the board
                    if self.squares[row][column] != 0:          
                        valid_moves_list.extend(self.squares[row][column].valid_moves(self.squares))

        print(valid_moves_list)
        return valid_moves_list


                    


