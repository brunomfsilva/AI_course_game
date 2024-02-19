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
                if piece and piece.color == turn:
                    selected_piece = piece
                elif selected_piece:  # If a piece is selected and a square is clicked

                    selected_piece.check_catch(board) # Check if there is any piece to catch
                    if selected_piece.legal == []:
                        selected_piece.legal_positions() # If there is no piece to catch, the legal moves list will be empty so we compute the moves normally
                        selected_piece.check_position(board) # Remove the occupied spaces from the legal moves 
                            
                    if (row, col) in selected_piece.legal: # If the selected square is a legal move for the piece
                        previous_position = (selected_piece.row, selected_piece.col) # Saving the original position of the piece that is going to move
                        selected_piece.move(row, col)
                        board.drop_piece((row+previous_position[0])/2, (col+previous_position[1])/2)
                        selected_piece = None #turn off the selected piece
                        if turn == WHITE:
                            turn = BLACK  
                        else:
                            turn = WHITE
                    
                    """this code below maybe should be a function inside board, once is called too many times"""
                    screen.fill((0,0,0)) 
                    board.draw_chessboard(screen) #draw chessboard again
    
                    for i in range(len(board.all_pieces_black)): #Put the pieces again
                        board.draw_piece(screen, board.all_pieces_black[i].row, board.all_pieces_black[i].col, board.all_pieces_black[i])
                    for i in range(len(board.all_pieces_white)):
                        board.draw_piece(screen, board.all_pieces_white[i].row, board.all_pieces_white[i].col, board.all_pieces_white[i])
                    
                    gui.display_turn(screen, "white" if turn == WHITE else "black")
                    pygame.display.flip()
            

    pygame.quit()

if __name__ == "__main__":
    main()


