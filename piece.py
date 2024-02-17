class Piece:

    def __init__(self, row, col, color, king = False):
        self.row = row
        self.col = col
        self.color = color
        self.king = king
    
    def move(self, row, col):
        self.row = row
        self.col = col

WHITE = (255, 255, 255) # Find a way to only have this once in the whole code
BLACK = (0, 0, 0)

# Lists to hold the pieces for each player
all_pieces_white = []
all_pieces_black = []

# Initial pieces for WHITE
for row in [5, 6, 7]:
    for col in range(8):
        if (row == 6 and col in [0, 7]) or (row == 5 and col in [0, 1, 6, 7]):
            continue
        else:
            piece = Piece(row, col, WHITE)
            all_pieces_white.append(piece)

# Initial pieces for BLACK
for row in range(3):
    for col in range(8):
        if (row == 1 and col in [0, 7]) or (row == 2 and col in [0, 1, 6, 7]):
            continue
        else:
            piece = Piece(row, col, BLACK)
            all_pieces_black.append(piece)