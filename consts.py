import pygame
import os

pygame.init()

#Screen data
info = pygame.display.Info()
HEIGHT = info.current_h
WIDTH = info.current_w
FPS = 30

#Images
WHITE_PAWN_IMG = pygame.image.load(os.path.join("Sources", "Chess_plt60.png"))
WHITE_KNIGHT_IMG = pygame.image.load(os.path.join("Sources", "Chess_nlt60.png"))
WHITE_BISHOP_IMG = pygame.image.load(os.path.join("Sources", "Chess_blt60.png"))
WHITE_ROOK_IMG = pygame.image.load(os.path.join("Sources", "Chess_rlt60.png"))
WHITE_QUEEN_IMG = pygame.image.load(os.path.join("Sources", "Chess_qlt60.png"))
WHITE_KING_IMG = pygame.image.load(os.path.join("Sources", "Chess_klt60.png"))

BLACK_PAWN_IMG = pygame.image.load(os.path.join("Sources", "Chess_pdt60.png"))
BLACK_KNIGHT_IMG = pygame.image.load(os.path.join("Sources", "Chess_kdt60.png"))
BLACK_BISHOP_IMG = pygame.image.load(os.path.join("Sources", "Chess_bdt60.png"))
BLACK_ROOK_IMG = pygame.image.load(os.path.join("Sources", "Chess_rdt60.png"))
BLACK_QUEEN_IMG = pygame.image.load(os.path.join("Sources", "Chess_qdt60.png"))
BLACK_KING_IMG = pygame.image.load(os.path.join("Sources", "Chess_kdt60.png"))

#Colours
BACKGROUND_COLOUR = (147,84,25)
LIGHT_BACKGROUND_COLOUR = (204,145,91)
LIGHT_SQUARE_COLOUR = (198,131,69)
DARK_SQUARE_COLOUR = (175,105,40)
BLACK = (30,30,30)
WHITE = (255,255,255)
BLUNDER_COLOUR = (255,47,0)
MISTAKE_COLOUR = (230,175,108)
GOOD_MOVE_COLOUR = (208,245,195)
GREAT_MOVE_COLOUR = (78,202,34)
