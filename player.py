import random
from vars import *
from board import Board

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
