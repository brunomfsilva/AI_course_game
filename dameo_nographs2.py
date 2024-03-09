import pygame
from board import Board
from piece import Piece
from ai import *
from vars import *
from player import Player
import time
from player import *
import random
import pandas as pd
import statistics

def calculate_time(start_time):
    return time.time() - start_time

def main():
    """Initiate game"""

    games = [
        ('Minimax', 1, 5, 'Minimax', 2, 5, 5, 5),
        ('Minimax', 1, 5, 'Minimax', 3, 5, 5, 5),
        ('Minimax', 2, 5, 'Minimax', 3, 5, 5, 5),
        ('Minimax', 1, 2, 'Minimax', 2, 2, 5, 5),
        ('Minimax', 1, 2, 'Minimax', 3, 2, 5, 5),
        ('Minimax', 2, 2, 'Minimax', 3, 2, 5, 5),
        ('Montecarlo', 'NA', 100, 'Montecarlo', 'NA', 500, 5, 3),
        ('Montecarlo', 'NA', 100, 'Montecarlo', 'NA', 1000, 5, 3),
        ('Montecarlo', 'NA', 500, 'Montecarlo', 'NA', 1000, 5, 3),
        ('Montecarlo', 'NA', 1000, 'Montecarlo', 'NA', 1000, 5, 1),
        ('Montecarlo', 'NA', 1000, 'Montecarlo', 'NA', 1000, 8, 1),
        ('Montecarlo', 'NA', 100, 'Minimax', 1, 2, 5, 3),
        ('Montecarlo', 'NA', 100, 'Minimax', 1, 5, 5, 3),
        ('Montecarlo', 'NA', 100, 'Minimax', 1, 7, 5, 3),
        ('Montecarlo', 'NA', 500, 'Minimax', 1, 2, 5, 3),
        ('Montecarlo', 'NA', 500, 'Minimax', 1, 5, 5, 3),
        ('Montecarlo', 'NA', 500, 'Minimax', 1, 7, 5, 3),
        ('Montecarlo', 'NA', 1000, 'Minimax', 1, 2, 5, 3),
        ('Montecarlo', 'NA', 1000, 'Minimax', 1, 5, 5, 3),
        ('Montecarlo', 'NA', 1000, 'Minimax', 1, 7, 5, 3)
    ]
        # (algorithm_1, eval_function, depth, algorithm_2, eval_function, depth, board_size, n_games)

    p1_difs = []
    p2_difs = []
    total_plays = []
    total_time = []
    player_winner = []
    p1_medium_time_play = []
    p1_medium_time_play_catch = []
    p2_medium_time_play = []
    p2_medium_time_play_catch = []

    for i in range(len(games)):
        for _ in range(games[i][7]):
            board = Board(games[i][6])
            board.initialize_pieces()
            selected_piece = None
            turn = WHITE
            winner = False

            player1 = Player(games[i][0], games[i][2], WHITE)
            player2 = Player(games[i][3], games[i][5], BLACK)

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
                    
                    start_time_play = time.time()
                    selected_piece = player.get_ai_move(board, games[i][1]) if player == player1 else player.get_ai_move(board, games[i][4])

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
                        playtime = calculate_time(start_time_play)

                        if catch == True:
                            if turn == WHITE:
                                p1_times_can_catch.append(playtime)


                            if turn == BLACK:
                                p2_times_can_catch.append(playtime)

                        if catch == False:
                            if turn == WHITE:
                                p1_times_no_catch.append(playtime)

                            if turn == BLACK:
                                p2_times_no_catch.append(playtime)



                        if turn == WHITE:
                            turn = BLACK  
                        else:
                            turn = WHITE
                        

                    end_time_play = time.time()

                        #time.sleep(1)
                    
                    n_plays += 1
                    winner = board.check_winner()

                    if winner:
                        print(winner + ' Wins!')
                        end_time = time.time()
                        p1_difs.append(p1_difficult)
                        p2_difs.append(p2_difficult)
                        total_plays.append(n_plays)
                        total_time.append(end_time - start_time)
                        player_winner.append(winner)

                        try:
                            p1_medium_time_play.append(statistics.mean(p1_times_no_catch))
                        except:
                            p1_medium_time_play.append('not eat')

                        try:
                            p1_medium_time_play_catch.append(statistics.mean(p1_times_can_catch))
                        except:
                            p1_medium_time_play_catch.append('not eat')
                        try:
                            p2_medium_time_play.append(statistics.mean(p2_times_no_catch))
                        except:
                            p2_medium_time_play.append('not eat')

                        try:
                            p2_medium_time_play_catch.append(statistics.mean(p2_times_can_catch))
                        except:
                            p2_medium_time_play_catch.append('no eat')
                            
                        data = {
                                'p1_difficult': p1_difs,
                                'p2_difficult': p2_difs,
                                'player_winner': player_winner,
                                'total_plays': total_plays,
                                'total_time': total_time,
                                'p1_medium_time_play': p1_medium_time_play,
                                'p1_medium_time_play_catch':p1_medium_time_play_catch,
                                'p2_medium_time_play': p2_medium_time_play,
                                'p2_medium_time_play_catch':p2_medium_time_play_catch,
                                }
                        
                        df = pd.DataFrame(data)
                        df.to_csv('game_results_5_2.csv', index=False)

                        
                        game_over = True
                        running = False

if __name__ == "__main__":
    main()