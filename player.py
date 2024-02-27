import random
from vars import *
from board import Board
import utils

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
    

    ####### MINIMAX #######

    def minimax(self, board, depth, maximizing_player, player2):
        if depth == 0 or self.game_over(board):
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves(board):
                new_board = self.make_move(board, move)
                eval = self.minimax(new_board, depth - 1, False, player2)
                max_eval = max(max_eval, eval)
            return max_eval

        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(board):
                new_board = self.make_move(board, move)
                eval = self.minimax(new_board, depth - 1, True, player2)
                min_eval = min(min_eval, eval)
            return min_eval

    def get_best_move(self, board, player2):
        best_move = None
        max_eval = float('-inf')
        for move in self.get_possible_moves(board):
            new_board = self.make_move(board, move)
            eval = self.minimax(new_board, 3, False, player2)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move

    def game_over(self, board):
        if not board.all_pieces_white or not board.all_pieces_black:
            return True
        else:
            return False

    def evaluate_board(self, board):
        ai_pieces = len(board.all_pieces_black)
        human_pieces = len(board.all_pieces_white)

        # Assign values to pieces based on their type (you might need to adjust these)
        ai_piece_value = 1
        human_piece_value = -1

        # Calculate the total value based on the material count
        board_value = (ai_pieces * ai_piece_value) + (human_pieces * human_piece_value)

        return board_value

    def get_possible_moves(self, board):

        if self.team == WHITE:
                selected_piece = board.all_pieces_white[1] #random.choice(board.all_pieces_white)
        else:
                selected_piece = board.all_pieces_black[1] #random.choice(board.all_pieces_black)

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

        return selected_piece.legal

    def make_move(self, board, move):

        if self.team == WHITE:
                selected_piece = board.all_pieces_white[1]
        else:
                selected_piece = board.all_pieces_black[1]

        board.chessboard[selected_piece.row][selected_piece.col] = None
        selected_piece.move(move[0], move[1], board)
        board.chessboard[selected_piece.row][selected_piece.col] = selected_piece
        new_board = board

        return new_board
