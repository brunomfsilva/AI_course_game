import pygame
from board import Board
from piece import Piece
from dameo_gui import GUI
from vars import *
from player import Player
import time
from player import *

def main():
    """Initiate game"""
    pygame.init()
    running = True
    gui = GUI()
    board=Board()
    board.initialize_pieces()
    selected_piece = None
    turn = WHITE
    winner = None
    player1 = Player('AI', 'Very easy', WHITE)
    player2 = Player('AI', 'Hard', BLACK)


    game_over=False
    while running:
            
        n_plays=0
        while not game_over and running:
            
            for player in (player1, player2):
                n_plays+=1
                print(n_plays)
                
                if game_over:
                    break
                
                if player.type == 'AI' and player.level == 'Very easy' and turn == player.team:
                    selected_piece = player.ai_random_move(board, turn)

                if player.type == 'AI' and player.level == 'Hard' and turn == player.team:
                    selected_piece, best_move = execute_minimax(board, 5, turn)
                    board.chessboard[selected_piece.row][selected_piece.col] = None
                    selected_piece.move(best_move[0], best_move[1], board)
                    board.chessboard[selected_piece.row][selected_piece.col] = selected_piece

                # Checking if there are other pieces to catch
                if not selected_piece.king:
                    selected_piece.check_catch(board)
                else:
                    selected_piece.check_catch_king(board)

                if selected_piece.legal and selected_piece.has_caught:
                    # if turn == WHITE:
                    #     turn = WHITE  
                    # else:
                    #     turn = BLACK
                    pass # NOT NEEDED
                else:
                    selected_piece.transform_king()
                    selected_piece = None #turn off the selected piece
                    if turn == WHITE:
                        turn = BLACK  
                    else:
                        turn = WHITE

                    #time.sleep(1)
    
                winner = board.check_winner()

                if winner:
                    print(winner + ' Wins!')
                    game_over = True
                    running = False

if __name__ == "__main__":
    main()