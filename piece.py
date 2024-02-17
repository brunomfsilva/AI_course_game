class Piece:

    def __init__(self, row, col, color, king = False):
        self.row = row
        self.col = col
        self.color = color
        self.king = king
    
    def move(self, row, col):
        self.row = row
        self.col = col