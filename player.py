import random
from vars import *
from board import Board
import math
from copy import deepcopy
from ai import Minimax, MontecarloTreeSearch
import pygame

class Player:
    def __init__(self, player_type, depth_or_iterations, team, evaluation_function = 1):
        self.type = player_type
        self.depth_or_iterations = depth_or_iterations
        self.team = team
        self.evaluation_function = evaluation_function
        

    def get_ai_move(self, board):
        """get the movements"""
        
        if self.type == "Minimax":
            minimax = Minimax(self.depth_or_iterations)
            best_piece_pos, best_move = minimax.execute_minimax(board, self.depth_or_iterations, self.team, self.evaluation_function)
            return self.make_ai_move(board, best_piece_pos, best_move)

            
        elif self.type == "Montecarlo":
            monte_carlo = MontecarloTreeSearch(self.depth_or_iterations)
            best_piece_pos, best_move = monte_carlo.mcts(board, self.team)
            return self.make_ai_move(board, best_piece_pos, best_move)


    def make_ai_move(self, board, best_piece_pos, best_move):
        """make the movement from AI players"""
        selected_piece = board.chessboard[best_piece_pos[0]][best_piece_pos[1]]
        board.chessboard[selected_piece.row][selected_piece.col] = None
        selected_piece.move(best_move[0], best_move[1], board)
        board.chessboard[selected_piece.row][selected_piece.col] = selected_piece
        return selected_piece

    def get_human_move(self, board, gui, screen, winner, square_size, selected_piece):
        human_playing = True
        while human_playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
                    if winner:
                        winner = None
                        game_over = False
                        players, size = gui.main_menu(screen)
                        square_size = int(min(width, height)/size)
                        gui.square_size = square_size
                        board.change_size(size)
                        board.start_game(gui, screen)
                        player1 = Player(players[0], players[2], WHITE)
                        player2 = Player(players[1], players[3], BLACK)
                        selected_piece = None
                        turn = WHITE
                        board.turn = WHITE
                        

                    x, y = pygame.mouse.get_pos()
                    row = y // square_size
                    col = x // square_size

                    
                    piece = board.find_piece(row, col, board.all_pieces_black, board.all_pieces_white)

                    
                    can_catch = board.check_piece_to_capture(self.team)
                    piece = board.check_if_capture( gui, screen, can_catch, piece, self.team, selected_piece) #check if piece already capture (if needed)

                    if piece and piece.color == self.team:
                        selected_piece = piece
                        
                        if not piece.king:
                            selected_piece.check_catch(board)
                        elif piece.king:
                            selected_piece.check_catch_king(board)
                            
                        if not selected_piece.legal:
                            selected_piece.legal_positions() # If there is no piece to catch, the legal moves list will be empty so we compute the moves normally
                            selected_piece.check_position(board) # Remove the occupied spaces from the legal moves
                            selected_piece.no_jump(board)
                            board.actual_state(screen)  # Redraw the board to clear previous highlights
                            gui.display_selected_piece(screen, selected_piece)  # Highlight selected piece 
                            gui.display_legal_moves(screen, selected_piece.legal) # Highlight legal moves
                            pygame.display.flip()

                        else:
                            #selected_piece.check_catch(board)
                            board.actual_state(screen)  # Redraw the board to clear previous highlights
                            gui.display_selected_piece(screen, selected_piece)  # Highlight selected piece 
                            gui.display_legal_moves(screen, selected_piece.legal) # Highlight legal moves
                            pygame.display.flip()

                    elif selected_piece:  # If a piece is selected and a square is clicked
                        
                        if not selected_piece.king:
                            selected_piece.check_catch(board)
                        else:
                            selected_piece.check_catch_king(board)

                        if not selected_piece.legal:
                            selected_piece.legal_positions() # If there is no piece to catch, the legal moves list will be empty so we compute the moves normally
                            selected_piece.check_position(board) # Remove the occupied spaces from the legal moves
                            selected_piece.no_jump(board) # If tt is king, it can't jump over
                            
                                
                        if (row, col) in selected_piece.legal: # If the selected square is a legal move for the piece

                            board.chessboard[selected_piece.row][selected_piece.col] = None ## MATRIX
                            
                            selected_piece.move(row, col, board) # move
                            board.chessboard[selected_piece.row][selected_piece.col] = selected_piece ## MATRIX
                            human_playing = False
                        
                            board.actual_state(screen)
                            gui.display_turn(screen, "player 1" if self.team == WHITE else "player 2")
                            pygame.display.flip()
                            return selected_piece
        


    
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

    return (best_piece.row, best_piece.col), best_move

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
            score += (board.size - 1 - piece.row)
        else:
            score -= (board.size - 1 - piece.row)  # Favor lower rows for black pieces

    for piece in board.all_pieces_black:
        if turn == BLACK:
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
        self.reward = 0

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

    new_state.check_winner()

    new_node = MCTSNode(new_state, parent=node)
    node.children.append(new_node)
    return new_node

def select(node):
    n_children = node.state.count_possible_moves()
    if not node.children or len(node.children) < n_children:
        return node

    selected_child = max(node.children, key=lambda child: ucb_score(child))
    return select(selected_child)

def ucb_score(node):
    exploration_weight = 1.4  # You may need to tune this parameter
    return node.reward / node.visits + exploration_weight * math.sqrt(math.log(node.parent.visits) / node.visits)

def simulate(node, initial_turn):
    current_state = deepcopy(node.state)


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

def backpropagate(node, result):
    node.visits += 1
    node.reward += result
    if node.parent:
        backpropagate(node.parent, result)



def mcts2(root_state, turn, iterations):
    root_state.turn = turn # So that the turn is associated with the state
    root = MCTSNode(root_state)

    for _ in range(iterations):
        node = root

        # Selection phase
        while not node.state.is_terminal:
            n_children = node.state.count_possible_moves()
            if len(node.children) < n_children:
                # Expand
                node = expand(node)
                break
            else: # Max expansion
                # Selection
                print('Init')
                node = select(node)
                print('End')

        # Simulation phase
        reward = simulate(node, turn)

        # Backpropagation phase
        backpropagate(node, reward)
    
    best_piece_pos = max(root.children, key=lambda child: child.visits).state.last_moved_piece.previous_position
    best_move = max(root.children, key=lambda child: child.visits).state.last_move
    return best_piece_pos, best_move

