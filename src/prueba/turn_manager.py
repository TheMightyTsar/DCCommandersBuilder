from itertools import cycle
from os import listdir, path
import importlib.util


from src.prueba.base_classes import Acciones, BaseTroop, Troops as T
import random
from colorama import Fore, Style
from src.prueba.dicts import COORD_TO_TUPLE, AVAILABLE_TROOPS
from src.prueba.parametros import ATACK, BAJAS, DETECT, MOV_SUCCESS

validPOS = ['A0', 'B0', 'C0', 'D0', 'E0', 'F0', 'G0', 'H0', 'I0', 'J0',
            'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1',
            'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2',
            'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3', 'J3',
            'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4', 'J4',
            'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5', 'J5',
            'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6', 'J6',
            'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7', 'J7',
            'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8', 'J8',
            'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9', 'J9']

class TurnManager:
    def __init__(self, commanders) -> None:
        print("-" * 40)
        print("Comienza la prueba de los comandantes")
        print("-" * 40)
        self.player_1 = commanders[0].Commander()
        self.player_2 = commanders[0].Commander()
        self.players = [self.player_1, self.player_2]

        self.troops = {}

        self.reportes = {
            self.player_1: {ATACK: [], DETECT: [], BAJAS: [], MOV_SUCCESS: None},
            self.player_2: {ATACK: [], DETECT: [], BAJAS: [], MOV_SUCCESS: None},
        }

        for player in self.players:
            try:
                print(f" {player.name} esta montando su tablero\n")
                self.troops[player.name] = player.montar_tropas()
            except Exception as e:
                print(f"Commander {player.name} tuvo un error montando el tablero: {e}")

            print(f" Verificando tablero de {player.name} \n")
            print(self.verifyTablero(self.troops[player.name]))
            print("-"*40)
            print("-" * 40)

        self.turno = 1
        self.muertos = {}
        self.ids_bajas_turno = []
        self.ids_detectados_turno = []
        self.pos_bajas = []
        self.posiciones_detectadas = []
        self.exception_counter = {
            self.player_1: 0,
            self.player_2: 0,
        }

    def verifyTablero(self, tropas):
        message = '| Verificacion al Montar Tablero |\n'
        if isinstance(tropas, list):
            message += 'Lista de Tropas: TRUE \n'
            listaDeListas = True
            listID = []
            listPOS = []
            numSoldier = 0
            numGauss = 0
            numTower = 0
            numScout = 0
            numGrenadier = 0
            if len(tropas) == 13:

                for unit in tropas:
                    if isinstance(tropas, list):
                    # contar cantida de unidades
                        pass
                    else:
                        listaDeListas = False
            else:
                message += 'ERROR: faltan tropas en el tablero \n'
        else:
            message += 'ERROR: montar_tropas no devuelve una lista \n'



        return message

    def run(self):
        for player in cycle(self.players):
            if self.turno == 1000:
                return self.find_timeout_winner()
            enemy = None
            reporte = self.reportes[player]
            reporte_enemigo = self.turn_into_enemy_report(
                enemy, self.ids_detectados_turno
            )
            try:
                accion = player.admin_troops(reporte, reporte_enemigo)
                self.reset_turn(player)
                self.exception_counter[player] = 0
            except Exception as e:
                if self.handle_exception(player, enemy, e):
                    return self.win(enemy)
                continue

            if not self.validate_action(accion, player):
                print(f"Player {player} sent an invalid action, skipping turn")
                self.turno += 1
                continue

            acc, _id, pos = accion["action"], accion["id"], accion["pos"]
            tropa = self.troops[player][_id]
            match acc:
                case Acciones.ATACAR.value:
                    self.handle_attack(tropa, reporte, enemy, pos)
                case Acciones.MOVER.value:
                    self.handle_movement(tropa, reporte, player, pos)
                case _:
                    pass
            self.print_game(player, self.pos_bajas, self.posiciones_detectadas)
            if self.game_finished(enemy):
                self.win(player)
                break
            self.turno += 1

    def reset_turn(self, player):
        self.ids_bajas_turno = []
        self.ids_detectados_turno = []
        self.pos_bajas = []
        self.posiciones_detectadas = []
        self.clear_report(player)

    def validate_action(self, action: dict, player) -> bool:
        """
        Validates a action sent by the player
        """
        if not isinstance(action, dict):
            return False

        acc, _id, pos = action["action"], action["id"], action["pos"]
        if acc not in (e.value for e in Acciones):
            return False
        if _id not in self.troops[player].keys():
            return False
        if not isinstance(pos, str) or pos not in COORD_TO_TUPLE.keys():
            return False
        return True

    def clear_report(self, player):
        """
        Clears a report at the end of the turn
        """
        self.reportes[player][ATACK] = []
        self.reportes[player][DETECT] = []
        self.reportes[player][MOV_SUCCESS] = None

    def game_finished(self, enemy) -> bool:
        """
        Returns true if the game is finished
        """
        return not self.troops[enemy]
    
    def find_timeout_winner(self):
        """
        Finds the winner in case of timeout
        """
        if len(self.troops[self.player_1]) > len(self.troops[self.player_2]):
            return self.win(self.player_1)
        elif len(self.troops[self.player_1]) < len(self.troops[self.player_2]):
            return self.win(self.player_2)
        return self.win(random.choice(self.players))

    def win(self, player):
        """
        Prints the winner
        """
        print(f"Player {player} wins!")

    def turn_into_enemy_report(
        self, player, ids_detectados: list[int]
    ) -> dict[str, list]:
        """
        Turns a player report into an enemy report
        """
        reporte = self.reportes[player].copy()
        del reporte[MOV_SUCCESS]
        reporte[BAJAS] = self.get_troop_types(player)
        reporte[DETECT] = ids_detectados
        return reporte
    
    def handle_exception(self, player, enemy, e) -> bool:
        print(f"Player {player} raised an exception: {e}")
        self.reset_turn(player)
        self.exception_counter[player] += 1
        if self.exception_counter[player] == 10:
            print(f"Player {player} raised 10 exceptions in a row")
            return True
        return False
    
    
    def handle_attack(self, tropa: BaseTroop, reporte: dict, enemy, pos: str) -> None:
        if tropa.type == T.SCOUTER.value:
            self.posiciones_detectadas = tropa.attack(pos)
            (
                self.ids_bajas_turno,
                self.pos_bajas,
                pos_detectados,
                self.ids_detectados_turno,
            ) = self.scout(enemy, pos, self.posiciones_detectadas)
            reporte[ATACK] = [pos]
            reporte[DETECT] = pos_detectados
        else:
            posiciones = tropa.attack(pos)
            self.ids_bajas_turno, self.pos_bajas = self.attack(
                enemy, posiciones
            )
            reporte[ATACK] = posiciones
        self.reportes[enemy][BAJAS].extend(self.ids_bajas_turno)

    def attack(self, enemy, posiciones: list[str]) -> tuple[list[int], list[str]]:
        """
        Performs the attack and returns the list of eliminated troop types and its ids
        """
        ids = []
        pos_bajas = []
        for pos in posiciones:
            for id, troop in self.troops[enemy].items():
                if troop.pos == pos:
                    ids.append(id)
                    pos_bajas.append(pos)
                    self.muertos[id] = self.troops[enemy].pop(id)
                    break
        return ids, pos_bajas

    def scout(
        self, enemy, pos: str, posiciones_detectadas: list[str]
    ) -> tuple[list[int], list[str], list[str], list[int]]:
        """
        Performs the scout action and returns the list of eliminated and detected troop types and ids
        """
        ids_bajas, posiciones = self.attack(enemy, [pos])
        pos_detectados = []
        ids_detectados = []
        for pos in posiciones_detectadas:
            for id, troop in self.troops[enemy].items():
                if troop.pos == pos:
                    pos_detectados.append(pos)
                    ids_detectados.append(id)
                    break
        return ids_bajas, posiciones, pos_detectados, ids_detectados
    
    def handle_movement(self, tropa: BaseTroop, reporte: dict, player, pos: str):
        can_move = tropa.move(pos)
        if can_move and self.pos_is_empty(player, pos):
            self.move(tropa, pos)
        reporte[MOV_SUCCESS] = can_move

    def move(self, tropa: BaseTroop, pos):
        """
        Moves the troop
        """
        tropa.pos = pos

    def pos_is_empty(self, player, pos: str) -> bool:
        """
        Returns true if the position is empty
        """
        for troop in self.troops[player].values():
            if troop.pos == pos:
                return False
        return True

    def get_troop_types(self, player):
        return [self.muertos[id].type for id in self.reportes[player][BAJAS].copy()]

    def print_game(
        self, current_player, pos_bajas: list[str], posiciones_detectadas: list[str]
    ):
        """
        Prints the game
        """
        print(
            f"\n---------------------- Turno {self.turno} ---------------------------\n"
        )
        reporte = self.reportes[current_player]
        ataques = reporte[ATACK]
        boards = []
        for i, player in enumerate(self.players, 1):
            board = [["." for _ in range(10)] for _ in range(10)]
            for tropa in self.troops[player].values():
                pos = COORD_TO_TUPLE[tropa.pos]
                board[pos[0]][pos[1]] = tropa.type[0]
            if current_player != player:
                for ataque in ataques:
                    pos = COORD_TO_TUPLE[ataque]
                    board[pos[0]][pos[1]] = f"{Fore.YELLOW}X{Style.RESET_ALL}"
                for pos in pos_bajas:
                    pos = COORD_TO_TUPLE[pos]
                    board[pos[0]][pos[1]] = f"{Fore.RED}X{Style.RESET_ALL}"
                for pos in posiciones_detectadas:
                    pos = COORD_TO_TUPLE[pos]
                    objeto = board[pos[0]][pos[1]]
                    if objeto == ".":
                        board[pos[0]][pos[1]] = f"{Fore.CYAN}X{Style.RESET_ALL}"
                    else:
                        board[pos[0]][pos[1]] = f"{Fore.BLUE}{objeto}{Style.RESET_ALL}"
            boards.append(board)
        x_axis = [chr(i) for i in range(ord("A"), ord("K"))]
        y_axis = [str(i) for i in range(10)]
        print("  " + " ".join(x_axis) + "   " + " ".join(x_axis))
        for i, rows in enumerate(zip(*boards)):
            row1, row2 = rows
            print(y_axis[i] + " " + " ".join(row1) + "   " + " ".join(row2))
        print("      Player 1                Player 2")
        print()
        self.print_summary()

    def print_summary(self):
        for i, player in enumerate(self.players, 1):
            print(f"Bajas player {i}:")
            for bajas in self.get_troop_types(player):
                print(f" - {bajas}")


if __name__ == "__main__":
    tm = TurnManager()
