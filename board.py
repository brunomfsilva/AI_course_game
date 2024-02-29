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
        self.last_moved_piece = None


    def start_game(self, gui, screen):
        gui.main_menu(screen)
        screen.fill((0,0,0))  
        self.initialize_pieces()
        self.draw_initial_state(screen, self.all_pieces_white, self.all_pieces_black)
        pygame.display.flip()

    def initialize_pieces(self):
        # MAYBE WE CAN TAKE THIS OFF
        self.all_pieces_white = []
        self.all_pieces_black = []
        ############################

        # Initial pieces for WHITE
        if self.size>=6:
            # Initial pieces for WHITE
            for row in range (self.size-3, self.size):
                for col in range(self.size):
                    if (row == self.size-2 and col in [0, self.size-1]) or (row == self.size-3 and col in [0, 1, self.size-1, self.size-2]):
                        continue     
                    else:
                        piece = Piece(row, col, WHITE)  # Assuming Piece class is defined elsewhere
                        self.all_pieces_white.append(piece)
                        ############ MATRIX #############
                        self.chessboard[row][col] = piece
                        #################################
        
            # Initial pieces por BLACK        
            for row in range (3):
                for col in range(self.size):
                    if (row == 1 and col in [0, self.size-1]) or (row == 2 and col in [0, 1, self.size-1, self.size-2]): 
                        continue     
                    else:
                        piece = Piece(row, col, BLACK)  # Assuming Piece class is defined elsewhere
                        self.all_pieces_black.append(piece)
                        ############ MATRIX #############
                        self.chessboard[row][col] = piece
                        #################################

        if self.size== 4 or self.size== 5:
            # Initial pieces for WHITE
            for row in range (self.size-2, self.size):
                for col in range(self.size):
                    if (row == self.size-2 and col in [0, self.size-1]):
                        continue     
                    else:
                        piece = Piece(row, col, WHITE)  # Assuming Piece class is defined elsewhere
                        self.all_pieces_white.append(piece)
                        ############ MATRIX #############
                        self.chessboard[row][col] = piece
                        #################################
        
            # Initial pieces por BLACK        
            for row in range (2):
                for col in range(self.size):
                    if (row == 1 and col in [0, self.size-1]): 
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
        #escrever "KING"
        # radius = self.square_size // 2 - 5
        # pygame.draw.circle(screen, piece.color, (col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2), radius)
        
        # if piece.king:  # If the piece is a king, draw a small yellow circle in the center
        #     pygame.draw.circle(screen, (0, 85, 0), (col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2), 5)
        if piece.color == WHITE:
            piece_image = pygame.image.load("icons\king_white.png")
        else:
            piece_image = pygame.image.load("icons\king_black.png")

        # pos
        x_pos = col * self.square_size + 12
        y_pos = row * self.square_size + 12

        screen.blit(piece_image, (x_pos, y_pos))

    def draw_piece(self, screen, row, col, piece):
        '''draw piece'''
        if piece.king: #if piece become king
            self.draw_king(screen, row, col, piece)
        else: #if piece is normal
            # radius = self.square_size // 2 - 5
            # pygame.draw.circle(screen, piece.color, (col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2), radius)

            if piece.color == WHITE:
                piece_image = pygame.image.load("icons\piece_white.png")
            else:
                piece_image = pygame.image.load("icons\piece_black.png")

            # pos
            x_pos = col * self.square_size + 12
            y_pos = row * self.square_size + 12

            screen.blit(piece_image, (x_pos, y_pos))

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
            
    def check_piece_to_capture(self, turn):
        can_catch=[]
        all_pieces = self.all_pieces_black if turn == BLACK else self.all_pieces_white
        for piece in all_pieces:
            if not piece.king:
                piece.check_catch(self)  # Updates legal moves considering captures
            elif piece.king:
                piece.check_catch_king(self) # Updates legal moves considering captures for kings

            if piece.legal:
                can_catch.append(piece)
        return can_catch
    
    def check_if_capture(self, gui, screen, can_catch, piece, turn, selected_piece):
        catch_position =[]
        for i in can_catch:
            catch_position.append((i.row, i.col))
        
        pos = ()
        piece_color=None
        if piece is not None:
            pos = (piece.row, piece.col)
            piece_color = piece.color
        
        message_displayed = True
        
        #you can not leave while loop while you not pick the right piece
        while can_catch and pos not in catch_position and piece_color == turn and pos != ():

            # Display the message
            if message_displayed:    
                self.actual_state(screen)
                gui.display_selected_piece(screen, selected_piece)
                gui.display_message(screen, '          Must capture piece!')
                pygame.display.flip()
                message_displayed = False
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row = y // square_size
                    col = x // square_size
        
                    piece = self.find_piece(row, col, self.all_pieces_black, self.all_pieces_white)
                    if piece is not None:
                        pos = (piece.row, piece.col)
                        colour = piece.color
        
        return piece
    

    def check_winner(board):
        '''check the winner'''
        if len(board.all_pieces_black) == 0: #or black cannot move
            return "Player 1"
        elif len(board.all_pieces_white) == 0:  #or white cannot move
            return "Player 2"
        
    def find_available_moves(self, turn):

        legal_moves = []
        # Check if any piece has to catch
        legal_pieces = self.check_piece_to_capture(turn)

        # It there are legal_pieces, it means there are pieces that can catch
        if legal_pieces:

            # Getting the legal moves for each piece, whether they are kings or not
            for piece in legal_pieces:
                if piece.king:
                    piece.check_catch_king(self)
                    legal_moves.append(piece.legal) # Confirm if should be .append([piece.legal]) instead
                else:
                    piece.check_catch(self)
                    legal_moves.append(piece.legal)

        # If there are no legal_pieces, it means there are no pieces that can catch. Proceed with normal moves
        else:

            # According to the turn, the legal_pieces are all pieces from that team
            if turn == WHITE:
                legal_pieces = self.all_pieces_white
            else:
                legal_pieces = self.all_pieces_black

            # Getting the legal moves for each piece
            for piece in legal_pieces:
                piece.legal_positions()
                piece.check_position(self)
                piece.no_jump(self)
                legal_moves.append(piece.legal) # Confirm if should be .append([piece.legal]) instead

            # Getting rid of the pieces with no moves available - this is only applicable if there are no pieces to capture
            index = []
            for i in range(len(legal_moves)):
                if legal_moves[i] == []:
                    index.append(i)

            legal_pieces = [legal_pieces[i] for i in range(len(legal_pieces)) if i not in index]
            legal_moves = [legal_moves[i] for i in range(len(legal_moves)) if i not in index]
            #print(legal_pieces)
            #print(legal_moves)
        return legal_pieces, legal_moves