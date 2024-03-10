import pygame
from board import Board
from piece import Piece
from dameo_gui import GUI
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
    

    
    #pygame.init()
    #gui = GUI()
    #difficults = ['Very easy', 'Easy', 'Medium', 'Hard']


    sizes = []
    p1_depth_or_iterations = []
    p2_depth_or_iterations = []
    p1_algorithm =[]
    p2_algorithm =[]
    p1_evaluation=[]
    p2_evaluation=[]
    total_plays = []
    total_time = []
    player_winner = []
    p1_medium_time_play = []
    p1_medium_time_play_catch = []
    p2_medium_time_play = []
    p2_medium_time_play_catch = []


    p1 = [
    ('Minimax', 1, 5),
    ('Minimax', 1, 5),
    ('Minimax', 2, 5),
    ('Minimax', 1, 2),
    ('Minimax', 1, 2),
    ('Minimax', 2, 2),
    ('Montecarlo', 'NA', 100),
    ('Montecarlo', 'NA', 100),
    ('Montecarlo', 'NA', 100),
    ('Montecarlo', 'NA', 100),
    ('Montecarlo', 'NA', 100),
    ('Montecarlo', 'NA', 100),
    ('Montecarlo', 'NA', 500),
    ('Montecarlo', 'NA', 500),
    ('Montecarlo', 'NA', 500),
    ('Montecarlo', 'NA', 1000),
    ('Montecarlo', 'NA', 100),
    ('Montecarlo', 'NA', 100),
    ('Montecarlo', 'NA', 100),
    ('Montecarlo', 'NA', 500),
    ('Montecarlo', 'NA', 500),
    ('Montecarlo', 'NA', 500),
    ('Montecarlo', 'NA', 1000),
    ('Montecarlo', 'NA', 1000),
    ('Montecarlo', 'NA', 1000),
    ('Montecarlo', 'NA', 1000),
    ('Montecarlo', 'NA', 2000),
    ('Montecarlo', 'NA', 3000),
    ('Montecarlo', 'NA', 4000),
    ('Montecarlo', 'NA', 5000),
]


    p2 = [
        ('Minimax', 2, 5),
        ('Minimax', 3, 5),
        ('Minimax', 3, 5),
        ('Minimax', 2, 2),
        ('Minimax', 3, 2),
        ('Minimax', 3, 2),
        ('Montecarlo', 'NA', 500),
        ('Montecarlo', 'NA', 500),
        ('Montecarlo', 'NA', 500),
        ('Montecarlo', 'NA', 1000),
        ('Montecarlo', 'NA', 1000),
        ('Montecarlo', 'NA', 1000),
        ('Montecarlo', 'NA', 1000),
        ('Montecarlo', 'NA', 1000),
        ('Montecarlo', 'NA', 1000),
        ('Montecarlo', 'NA', 1000),
        ('Minimax', 1, 2),
        ('Minimax', 1, 5),
        ('Minimax', 1, 7),
        ('Minimax', 1, 2),
        ('Minimax', 1, 5),
        ('Minimax', 1, 7),
        ('Minimax', 1, 2),
        ('Minimax', 1, 5),
        ('Minimax', 1, 7),
        ('Minimax', 1, 5),
        ('Minimax', 1, 5),
        ('Minimax', 1, 5),
        ('Minimax', 1, 5),
        ('Minimax', 1, 5)
    ]

    board_size = [5,5,5,5,5,5,5,6,7,5,6,7,5,6,7,8,5,5,5,5,5,5,5,5,5,6,6,6,6,6]

    n_games = [1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,1,3,3,3,3,3,3,3,3,3,5,5,5,5,5]




    for n, size in enumerate(board_size):
        try:
            for n_game in range(n_games[n]):
                size= board_size[n]
                board = Board(size)
                board.initialize_pieces()
                selected_piece = None
                turn = WHITE
                winner = False
                
                pls = [p1[n], p2[n]]

                pl1_index = random.randint(0,1)
                pl2_index = random.randint(0,1)

                while pl1_index == pl2_index:
                    pl2_index = random.randint(0,1)
                
                pl1 = pls[pl1_index]
                pl2 = pls[pl2_index]

                print ('n: ', n, ' n_game: ', n_game, ' size: ',size, pl1, pl2)

                player1 = Player(pl1[0], pl1[2], WHITE, pl1[1])
                player2 = Player(pl2[0], pl2[2], BLACK, pl2[1])

                p1_algorithm.append(pl1[0])
                p2_algorithm.append(pl2[0])
                p1_evaluation.append(pl1[1])
                p2_evaluation.append(pl2[2])
                



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
                        start_time_play = time.time()
                            

                        
                        

                        if player.type != 'Human' and turn == player.team:

                            can_catch = board.check_piece_to_capture(turn)
                            if can_catch:
                                catch= True
                            selected_piece = player.get_ai_move(board)

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
                            sizes.append(size)
                            p1_depth_or_iterations.append(pl1[2])
                            p2_depth_or_iterations.append(pl2[2])
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
                                    'sizes': sizes,
                                    'p1_difficult': p1_depth_or_iterations,
                                    'p2_difficult': p2_depth_or_iterations,
                                    'p1_algorithm': p1_algorithm,
                                    'p2_algorithm': p2_algorithm,
                                    'p1_evaluation': p1_evaluation,
                                    'p2_evaluation': p2_evaluation,
                                    'player_winner': player_winner,
                                    'total_plays': total_plays,
                                    'total_time': total_time,
                                    'p1_medium_time_play': p1_medium_time_play,
                                    'p1_medium_time_play_catch':p1_medium_time_play_catch,
                                    'p2_medium_time_play': p2_medium_time_play,
                                    'p2_medium_time_play_catch':p2_medium_time_play_catch,
                                    }
                            
                            df = pd.DataFrame(data)
                            df.to_csv('game_results.csv', index=False)

                            
                            game_over = True
                            running = False

        except:
            null_row = {col: None for col in df.columns}
            df = df.append(null_row, ignore_index=True)
            df.to_csv('game_results.csv', index=False)
            continue

if __name__ == "__main__":
    main()