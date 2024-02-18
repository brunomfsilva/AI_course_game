import pygame
import sys
from piece import Piece

class Board:
    def __init__(self):
        self.size = 8
        self.square_size = 50
        self.color1 =  (180, 180, 180)
        self.color2 = (50, 50, 50)
        self.chessboard = [[None for i in range(self.size)] for j in range(self.size)]

    def initialize_pieces(self):
        WHITE = (255, 255, 255)  # Find a way to only have this once in the whole code
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
                    piece = Piece(row, col, WHITE)  # Assuming Piece class is defined elsewhere
                    all_pieces_white.append(piece)

        # Initial pieces for BLACK
        for row in range(3):
            for col in range(8):
                if (row == 1 and col in [0, 7]) or (row == 2 and col in [0, 1, 6, 7]):
                    continue
                else:
                    piece = Piece(row, col, BLACK)  # Assuming Piece class is defined elsewhere
                    all_pieces_black.append(piece)

        return all_pieces_white, all_pieces_black
    
    def draw_initial_state(self, screen, all_pieces_white, all_pieces_black):
        self.draw_chessboard(screen)
        for piece in all_pieces_black + all_pieces_white:
            self.draw_piece(screen, piece.row, piece.col, piece)

    def draw_piece(self, screen, row, col, piece):
        radius = self.square_size // 2 - 5
        pygame.draw.circle(screen, piece.color, (col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2), radius)

    def draw_chessboard(self, screen):
        for row in range(self.size):
            for col in range(self.size):
                color = self.color1 if (row + col) % 2 == 0 else self.color2
                pygame.draw.rect(screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def find_piece(self, row, col, all_pieces_black, all_pieces_white):
        for piece in all_pieces_black + all_pieces_white:
            if piece.row == row and piece.col == col:
                return piece
        return None