import pygame
import utils
from board import Board
from piece import Piece


##TRY TO PUT THIS ON A CLASS, I TRY BUT GIVES AN ERROR;;;    WHEN CALLING FROM UTILS OR BOARD GIVES AN ERROR
def initialize_pieces():
    WHITE = (255, 255, 255) # Find a way to only have this once in the whole code
    BLACK = (0, 0, 0)

    # Lists to hold the pieces for each player
    all_pieces_white = []
    all_pieces_black = []

    # Initial pieces for WHITE
    for row in [5, 6, 7]:
        for col in range(8):
            if (row == 6 and col in [0, 7]) or (row == 5 and col in [0, 1, 6, 7]):
                continue
            else:
                piece = Piece(row, col, WHITE)
                all_pieces_white.append(piece)

    # Initial pieces for BLACK
    for row in range(3):
        for col in range(8):
            if (row == 1 and col in [0, 7]) or (row == 2 and col in [0, 1, 6, 7]):
                continue
            else:
                piece = Piece(row, col, BLACK)
                all_pieces_black.append(piece)

    return all_pieces_white, all_pieces_black


def main():
    """Initiate game"""

    GREY1 = (200, 200, 200)  #white squares on the board
    GREY2 = (50, 50, 50) #black squares on the board 


    pygame.init()
    square_size = 50
    width = 8 * square_size
    height = 8 * square_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('DAMEO')
    running = True

    utils.main_menu(screen) #Start with the main menu

    screen.fill((0,0,0))  
    utils.draw_chessboard(screen, square_size, GREY1, GREY2) #draw the chessboard
    pygame.display.flip()

    all_pieces_white, all_pieces_black = initialize_pieces() #WHEN CALLING FROM UTILS OR BOARD GIVES AN ERROR

    #put pieces on the board
    for i in range(18):
        utils.draw_piece(screen, all_pieces_black[i].row, all_pieces_black[i].col, square_size, all_pieces_black[i])
        utils.draw_piece(screen, all_pieces_white[i].row, all_pieces_white[i].col, square_size, all_pieces_white[i])
    pygame.display.flip()

    selected_piece = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                x, y = pygame.mouse.get_pos()
                row = y // square_size
                col = x // square_size
                piece = utils.find_piece(row, col, all_pieces_black, all_pieces_white)
                if piece:
                    selected_piece = piece
                elif selected_piece:  # If a piece is selected and a square is clicked
                    selected_piece.move(row, col)
                    selected_piece = None #turn off the selected piece
                    
                    """this code below maybe should be a function inside board, once is called too many times"""
                    screen.fill((0,0,0)) 
                    utils.draw_chessboard(screen, square_size, GREY1, GREY2) #draw chessboard again

                    for i in range(18): #Put the pieces again
                        utils.draw_piece(screen, all_pieces_black[i].row, all_pieces_black[i].col, square_size, all_pieces_black[i])
                        utils.draw_piece(screen, all_pieces_white[i].row, all_pieces_white[i].col, square_size, all_pieces_white[i])
                    pygame.display.flip()
            

    pygame.quit()

if __name__ == "__main__":
    main()


