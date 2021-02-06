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
            return self.heuristicFunction(maxPlayer), None

        # Iniciar las variables y encontrar los posibles movimientos
        greatMove = None
        if maxing:
            greatValue = float("-inf")
            moves = self.getNextMoves(maxPlayer)
        else:
            greatValue = float("inf")
            moves = self.getNextMoves((Coin.RED_PIECE
                    if maxPlayer == Coin.BLUE_PIECE else Coin.BLUE_PIECE))
        
        # Para cada movimiento encontrado
        for move in moves:
            for to in move["to"]:
                
                # Terminar cuando se acabe el tiempo
                if time.time() > timeOut:
                    return greatValue, greatMove

                # Mueve la ficha a ese movimiento
                piece = move["from"].piece
                move["from"].piece = Coin.BLANK_PIECE
                to.piece = piece
                
                # Se vuelve a llamar a si misma para probar el movimiento
                val, _,  = self.minimax(depth - 1,
                    maxPlayer, timeOut, alpha, beta, not maxing)
                
                # Mueve la ficha de regreso
                to.piece = Coin.BLANK_PIECE
                move["from"].piece = piece

                if maxing and val > greatValue:
                    greatValue = val
                    greatMove = (move["from"].position, to.position)
                    alpha = max(alpha, val)

                if not maxing and val < greatValue:
                    greatValue = val
                    greatMove = (move["from"].position, to.position)
                    beta = min(beta, val)

                if beta <= alpha:
                    return greatValue, greatMove

        return greatValue, greatMove

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
        self.moveCoin(moveFrom, moveTo)

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

    def getNextMoves(self, player=1):
        moves = []
        for col in range(self.boardSize):
            for row in range(self.boardSize):

                currentCoin = self.board[row][col]

                # Descartar los movimientos del otro jugador
                if currentCoin.piece != player:
                    continue

                move = {
                    "from": currentCoin,
                    "to": self.getCoinMoves(currentCoin, player)
                }
                moves.append(move)

        return moves

    def getCoinMoves(self, coin, player, moves=None, adj=True):

        if moves is None:
            moves = []

        row = coin.position[0]
        col = coin.position[1]

        # Posibles valores validos para moverse
        validOptions = [Coin.BLANK_TARGET, Coin.BLUE_TARGET, Coin.RED_TARGET]

        # Si se esta movimiendo a su propia casa
        if coin.coin != player:
            validOptions.remove(player)
        # Moviendose fuera de su objetivo
        if coin.coin != Coin.BLANK_TARGET and coin.coin != player:
            validOptions.remove(Coin.BLANK_TARGET)

        # Encontrar los posibles movimientos adyacentes
        for colD in range(-1, 2):
            for rowD in range(-1, 2):

                # Revisar cada casilla cercana
                rowN = row + rowD
                colN = col + colD

                # Revisar que este dentro del tablero
                if ((rowN == row and colN == col) or
                    rowN < 0 or colN < 0 or
                    rowN >= self.boardSize or colN >= self.boardSize):
                    continue

                # Revisar movimientro dentro/fuera del objetivo
                newCoin = self.board[rowN][colN]
                
                # No regresar a casa despues de salir
                if newCoin.coin not in validOptions:
                    continue
                
                # Ya reviso los cercanos, no los revise despues
                if newCoin.piece == Coin.BLANK_PIECE:
                    if adj: 
                        moves.append(newCoin)
                    continue

                # Ver si es posible saltar
                rowN = rowN + rowD
                colN = colN + colD

                # No revisar valores fuera del tablero
                if (rowN < 0 or colN < 0 or
                    rowN >= self.boardSize or colN >= self.boardSize):
                    continue

                # Verificar que no regrese o se salga del objetivo
                newCoin = self.board[rowN][colN]
                if newCoin in moves or (newCoin.coin not in validOptions):
                    continue

                # Importancia a saltar
                if newCoin.piece == Coin.BLANK_PIECE:
                    moves.insert(0, newCoin)
                    self.getCoinMoves(newCoin, player, moves, False)

        return moves

    def moveCoin(self, fromCoin, toCoin):

        # Si esta tratando de mover una casilla en blanco
        # o esta tratando de ocupar una casilla ocupada
        
        if fromCoin.piece == Coin.BLANK_PIECE or toCoin.piece != Coin.BLANK_PIECE:
            print("Movimiento inválido\n")
            return

        # Mover la ficha
        toCoin.piece = fromCoin.piece
        fromCoin.piece = Coin.BLANK_PIECE

        self.attempts += 1

        print("Ficha movida de " + str(fromCoin) +
            " a " + str(toCoin) + ", Turno del jugador " + ("azul" if
            self.currentPlayer == Coin.RED_PIECE else "rojo"))

    # Verifica si existe algun ganador
    def winnerIs(self):

        # Si algun jugador ya tiene todas sus fichas en su objetivo

        if all(g.piece == Coin.BLUE_PIECE for g in self.redTargets):
            return Coin.BLUE_PIECE
        elif all(g.piece == Coin.RED_PIECE for g in self.greenTargets):
            return Coin.RED_PIECE
        else:
            return None

    
    def heuristicFunction(self, player):

        def calculateHeuristic(p0, p1):
            return math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2)

        value = 0

        # Para todas las posiciones en el tablero calcula el valor 
        # que tan cercano o lejano se encuentra de su area objetivo

        for col in range(self.boardSize):
            for row in range(self.boardSize):

                coin = self.board[row][col]

                if coin.piece == Coin.BLUE_PIECE:
                    distances = [calculateHeuristic(coin.position, g.position) for g in
                                 self.redTargets if g.piece != Coin.BLUE_PIECE]
                    value -= max(distances) if len(distances) else -50

                elif coin.piece == Coin.RED_PIECE:
                    distances = [calculateHeuristic(coin.position, g.position) for g in
                                 self.greenTargets if g.piece != Coin.RED_PIECE]
                    value += max(distances) if len(distances) else -50

        if player == Coin.RED_PIECE:
            value *= -1

        return value
    
    def humanMove(self):

        print("Turno del Jugador")
        
        # Pedir las coordenadas de la ficha que desea mover
        row = int(input("Ingrese la fila de la ficha que desea mover: "))
        col = int(input("Ingrese la columna de la ficha que desea mover: "))

        newCoin = self.board[row][col]

        # Verificar que la ficha seleccionada sea del jugador
        if newCoin.piece == self.currentPlayer:

            print("Selecciono la casilla: " + str(newCoin))
            
            # Buscar los posibles movimientos de esa ficha
            self.validMoves = self.getCoinMoves(newCoin,
                self.currentPlayer)
            print("Posibles movimientos desde esa casilla: " + str(self.validMoves))
            self.selectedCoin = newCoin

            # Pedir las coordenadas de la ficha a la que desea moverse
            row = int(input("Ingrese la fila de la casilla a la que se desea mover: "))
            col = int(input("Ingrese la columna de la casilla a la que se desea mover: "))
            newCoin = self.board[row][col]
       
            # Si la casilla a la que desea moverse es valida
            if self.selectedCoin and newCoin in self.validMoves:
                
                # Entonces mueve la ficha
                self.moveCoin(self.selectedCoin, newCoin)

                # Actualiza el estado de las variables
                self.selectedCoin = None
                self.validMoves = []
                self.currentPlayer = (Coin.RED_PIECE
                    if self.currentPlayer == Coin.BLUE_PIECE else Coin.BLUE_PIECE)

                # Verificar si hay un ganador
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


    # Funcion para mostrar el estado actual del tablero  
    def showBoard(self):
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
        hopper.showBoard()
        hopper.humanMove()
