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
    

    all_pieces_white, all_pieces_black = board.initialize_pieces()
    #put pieces on the board
    board.draw_initial_state(screen, all_pieces_white, all_pieces_black)
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
                piece = board.find_piece(row, col, all_pieces_black, all_pieces_white)
                if piece and piece.color == turn:
                    selected_piece = piece
                elif selected_piece:  # If a piece is selected and a square is clicked
                    selected_piece.legal_positions()
                    board.occupied()
                    
                    # This will be moved to piece.py
                    arg_taken = []
                    for i in range(len(selected_piece.legal)):
                        if selected_piece.legal[i] in board.occupied():
                            arg_taken.append(i)
                    selected_piece.legal = [selected_piece.legal[i] for i in range(len(selected_piece.legal)) if i not in arg_taken]
                    ################################
                            
                    if (row, col) in selected_piece.legal: # If the selected square is a legal move for the piece
                        selected_piece.move(row, col)
                        selected_piece = None #turn off the selected piece
                        if turn == WHITE:
                            turn = BLACK  
                        else:
                            turn = WHITE
                    
                    """this code below maybe should be a function inside board, once is called too many times"""
                    screen.fill((0,0,0)) 
                    board.draw_chessboard(screen) #draw chessboard again
    
                    for i in range(18): #Put the pieces again
                        board.draw_piece(screen, all_pieces_black[i].row, all_pieces_black[i].col, all_pieces_black[i])
                        board.draw_piece(screen, all_pieces_white[i].row, all_pieces_white[i].col, all_pieces_white[i])
                    
                    gui.display_turn(screen, "white" if turn == WHITE else "black")
                    pygame.display.flip()
            

    pygame.quit()

if __name__ == "__main__":
    main()


