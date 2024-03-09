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
    players, size = gui.main_menu(screen)
    square_size = int(min(width, height)/size)
    gui.square_size = square_size
    board=Board(size)
    board.start_game(gui, screen)
    selected_piece = None
    turn = WHITE
    winner = None
    player1 = Player('Minimax', 5, WHITE, 1)
    player2 = Player('Minimax', 5, BLACK, 1)

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
                    
                    if player.type == 'AI':
                        if player.level == 'Very easy':
                            depth= 1
                        elif player.level == 'Easy':
                            depth= 2
                        elif player.level == 'Medium':
                            depth= 4
                        elif player.level == 'Hard':
                            depth= 5
                    
                    if player.type == 'Human' and turn == player.team:
                        selected_piece = player.get_human_move(board, gui, screen, winner, square_size, selected_piece)
                        # human_playing = True
                        # while human_playing:
                        #     for event in pygame.event.get():
                        #         if event.type == pygame.QUIT:
                        #             running = False
                        #             pygame.quit()
                        #         elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                        #             if winner:
                        #                 winner = None
                        #                 game_over = False
                        #                 players, size = gui.main_menu(screen)
                        #                 square_size = int(min(width, height)/size)
                        #                 gui.square_size = square_size
                        #                 board.change_size(size)
                        #                 board.start_game(gui, screen)
                        #                 player1 = Player(players[0], players[2], WHITE)
                        #                 player2 = Player(players[1], players[3], BLACK)
                        #                 selected_piece = None
                        #                 turn = WHITE
                        #                 board.turn = WHITE
                                        
        
                        #             x, y = pygame.mouse.get_pos()
                        #             row = y // square_size
                        #             col = x // square_size
        
                                    
                        #             piece = board.find_piece(row, col, board.all_pieces_black, board.all_pieces_white)
        
                                    
                        #             can_catch = board.check_piece_to_capture(turn)
                        #             piece = board.check_if_capture( gui, screen, can_catch, piece, turn, selected_piece) #check if piece already capture (if needed)
        
                        #             if piece and piece.color == turn:
                        #                 selected_piece = piece
                                        
                        #                 if not piece.king:
                        #                     selected_piece.check_catch(board)
                        #                 elif piece.king:
                        #                     selected_piece.check_catch_king(board)
                                            
                        #                 if not selected_piece.legal:
                        #                     selected_piece.legal_positions() # If there is no piece to catch, the legal moves list will be empty so we compute the moves normally
                        #                     selected_piece.check_position(board) # Remove the occupied spaces from the legal moves
                        #                     selected_piece.no_jump(board)
                        #                     board.actual_state(screen)  # Redraw the board to clear previous highlights
                        #                     gui.display_selected_piece(screen, selected_piece)  # Highlight selected piece 
                        #                     gui.display_legal_moves(screen, selected_piece.legal) # Highlight legal moves
                        #                     pygame.display.flip()
        
                        #                 else:
                        #                     #selected_piece.check_catch(board)
                        #                     board.actual_state(screen)  # Redraw the board to clear previous highlights
                        #                     gui.display_selected_piece(screen, selected_piece)  # Highlight selected piece 
                        #                     gui.display_legal_moves(screen, selected_piece.legal) # Highlight legal moves
                        #                     pygame.display.flip()
        
                        #             elif selected_piece:  # If a piece is selected and a square is clicked
                                        
                        #                 if not selected_piece.king:
                        #                     selected_piece.check_catch(board)
                        #                 else:
                        #                     selected_piece.check_catch_king(board)
        
                        #                 if not selected_piece.legal:
                        #                     selected_piece.legal_positions() # If there is no piece to catch, the legal moves list will be empty so we compute the moves normally
                        #                     selected_piece.check_position(board) # Remove the occupied spaces from the legal moves
                        #                     selected_piece.no_jump(board) # If tt is king, it can't jump over
                                            
                                                
                        #                 if (row, col) in selected_piece.legal: # If the selected square is a legal move for the piece
        
                        #                     board.chessboard[selected_piece.row][selected_piece.col] = None ## MATRIX
                                            
                        #                     selected_piece.move(row, col, board) # move
                        #                     board.chessboard[selected_piece.row][selected_piece.col] = selected_piece ## MATRIX
                        #                     human_playing = False
                                        
                        #                 board.actual_state(screen)
                        #                 gui.display_turn(screen, "player 1" if turn == WHITE else "player 2")
                        #                 pygame.display.flip()
                    

                    if player.type != 'Human' and turn == player.team:
                    #else:
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
                    efeito_w = pygame.mixer.Sound("sounds\winner.mp3")

                    if winner:
                        game_over = True
                        #efeito_w.play()
                        font = pygame.font.SysFont("Impact", 45)
                        if winner == 'Tie':
                            text = font.render("It is a Tie!", True, (255, 255, 153))
                        elif winner and winner != 'Tie':
                            text = font.render(f"The Winner is {winner}!", True, (255, 255, 153))
                        screen.blit(text, (100, height // 2))
                        pygame.display.flip()
                        break
               #     for event in pygame.event.get():
                #        if event.type == pygame.QUIT:
                 #           running = False

if __name__ == "__main__":
    main()