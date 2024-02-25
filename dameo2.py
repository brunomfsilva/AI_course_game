import pygame
from board import Board
from piece import Piece
from dameo_gui import GUI
from vars import *
from player import Player
import time

def main():
    """Initiate game"""
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('DAMEO')
    running = True
    gui = GUI()
    board=Board()
    board.start_game(gui, screen)
    selected_piece = None
    turn = WHITE
    winner = None
    player2 = Player('AI', 'Very easy', BLACK)
    human = Player('Human', 'Human', WHITE)
    # Create
    # more
    # players

    while running:
        if turn == human.team:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        else:
            player2.ai_random_move(board, turn)
            if turn == WHITE:
                turn = BLACK  
            else:
                turn = WHITE          
            time.sleep(3)
            board.actual_state(screen)
            pygame.display.flip()

if __name__ == "__main__":
    main()