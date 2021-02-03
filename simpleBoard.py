board = [
    ['X', 'X', 'X', 'X', 'X', ' ', ' ', ' ', ' ', ' '], 
    ['X', 'X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
    ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O', 'O'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O', 'O', 'O'],
    [' ', ' ', ' ', ' ', ' ', ' ', 'O', 'O', 'O', 'O'],
    [' ', ' ', ' ', ' ', ' ', 'O', 'O', 'O', 'O', 'O']
]

opcion = 5
turn = True
col = 0
row = 0
colN = 0
rowN = 0

while opcion != 1:
    col = int(input("\n Ingrese la columna actual: ")) - 1
    row = int(input("\n Ingrese la fila actual: ")) - 1
    colN = int(input("\n Ingrese la columna a la que desea moverse: ")) - 1
    rowN = int(input("\n Ingrese la fila a la que desea moverse: ")) - 1
    board[row][col] = ' '
    if turn:
        board[rowN][colN] = 'X'
    else:
        board[rowN][colN] = 'O'
    for x in board:
        print(x)
    opcion = int(input("\n Desea salir? "))
    turn = not turn