def check_piece_to_capture(board, turn):
    all_pieces = board.all_pieces_black if turn == BLACK else board.all_pieces_white
    for piece in all_pieces:
        piece.check_catch(board)  # Updates legal moves considering captures
        if piece.legal:
            return True
    return False