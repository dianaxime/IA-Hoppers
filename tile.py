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
#
# index 2 is the outline type
#   0 = no outline
#   1 = selected outline
#   2 = just moved


class Tile():

    # Goal constants
    T_NONE = 0
    T_GREEN = 1
    T_RED = 2

    # Piece constants
    P_NONE = 0
    P_GREEN = 1
    P_RED = 2

    # Outline constants
    O_NONE = 0
    O_SELECT = 1
    O_MOVED = 2

    def __init__(self, tile=0, piece=0, outline=0, row=0, col=0):
        self.tile = tile
        self.piece = piece
        self.outline = outline
        self.row = row
        self.col = col
        self.loc = (row, col)

    def __str__(self):
        return "(" + str(self.loc[1]) + "," + str(self.loc[0]) + ")"

    def __repr__(self):
        return "(" + str(self.loc[1]) + "," + str(self.loc[0]) + ")"
