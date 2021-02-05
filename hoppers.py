'''
************************************************

Diana Ximena de Leon Figueroa
Carne 18607
Inteligencia Artificial
01 de febrero de 2021

************************************************
'''

# Librerias utilizadas
import sys
import time
import math

# Importar el modulo de casilla adicional
from coin import Coin


class HopperPlayer():

    def __init__(self, boardSize=10, timeLimit=60, chosenPlayer=Coin.RED_PIECE):

        # Crear el tablero vacio
        board = [[None] * boardSize for _ in range(boardSize)]
        
        # Colocar las piezas de cada jugador
        for row in range(boardSize):
            for col in range(boardSize):
                if row + col < 5:
                    element = Coin(2, 2, row, col)
                elif 1 + row + col > 2 * (boardSize - 3):
                    element = Coin(1, 1, row, col)
                else:
                    element = Coin(0, 0, row, col)
                board[row][col] = element
        
        self.boardSize = boardSize
        self.timeLimit = timeLimit
        self.chosenPlayer = chosenPlayer
        self.board = board
        self.currentPlayer = Coin.BLUE_PIECE
        self.selectedCoin = None
        self.validMoves = []
        self.thinking = False
        self.attempts = 0
        self.deepness = 3

        self.redTargets = [t for row in board
                        for t in row if t.coin == Coin.RED_TARGET]
        self.greenTargets = [t for row in board
                        for t in row if t.coin == Coin.BLUE_TARGET]

        if self.chosenPlayer == self.currentPlayer:
            self.moveIA()

    def minimax(self, depth, maxPlayer, timeOut, alpha=float("-inf"),
                beta=float("inf"), maxing=True):

        # Si estamos en la base
        if depth == 0 or self.winnerIs() or time.time() > timeOut:
            return self.utility_distance(maxPlayer), None

        # Iniciar las variables y encontrar los posibles movimientos
        best_move = None
        if maxing:
            best_val = float("-inf")
            moves = self.get_next_moves(maxPlayer)
        else:
            best_val = float("inf")
            moves = self.get_next_moves((Coin.RED_PIECE
                    if maxPlayer == Coin.BLUE_PIECE else Coin.BLUE_PIECE))
        
        # For each move
        for move in moves:
            for to in move["to"]:
                
                # Bail out when we're out of time
                if time.time() > timeOut:
                    return best_val, best_move

                # Move piece to the move outlined
                piece = move["from"].piece
                move["from"].piece = Coin.BLANK_PIECE
                to.piece = piece
                
                # Recursively call self
                #se vuelve a llamar de acuerdo a la profundidad programada para poder ver la mejor jugada a largo plazo
                val, _,  = self.minimax(depth - 1,
                    maxPlayer, timeOut, alpha, beta, not maxing)
                
                # Move the piece back
                to.piece = Coin.BLANK_PIECE
                move["from"].piece = piece

                if maxing and val > best_val:
                    best_val = val
                    best_move = (move["from"].loc, to.loc)
                    alpha = max(alpha, val)

                if not maxing and val < best_val:
                    best_val = val
                    best_move = (move["from"].loc, to.loc)
                    beta = min(beta, val)

                if beta <= alpha:
                    return best_val, best_move

        return best_val, best_move

    def moveIA(self):
        print("Turno de IA")
        print("Buscando...", end=" ")
        sys.stdout.flush()

        self.thinking = True
        timeOut = time.time() + self.timeLimit

        # Llamar a la función de minimax con alpha-beta pruning 
        _, move = self.minimax(self.deepness,
            self.chosenPlayer, timeOut)
        print("¡Completado!")

        # Realizar el movimiento devuelto por el algoritmo
        moveFrom = self.board[move[0][0]][move[0][1]]
        moveTo = self.board[move[1][0]][move[1][1]]
        self.move_piece(moveFrom, moveTo)

        winner = self.winnerIs()
        if winner:
            print("El jugador " + ("azul"
                if winner == Coin.BLUE_PIECE else "rojo") + " es el ganador")
            self.currentPlayer = None

            print("\nEstadisticas del juego")
            print("..........................")
            print("Ganador: ", "jugador azul"
                if winner == Coin.BLUE_PIECE else "jugador rojo")
            print("Cantidad de jugadas: ", self.attempts)

        else:  # Darle el turno al otro jugador
            self.currentPlayer = (Coin.RED_PIECE
                if self.currentPlayer == Coin.BLUE_PIECE else Coin.BLUE_PIECE)

        self.thinking = False
        print()

    def get_next_moves(self, player=1):

        moves = []  # All possible moves
        for col in range(self.boardSize):
            for row in range(self.boardSize):

                curr_tile = self.board[row][col]

                # Skip board elements that are not the current player
                if curr_tile.piece != player:
                    continue

                move = {
                    "from": curr_tile,
                    "to": self.get_moves_at_tile(curr_tile, player)
                }
                moves.append(move)

        return moves

    def get_moves_at_tile(self, coin, player, moves=None, adj=True):

        if moves is None:
            moves = []

        row = coin.loc[0]
        col = coin.loc[1]

        # List of valid coin types to move to
        valid_tiles = [Coin.BLANK_TARGET, Coin.BLUE_TARGET, Coin.RED_TARGET]
        if coin.coin != player:
            #print("ya estas aqui men")
            valid_tiles.remove(player)  # Moving back into your own goal
        if coin.coin != Coin.BLANK_TARGET and coin.coin != player:
            #print("pa que te vassssss")
            valid_tiles.remove(Coin.BLANK_TARGET)  # Moving out of the enemy's goal

        # Find and save immediately adjacent moves
        for col_delta in range(-1, 2):
            for row_delta in range(-1, 2):

                # Check adjacent tiles

                new_row = row + row_delta
                new_col = col + col_delta

                # Skip checking degenerate values
                #para revisar que no me estoy saliendo del tablero
                if ((new_row == row and new_col == col) or
                    new_row < 0 or new_col < 0 or
                    new_row >= self.boardSize or new_col >= self.boardSize):
                    continue

                # Handle moves out of/in to goals
                new_tile = self.board[new_row][new_col]
                
                if new_tile.coin not in valid_tiles: # para no poder regresar a mi área después de salir
                    continue
                

                if new_tile.piece == Coin.BLANK_PIECE:
                    if adj:  # Don't consider adjacent on subsequent calls 
                    #si hay un movimiento para seguirle dando
                        moves.append(new_tile)
                    continue

                # Check jump tiles

                new_row = new_row + row_delta
                new_col = new_col + col_delta

                # Skip checking degenerate values
                if (new_row < 0 or new_col < 0 or
                    new_row >= self.boardSize or new_col >= self.boardSize):
                    continue

                # Handle returning moves and moves out of/in to goals
                new_tile = self.board[new_row][new_col] #para no poder regresar a mi área 
                if new_tile in moves or (new_tile.coin not in valid_tiles):
                    continue

                if new_tile.piece == Coin.BLANK_PIECE:
                    moves.insert(0, new_tile)  # Prioritize jumps
                    self.get_moves_at_tile(new_tile, player, moves, False)

        return moves

    def move_piece(self, from_tile, to_tile):

        # Handle trying to move a non-existant piece and moving into a piece
        if from_tile.piece == Coin.BLANK_PIECE or to_tile.piece != Coin.BLANK_PIECE:
            print("Movimiento inválido\n")
            return

        # Move piece
        to_tile.piece = from_tile.piece
        from_tile.piece = Coin.BLANK_PIECE

        self.attempts += 1

        print("Ficha movida de " + str(from_tile) +
            " a " + str(to_tile) + ", Turno del jugador " + ("azul" if
            self.currentPlayer == Coin.RED_PIECE else "rojo"))

    def winnerIs(self):

        if all(g.piece == Coin.BLUE_PIECE for g in self.redTargets):
            return Coin.BLUE_PIECE
        elif all(g.piece == Coin.RED_PIECE for g in self.greenTargets):
            return Coin.RED_PIECE
        else:
            return None

    
    def utility_distance(self, player):

        def point_distance(p0, p1):
            return math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2)

        value = 0

        for col in range(self.boardSize):
            for row in range(self.boardSize):

                coin = self.board[row][col]

                if coin.piece == Coin.BLUE_PIECE:
                    distances = [point_distance(coin.loc, g.loc) for g in
                                 self.redTargets if g.piece != Coin.BLUE_PIECE]
                    value -= max(distances) if len(distances) else -50

                elif coin.piece == Coin.RED_PIECE:
                    distances = [point_distance(coin.loc, g.loc) for g in
                                 self.greenTargets if g.piece != Coin.RED_PIECE]
                    value += max(distances) if len(distances) else -50

        if player == Coin.RED_PIECE:
            value *= -1

        return value
    
    def moveHuman(self):

        print("Turno del Jugador")
        
        # Pedir las coordenadas de la ficha que desea mover
        row = int(input("Ingrese la fila de la ficha que desea mover: "))
        col = int(input("Ingrese la columna de la ficha que desea mover: "))

        new_tile = self.board[row][col]

        # Verificar que la ficha seleccionada sea del jugador
        if new_tile.piece == self.currentPlayer:

            print("Selecciono la casilla: " + str(new_tile))
            
            # Buscar los posibles movimientos de esa ficha
            self.validMoves = self.get_moves_at_tile(new_tile,
                self.currentPlayer)
            print("Posibles movimientos desde esa casilla: " + str(self.validMoves))
            self.selectedCoin = new_tile

            # Pedir las coordenadas de la ficha a la que desea moverse
            row = int(input("Ingrese la fila de la casilla a la que se desea mover: "))
            col = int(input("Ingrese la columna de la casilla a la que se desea mover: "))
            new_tile = self.board[row][col]
       
            # Si la casilla a la que desea moverse es valida
            if self.selectedCoin and new_tile in self.validMoves:
                
                # Entonces mueve la ficha
                self.move_piece(self.selectedCoin, new_tile)

                # Update status and reset tracking variables
                self.selectedCoin = None
                self.validMoves = []
                self.currentPlayer = (Coin.RED_PIECE
                    if self.currentPlayer == Coin.BLUE_PIECE else Coin.BLUE_PIECE)

                # If there is a winner to the game
                winner = self.winnerIs()
                if winner:
                    print("El jugador " + ("azul"
                        if winner == Coin.BLUE_PIECE else "rojo") + "es el ganador")
                    self.currentPlayer = None

                    print("\nEstadisticas del juego")
                    print("..........................")
                    print("Ganador: ", "jugador azul"
                        if winner == Coin.BLUE_PIECE else "jugador rojo")
                    print("Cantidad de jugadas: ", self.attempts)

                elif self.chosenPlayer is not None:
                    self.moveIA()
            else:
                print("Movimiento inválido\n")
        else:
            print("Movimiento inválido\n")


        
    def show_board(self):
        print(" ", end=" ")
        for x in range(10):
            print("| ", x, end=" ")
        print("\n_____________________________________________________\n")
        a = 0
        for i in hopper.board:
            print(a, end=" ")
            a += 1
            for j in i:
                print("| ", j.piece, end=" ")
            print()
        print("_____________________________________________________")

            

        


if __name__ == "__main__":
    hopper = HopperPlayer()
    while hopper.winnerIs() == None:
        hopper.show_board()
        hopper.moveHuman()
