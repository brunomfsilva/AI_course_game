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
    size= 5

    
    pygame.init()
    gui = GUI()
    #difficults = ['Very easy', 'Easy', 'Medium', 'Hard']


    sizes = []
    p1_difs = []
    p2_difs = []
    total_plays = []
    total_time = []
    player_winner = []
    p1_medium_time_play = []
    p1_medium_time_play_catch = []
    p2_medium_time_play = []
    p2_medium_time_play_catch = []

    

    # games = [
    #     ('Minimax', evaluate, 5, 'Minimax', evaluate_2, 5, 5, 5),
    #     ('Minimax', evaluate, 5, 'Minimax', evaluate_3, 5, 5, 5),
    #     ('Minimax', evaluate_2, 5, 'Minimax', evaluate_3, 5, 5, 5),
    #     ('Minimax', evaluate, 2, 'Minimax', evaluate_2, 2, 5, 5),
    #     ('Minimax', evaluate, 2, 'Minimax', evaluate_3, 2, 5, 5),
    #     ('Minimax', evaluate_2, 2, 'Minimax', evaluate_3, 2, 5, 5),
    #     ('Montecarlo', 100, 'Montecarlo', 500, 5, 3),
    #     ('Montecarlo', 100, 'Montecarlo', 1000, 5, 3),
    #     ('Montecarlo', 500, 'Montecarlo', 1000, 5, 3),
    #     ('Montecarlo', 1000, 'Montecarlo', 1000, 5, 1),
    #     ('Montecarlo', 1000, 'Montecarlo', 1000, 8, 1),
    #     ('Minimax', evaluate, 2, 'Montecarlo', 100, 5, 3),
    #     ('Minimax', evaluate, 2, 'Montecarlo', 1000, 5, 3),
    #     ('Minimax', evaluate, 2, 'Montecarlo', 5000, 5, 3),
    #     ('Minimax', evaluate, 5, 'Montecarlo', 100, 5, 3),
    #     ('Minimax', evaluate, 5, 'Montecarlo', 1000, 5, 3),
    #     ('Minimax', evaluate, 5, 'Montecarlo', 5000, 5, 3),
    #     ('Minimax', evaluate, 7, 'Montecarlo', 100, 5, 3),
    #     ('Minimax', evaluate, 7, 'Montecarlo', 1000, 5, 3),
    #     ('Minimax', evaluate, 7, 'Montecarlo', 5000, 5, 3),
    # ]
    for _ in range(20):
        board = Board(5)
        board.initialize_pieces()
        selected_piece = None
        turn = WHITE
        winner = False
        p1_difficult = random.randint(0, 3)
       
        p2_difficult = p1_difficult 
        while p2_difficult == p1_difficult:
            p2_difficult = random.randint(0, 3)
        
        # if p1_difficult == 0 and p2_difficult==2:
        #     p2_difficult == 1

        player1 = Player('Montecarlo', 100, WHITE)
        player2 = Player('Minimax', 5, BLACK)

        print(board.size, p1_difficult, p2_difficult)

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

                if player.type == 'AI' and turn == player.team:
                    if player.level == 'Very easy':
                        depth= 1
                    elif player.level == 'Easy':
                        depth= 2
                    elif player.level == 'Medium':
                        depth= 4
                    elif player.level == 'Hard':
                        depth= 5
                    
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
                            'sizes': sizes,
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