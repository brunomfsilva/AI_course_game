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
        self.previous_position = ()
        self.has_caught = False
    
    def move(self, row, col, board):
        self.previous_position = (self.row, self.col)
        self.row = row
        self.col = col
        self.right = size - 1 - col
        self.down = size - 1 - row
        self.has_caught = False # To reset this state if it does not catch anything
        # If the piece reaches the last row, it becomes a king
        if row == 0 and self.color == WHITE:
            self.king = True
        if row == size - 1 and self.color == BLACK:
            self.king = True

        # To eliminate the piece caught
        if abs(self.previous_position[0] - self.row) > 1: # Moved vertically more than one square
            for i in range(1, abs(self.row - self.previous_position[0])):
                if self.previous_position[0] > self.row and board.chessboard[self.previous_position[0] - i][self.previous_position[1]] != None and board.chessboard[self.previous_position[0] - i][self.previous_position[1]].color != self.color:
                    board.drop_piece(self.previous_position[0] - i, self.previous_position[1])
                    board.chessboard[self.previous_position[0] - i][self.previous_position[1]] = None
                    self.has_caught = True
                if self.previous_position[0] < self.row and board.chessboard[self.previous_position[0] + i][self.previous_position[1]] != None and board.chessboard[self.previous_position[0] + i][self.previous_position[1]].color != self.color:
                    board.drop_piece(self.previous_position[0] + i, self.previous_position[1])
                    board.chessboard[self.previous_position[0] + i][self.previous_position[1]] = None
                    self.has_caught = True

        if abs(self.previous_position[1] - self.col) > 1: # Moved horizontally more than one square
            for i in range(1, abs(self.col - self.previous_position[1])):
                if self.previous_position[1] > self.col and board.chessboard[self.previous_position[0]][self.previous_position[1] - i] != None and board.chessboard[self.previous_position[0]][self.previous_position[1] - i].color != self.color:
                    board.drop_piece(self.previous_position[0], self.previous_position[1] - i)
                    board.chessboard[self.previous_position[0]][self.previous_position[1] - i] = None
                    self.has_caught = True
                if self.previous_position[1] < self.col and board.chessboard[self.previous_position[0]][self.previous_position[1] + i] != None and board.chessboard[self.previous_position[0]][self.previous_position[1] + i].color != self.color:
                    board.drop_piece(self.previous_position[0], self.previous_position[1] + i)
                    board.chessboard[self.previous_position[0]][self.previous_position[1] + i] = None
                    self.has_caught = True

    # Function to check the legal moves
    def legal_positions(self):
 
       # if self.king:
            self.legal = []

            # Moves to the right
            if self.right and self.king:
                for col in range(1, self.right + 1):
                    self.legal += [(self.row, self.col + col)]
            
            # Moves to the left 
            if self.col and self.king:
                for col in range(1, self.col + 1):
                    self.legal += [(self.row, self.col - col)]

            # Moves upwards
            if self.row  and not (self.color == BLACK and not self.king):
                for row in range(1, self.row + 1):
                    self.legal += [(self.row - row, self.col)]  

            # Moves downwards
            if self.down and not (self.color == WHITE and not self.king):
                for row in range(1, self.down + 1):
                    self.legal += [(self.row + row, self.col)]

            # Moves diagonally
                # up right
            if self.row and self.right and not (self.color == BLACK and not self.king):
                for i in range(1, min(self.row, self.right) + 1):
                    self.legal += [(self.row - i, self.col + i)]
            
                # down right
            if self.down and self.right and not (self.color == WHITE and not self.king):
                for i in range(1, min(self.down, self.right) + 1):
                    self.legal += [(self.row + i, self.col + i)]

                # up left
            if self.row and self.col and not (self.color == BLACK and not self.king):
                for i in range(1, min(self.row, self.col) + 1):
                    self.legal += [(self.row - i, self.col - i)]

                # down left
            if self.down and self.col and not (self.color == WHITE and not self.king):
                for i in range(1, min(self.down, self.col) + 1):
                    self.legal += [(self.row + i, self.col - i)]
    
    # Function to check if the position is free
    def check_position(self, board):
        arg_taken = []
        arg_inval = []
        inval=[]        
        whites, blacks = board.occupied()
        for i in range(len(self.legal)):
            if self.legal[i] in whites or self.legal[i] in blacks:
                arg_taken.append(i)
        self.legal = [self.legal[i] for i in range(len(self.legal)) if i not in arg_taken]

        if self.color == BLACK and not self.king:
            #remove positions extra down
            if self.down >=2:
                if (self.row+1, self.col) not in blacks and (self.row+1, self.col) not in whites:
                    for i in range(2, self.down+1):
                        inval+= [(self.row+i, self.col)]
                        
                if self.down >=3 and (self.row+1, self.col) in whites:
                    #remove a casa três espaços abaixo até fim
                    for i in range(3, self.down+1):
                        inval+= [(self.row+i, self.col)]   
                
                for j in range (3, size-1):
                    if self.down >= j and (self.row+1, self.col) in blacks:
                        for k in range (2, j):
                            if (self.row+k, self.col) not in blacks:
                             #tirar a casa k+1 espaços abaixo até fim    
                                 for i in range(k+1, self.down+1):
                                     inval+= [(self.row+i, self.col)]   
        
                #retirar posições em excesso diagonal direita/baixo
                for j in range (2, size-1):
                     if min(self.down, self.right) >= j: #and (self.row+1, self.col+1) not in blacks:
                       for k in range (1, j):
                            if (self.row+k, self.col+k) not in blacks:
                                for i in range(k+1, min(self.down, self.right)+1):
                                     inval+= [(self.row+i, self.col+i)]   
            
                #retirar posições em excesso left/down
                for j in range (2, size-1):
                     if min(self.down, self.col) >= j: #and (self.row+1, self.col+1) not in blacks:
                       for k in range (1, j):
                            if (self.row+k, self.col-k) not in blacks:
                                for i in range(k+1, min(self.down, self.col)+1):
                                     inval+= [(self.row+i, self.col-i)]
        
        if self.color == WHITE and not self.king:
            #retirar posições em excesso up
            if self.row >=2:
                if (self.row-1, self.col) not in blacks and (self.row-1, self.col) not in whites:
                    #tirar a casa dois espaços acima até fim do range como disponível
                    for i in range(2, self.row+1):
                        inval+= [(self.row-i, self.col)]
                        
                if self.row >=3 and (self.row-1, self.col) in blacks:
                    #tirar a casa três espaços acima até fim do range como disponível    
                    for i in range(3, self.row-1):
                        inval+= [(self.row-i, self.col)]   
                
                for j in range (3, size-1):
                    if self.row >= j and (self.row-1, self.col) in whites:
                        for k in range (2, j):
                            if (self.row-k, self.col) not in whites:
                             #tirar a casa k+1 espaços acima até fim do range como disponível    
                                 for i in range(k+1, self.row+1):
                                     inval+= [(self.row-i, self.col)]   
        
                #retirar posições em excesso diagonal direita/cima
                for j in range (2, size-1):
                     if min(self.row, self.right) >= j:
                       for k in range (1, j):
                            if (self.row-k, self.col+k) not in whites:
                                for i in range(k+1, min(self.row, self.right)+1):
                                     inval+= [(self.row-i, self.col+i)]   
            
                #retirar posições em excesso left/cima
                for j in range (2, size-1):
                     if min(self.row, self.col) >= j:
                       for k in range (1, j):
                            if (self.row-k, self.col-k) not in whites:
                                for i in range(k+1, min(self.row, self.col)+1):
                                     inval+= [(self.row-i, self.col-i)]
            
        for j in range(len(self.legal)):
            if self.legal[j] in inval:
                arg_inval.append(j)
            
        self.legal = [self.legal[j] for j in range(len(self.legal)) if j not in arg_inval]     


    # To stop the legal positions when an adversary piece is in the way
    def no_jump(self, board):
        to_pop = []
        whites, blacks = board.occupied()
        op_pieces = whites + blacks
        
        if self.king:
            for i in range(len(self.legal)):
                if self.legal[i][0] == self.row: # legal position in the same row
                    for j in range(1, abs(self.legal[i][1] - self.col) + 1):
                        #if self.col > self.legal[i][1] and (self.row, self.col - j) in whites: # legal position to the left
                        if self.col > self.legal[i][1] and (self.row, self.col - j) in op_pieces: # legal position to the left
                            to_pop.append(i)
                        if self.col < self.legal[i][1] and (self.row, self.col + j) in op_pieces: # legal position to the right
                            to_pop.append(i)

                elif self.legal[i][1] == self.col: # legal position in the same column
                    for j in range(1, abs(self.legal[i][0] - self.row) + 1):
                        if self.row > self.legal[i][0] and (self.row - j, self.col) in op_pieces: # legal position up
                            to_pop.append(i)
                        if self.row < self.legal[i][0] and (self.row + j, self.col) in op_pieces: # legal position down
                            to_pop.append(i)

                else: # legal position in the diagonal
                    for j in range(1, abs(self.legal[i][0] - self.row)):
                        if self.row > self.legal[i][0] and self.col > self.legal[i][1] and (self.row - j, self.col - j) in op_pieces: # legal position up left
                            to_pop.append(i)
                        if self.row > self.legal[i][0] and self.col < self.legal[i][1] and (self.row - j, self.col + j) in op_pieces: # legal position up right
                            to_pop.append(i)
                        if self.row < self.legal[i][0] and self.col > self.legal[i][1] and (self.row + j, self.col - j) in op_pieces: # legal position down left
                            to_pop.append(i)
                        if self.row < self.legal[i][0] and self.col < self.legal[i][1] and (self.row + j, self.col + j) in op_pieces: # legal position down right
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
                if catchable[i] in blacks and landing_pos[i] not in whites + blacks and landing_pos[i][1] <= size - 1:
                    self.legal += [(landing_pos[i])]
        if self.color == BLACK:
            for i in range(len(catchable)):
                if catchable[i] in whites and landing_pos[i] not in whites + blacks and landing_pos[i][1] <= size - 1:
                    self.legal += [(landing_pos[i])]
        self.drop_out_range()
        
    def check_catch_king(self, board):
        self.legal = []
        # down check
        end = False
        for i in range(1, self.down + 1):
            if board.chessboard[self.row + i][self.col] != None and board.chessboard[self.row + i][self.col].color != self.color and board.chessboard[self.row + i + 1][self.col] == None:
                if i == 1:
                    self.legal += [(self.row + i + 1, self.col)]
                    for j in range(1, self.row + i + 2):
                        if board.chessboard[self.row + i + 1 + j][self.col] == None:
                            self.legal += [(self.row + i + 1 + j, self.col)]
                        else:
                            end = True
                            break
                elif i > 1 and board.chessboard[self.row + i - 1][self.col] == None:
                    self.legal += [(self.row + i + 1, self.col)]
                    for j in range(1, self.row + i + 2):
                        if board.chessboard[self.row + i + 1 + j][self.col] == None:
                            self.legal += [(self.row + i + 1 + j, self.col)]
                        else:
                            end = True
                            break
            if end:
                break

        # up check
        end = False
        for i in range(1, self.row + 1):
            if board.chessboard[self.row - i][self.col] != None and board.chessboard[self.row - i][self.col].color != self.color and board.chessboard[self.row - i - 1][self.col] == None:
                if i == 1:
                    self.legal += [(self.row - i - 1, self.col)]
                    for j in range(1, self.row - i):
                        if board.chessboard[self.row - i - 1 - j][self.col] == None:
                            self.legal += [(self.row - i - 1 - j, self.col)]
                        else:
                            end = True
                            break
                elif i > 1 and board.chessboard[self.row - i + 1][self.col] == None:
                    self.legal += [(self.row - i - 1, self.col)]
                    for j in range(1, self.row - i):
                        if board.chessboard[self.row - i - 1 - j][self.col] == None:
                            self.legal += [(self.row - i - 1 - j, self.col)]
                        else:
                            end = True
                            break
            if end:
                break
        
        # right check
        # this one is slightly different from the other checks because of the boarder on the right side of the board
        # use the same logic if eventually the game window is increased for other sides (top, down, left) 
        end = False
        for i in range(1, self.right + 1):
            if self.col + i + 1 <= size - 1 and board.chessboard[self.row][self.col + i] != None and board.chessboard[self.row][self.col + i].color != self.color and board.chessboard[self.row][self.col + i + 1] == None:
                if i == 1:
                    self.legal += [(self.row, self.col + i + 1)]
                    for j in range(1, self.col + i + 2):
                        if self.col + i + 1 + j <= size - 1 and board.chessboard[self.row][self.col + i + 1 + j] == None:
                            self.legal += [(self.row, self.col + i + 1 + j)]
                        else:
                            end = True
                            break
                elif i > 1 and board.chessboard[self.row][self.col + i - 1] == None:
                    self.legal += [(self.row, self.col + i + 1)]
                    for j in range(1, self.col + i + 2):
                        if self.col + i + 1 + j <= size - 1 and board.chessboard[self.row][self.col + i + 1 + j] == None:
                            self.legal += [(self.row, self.col + i + 1 + j)]
                        else:
                            end = True
                            break
            if end:
                break

        # left check
        end = False
        for i in range(1, self.col + 1):
            if board.chessboard[self.row][self.col - i] != None and board.chessboard[self.row][self.col - i].color != self.color and board.chessboard[self.row][self.col - i - 1] == None:
                if i == 1:
                    self.legal += [(self.row, self.col - i - 1)]
                    for j in range(1, self.col - i):
                        if board.chessboard[self.row][self.col - i - 1 - j] == None:
                            self.legal += [(self.row, self.col - i - 1 - j)]
                        else:
                            end = True
                            break
            
                elif i > 1 and board.chessboard[self.row][self.col - i + 1] == None: # This is to avoid jumping over more than one consecutive adv piece 
                    self.legal += [(self.row, self.col - i - 1)]
                    for j in range(1, self.col - i):
                        if board.chessboard[self.row][self.col - i - 1 - j] == None:
                            self.legal += [(self.row, self.col - i - 1 - j)]
                        else:
                            end = True
                            break
            if end:
                break # this is because after finding one piece to capture and the following free spots, the inner loop breaks and the outter loop
                      # keeps going and there might be another adv piece to capture but we are not suppose to care about that one so this break the outter loop
                    
    def drop_out_range(self):
        drop = []
        for i in range(len(self.legal)):
            if self.legal[i][0] < 0 or self.legal[i][0] > size - 1 or self.legal[i][1] < 0 or self.legal[i][1] > size - 1:
                drop.append(i)
        self.legal = [self.legal[i] for i in range(len(self.legal)) if i not in drop]