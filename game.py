import pygame
from board import Board
from chessAI import ChessAI
from consts import *

pygame.init()

clock_active = False
font = pygame.font.Font(None, 128)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
board = Board(8,8, screen, "white") 
bot = ChessAI(board, "black")


def main():
    # pygame setup
    
    clock = pygame.time.Clock()
    running = True

    
    board.starting_position()

    elapsed_time = 0  # Initialize elapsed_time outside the main loop

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                board.select(click())

        # Fill the screen with the desired color
        screen.fill(BACKGROUND_COLOUR)

        # Draw the Chessboard
        board.draw_board()
        draw_move_window(screen)

        if len(board.moves_history) != 0:
            print(move_translator(board.moves_history[-1], bot))
            if board.turn != bot.colour:
                elapsed_time = countdown(screen, clock, 600000, board, board.moves_history, elapsed_time)
        else:
            draw_clock(screen, 600000)

        if board.turn == bot.colour and not (board.is_checkmate(board.valid_moves_list) or board.is_stalemate(board.valid_moves_list)):
            board.draw_board()
            bot.play_best_move()


        # Update the screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS

    pygame.quit()

def click():
    return pygame.mouse.get_pos()

def draw_clock(screen, clock_value):
    clock_rect = (WIDTH/24, 3* HEIGHT/8, HEIGHT/3, WIDTH/12)
    minutes = clock_value // 60000
    seconds = (clock_value % 60000) // 1000
    time_str = "{:02d}:{:02d}".format(minutes, seconds)
    pygame.draw.rect(screen, (255,255,255), clock_rect)
    text = font.render(time_str, True, (0, 0, 0))  # Black text
    screen.blit(text, (WIDTH/12, 13* HEIGHT/32))

def countdown(screen, clock, timer_duration, board, moves_history, elapsed_time=0):
    start_ticks = pygame.time.get_ticks() - elapsed_time

    while len(board.moves_history) == len(moves_history):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.select(click())

        current_ticks = pygame.time.get_ticks()
        elapsed_time = current_ticks - start_ticks
        remaining_time = max(timer_duration - elapsed_time, 0)

        screen.fill(BACKGROUND_COLOUR)
        board.draw_board()

        if board.turn == bot.colour and not (board.is_checkmate(board.valid_moves_list) or board.is_stalemate(board.valid_moves_list)):
            bot.play_best_move()

        if len(board.moves_history) != 0:
            print(move_translator(board.moves_history[-1], bot))

        # Draw the board again (if needed)
        if board.turn != bot.colour or (board.is_checkmate(board.valid_moves_list) or board.is_stalemate(board.valid_moves_list)):
            board.draw_board()

        draw_clock(screen, remaining_time)
        clock.tick(FPS)
        pygame.display.flip()

        if remaining_time == 0:
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer

    return elapsed_time

def draw_move_window(screen):
    move_window_rect = (2* WIDTH/3, HEIGHT/16, 5* WIDTH/16, 7* HEIGHT/8)
    pygame.draw.rect(screen, MOVE_WINDOW_COLOUR, move_window_rect)

def move_translator(move, bot):
    letters = "abcdefgh"
    if move[0].colour == bot.colour:
        user = "Your opponent"
    else: 
        user = "You"
    piece_name = move[0].__class__.__name__
    move_string = f"{user} played {piece_icons[f'{move[0].colour}{piece_name}']}{letters[move[3]]}{move[4]}"
    return move_string
    








    


    
