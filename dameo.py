import pygame
from board import Board
from piece import Piece
from dameo_gui import GUI
from vars import *
from player import Player
import time
from player import *
import ai

def main():
    """Initiate game"""
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('DAMEO')
    running = True
    gui = GUI()
    players, size = gui.main_menu(screen)  # [player1, player2, depth1, depth2], size board
    print(players)
    square_size = int(min(width, height)/size)
    gui.square_size = square_size
    board=Board(size)
    board.start_game(gui, screen)
    selected_piece = None
    turn = WHITE
    winner = None
    player1 = Player(players[0], players[2], WHITE)
    player2 = Player(players[1], players[3], BLACK)

    game_over=False

    while running:

        for event in pygame.event.get():
          #  if event.type == pygame.QUIT:
           #     running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                if winner:
                    winner = None
                    game_over = False
                    players, size = gui.main_menu(screen)
                    square_size = int(min(width, height)/size)
                    gui.square_size = square_size
                    board.change_size(size)
                    board.start_game(gui, screen)
                    player1 = Player(players[0], players[2], WHITE)
                    player2 = Player(players[1], players[3], BLACK)
                    selected_piece = None
                    turn = WHITE
                    board.turn = WHITE
                                        
            
            if game_over:
                break
            
            while not game_over and running:
                for player in (player1, player2):
                    
                    if player.type == 'Human' and turn == player.team:
                        selected_piece = player.get_human_move(board, gui, screen, winner, square_size, selected_piece)
                    

                    if player.type != 'Human' and turn == player.team:
                    #else:
                        selected_piece = player.get_ai_move(board)

                    # Checking if there are other pieces to catch
                    if not selected_piece.king:
                        selected_piece.check_catch(board)
                    else:
                        selected_piece.check_catch_king(board)
    
                    if selected_piece.legal and selected_piece.has_caught:
                        pass # NOT NEEDED
                    
                    else:
                        selected_piece.transform_king()
                        selected_piece = None #turn off the selected piece
                        if turn == WHITE:
                            turn = BLACK
                            board.turn = BLACK  
                        else:
                            turn = WHITE
                            board.turn = WHITE
    
                        
                        board.actual_state(screen)
                        gui.display_turn(screen, "player 1" if turn == WHITE else "player 2")
                        time.sleep(0.5)
                        pygame.display.flip()
                    

                    winner = board.check_winner()
                    

                    if winner:
                        efeito_w = pygame.mixer.Sound("sounds\winner.mp3")
                        game_over = True
                        efeito_w.play()
                        font = pygame.font.SysFont("Impact", 45)
                        if winner == 'Tie':
                            text = font.render("It is a Tie!", True, (255, 255, 153))
                        elif winner and winner != 'Tie':
                            text = font.render(f"The Winner is {winner}!", True, (255, 255, 153))
                        screen.blit(text, (100, height // 2))
                        pygame.display.flip()
                        break

if __name__ == "__main__":
    main()