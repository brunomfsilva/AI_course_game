from vars import *

class Piece:

    def __init__(self, row, col, color, king = False):
        self.row = row
        self.col = col
        self.color = color
        self.king = king
        self.legal = []
        self.right = size - 1 - self.col # Space left until right limit
        self.down = size - 1 - self.row # Space left until bottom limit
        self.catch = False # To check if there is a piece to catch or not
    
    def move(self, row, col):
        self.row = row
        self.col = col
        self.right = size - 1 - col
        self.down = size - 1 - row
        # If the piece reaches the last row, it becomes a king
        if row == 0 and self.color == WHITE:
            self.king = True
        if row == 7 and self.color == BLACK:
            self.king = True

    # Function to check the legal moves (later we have to deal with capturing pieces)
    def legal_positions(self):
        if not self.king and self.color == BLACK and self.row < 7:
            if self.right == 0:
                self.legal = [(self.row + 1, self.col), (self.row + 1, self.col - 1)]
            elif self.col == 0:
                self.legal = [(self.row + 1, self.col), (self.row + 1, self.col + 1)]
            else:
                self.legal = [(self.row + 1, self.col), (self.row + 1, self.col + 1), (self.row + 1, self.col - 1)]

        if not self.king and self.color == WHITE and self.row:
            if self.right == 0:
                self.legal = [(self.row - 1, self.col), (self.row - 1, self.col - 1)]
            elif self.col == 0:
                self.legal = [(self.row - 1, self.col), (self.row - 1, self.col + 1)]
            else:
                self.legal = [(self.row - 1, self.col), (self.row - 1, self.col + 1), (self.row - 1, self.col - 1)]

        if self.king:
            self.legal = []

            # Moves to the right
            if self.right:
                for col in range(1, self.right + 1):
                    self.legal += [(self.row, self.col + col)]
            
            # Moves to the left
            if self.col:
                for col in range(1, self.col + 1):
                    self.legal += [(self.row, self.col - col)]

            # Moves upwards
            if self.row:
                for row in range(1, self.row + 1):
                    self.legal += [(self.row - row, self.col)]  

            # Moves downwards
            if self.down:
                for row in range(1, self.down + 1):
                    self.legal += [(self.row + row, self.col)]

            # Moves diagonally
                # up right
            if self.row and self.right:
                for i in range(1, min(self.row, self.right) + 1):
                    self.legal += [(self.row - i, self.col + i)]
            
                # down right
            if self.down and self.right:
                for i in range(1, min(self.down, self.right) + 1):
                    self.legal += [(self.row + i, self.col + i)]

                # up left
            if self.row and self.col:
                for i in range(1, min(self.row, self.col) + 1):
                    self.legal += [(self.row - i, self.col - i)]

                # down left
            if self.down and self.col:
                for i in range(1, min(self.down, self.col) + 1):
                    self.legal += [(self.row + i, self.col - i)]
    
    # Function to check if the position is free
    def check_position(self, board):
        arg_taken = []
        whites, blacks = board.occupied()
        for i in range(len(self.legal)):
            if self.legal[i] in whites or self.legal[i] in blacks:
                arg_taken.append(i)
        self.legal = [self.legal[i] for i in range(len(self.legal)) if i not in arg_taken]

        # To stop the legal positions when an adversary piece is in the way
        to_pop = []
        if self.king and self.color == WHITE:
            for i in range(len(self.legal)):
                if self.legal[i][0] == self.row: # legal position in the same row
                    for j in range(1, abs(self.legal[i][1] - self.col) + 1):
                        if self.col > self.legal[i][1] and (self.row, self.col - j) in blacks: # legal position to the left
                            to_pop.append(i)
                        if self.col < self.legal[i][1] and (self.row, self.col + j) in blacks: # legal position to the right
                            to_pop.append(i)

                elif self.legal[i][1] == self.col: # legal position in the same column
                    for j in range(1, abs(self.legal[i][0] - self.row) + 1):
                        if self.row > self.legal[i][0] and (self.row - j, self.col) in blacks: # legal position up
                            to_pop.append(i)
                        if self.row < self.legal[i][0] and (self.row + j, self.col) in blacks: # legal position down
                            to_pop.append(i)

                else: # legal position in the diagonal
                    for j in range(1, abs(self.legal[i][0] - self.row)):
                        if self.row > self.legal[i][0] and self.col > self.legal[i][1] and (self.row - j, self.col - j) in blacks: # legal position up left
                            to_pop.append(i)
                        if self.row > self.legal[i][0] and self.col < self.legal[i][1] and (self.row - j, self.col + j) in blacks: # legal position up right
                            to_pop.append(i)
                        if self.row < self.legal[i][0] and self.col > self.legal[i][1] and (self.row + j, self.col - j) in blacks: # legal position down left
                            to_pop.append(i)
                        if self.row < self.legal[i][0] and self.col < self.legal[i][1] and (self.row + j, self.col + j) in blacks: # legal position down right
                            to_pop.append(i)
        
        # CREATE FUNCTION TO AVOID REPEATING ALL THIS JUST BECAUSE OF SELF.COLOR == WHITE OR BLACK
        if self.king and self.color == BLACK:
            for i in range(len(self.legal)):
                if self.legal[i][0] == self.row: # legal position in the same row
                    for j in range(1, abs(self.legal[i][1] - self.col) + 1):
                        if self.col > self.legal[i][1] and (self.row, self.col - j) in whites: # legal position to the left
                            to_pop.append(i)
                        if self.col < self.legal[i][1] and (self.row, self.col + j) in whites: # legal position to the right
                            to_pop.append(i)

                elif self.legal[i][1] == self.col: # legal position in the same column
                    for j in range(1, abs(self.legal[i][0] - self.row) + 1):
                        if self.row > self.legal[i][0] and (self.row - j, self.col) in whites: # legal position up
                            to_pop.append(i)
                        if self.row < self.legal[i][0] and (self.row + j, self.col) in whites: # legal position down
                            to_pop.append(i)

                else: # legal position in the diagonal
                    for j in range(1, abs(self.legal[i][0] - self.row)):
                        if self.row > self.legal[i][0] and self.col > self.legal[i][1] and (self.row - j, self.col - j) in whites: # legal position up left
                            to_pop.append(i)
                        if self.row > self.legal[i][0] and self.col < self.legal[i][1] and (self.row - j, self.col + j) in whites: # legal position up right
                            to_pop.append(i)
                        if self.row < self.legal[i][0] and self.col > self.legal[i][1] and (self.row + j, self.col - j) in whites: # legal position down left
                            to_pop.append(i)
                        if self.row < self.legal[i][0] and self.col < self.legal[i][1] and (self.row + j, self.col + j) in whites: # legal position down right
                            to_pop.append(i)

        self.legal = [self.legal[i] for i in range(len(self.legal)) if i not in to_pop]

    # Function to check if there are any pieces to catch
    def check_catch(self, board):
        catchable = [(self.row - 1, self.col), (self.row + 1, self.col), (self.row, self.col + 1), (self.row, self.col - 1)] # Positions where catchable pieces might be
        landing_pos = [(self.row - 2, self.col), (self.row + 2, self.col), (self.row, self.col + 2), (self.row, self.col - 2)] # Position after that
        self.legal = []
        whites, blacks = board.occupied()
        if self.color == WHITE:
            for i in range(len(catchable)):
                if catchable[i] in blacks and landing_pos[i] not in whites + blacks and landing_pos[i][1] < size - 1:
                    self.legal += [(landing_pos[i])]
        if self.color == BLACK:
            for i in range(len(catchable)):
                if catchable[i] in whites and landing_pos[i] not in whites + blacks and landing_pos[i][1] < size - 1:
                    self.legal += [(landing_pos[i])]
        
    def check_catch_king(self, board):    
        catchable_king = []
        self.legal = []
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)] # unitary directional moves
        space = [self.down, self.row, self.right, self.col] # space around the piece
        for i in range(len(moves)):
            for j in range(1, space[i]+1):
                catchable_king += [(self.row + moves[i][0]*j, self.col + moves[i][1]*j)]
        whites, blacks = board.occupied()
        targets = []
        if self.color == WHITE:
            for i in range(len(catchable_king)):
                if catchable_king[i] in blacks:
                    targets += [catchable_king[i]] # isolating the catchable pieces that are of the opposite team
        diff = []
        for i in range(len(targets)):
            diff += [(targets[i][0] - self.row, targets[i][1] - self.col)] # list with the differences between target pieces and king piece
        diff_r = []
        diff_c = []
        final_targets = []
        for i in range(len(diff)):
            if diff[i][0] == 0: # target in the same row, different column
                diff_r.append(diff[i][1]) # getting the difference in columns
        
        closest = min(diff_r, key=lambda x: abs(x))
        if (self.row, self.col + closest -1) not in whites + blacks:
            self.legal = [(self.row, self.col + closest -1)]
        
        #while True:




    def drop_out_range(self):
        drop = []
        for i in range(len(self.legal)):
            if self.legal[i][0] < 0 or self.legal[i][0] > size - 1 or self.legal[i][1] < 0 or self.legal[i][1] > size - 1:
                drop.append(i)
        self.legal = [self.legal[i] for i in range(len(self.legal)) if i not in drop]