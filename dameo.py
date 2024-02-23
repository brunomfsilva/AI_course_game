import pygame
from board import Board
from piece import Piece
from dameo_gui import GUI
from vars import *


def main():
    """Initiate game"""
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('DAMEO')
    running = True

    gui = GUI()
    gui.main_menu(screen) #Start with the main menu

    screen.fill((0,0,0))  
    board = Board()
    

    #all_pieces_white, all_pieces_black = board.initialize_pieces()
    board.initialize_pieces() # Did it this way so the list of pieces called are always connected to the board object itself

    #put pieces on the board
    board.draw_initial_state(screen, board.all_pieces_white, board.all_pieces_black)
    pygame.display.flip()

    selected_piece = None
    turn = WHITE
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
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
                        selected_piece.drop_out_range()
                    else:
                        selected_piece.check_catch_king(board)

                    if selected_piece.legal == []:
                        selected_piece.legal_positions() # If there is no piece to catch, the legal moves list will be empty so we compute the moves normally
                        selected_piece.check_position(board) # Remove the occupied spaces from the legal moves
                        selected_piece.no_jump(board) # If tt is king, it can't jump over
                        
                            
                    if (row, col) in selected_piece.legal: # If the selected square is a legal move for the piece

                        previous_position = (selected_piece.row, selected_piece.col) # Saving the original position of the piece that is going to move
                        board.chessboard[selected_piece.row][selected_piece.col] = None ## MATRIX
                        
                        selected_piece.move(row, col) # move
                        board.chessboard[selected_piece.row][selected_piece.col] = selected_piece ## MATRIX
                        
                        if abs(selected_piece.row - previous_position[0]) > 1 or abs(selected_piece.col - previous_position[1]) > 1:
                            board.drop_piece((row+previous_position[0])/2, (col+previous_position[1])/2) # Drops the piece in the middle of the original and new positions
                            board.chessboard[int((row+previous_position[0])/2)][int((col+previous_position[1])/2)] = None # Also eliminating from the matrix (martelada no int)

                        selected_piece = None #turn off the selected piece
                        if turn == WHITE:
                            turn = BLACK  
                        else:
                            turn = WHITE
                    
                    board.actual_state(screen)
                    gui.display_turn(screen, "white" if turn == WHITE else "black")
                    pygame.display.flip()
            

    pygame.quit()

if __name__ == "__main__":
    main()


