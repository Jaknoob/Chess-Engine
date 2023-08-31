import pygame
from board import Board
from consts import *


def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    board = Board(8,8) 
    board.starting_position()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(board.select(click()))

        # Fill the screen with the desired color
        screen.fill(BACKGROUND_COLOUR)
        #Draw the Chessboard
        board.draw_board(screen)


        # Update the screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS

    pygame.quit()

def click():
    return pygame.mouse.get_pos()
