import random
from vars import *
from board import Board
import utils
import math
from copy import deepcopy


class Minimax:
    
    def __init__(self, depth):
        self.depth = depth

    
    def minimax(self, board, depth, maximizing_player, alpha, beta, turn):
        if depth == 0 or board.check_winner():
            # Evaluate the current state of the board

            return self.evaluate(board, turn)
        
        turn = WHITE if turn == BLACK else BLACK

        legal_pieces, legal_moves = board.find_available_moves(turn)
        # print(legal_pieces)
        # print(legal_moves)
        # print('-----------------------------------------------------------')

        if maximizing_player:
            max_eval = float('-inf')
            for i, piece in enumerate(legal_pieces):
                for move in legal_moves[i]:
                    # Make the move
                    previous_row = piece.row
                    previous_col = piece.col
                    board.chessboard[piece.row][piece.col] = None
                    piece.move(move[0], move[1], board)
                    board.chessboard[piece.row][piece.col] = piece

                    #if piece.has_caught:
                        #maximizing remains True
                    #else:
                        #maximizing swithces to minimizing
                    eval = self.minimax(deepcopy(board), depth - 1, False, alpha, beta, turn)
                    
                    # Undo the move
                    board.chessboard[piece.row][piece.col] = None
                    piece.move(previous_row, previous_col, board)
                    board.chessboard[piece.row][piece.col] = piece
                    
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    
                    if beta <= alpha:
                        break  # Pruning
                    
            return max_eval
        else:
            min_eval = float('inf')
            for i, piece in enumerate(legal_pieces):
                for move in legal_moves[i]:
                    # Make the move
                    previous_row = piece.row
                    previous_col = piece.col
                    board.chessboard[piece.row][piece.col] = None
                    piece.move(move[0], move[1], board)
                    board.chessboard[piece.row][piece.col] = piece

                    #if piece.has_caught:
                        #maximizing remains False
                    #else:
                        #minimizing swithces to maximizing
                    eval = self.minimax(board, depth - 1, True, alpha, beta, turn)
                    
                    # Undo the move
                    board.chessboard[piece.row][piece.col] = None
                    piece.move(previous_row, previous_col, board)
                    board.chessboard[piece.row][piece.col] = piece
                    
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    
                    if beta <= alpha:
                        break  # Pruning
                    
            return min_eval
        

    def execute_minimax(self, board, depth, turn):
        legal_pieces, legal_moves = board.find_available_moves(turn)
        best_eval = float('-inf')
        best_move = None
        best_piece = None

        board_copy = deepcopy(board)
        legal_pieces_copy, legal_moves_copy = board_copy.find_available_moves(turn)

        for i, piece in enumerate(legal_pieces_copy):

            for move in legal_moves_copy[i]:
                # Make the move
                previous_row = piece.row
                previous_col = piece.col
                board_copy.chessboard[piece.row][piece.col] = None
                piece.move(move[0], move[1], board_copy)

                board_copy.chessboard[piece.row][piece.col] = piece
                
                eval = self.minimax(deepcopy(board_copy), depth - 1, True, float('-inf'), float('inf'), turn)

                # Undo the move
                board_copy.chessboard[piece.row][piece.col] = None
                piece.move(previous_row, previous_col, board_copy)
                board_copy.chessboard[piece.row][piece.col] = piece
                
                if eval > best_eval:
                    best_eval = eval
                    best_move = move
                    best_piece = legal_pieces[i]

        return (best_piece.row, best_piece.col), best_move

    def evaluate(self, board, turn):
        score = 0

        # Piece Count
        white_pieces = len(board.all_pieces_white)
        black_pieces = len(board.all_pieces_black)
        score += white_pieces - black_pieces if turn == WHITE else black_pieces - white_pieces

        # King Count
        white_kings = sum(piece.king for piece in board.all_pieces_white)
        black_kings = sum(piece.king for piece in board.all_pieces_black)
        score += (white_kings - black_kings) * 2 if turn == WHITE else (black_kings - white_kings) * 2

        # Board Control
        for piece in board.all_pieces_white:
            if turn == WHITE:
                #score += piece.row  # Favor higher rows for white pieces
                score += (board.size - 1 - piece.row)
            else:
                score -= (board.size - 1 - piece.row)  # Favor lower rows for black pieces

        for piece in board.all_pieces_black:
            if turn == BLACK:
                #score += (board.size - 1 - piece.row)  # Favor higher rows for black pieces
                score += piece.row
            else:
                score -= piece.row  # Favor lower rows for white pieces

        return score
    


