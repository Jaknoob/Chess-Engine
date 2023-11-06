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

    def draw_piece(self, surface, x , y):
        transparent_image = self.image.convert_alpha() #Makes PNG background transparent
        surface.blit(transparent_image, (x, y)) #Draws image onto screen


class Pawn(Piece):
    def __init__(self, rank, file, colour):
        super().__init__(rank, file, colour)
        if colour == "white":
            self.image = WHITE_PAWN_IMG
        else:
            self.image = BLACK_PAWN_IMG

    def valid_moves(self, squares):
        valid_moves_list = []
        if self.colour == "white":                                                          #Direction of move depends on colour
            direction = -1
        elif self.colour == "black":
            direction = 1

        if squares[self.rank + direction][self.file] == 0:
            valid_moves_list.append((self, self.file ,self.rank, self.file, self.rank + direction))         #Move 1 square forward
            if (self.colour == "black" and self.rank == 1) or (self.colour == "white" and self.rank == 6):      #If in starting position
                if squares[self.rank + direction*2][self.file] == 0:
                    valid_moves_list.append((self, self.file ,self.rank, self.file, self.rank + direction*2))       #Move 2 squares forward

        if self.file < 7:
            if squares[self.rank + direction][self.file + 1] != 0:
                if squares[self.rank + direction][self.file + 1].colour != self.colour:                      #Check for captures forward and right
                    valid_moves_list.append((self, self.file ,self.rank, self.file + 1, self.rank + direction))

        if self.file > 0:    
            if squares[self.rank + direction][self.file - 1] != 0:
                if squares[self.rank + direction][self.file - 1].colour != self.colour:                      #Check for captures forward and left
                    valid_moves_list.append((self, self.file ,self.rank, self.file - 1, self.rank + direction))
        
        return valid_moves_list

class Knight(Piece):
    def __init__(self, rank, file, colour):
        super().__init__(rank, file, colour)
        if colour == "white":
            self.image = WHITE_KNIGHT_IMG
        else:
            self.image = BLACK_KNIGHT_IMG
    
    def valid_moves(self, squares):
        valid_moves_list = []
        dr = self.move_check(squares, valid_moves_list, 1, 2)       #Checks for moves 2 down and 1 right
        dl = self.move_check(squares, valid_moves_list, -1, 2)       #Checks for moves 2 down and 1 left
        ur = self.move_check(squares, valid_moves_list, 1, -2)       #Checks for moves 2 up and 1 right
        ul = self.move_check(squares, valid_moves_list, -1, -2)      #Checks for moves 2 up and 1 left
        ru = self.move_check(squares, valid_moves_list, 2, -1)      #Checks for moves 1 up and 2 right
        rd = self.move_check(squares, valid_moves_list, 2, 1)      #Checks for moves 1 down and 2 right
        lu = self.move_check(squares, valid_moves_list, -2, -1)      #Checks for moves 1 up and 2 left
        ld = self.move_check(squares, valid_moves_list, -2, 1)      #Checks for moves 1 down and 2 left

        valid_moves_list = [*dr, *ur, *dl, *ul, *ru, *rd, *ld, *lu]

        return valid_moves_list
        

    def move_check(self, squares, valid_moves_list, direction_file, direction_rank):
        temp_file = self.file
        temp_rank = self.rank
        temp_file = temp_file + direction_file             #Continues move in set direction
        temp_rank = temp_rank + direction_rank
        if 0 <= temp_file <= 7 and 0 <= temp_rank <= 7:      #While move is on the chessboard
            if squares[temp_rank][temp_file] !=0:
                if squares[temp_rank][temp_file].colour == self.colour:
                    return valid_moves_list
                else:
                    valid_moves_list.append((self, self.file ,self.rank, temp_file, temp_rank))
            else:
                valid_moves_list.append((self, self.file ,self.rank, temp_file, temp_rank))
            
            
        return valid_moves_list

class Bishop(Piece):
    def __init__(self, rank, file, colour):
        super().__init__(rank, file, colour)
        if colour == "white":
            self.image = WHITE_BISHOP_IMG
        else:
            self.image = BLACK_BISHOP_IMG

    def valid_moves(self, squares):
        valid_moves_list = []
        dr = self.move_check(squares, valid_moves_list, 1, 1)     #Checks for moves down and right
        ur = self.move_check(squares, valid_moves_list, 1, -1)       #Checks for moves up and right
        dl = self.move_check(squares, valid_moves_list, -1, 1)       #Checks for moves down and left
        ul = self.move_check(squares, valid_moves_list, -1, -1)      #Checks for moves up and left

        valid_moves_list = [*dr, *ur, *dl, *ul]

        return valid_moves_list
        

    def move_check(self, squares, valid_moves_list, direction_file, direction_rank):
        temp_file = self.file
        temp_rank = self.rank
        temp_file = temp_file + direction_file             #Continues move in set direction
        temp_rank = temp_rank + direction_rank
        while 0 <= temp_file <= 7 and 0 <= temp_rank <= 7:      #While move is on the chessboard
            if squares[temp_rank][temp_file] !=0:
                if squares[temp_rank][temp_file].colour == self.colour:
                    break
            valid_moves_list.append((self, self.file ,self.rank, temp_file, temp_rank))
            if squares[temp_rank][temp_file] != 0:
                if squares[temp_rank][temp_file] != self:
                    break
            temp_file = temp_file + direction_file             #Continues move in set direction
            temp_rank = temp_rank + direction_rank
            
        return valid_moves_list
            
            


class Rook(Piece):
    def __init__(self, rank, file, colour):
        super().__init__(rank, file, colour)
        if colour == "white":
            self.image = WHITE_ROOK_IMG
        else:
            self.image = BLACK_ROOK_IMG

    def valid_moves(self, squares):
        valid_moves_list = []
        up = self.move_check(squares, valid_moves_list, 0, -1)     #Checks for moves up
        down = self.move_check(squares, valid_moves_list, 0, 1)       #Checks for moves down
        left = self.move_check(squares, valid_moves_list, -1, 0)       #Checks for moves left
        right = self.move_check(squares, valid_moves_list, 1, 0)      #Checks for moves right

        valid_moves_list = [*up, *down, *left, *right]

        return valid_moves_list
        

    def move_check(self, squares, valid_moves_list, direction_file, direction_rank):
        temp_file = self.file
        temp_rank = self.rank
        temp_file = temp_file + direction_file             #Continues move in set direction
        temp_rank = temp_rank + direction_rank
        while 0 <= temp_file <= 7 and 0 <= temp_rank <= 7:      #While move is on the chessboard
            if squares[temp_rank][temp_file] !=0:
                if squares[temp_rank][temp_file].colour == self.colour:
                    break
            valid_moves_list.append((self, self.file ,self.rank, temp_file, temp_rank))
            if squares[temp_rank][temp_file] != 0:
                if squares[temp_rank][temp_file] != self:
                    break
            temp_file = temp_file + direction_file             #Continues move in set direction
            temp_rank = temp_rank + direction_rank
            
        return valid_moves_list
            

class Queen(Piece):
    def __init__(self, rank, file, colour):
        super().__init__(rank, file, colour)
        if colour == "white":
            self.image = WHITE_QUEEN_IMG
        else:
            self.image = BLACK_QUEEN_IMG

    def valid_moves(self, squares):
        valid_moves_list = []
        up = self.move_check(squares, valid_moves_list, 0, -1)     #Checks for moves up
        down = self.move_check(squares, valid_moves_list, 0, 1)       #Checks for moves down
        left = self.move_check(squares, valid_moves_list, -1, 0)       #Checks for moves left
        right = self.move_check(squares, valid_moves_list, 1, 0)      #Checks for moves right
        dr = self.move_check(squares, valid_moves_list, 1, 1)     #Checks for moves down and right
        ur = self.move_check(squares, valid_moves_list, 1, -1)       #Checks for moves up and right
        dl = self.move_check(squares, valid_moves_list, -1, 1)       #Checks for moves down and left
        ul = self.move_check(squares, valid_moves_list, -1, -1)      #Checks for moves up and left

        valid_moves_list = [*up, *down, *left, *right, *dr, *ur, *dl, *ul]

        return valid_moves_list
        

    def move_check(self, squares, valid_moves_list, direction_file, direction_rank):
        temp_file = self.file
        temp_rank = self.rank
        temp_file = temp_file + direction_file             #Continues move in set direction
        temp_rank = temp_rank + direction_rank
        while 0 <= temp_file <= 7 and 0 <= temp_rank <= 7:      #While move is on the chessboard
            if squares[temp_rank][temp_file] != 0:
                if squares[temp_rank][temp_file].colour == self.colour:
                    break
            valid_moves_list.append((self, self.file ,self.rank, temp_file, temp_rank))
            if squares[temp_rank][temp_file] != 0:
                if squares[temp_rank][temp_file] != self:
                    break
            temp_file = temp_file + direction_file             #Continues move in set direction
            temp_rank = temp_rank + direction_rank
            
        return valid_moves_list

class King(Piece):
    def __init__(self, rank, file, colour):
        super().__init__(rank, file, colour)
        if colour == "white":
            self.image = WHITE_KING_IMG
        else:
            self.image = BLACK_KING_IMG

    def valid_moves(self, squares):
        valid_moves_list = []
        up = self.move_check(squares, valid_moves_list, 0, -1)     #Checks for moves up
        down = self.move_check(squares, valid_moves_list, 0, 1)       #Checks for moves down
        left = self.move_check(squares, valid_moves_list, -1, 0)       #Checks for moves left
        right = self.move_check(squares, valid_moves_list, 1, 0)      #Checks for moves right
        dr = self.move_check(squares, valid_moves_list, 1, 1)     #Checks for moves down and right
        ur = self.move_check(squares, valid_moves_list, 1, -1)       #Checks for moves up and right
        dl = self.move_check(squares, valid_moves_list, -1, 1)       #Checks for moves down and left
        ul = self.move_check(squares, valid_moves_list, -1, -1)      #Checks for moves up and left

        valid_moves_list = [*up, *down, *left, *right, *dr, *ur, *dl, *ul]

        return valid_moves_list
        

    def move_check(self, squares, valid_moves_list, direction_file, direction_rank):
        temp_file = self.file
        temp_rank = self.rank
        temp_file = temp_file + direction_file             #Continues move in set direction
        temp_rank = temp_rank + direction_rank
        if 0 <= temp_file <= 7 and 0 <= temp_rank <= 7:      #While move is on the chessboard
            if squares[temp_rank][temp_file] !=0:
                if squares[temp_rank][temp_file].colour == self.colour:
                    return valid_moves_list
                else:
                    valid_moves_list.append((self, self.file ,self.rank, temp_file, temp_rank))
            else:
                valid_moves_list.append((self, self.file ,self.rank, temp_file, temp_rank))
            
            
        return valid_moves_list
            
