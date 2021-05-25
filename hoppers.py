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
from xml.dom import minidom

# Importar el modulo de casilla adicional
from coin import Coin

BOARD_SIZE = 10
TIME_LIMIT = 60
DEEPNESS = 3

class HopperPlayer():

    def __init__(self, chosenPlayer=Coin.RED_PIECE):

        self.board = self.createBoard()
        self.currentPlayer = Coin.BLUE_PIECE
        self.chosenPlayer = chosenPlayer
        self.validMoves = []
        self.selectedCoin = None
        self.attempts = 0
        self.thinking = False
        self.redTargets = [coin for row in self.board
                        for coin in row if coin.coin == Coin.RED_TARGET]
        self.blueTargets = [coin for row in self.board
                        for coin in row if coin.coin == Coin.BLUE_TARGET]

        if self.chosenPlayer == self.currentPlayer:
            self.moveIA()
        self.path = []

    def createBoard(self):
        # Crear el tablero vacio
        board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        
        # Colocar las piezas de cada jugador
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if row + col < 5:
                    element = Coin(2, 2, row, col)
                elif 1 + row + col > 2 * (BOARD_SIZE - 3):
                    element = Coin(1, 1, row, col)
                else:
                    element = Coin(0, 0, row, col)
                board[row][col] = element

        return board

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
            for to in move[1]:
                
                # Terminar cuando se acabe el tiempo
                if time.time() > timeOut:
                    return greatValue, greatMove

                # Mueve la ficha a ese movimiento
                piece = move[0].piece
                move[0].piece = Coin.BLANK_PIECE
                to.piece = piece
                
                # Se vuelve a llamar a si misma para probar el movimiento
                val, _,  = self.minimax(depth - 1,
                    maxPlayer, timeOut, alpha, beta, not maxing)
                
                # Mueve la ficha de regreso
                to.piece = Coin.BLANK_PIECE
                move[0].piece = piece

                if maxing and val > greatValue:
                    greatValue = val
                    greatMove = (move[0].position, to.position)
                    alpha = max(alpha, val)

                if not maxing and val < greatValue:
                    greatValue = val
                    greatMove = (move[0].position, to.position)
                    beta = min(beta, val)

                if beta <= alpha:
                    return greatValue, greatMove

        return greatValue, greatMove

    def heuristicFunction(self, player):

        def calculateHeuristic(c, cG):
            # 1.67 por la masa del proton
            # 1.26 por la permeabilidad magnetica del vacio
            # return (((cG[0] - c[0]) + 1.67) * ((cG[1] - c[1]) + 1.26)) / ((math.e)**2)
            return math.sqrt((cG[0] - c[0]) ** 2 + (cG[1] - c[1]) ** 2)

        result = 0
        # Para todas las posiciones en el tablero calcula el valor 
        # que tan cercano o lejano se encuentra de su area objetivo

        for col in range(BOARD_SIZE):
            for row in range(BOARD_SIZE):

                coin = self.board[row][col]

                if coin.piece == Coin.BLUE_PIECE:
                    reach = list(map(lambda x: calculateHeuristic(coin.position, x.position) 
                            if x.piece != Coin.BLUE_PIECE else 0.0, 
                            self.redTargets))
                    result -= max(reach) if len(reach) else -706

                elif coin.piece == Coin.RED_PIECE:
                    reach = list(map(lambda x: calculateHeuristic(coin.position, x.position) 
                            if x.piece != Coin.RED_PIECE else 0.0, 
                            self.blueTargets))
                    result += max(reach) if len(reach) else -706
        
        if player == Coin.RED_PIECE:
            result *= -1

        return result

    def getNextMoves(self, player=1):
        moves = []
        for col in range(BOARD_SIZE):
            for row in range(BOARD_SIZE):

                currentCoin = self.board[row][col]

                # Descartar los movimientos del otro jugador
                if currentCoin.piece != player:
                    continue

                moves.append((currentCoin, self.getCoinMoves(currentCoin, player)))

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
                    rowN >= BOARD_SIZE or colN >= BOARD_SIZE):
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
                    rowN >= BOARD_SIZE or colN >= BOARD_SIZE):
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

        red = [coin.piece == Coin.BLUE_PIECE for coin in self.redTargets]
        blue = [coin.piece == Coin.RED_PIECE for coin in self.blueTargets]
        
        # Si algun jugador ya tiene todas sus fichas en su objetivo
        if all(red):
            return Coin.BLUE_PIECE
        elif all(blue):
            return Coin.RED_PIECE
        else:
            return None

    
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

    def moveIA(self):
        print("Turno de IA")
        print("Buscando...", end=" ")
        sys.stdout.flush()

        self.thinking = True
        timeOut = time.time() + TIME_LIMIT

        # Llamar a la función de minimax con alpha-beta pruning 
        _, move = self.minimax(DEEPNESS,
            self.chosenPlayer, timeOut)
        print("¡Completado!")
        
        # Realizar el movimiento devuelto por el algoritmo
        moveFrom = self.board[move[0][0]][move[0][1]]
        moveTo = self.board[move[1][0]][move[1][1]]
        self.path = self.getCoinMoves(moveFrom, self.chosenPlayer)
        self.moveCoin(moveFrom, moveTo)
        
        # Escribir XML 
        root = minidom.Document()
  
        xml = root.createElement('move') 
        root.appendChild(xml)
        
        fromChild = root.createElement('from')
        fromChild.setAttribute('row', str(move[0][0]))
        fromChild.setAttribute('col', str(move[0][1]))
        
        xml.appendChild(fromChild)

        toChild = root.createElement('to')
        toChild.setAttribute('row', str(move[1][0]))
        toChild.setAttribute('col', str(move[1][1]))
        
        xml.appendChild(toChild)

        pathChild = root.createElement('path')
        xml.appendChild(pathChild)

        for x in reversed(self.path):
            posChild = root.createElement('pos')
            posChild.setAttribute('row', str(x.position[0]))
            posChild.setAttribute('col', str(x.position[1]))
            pathChild.appendChild(posChild)
            if (x.position == moveTo.position):
                break
          
        xml_str = root.toprettyxml(indent ="\t") 

        print(xml_str)

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

            
if __name__ == "__main__":
    print("Vamos a jugar Hoppers")
    player = input("1. Rojo \n2. Azul \nSeleccione la ficha para el jugador Inteligente: ")
    if (player == "1"):
        hopper = HopperPlayer()
    else:
        hopper = HopperPlayer(chosenPlayer=Coin.BLUE_PIECE)

    while hopper.winnerIs() == None:
        hopper.showBoard()
        hopper.humanMove()
