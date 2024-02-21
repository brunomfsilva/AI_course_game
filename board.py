import pygame
import sys
from piece import Piece
from vars import *

class Board:
    def __init__(self):
        self.size = size
        self.square_size = square_size
        self.color1 =  GREY1
        self.color2 = GREY2
        self.chessboard = [[None for i in range(self.size)] for j in range(self.size)]
        self.all_pieces_white = [] # Lists to hold the pieces for each player
        self.all_pieces_black = []

    def initialize_pieces(self):

        # MAYBE WE CAN TAKE THIS OFF
        self.all_pieces_white = []
        self.all_pieces_black = []
        ############################

        # Initial pieces for WHITE
        for row in [5, 6, 7]:
            for col in range(8):
                if (row == 6 and col in [0, 7]) or (row == 5 and col in [0, 1, 6, 7]):
                    continue
                else:
                    piece = Piece(row, col, WHITE)  # Assuming Piece class is defined elsewhere
                    self.all_pieces_white.append(piece)
                    ############ MATRIX #############
                    self.chessboard[row][col] = piece
                    #################################

        # Initial pieces for BLACK
        for row in range(3):
            for col in range(8):
                if (row == 1 and col in [0, 7]) or (row == 2 and col in [0, 1, 6, 7]):
                    continue
                else:
                    piece = Piece(row, col, BLACK)  # Assuming Piece class is defined elsewhere
                    self.all_pieces_black.append(piece)
                    ############ MATRIX #############
                    self.chessboard[row][col] = piece
                    #################################
                    
        return self.all_pieces_white, self.all_pieces_black
    
    def draw_initial_state(self, screen, all_pieces_white, all_pieces_black):
        self.draw_chessboard(screen)
        for piece in all_pieces_black + all_pieces_white:
            self.draw_piece(screen, piece.row, piece.col, piece)

    def actual_state(self, screen):
        '''actual state'''
        screen.fill((0, 0, 0))
        self.draw_chessboard(screen)

        for i in range(len(self.all_pieces_black)): #Put the pieces again
            self.draw_piece(screen, self.all_pieces_black[i].row, self.all_pieces_black[i].col, self.all_pieces_black[i])
        for i in range(len(self.all_pieces_white)):
            self.draw_piece(screen, self.all_pieces_white[i].row, self.all_pieces_white[i].col, self.all_pieces_white[i])

        pygame.display.flip()

    def draw_king(self, screen, row, col, piece):
        "new form when become king"
        radius = self.square_size // 2 - 5
        pygame.draw.circle(screen, piece.color, (col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2), radius)
        
        if piece.king:  # If the piece is a king, draw a small yellow circle in the center
            pygame.draw.circle(screen, (255, 0, 0), (col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2), 5)

    def draw_piece(self, screen, row, col, piece):
        '''draw piece'''
        if piece.king: #if piece become king
            self.draw_king(screen, row, col, piece)
        else: #if piece is normal
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
    
    # Function to get the taken positions
    def occupied(self):
        taken_white = []
        taken_black = []
        for i in range(len(self.all_pieces_white)):
            taken_white += [(self.all_pieces_white[i].row, self.all_pieces_white[i].col)]
        for i in range(len(self.all_pieces_black)):
            taken_black += [(self.all_pieces_black[i].row, self.all_pieces_black[i].col)]
        return taken_white, taken_black
    
    # Function to delete a piece from the board
    def drop_piece(self, row, col):
        for i in range(len(self.all_pieces_black)):
            if row == self.all_pieces_black[i].row and col == self.all_pieces_black[i].col:
                self.all_pieces_black.pop(i)
                break
        
        for i in range(len(self.all_pieces_white)):
            if row == self.all_pieces_white[i].row and col == self.all_pieces_white[i].col:
                self.all_pieces_white.pop(i)
                break
        # WORKING BUT DOESN'T MAKE ANY SENSE TO HAVE TWO LOOPS HERE. THERE SHOULD BE A WAY TO OPTIMIZE
    
    '''
    # To check if a specific spot is empty
    def is_empty(self, row, col):
        whites, blacks = self.occupied()
        return (self.row, self.col) not in whites + blacks
    '''