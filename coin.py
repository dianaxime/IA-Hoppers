'''
************************************************

Diana Ximena de Leon Figueroa
Carne 18607
Inteligencia Artificial
01 de febrero de 2021

************************************************
'''

class Coin():

    # Constantes "OBJETIVO"
    BLANK_TARGET = 0
    BLUE_TARGET = 1
    RED_TARGET = 2

    # Constantes de las casillas
    BLANK_PIECE = 0 
    BLUE_PIECE = 1
    RED_PIECE = 2

    def __init__(self, coin=0, piece=0, row=0, col=0):
        self.coin = coin
        self.piece = piece
        self.row = row
        self.col = col
        self.position = (row, col)

    def __str__(self):
        return str(self.position)

    def __repr__(self):
        return str(self.position)
