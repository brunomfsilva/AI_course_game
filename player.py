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

        # Choose one of the legal_moves
        chosen_move = random.choice(legal_moves)
        board.chessboard[selected_piece.row][selected_piece.col] = None
        selected_piece.move(chosen_move[0], chosen_move[1], board)
        board.chessboard[selected_piece.row][selected_piece.col] = selected_piece
        return selected_piece

#########################################
# MINIMAX CHATGPT
# def minimax(board, depth, maximizing_player, alpha, beta, turn):
#     if depth == 0 or board.check_winner():
#         # Evaluate the current state of the board
#         return evaluate(board, turn)

#     turn = WHITE if turn == BLACK else BLACK
#     # turn = WHITE if (turn == BLACK) and board.last_moved_piece.has_caught else BLACK
#     # turn = turn if board.last_moved_piece.has_caught else (WHITE if turn == BLACK else BLACK)

#     # if not board.last_moved_piece.has_caught:
#     #     turn = WHITE if turn == BLACK else BLACK
#     #     maximizing_player = not maximizing_player

#     legal_pieces, legal_moves = board.find_available_moves(turn)

#     max_eval = float('-inf')
#     min_eval = float('inf')

#     for i, piece in enumerate(legal_pieces):
#         for move in legal_moves[i]:
#             # Make the move
#             previous_row = piece.row
#             previous_col = piece.col
#             board.chessboard[piece.row][piece.col] = None
#             piece.move(move[0], move[1], board)
#             board.chessboard[piece.row][piece.col] = piece

#             eval = minimax(deepcopy(board), depth - 1, not maximizing_player, alpha, beta, turn)

#             # Undo the move
#             board.chessboard[piece.row][piece.col] = None
#             piece.move(previous_row, previous_col, board)
#             board.chessboard[piece.row][piece.col] = piece

#             #if maximizing_player:
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             #else:
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)

#             if beta <= alpha:
#                 break  # Pruning

#     return max_eval if maximizing_player else min_eval
    
def minimax(board, depth, maximizing_player, alpha, beta, turn):
    if depth == 0 or board.check_winner():
        # Evaluate the current state of the board
        return evaluate(board, turn)
    
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
                eval = minimax(deepcopy(board), depth - 1, False, alpha, beta, turn)
                
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
                eval = minimax(board, depth - 1, True, alpha, beta, turn)
                
                # Undo the move
                board.chessboard[piece.row][piece.col] = None
                piece.move(previous_row, previous_col, board)
                board.chessboard[piece.row][piece.col] = piece
                
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                
                if beta <= alpha:
                    break  # Pruning
                
        return min_eval

def execute_minimax(board, depth, turn):
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
            
            eval = minimax(deepcopy(board_copy), depth - 1, True, float('-inf'), float('inf'), turn)

            # Undo the move
            board_copy.chessboard[piece.row][piece.col] = None
            piece.move(previous_row, previous_col, board_copy)
            board_copy.chessboard[piece.row][piece.col] = piece
            
            if eval > best_eval:
                best_eval = eval
                best_move = move
                best_piece = legal_pieces[i]

    return best_piece, best_move

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

#---------- MONTE CARLO TREE SEARCH ---------------------------------------

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0.0

def expand(node):
    new_state = deepcopy(node.state)  # Create a copy of the current board
    new_legal_pieces, new_legal_moves = new_state.find_available_moves(new_state.turn)
    if not new_legal_pieces:
        new_state.print_board()
    random_piece_index = random.choice(range(len(new_legal_pieces)))
    random_piece = new_legal_pieces[random_piece_index]
    random_move_index = random.choice(range(len(new_legal_moves[random_piece_index])))
    random_move = new_legal_moves[random_piece_index][random_move_index]

    new_state.chessboard[random_piece.row][random_piece.col] = None
    random_piece.move(random_move[0], random_move[1], new_state)
    new_state.chessboard[random_piece.row][random_piece.col] = random_piece

    if random_piece.has_caught and not random_piece.king:
        random_piece.check_catch(new_state)
        if random_piece.legal:
            new_state.turn = WHITE if new_state.turn == WHITE else BLACK
        else:
            new_state.turn = WHITE if new_state.turn == BLACK else BLACK

    elif random_piece.has_caught and random_piece.king:
        random_piece.check_catch_king(new_state)
        if random_piece.legal:
            new_state.turn = WHITE if new_state.turn == WHITE else BLACK
        else:
            new_state.turn = WHITE if new_state.turn == BLACK else BLACK

    else:
        new_state.turn = WHITE if new_state.turn == BLACK else BLACK
    
    if random_piece.legal and random_piece.has_caught:
        pass
        
    else:
        random_piece.transform_king()

    new_node = MCTSNode(new_state, parent=node)
    node.children.append(new_node)
    return new_node

def select(node):
    legal_pieces, legal_moves = node.state.find_available_moves(node.state.turn)
    n_children = 0
    for i in range(len(legal_pieces)):
        for j in range(len(legal_moves)):
            n_children += 1
    if not node.children or len(node.children) < n_children:
        return node

    selected_child = max(node.children, key=lambda child: ucb_score(child))
    return select(selected_child)

def ucb_score(node):
    exploration_weight = 1.4  # You may need to tune this parameter
    return node.reward / node.visits + exploration_weight * math.sqrt(math.log(node.parent.visits) / node.visits)

def simulate(node, initial_turn):
    #print('--------init----------')
    # node.state.print_board()
    current_state = deepcopy(node.state)
    # current_state.print_board()
    # print('--------end----------')

    winner = current_state.check_winner()
    if (winner == 'Player 1' and initial_turn == WHITE) or (winner == 'Player 2' and initial_turn == BLACK):
        return 1
    elif (winner == 'Player 1' and initial_turn == BLACK) or (winner == 'Player 2' and initial_turn == WHITE):
        return -1
    
    while True:

        winner = current_state.check_winner()
        if (winner == 'Player 1' and initial_turn == WHITE) or (winner == 'Player 2' and initial_turn == BLACK):
            return 1
        elif (winner == 'Player 1' and initial_turn == BLACK) or (winner == 'Player 2' and initial_turn == WHITE):
            return -1
        
        legal_pieces, legal_moves = current_state.find_available_moves(current_state.turn)
        # if not legal_pieces:
        #     current_state.print_board()
        random_piece_index = random.choice(range(len(legal_pieces)))
        random_piece = legal_pieces[random_piece_index]
        random_move_index = random.choice(range(len(legal_moves[random_piece_index])))
        random_move = legal_moves[random_piece_index][random_move_index]
        current_state.chessboard[random_piece.row][random_piece.col] = None
        random_piece.move(random_move[0], random_move[1], current_state)
        current_state.chessboard[random_piece.row][random_piece.col] = random_piece

        # winner = current_state.check_winner()
        # if (winner == 'Player 1' and initial_turn == WHITE) or (winner == 'Player 2' and initial_turn == BLACK):
        #     return 1
        # elif (winner == 'Player 1' and initial_turn == BLACK) or (winner == 'Player 2' and initial_turn == WHITE):
        #     return -1

        # Checking if there are other pieces to catch
        if not random_piece.king:
            random_piece.check_catch(current_state)
        else:
            random_piece.check_catch_king(current_state)

        if random_piece.legal and random_piece.has_caught:
            pass
        
        else:
            random_piece.transform_king()
            if current_state.turn == WHITE:
                current_state.turn = BLACK  
            else:
                current_state.turn = WHITE

    # if current_state.last_moved_piece.color == initial_turn: # if the last moved piece is of the same color of the MCTS color, MCTS wins
    #     reward = 1
    # else:
    #     reward = -1
    # return reward

def backpropagate(node, reward):
    while node is not None:
        node.visits += 1
        node.reward += reward
        node = node.parent

def mcts(root_state, turn, iterations):
    root_state.turn = turn # So that the turn is associated with the state
    root = MCTSNode(root_state)

    for _ in range(iterations):

        # while not root_state.is_terminal:
        #     if len(root.children) < numb_of_possible_moves:
        #         new_node = expand(selected_node)
        #         break
        #     else:
        #         select(root)

        selected_node = select(root)
        # print('--------init----------')
        # selected_node.state.print_board()
        new_node = expand(selected_node)
        #new_node.state.print_board()
        #print('--------end-----------')
        reward = simulate(new_node, root_state.turn)
        backpropagate(new_node, reward)

    best_piece_pos = max(root.children, key=lambda child: child.visits).state.last_moved_piece.previous_position
    best_move = max(root.children, key=lambda child: child.visits).state.last_move
    return best_piece_pos, best_move
