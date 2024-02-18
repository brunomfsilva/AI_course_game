import pygame
import sys

class Board:
    def __init__(self, size):
        self.size = size
        self.chessboard = [[None for i in range(self.size)] for j in range(self.size)]


    def draw_chessboard(screen, square_size, color1, color2):
        for row in range(8):
            for col in range(8):
                color = color1 if (row + col) % 2 == 0 else color2
                pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

    def draw_piece(self, screen, row, col, square_size, piece):
        radius = square_size // 2 - 5
        pygame.draw.circle(screen, piece.color, (col * square_size + square_size // 2, row * square_size + square_size // 2), radius)

class Piece:
    def __init__(self, row, col, color, king = False):
        self.row = row
        self.col = col
        self.color = color
        self.king = king
    
    def move(self, row, col):
        self.row = row
        self.col = col


    def draw_piece(screen, row, col, square_size, piece):
        radius = square_size // 2 - 5
        pygame.draw.circle(screen, piece.color, (col * square_size + square_size // 2, row * square_size + square_size // 2), radius)


    def find_piece(row, col, all_pieces_black, all_pieces_white):
        for piece in all_pieces_black + all_pieces_white:
            if piece.row == row and piece.col == col:
                return piece
        return None

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Lists to hold the pieces for each player
def initialize_pieces():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

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
    GREY1 = (200, 200, 200)  # white squares on the board
    GREY2 = (50, 50, 50)  # black squares on the board 

    pygame.init()
    square_size = 50
    width = 8 * square_size
    height = 8 * square_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('DAMEO')

    running = True
    screen.fill((0,0,0))
    Board.draw_chessboard(screen, square_size, GREY1, GREY2)
    pygame.display.flip()

    all_pieces_white, all_pieces_black = initialize_pieces()

    for i in range(18):
        Piece.draw_piece(screen, all_pieces_black[i].row, all_pieces_black[i].col, square_size, all_pieces_black[i])
        Piece.draw_piece(screen, all_pieces_white[i].row, all_pieces_white[i].col, square_size, all_pieces_white[i])
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
                piece = Piece.find_piece(row, col, all_pieces_black, all_pieces_white)
                if piece:
                    selected_piece = piece
                elif selected_piece:  # If a piece is selected and a square is clicked
                    selected_piece.move(row, col)
                    selected_piece = None
                    screen.fill((0,0,0))
                    Board.draw_chessboard(screen, square_size, GREY1, GREY2)
                    for piece in all_pieces_black + all_pieces_white:
                        Piece.draw_piece(screen, piece.row, piece.col, square_size, piece)
                    pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()