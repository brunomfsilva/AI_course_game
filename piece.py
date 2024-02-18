class Piece:

    def __init__(self, row, col, color, king = False):
        self.row = row
        self.col = col
        self.color = color
        self.king = king
        self.legal = []
        self.right = 7 - self.col # Space left until right limit
        self.down = 7 - self.row # Space left until bottom limit
    
    def move(self, row, col):
        self.row = row
        self.col = col

    # Function to check the legal moves (later we have to deal with occupied positions, the switch from normal piece to king, and capturing pieces)
    # Maybe the occupied positions are handled with the dameo.py logic already?
    def legal_positions(self):
        if not self.king and self.color == BLACK and self.row < 7:
            if self.right == 0:
                self.legal = [(self.row + 1, self.col), (self.row + 1, self.col - 1)]
            elif self.col == 0:
                self.legal = [(self.row + 1, self.col), (self.row + 1, self.col + 1)]
            else:
                self.legal = [(self.row + 1, self.col), (self.row + 1, self.col + 1), (self.row + 1, self.col - 1)]

        if not self.king and self.color == WHITE and self.row > 0:
            if self.right == 0:
                self.legal = [(self.row - 1, self.col), (self.row - 1, self.col - 1)]
            elif self.col == 0:
                self.legal = [(self.row - 1, self.col), (self.row - 1, self.col + 1)]
            else:
                self.legal = [(self.row - 1, self.col), (self.row - 1, self.col + 1), (self.row - 1, self.col - 1)]

        # MISSING THE PIECES THAT ARE ALREADY IN THE BORDERS
        if self.king:
            self.legal = []

            # Moves to the right
            for col in range(1, self.right + 1):
                self.legal += [(self.row, self.col + col)]
            
            # Moves to the left
            for col in range(1, self.col + 1):
                self.legal += [(self.row, self.col - col)]

            # Moves upwards
            for row in range(1, self.row + 1):
                self.legal += [(self.row - row, self.col)]    

            # Moves downwards
            for row in range(1, self.down + 1):
                self.legal += [(self.row + row, self.col)]

            # Moves diagonally
                # up right
            for row in range(1, self.row + 1):
                for col in range(1, self.right + 1):
                    self.legal += [(self.row - row, self.col + col)]
            
                # down right
            for row in range(1, self.down + 1):
                for col in range(1, self.right + 1):
                    self.legal += [(self.row + row, self.col + col)]

                # up left
            for row in range(1, self.row + 1):
                for col in range(1, self.col + 1):
                    self.legal += [(self.row - row, self.col - col)]

                # down left
            for row in range(1, self.down + 1):
                for col in range(1, self.col + 1):
                    self.legal += [(self.row + row, self.col - col)]

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