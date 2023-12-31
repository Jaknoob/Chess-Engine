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
                if column % 2 == row % 2:       
                    pygame.draw.rect(surface, DARK_SQUARE_COLOUR, square)   #Draws a dark square when rows and columns are both odd, or both even
                else:
                    pygame.draw.rect(surface, LIGHT_SQUARE_COLOUR, square)
                if self.squares[row][column] !=0:
                    transparent_image = self.squares[row][column].image.convert_alpha() #Makes PNG background transparent
                    surface.blit(transparent_image, (temp_x, temp_y)) #Draws image onto screen

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