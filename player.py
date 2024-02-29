import random
from vars import *
from board import Board
import utils
import math
from copy import deepcopy

class Player:

    def __init__(self, type, level, team):
        self.type = type
        self.level = level
        self.team = team

    def ai_random_move(self, board, turn):
        
        while True:
            # Check if there is any piece that can capture and only those can be selected
            legal_pieces = board.check_piece_to_capture(turn)
            if not legal_pieces:
                legal_pieces = board.all_pieces_black if turn == BLACK else board.all_pieces_white

            # Select one of those pieces
            selected_piece = random.choice(legal_pieces)

            # Check legal moves for that piece
            # If it is king and can catch
            if selected_piece.king:
                selected_piece.check_catch_king(board)
            
            # If it isn't king and can catch
            if not selected_piece.king:
                selected_piece.check_catch(board)

            # If it can't catch
            if not selected_piece.legal:
                selected_piece.legal_positions()
                selected_piece.check_position(board)
                selected_piece.no_jump(board)

            legal_moves = selected_piece.legal
            #print(legal_moves)

            # To avoid chosing a piece that's stuck and with no legal moves
            # CAREFUL BECAUSE THERE CAN BE JUST ONE OR TWO PIECES WITH NO LEGAL MOVES TO DO -> WINNER FUNCTION?
            if not legal_moves and legal_pieces:
                continue
            else:
                break

        # Chose one of the legal_moves
        chosen_move = random.choice(legal_moves)
        board.chessboard[selected_piece.row][selected_piece.col] = None
        selected_piece.move(chosen_move[0], chosen_move[1], board)
        board.chessboard[selected_piece.row][selected_piece.col] = selected_piece
        return selected_piece

#########################################
# MINIMAX CHATGPT
def minimax(board, depth, maximizing_player, alpha, beta, turn):
    if depth == 0 or board.check_winner():
        # Evaluate the current state of the board
        return evaluate(board, turn)

    # if not board.last_moved_piece.king:
    #     board.last_moved_piece.check_catch(board)
    # else:
    #     board.last_moved_piece.check_catch_king(board)

    # if board.last_moved_piece.legal and board.last_moved_piece.has_caught:
    #     if turn == WHITE:
    #         turn = WHITE
    #     else:
    #         turn = BLACK
    # else:
    #     if turn == WHITE:
    #         turn = BLACK
    #     else:
    #         turn = WHITE

    turn = WHITE if turn == BLACK else BLACK # MOVES SEGUIDOS NÃO ESTÃO INCLUIDOS DE CERTEZA

    legal_pieces, legal_moves = board.find_available_moves(turn)
    # print(legal_pieces)
    # print(legal_moves)
    # print('-----------------------------------------------------------')

    max_eval = float('-inf')
    min_eval = float('inf')

    for i, piece in enumerate(legal_pieces):
        for move in legal_moves[i]:
            # Make the move
            previous_row = piece.row
            previous_col = piece.col
            board.chessboard[piece.row][piece.col] = None
            piece.move(move[0], move[1], board)
            board.chessboard[piece.row][piece.col] = piece

            eval = minimax(deepcopy(board), depth - 1, not maximizing_player, alpha, beta, turn)

            # Undo the move
            board.chessboard[piece.row][piece.col] = None
            piece.move(previous_row, previous_col, board)
            board.chessboard[piece.row][piece.col] = piece

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            if beta <= alpha:
                break  # Pruning

    return max_eval if maximizing_player else min_eval
    
# def minimax(board, depth, maximizing_player, alpha, beta, turn):
#     if depth == 0 or board.check_winner():
#         # Evaluate the current state of the board
#         return evaluate(board, turn)
    
#     legal_pieces, legal_moves = board.find_available_moves(turn)
#     # print(legal_pieces)
#     # print(legal_moves)
#     # print('-----------------------------------------------------------')
    
#     if maximizing_player:
#         max_eval = float('-inf')
#         for i, piece in enumerate(legal_pieces):
#             for move in legal_moves[i]:
#                 # Make the move
#                 previous_row = piece.row
#                 previous_col = piece.col
#                 board.chessboard[piece.row][piece.col] = None
#                 piece.move(move[0], move[1], board)
#                 board.chessboard[piece.row][piece.col] = piece

#                 eval = minimax(deepcopy(board), depth - 1, False, alpha, beta, turn)
                
#                 # Undo the move
#                 board.chessboard[piece.row][piece.col] = None
#                 piece.move(previous_row, previous_col, board)
#                 board.chessboard[piece.row][piece.col] = piece
                
#                 max_eval = max(max_eval, eval)
#                 alpha = max(alpha, eval)
                
#                 if beta <= alpha:
#                     break  # Pruning
                
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for i, piece in enumerate(legal_pieces):
#             for move in legal_moves[i]:
#                 # Make the move
#                 previous_row = piece.row
#                 previous_col = piece.col
#                 board.chessboard[piece.row][piece.col] = None
#                 piece.move(move[0], move[1], board)
#                 board.chessboard[piece.row][piece.col] = piece

#                 eval = minimax(board, depth - 1, True, alpha, beta, turn)
                
#                 # Undo the move
#                 board.chessboard[piece.row][piece.col] = None
#                 piece.move(previous_row, previous_col, board)
#                 board.chessboard[piece.row][piece.col] = piece
                
#                 min_eval = min(min_eval, eval)
#                 beta = min(beta, eval)
                
#                 if beta <= alpha:
#                     break  # Pruning
                
#         return min_eval

def execute_minimax(board, depth, turn):
    legal_pieces, legal_moves = board.find_available_moves(turn)
    best_eval = float('-inf')
    best_move = None
    best_piece = None
    catching_piece = None

    for i, piece in enumerate(legal_pieces):

        

        for move in legal_moves[i]:
            # Make the move
            previous_row = piece.row
            previous_col = piece.col
            board.chessboard[piece.row][piece.col] = None
            piece.move(move[0], move[1], board)

            if piece.has_caught:
                catching_piece = piece

            board.chessboard[piece.row][piece.col] = piece
            
            eval = minimax(deepcopy(board), depth - 1, True, float('-inf'), float('inf'), turn)

            # Undo the move
            board.chessboard[piece.row][piece.col] = None
            piece.move(previous_row, previous_col, board)
            board.chessboard[piece.row][piece.col] = piece
            
            if eval > best_eval:
                best_eval = eval
                best_move = move
                best_piece = piece

    return best_piece , best_move, best_eval, catching_piece

def evaluate(board, turn):
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
            score += piece.row  # Favor higher rows for white pieces
        else:
            score -= (board.size - 1 - piece.row)  # Favor lower rows for black pieces

    for piece in board.all_pieces_black:
        if turn == BLACK:
            score += (board.size - 1 - piece.row)  # Favor higher rows for black pieces
        else:
            score -= piece.row  # Favor lower rows for white pieces

    return score