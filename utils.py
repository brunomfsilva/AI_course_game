import pygame
from piece import Piece


def draw_chessboard(screen, square_size, color1, color2):
    for row in range(8):
        for col in range(8):
            color = color1 if (row + col) % 2 == 0 else color2
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

def draw_piece(screen, row, col, square_size, piece):
    radius = square_size // 2 - 5
    pygame.draw.circle(screen, piece.color, (col * square_size + square_size // 2, row * square_size + square_size // 2), radius)

def find_piece(row, col, all_pieces_black, all_pieces_white):
        for piece in all_pieces_black + all_pieces_white:
            if piece.row == row and piece.col == col:
                return piece
        return None

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


def main_menu(screen):
    """Main Menu"""
    font = pygame.font.Font(None, 36)

    start_text = font.render("Click to Start", True, (255, 255, 255)) #select text and color
    text_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)) #Centre the text

    screen.fill((0, 0, 0))
    screen.blit(start_text, text_rect)
    pygame.display.flip() #display

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #close if click on 'x' symbol
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Start if click on ecran
                waiting = False