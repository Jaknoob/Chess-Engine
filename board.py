import pygame
from consts import *
from piece import Pawn, Knight, Bishop, Rook, Queen, King

class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns              
        self.start_x = WIDTH/4              #Position on the screen from the left where chessboard should start being drawn
        self.start_y = HEIGHT/8             #Position on the screen from the top where chessboard should start being drawn
        self.square_size = HEIGHT/12        #Size of the squares on the chessboard
        self.squares = []
        
        
        for _ in range(rows):
            row = []
            for _ in range(columns):        #Creates a 2 dimensional array full of 0s
                row.append(0)
            self.squares.append(row)

        print(self.squares)
        print(self.square_size)

    
    #Displays the chessboard on the screen, passes the surface to be drawn onto as a parameter

    def draw_board(self, surface: pygame.Surface): 
        outer_border = pygame.Rect(self.start_x -5, self.start_y -5, (self.square_size*8) + 10, (self.square_size*8) + 10)        
        pygame.draw.rect(surface, BLACK, outer_border, 5)   #Draws the outer border around the chessboard

        temp_x = self.start_x
        temp_y = self.start_y

        for row in range(len(self.squares)):                        #Loops through rows and columns in array
            for column in range(len(self.squares[row])):
                square = pygame.Rect(temp_x, temp_y, self.square_size, self.square_size)
                
                if self.squares[row][column] == 0 or self.squares[row][column].is_selected() == False:
                    if column % 2 == row % 2:       
                        pygame.draw.rect(surface, DARK_SQUARE_COLOUR, square)   #Draws a dark square when rows and columns are both odd, or both even
                    else:
                        pygame.draw.rect(surface, LIGHT_SQUARE_COLOUR, square)
                    if self.squares[row][column] !=0:
                        self.squares[row][column].draw_piece(surface, temp_x, temp_y)
                else:
                    pygame.draw.rect(surface, SELECTED_SQUARE_COLOUR, square)
                    self.squares[row][column].draw_piece(surface, temp_x, temp_y)



                temp_x += self.square_size
            temp_x = self.start_x               #Reset temp_x after each row is completed.
            temp_y += self.square_size

    def starting_position(self):
        self.squares[0][0] = Rook(0,0,"black")
        self.squares[0][1] = Knight(0,1,"black")
        self.squares[0][2] = Bishop(0,2,"black")
        self.squares[0][3] = Queen(0,2,"black")
        self.squares[0][4] = King(0,4,"black")
        self.squares[0][5] = Bishop(0,5,"black")
        self.squares[0][6] = Knight(0,6,"black")
        self.squares[0][7] = Rook(0,7,"black")

        for i in range(8):
            self.squares[1][i] = Pawn(1,i,"black")
            self.squares[6][i] = Pawn(6,i,"white")

        self.squares[7][0] = Rook(7,0,"white")
        self.squares[7][2] = Bishop(7,2,"white")
        self.squares[7][3] = Queen(7,2,"white")
        self.squares[7][4] = King(7,4,"white")
        self.squares[7][5] = Bishop(7,5,"white")
        self.squares[7][6] = Knight(7,6,"white")
        self.squares[7][7] = Rook(7,7,"white")
        self.squares[7][1] = Knight(7,1,"white")

    def select(self, click: tuple):
        if (
            (click[0] >= self.start_x) and                  #If the user clicks inside the chessboard
            (click[0] <= self.start_x + self.square_size*8) and 
            (click[1] >= self.start_y) and 
            (click[1] <= self.start_y +self.square_size*8)
        ):
            click_x, click_y = click[0] - self.start_x, click[1] - self.start_y #Compares click to top left of board
            click_x, click_y = click_x / self.square_size, click_y / self.square_size #Puts difference in terms of squares
            click_x, click_y = click_x // 1, click_y // 1                       #Round down to the nearest integer

            selected_square = self.squares[int(click_y)][int(click_x)]
            self.unselect()
            if selected_square != 0:
                selected_square.selected = True
                selected_square.is_selected()
        else:
            self.unselect()


    #Loops through all the pieces and deselects all
    def unselect(self):
        for row in range(len(self.squares)):        
                for column in range(len(self.squares)):
                    if self.squares[row][column] != 0:
                        self.squares[row][column].selected = False
                    


