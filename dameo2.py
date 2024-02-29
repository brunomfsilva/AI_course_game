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
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('DAMEO')
    running = True
    gui = GUI()
    board=Board()
    board.start_game(gui, screen)
    selected_piece = None
    turn = WHITE
    winner = None
    player1 = Player('Human', 'Very easy', WHITE)
    player2 = Player('AI', 'Hard', BLACK)

    game_over=False

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                if winner:
                    winner = None
                    game_over = False
                    board.start_game(gui, screen)
                    selected_piece = None
                    turn = WHITE
            
            while not game_over and running:
                for player in (player1, player2):
                    
                    if game_over:
                        break
                    
                    if player.type == 'Human' and turn == player.team:
                        human_playing = True
                        while human_playing:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
        
                                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                                    if winner:
                                        winner = None
                                        board.start_game(gui, screen)
                                        selected_piece = None
                                        turn = WHITE
                                        
        
                                    x, y = pygame.mouse.get_pos()
                                    row = y // square_size
                                    col = x // square_size
        
                                    
                                    piece = board.find_piece(row, col, board.all_pieces_black, board.all_pieces_white)
        
                                    
                                    can_catch = board.check_piece_to_capture(turn)
                                    piece = board.check_if_capture( gui, screen, can_catch, piece, turn, selected_piece) #check if piece already capture (if needed)
        
                                    if piece and piece.color == turn:
                                        selected_piece = piece
                                        
                                        if not piece.king:
                                            selected_piece.check_catch(board)
                                        elif piece.king:
                                            selected_piece.check_catch_king(board)
                                            
                                        if not selected_piece.legal:
                                            selected_piece.legal_positions() # If there is no piece to catch, the legal moves list will be empty so we compute the moves normally
                                            selected_piece.check_position(board) # Remove the occupied spaces from the legal moves
                                            selected_piece.no_jump(board)
                                            board.actual_state(screen)  # Redraw the board to clear previous highlights
                                            gui.display_selected_piece(screen, selected_piece)  # Highlight selected piece 
                                            gui.display_legal_moves(screen, selected_piece.legal) # Highlight legal moves
                                            pygame.display.flip()
        
                                        else:
                                            #selected_piece.check_catch(board)
                                            board.actual_state(screen)  # Redraw the board to clear previous highlights
                                            gui.display_selected_piece(screen, selected_piece)  # Highlight selected piece 
                                            gui.display_legal_moves(screen, selected_piece.legal) # Highlight legal moves
                                            pygame.display.flip()
        
                                    elif selected_piece:  # If a piece is selected and a square is clicked
                                        
                                        if not selected_piece.king:
                                            selected_piece.check_catch(board)
                                        else:
                                            selected_piece.check_catch_king(board)
        
                                        if not selected_piece.legal:
                                            selected_piece.legal_positions() # If there is no piece to catch, the legal moves list will be empty so we compute the moves normally
                                            selected_piece.check_position(board) # Remove the occupied spaces from the legal moves
                                            selected_piece.no_jump(board) # If tt is king, it can't jump over
                                            
                                                
                                        if (row, col) in selected_piece.legal: # If the selected square is a legal move for the piece
        
                                            board.chessboard[selected_piece.row][selected_piece.col] = None ## MATRIX
                                            
                                            selected_piece.move(row, col, board) # move
                                            board.chessboard[selected_piece.row][selected_piece.col] = selected_piece ## MATRIX
                                            human_playing = False
                                        
                                        board.actual_state(screen)
                                        gui.display_turn(screen, "player 1" if turn == WHITE else "player 2")
                                        pygame.display.flip()
                    
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
    
                        time.sleep(1)
                        board.actual_state(screen)
        
                    winner = board.check_winner()
                    if winner:
                        game_over = True
                        font = pygame.font.SysFont(None, 45)
                        text = font.render(f"The winner is {winner}!", True, (255, 255, 255))
                        screen.blit(text, (100, height // 2))
                        pygame.display.flip()
                    

if __name__ == "__main__":
    main()