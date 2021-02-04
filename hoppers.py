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
from tile import Tile


class Hopper_Player():

    def __init__(self, boardSize=10, timeLimit=60, chosenPlayer=Tile.P_RED):

        # Crear el tablero vacio
        board = [[None] * boardSize for _ in range(boardSize)]
        
        # Colocar las piezas de cada jugador
        for row in range(boardSize):
            for col in range(boardSize):
                if row + col < 5:
                    element = Tile(2, 2, row, col)
                elif 1 + row + col > 2 * (boardSize - 3):
                    element = Tile(1, 1, row, col)
                else:
                    element = Tile(0, 0, row, col)
                board[row][col] = element
        
        self.boardSize = boardSize
        self.timeLimit = timeLimit
        self.chosenPlayer = chosenPlayer
        self.board = board
        self.currentPlayer = Tile.P_GREEN
        self.selected_tile = None
        self.validMoves = []
        self.computing = False
        self.attempts = 0

        self.deepness = 3

        self.redTargets = [t for row in board
                        for t in row if t.tile == Tile.T_RED]
        self.greenTargets = [t for row in board
                        for t in row if t.tile == Tile.T_GREEN]

        if self.chosenPlayer == self.currentPlayer:
            self.execute_computer_move()

    def minimax(self, depth, player_to_max, max_time, a=float("-inf"),
                b=float("inf"), maxing=True, prunes=0, boards=0):

        # Bottomed out base case
        if depth == 0 or self.find_winner() or time.time() > max_time:
            return self.utility_distance(player_to_max), None, prunes, boards

        # Setup initial variables and find moves
        best_move = None
        if maxing:
            best_val = float("-inf")
            moves = self.get_next_moves(player_to_max)
        else:
            best_val = float("inf")
            moves = self.get_next_moves((Tile.P_RED
                    if player_to_max == Tile.P_GREEN else Tile.P_GREEN))
        # For each move
        for move in moves:
            #print(move)
            for to in move["to"]:
                #print(to)

                # Bail out when we're out of time
                if time.time() > max_time:
                    return best_val, best_move, prunes, boards

                # Move piece to the move outlined
                piece = move["from"].piece
                move["from"].piece = Tile.P_NONE
                to.piece = piece
                boards += 1

                # Recursively call self
                #se vuelve a llamar de acuerdo a la profundidad programada para poder ver la mejor jugada a largo plazo
                val, _, new_prunes, new_boards = self.minimax(depth - 1,
                    player_to_max, max_time, a, b, not maxing, prunes, boards)
                prunes = new_prunes
                boards = new_boards

                # Move the piece back
                to.piece = Tile.P_NONE
                move["from"].piece = piece

                if maxing and val > best_val:
                    best_val = val
                    """print("*************************")
                    print(to.loc)"""
                    best_move = (move["from"].loc, to.loc)
                    a = max(a, val)

                if not maxing and val < best_val:
                    best_val = val
                    best_move = (move["from"].loc, to.loc)
                    b = min(b, val)

                if b <= a:
                    return best_val, best_move, prunes + 1, boards

        return best_val, best_move, prunes, boards

    def execute_computer_move(self):
        #print(self.chosenPlayer, "chosenPlayer")

        # Print out search information
        current_turn = (self.attempts // 2) + 1
        print("Turn", current_turn, "Computation")
        print("=================" + ("=" * len(str(current_turn))))
        print("Executing search ...", end=" ")
        sys.stdout.flush()

        # self.board_view.set_status("Computing next move...")
        self.computing = True
        max_time = time.time() + self.timeLimit

        # Execute minimax search
        start = time.time()
        _, move, prunes, boards = self.minimax(self.deepness,
            self.chosenPlayer, max_time)
        end = time.time()

        # Print search result stats
        print("complete")
        print("Time to compute:", round(end - start, 4))
        print("Total boards generated:", boards)
        print("Total prune events:", prunes)

        # Move the resulting piece
        """MOVE ES EL MOVIMIENTO DE AI"""
        move_from = self.board[move[0][0]][move[0][1]]
        move_to = self.board[move[1][0]][move[1][1]]
        self.move_piece(move_from, move_to)

        winner = self.find_winner()
        if winner:
            print("El jugador " + ("azul"
                if winner == Tile.P_GREEN else "rojo") + " es el ganador")
            self.currentPlayer = None

            print("\nEstadisticas del juego")
            print("..........................")
            print("Ganador: ", "jugador azul"
                if winner == Tile.P_GREEN else "jugador rojo")
            print("Cantidad de jugadas: ", self.attempts)

        else:  # Toggle the current player
            self.currentPlayer = (Tile.P_RED
                if self.currentPlayer == Tile.P_GREEN else Tile.P_GREEN)

        self.computing = False
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

    def get_moves_at_tile(self, tile, player, moves=None, adj=True):

        if moves is None:
            moves = []

        row = tile.loc[0]
        col = tile.loc[1]

        # List of valid tile types to move to
        valid_tiles = [Tile.T_NONE, Tile.T_GREEN, Tile.T_RED]
        if tile.tile != player:
            #print("ya estas aqui men")
            valid_tiles.remove(player)  # Moving back into your own goal
        if tile.tile != Tile.T_NONE and tile.tile != player:
            #print("pa que te vassssss")
            valid_tiles.remove(Tile.T_NONE)  # Moving out of the enemy's goal

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
                
                if new_tile.tile not in valid_tiles: # para no poder regresar a mi área después de salir
                    """print("no es valid tiles")
                    print(valid_tiles)
                    print(new_tile.tile)"""
                    continue
                

                if new_tile.piece == Tile.P_NONE:
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
                if new_tile in moves or (new_tile.tile not in valid_tiles):
                    continue

                if new_tile.piece == Tile.P_NONE:
                    moves.insert(0, new_tile)  # Prioritize jumps
                    self.get_moves_at_tile(new_tile, player, moves, False)

        return moves

    def move_piece(self, from_tile, to_tile):

        # Handle trying to move a non-existant piece and moving into a piece
        if from_tile.piece == Tile.P_NONE or to_tile.piece != Tile.P_NONE:
            print("Movimiento inválido\n")
            return

        # Move piece
        to_tile.piece = from_tile.piece
        from_tile.piece = Tile.P_NONE


        self.attempts += 1

        print("Ficha movida de " + str(from_tile) +
            " a " + str(to_tile) + ", Turno del jugador " + ("azul" if
            self.currentPlayer == Tile.P_RED else "rojo"))

    def find_winner(self):

        if all(g.piece == Tile.P_GREEN for g in self.redTargets):
            return Tile.P_GREEN
        elif all(g.piece == Tile.P_RED for g in self.greenTargets):
            return Tile.P_RED
        else:
            return None

    
    def utility_distance(self, player):

        def point_distance(p0, p1):
            return math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2)

        value = 0

        for col in range(self.boardSize):
            for row in range(self.boardSize):

                tile = self.board[row][col]

                if tile.piece == Tile.P_GREEN:
                    distances = [point_distance(tile.loc, g.loc) for g in
                                 self.redTargets if g.piece != Tile.P_GREEN]
                    value -= max(distances) if len(distances) else -50

                elif tile.piece == Tile.P_RED:
                    distances = [point_distance(tile.loc, g.loc) for g in
                                 self.greenTargets if g.piece != Tile.P_RED]
                    value += max(distances) if len(distances) else -50

        if player == Tile.P_RED:
            value *= -1

        return value
    
    def execute_player_move(self):

        print("Turno del Jugador")
        
        row = int(input("Ingrese la fila de la ficha que desea mover: "))
        col = int(input("Ingrese la columna de la ficha que desea mover: "))

        new_tile = self.board[row][col]

        # If we are selecting a friendly piece
        if new_tile.piece == self.currentPlayer:

            
            # Outline the new and valid move tiles
            print("Selecciono la casilla: " + str(new_tile))
            self.validMoves = self.get_moves_at_tile(new_tile,
                self.currentPlayer)
            print("Posibles movimientos desde esa casilla: " + str(self.validMoves))

            # Update status and save the new tile
            self.selected_tile = new_tile

            row = int(input("Ingrese la fila de la casilla a la que se desea mover: "))
            col = int(input("Ingrese la columna de la casilla a la que se desea mover: "))
            new_tile = self.board[row][col]
       
        # If we already had a piece selected and we are moving a piece
            if self.selected_tile and new_tile in self.validMoves:
                
                self.move_piece(self.selected_tile, new_tile)  # Move the piece

                # Update status and reset tracking variables
                self.selected_tile = None
                self.validMoves = []
                self.currentPlayer = (Tile.P_RED
                    if self.currentPlayer == Tile.P_GREEN else Tile.P_GREEN)

                # If there is a winner to the game
                winner = self.find_winner()
                if winner:
                    print("El jugador " + ("azul"
                        if winner == Tile.P_GREEN else "rojo") + "es el ganador")
                    self.currentPlayer = None

                    print("\nEstadisticas del juego")
                    print("..........................")
                    print("Ganador: ", "jugador azul"
                        if winner == Tile.P_GREEN else "jugador rojo")
                    print("Cantidad de jugadas: ", self.attempts)

                elif self.chosenPlayer is not None:
                    self.execute_computer_move()
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
    hopper = Hopper_Player()
    while hopper.find_winner() == None:
        hopper.show_board()
        hopper.execute_player_move()
