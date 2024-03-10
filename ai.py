import random
from vars import *
from board import Board
import math
from copy import deepcopy
import time


class Minimax:
    
    def __init__(self, depth):
        self.depth = depth

    
    def minimax(self, board, depth, maximizing_player, alpha, beta, turn, evaluation_func):
        if depth == 0 or board.check_winner():
            # Evaluate the current state of the board
            if evaluation_func == 1:
                return self.evaluate(board, turn)
            elif evaluation_func == 2:
                return self.evaluate_2(board, turn)
            elif evaluation_func == 3:
                return self.evaluate_3(board, turn)
        
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
                    eval = self.minimax(deepcopy(board), depth - 1, False, alpha, beta, turn, evaluation_func)
                    
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
                    eval = self.minimax(board, depth - 1, True, alpha, beta, turn, evaluation_func)
                    
                    # Undo the move
                    board.chessboard[piece.row][piece.col] = None
                    piece.move(previous_row, previous_col, board)
                    board.chessboard[piece.row][piece.col] = piece
                    
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    
                    if beta <= alpha:
                        break  # Pruning
                    
            return min_eval
        

    def execute_minimax(self, board, depth, turn, evaluation_func):
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
                
                eval = self.minimax(deepcopy(board_copy), depth - 1, True, float('-inf'), float('inf'), turn, evaluation_func)

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
    
    def evaluate_2(self, board, turn):
        score = 0

        # Piece Count
        white_pieces = len(board.all_pieces_white)
        black_pieces = len(board.all_pieces_black)
        score += white_pieces - black_pieces if turn == WHITE else black_pieces - white_pieces
        return score

    def evaluate_3(self, board, turn):
        score = 0

        # Piece Count
        white_pieces = len(board.all_pieces_white)
        black_pieces = len(board.all_pieces_black)
        score += white_pieces - black_pieces if turn == WHITE else black_pieces - white_pieces

        # King Count
        white_kings = sum(piece.king for piece in board.all_pieces_white)
        black_kings = sum(piece.king for piece in board.all_pieces_black)
        score += (white_kings - black_kings) * 5 if turn == WHITE else (black_kings - white_kings) * 5
        return score


class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0


class MontecarloTreeSearch:
    def __init__(self, iterations, exploration_weight=1.4):
        self.iterations = iterations
        self.exploration_weight = exploration_weight
        


    def expand(self, node):
        new_state = deepcopy(node.state)  # Create a copy of the current board
        new_legal_pieces, new_legal_moves = new_state.find_available_moves(new_state.turn)
        # if not new_legal_pieces:
        #     new_state.print_board()
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

        new_state.check_winner()

        new_node = MCTSNode(new_state, parent=node)
        node.children.append(new_node)
        return new_node

    def select(self, node):
        n_children = node.state.count_possible_moves()
        if not node.children or len(node.children) < n_children:
            return node

        selected_child = max(node.children, key=lambda child: self.ucb_score(child))
        return self.select(selected_child)

    def ucb_score(self, node):
        self.exploration_weight = 1.4  # You may need to tune this parameter
        return node.reward / node.visits + self.exploration_weight * math.sqrt(math.log(node.parent.visits) / node.visits)

    def simulate(self, node, initial_turn):
        current_state = deepcopy(node.state)

        winner = current_state.check_winner()
        if (winner == 'Player 1' and initial_turn == WHITE) or (winner == 'Player 2' and initial_turn == BLACK):
            return 1
        elif (winner == 'Player 1' and initial_turn == BLACK) or (winner == 'Player 2' and initial_turn == WHITE):
            return -1
        elif winner == 'Tie':
            return 0
        
        while True:

            winner = current_state.check_winner()
            if (winner == 'Player 1' and initial_turn == WHITE) or (winner == 'Player 2' and initial_turn == BLACK):
                return 1
            elif (winner == 'Player 1' and initial_turn == BLACK) or (winner == 'Player 2' and initial_turn == WHITE):
                return -1
            elif winner == 'Tie':
                return 0
            
            legal_pieces, legal_moves = current_state.find_available_moves(current_state.turn)
            random_piece_index = random.choice(range(len(legal_pieces)))
            random_piece = legal_pieces[random_piece_index]
            random_move_index = random.choice(range(len(legal_moves[random_piece_index])))
            random_move = legal_moves[random_piece_index][random_move_index]
            current_state.chessboard[random_piece.row][random_piece.col] = None
            random_piece.move(random_move[0], random_move[1], current_state)
            current_state.chessboard[random_piece.row][random_piece.col] = random_piece

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


    def backpropagate(self, node, result):
        node.visits += 1
        node.reward += result
        if node.parent:
            # node.parent.backpropagate(result)
            self.backpropagate(node.parent, result)


    def mcts(self, root_state, turn):
        root_state.turn = turn # So that the turn is associated with the state
        root = MCTSNode(root_state)
        for _ in range(self.iterations):
            node = root

            # Selection phase
            while not node.state.is_terminal:
                n_children = node.state.count_possible_moves()
                if len(node.children) < n_children:
                    # Expand
                    node = self.expand(node)
                    break
                else: # Max expansion
                    # Selection
                    # print('Init')
                    node = self.select(node)
                    # print('End')

            # Simulation phase
            reward = self.simulate(node, turn)

            # Backpropagation phase
            self.backpropagate(node, reward)
        
        best_piece_pos = max(root.children, key=lambda child: child.visits).state.last_moved_piece.previous_position
        best_move = max(root.children, key=lambda child: child.visits).state.last_move
        return best_piece_pos, best_move
