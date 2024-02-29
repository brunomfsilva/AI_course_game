import pygame
from board import Board
from piece import Piece
from dameo_gui import GUI
from vars import *
from player import Player
import time
from player import *
import random

def calculate_time(start_time):
    return time.time() - start_time

def main():
    """Initiate game"""
    pygame.init()
    gui = GUI()
    difficults = ['Very easy', 'Easy', 'Medium', 'Hard']


    sizes = []
    p1_difs = []
    p2_difs = []
    total_plays = []
    total_time = []
    p1_medium_time_play = []
    p2_medium_time_play_catch = []
    p2_medium_time_play = []
    p2_medium_time_play_catch = []


    for _ in range(2):
        size = random.randint(5, 7)
        board = Board()
        board.size = size
        board.initialize_pieces()
        selected_piece = None
        turn = WHITE
        winner = None
        p1_difficult = random.randint(0, 3)
        p2_difficult = random.randint(0, 3)
        player1 = Player('AI', difficults[p1_difficult], WHITE)
        player2 = Player('AI', difficults[p2_difficult], BLACK)
        
        print(size, p1_difficult, p2_difficult)

        game_over = False
        n_plays = 0
        

        start_time = time.time()
        p1_times_can_catch = []
        p2_times_can_catch = []
        p1_times_no_catch = []
        p2_times_no_catch = []

        while not game_over:
            for player in (player1, player2):
                catch = False
                if game_over:
                    break
                
                # if player.type == 'AI' and player.level == 'Very easy' and turn == player.team:
                #     selected_piece = player.ai_random_move(board, turn)

                if player.type == 'AI' and player.level != 'Very easy' and turn == player.team:
                    if player.level == 'Very Easy':
                        depth= 1
                    elif player.level == 'Easy':
                        depth= 2
                    elif player.level == 'Medium':
                        depth= 4
                    elif player.level == 'Hard':
                        depth= 6
                    
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
                
                n_plays += 1
                winner = board.check_winner()

                if winner:
                    end_time = time.time
                    sizes.append(size)
                    p1_difs.append(p1_difficult)
                    p2_difs.append(p2_difficult)
                    total_plays.append(n_plays)
                    total_time.append(end_time - start_time)


                    print(winner + ' Wins!')
                    game_over = True
                    running = False

if __name__ == "__main__":
    main()