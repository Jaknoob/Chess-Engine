import pygame
from consts import *

class Piece:
    def __init__(self, rank, file, colour):
        self.rank = rank
        self.file = file
        self.colour = colour
        self.is_king = False
        self.is_pawn = False
        self.selected = False

    def is_selected(self):
        return self.selected

    def move_validation(self):
        pass

    def draw_piece(self, surface, x , y):
        transparent_image = self.image.convert_alpha() #Makes PNG background transparent
        surface.blit(transparent_image, (x, y)) #Draws image onto screen

    def change_position(self):
        pass

class Pawn(Piece):
    def __init__(self, rank, file, colour):
        super().__init__(rank, file, colour)
        if colour == "white":
            self.image = WHITE_PAWN_IMG
        else:
            self.image = BLACK_PAWN_IMG

class Knight(Piece):
    def __init__(self, rank, file, colour):
        super().__init__(rank, file, colour)
        if colour == "white":
            self.image = WHITE_KNIGHT_IMG
        else:
            self.image = BLACK_KNIGHT_IMG

class Bishop(Piece):
    def __init__(self, rank, file, colour):
        super().__init__(rank, file, colour)
        if colour == "white":
            self.image = WHITE_BISHOP_IMG
        else:
            self.image = BLACK_BISHOP_IMG

class Rook(Piece):
    def __init__(self, rank, file, colour):
        super().__init__(rank, file, colour)
        if colour == "white":
            self.image = WHITE_ROOK_IMG
        else:
            self.image = BLACK_ROOK_IMG

class Queen(Piece):
    def __init__(self, rank, file, colour):
        super().__init__(rank, file, colour)
        if colour == "white":
            self.image = WHITE_QUEEN_IMG
        else:
            self.image = BLACK_QUEEN_IMG

class King(Piece):
    def __init__(self, rank, file, colour):
        super().__init__(rank, file, colour)
        if colour == "white":
            self.image = WHITE_KING_IMG
        else:
            self.image = BLACK_KING_IMG