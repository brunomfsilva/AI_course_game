import pygame

def draw_chessboard(screen, square_size, color1, color2):
    for row in range(8):
        for col in range(8):
            color = color1 if (row + col) % 2 == 0 else color2
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

def draw_piece(screen, row, col, square_size, piece):
    radius = square_size // 2 - 5
    pygame.draw.circle(screen, piece.color, (col * square_size + square_size // 2, row * square_size + square_size // 2), radius)