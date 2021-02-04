'''
************************************************

Diana Ximena de Leon Figueroa
Carne 18607
Inteligencia Artificial
01 de febrero de 2021

************************************************
'''

# index 0 is tile type
#   0 = blank normal tile
#   1 = blank green goal tile
#   2 = blank red goal tile
#
# index 1 is piece type
#   0 = no piece
#   1 = green piece
#   2 = red piece

class Tile():

    # Goal constants
    BLANK_TARGET = 0
    BLUE_TARGET = 1
    RED_TARGET = 2

    # Piece constants
    BLANK_PIECE = 0
    BLUE_PIECE = 1
    RED_PIECE = 2

    def __init__(self, tile=0, piece=0, row=0, col=0):
        self.tile = tile
        self.piece = piece
        self.row = row
        self.col = col
        self.loc = (row, col)

    def __str__(self):
        return str(self.loc)

    def __repr__(self):
        return str(self.loc)
