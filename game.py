import pygame
from consts import *

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with the desired color
        screen.fill(BACKGROUND_COLOUR)

        # Update the screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS

    pygame.quit()
