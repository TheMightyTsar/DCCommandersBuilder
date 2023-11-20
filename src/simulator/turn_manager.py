# pylint: disable=missing-docstring, W0718, W0719

import random
from itertools import cycle
from traceback import print_exception

import colorama

# from icecream import ic
import src.simulator.server_troops as troops
from src.base_files.base_classes import Movement, Report
from src.base_files.parametros import (
    ACCIONES,
    ATACAR,
    AVAILABLE_TROOPS,
    CANTIDAD_TOTAL_TROPAS,
    COORD_TO_TUPLE,
    GAUSS,
    HIMARS,
    MOVER,
    SCOUT,
    SOLDIER,
    TOWER,
)

GRN = colorama.Style.BRIGHT + colorama.Fore.GREEN  # ? MOVE
RED = colorama.Style.BRIGHT + colorama.Fore.RED  # ? HIT
YEL = colorama.Style.BRIGHT + colorama.Fore.YELLOW  # ? MISS
CYA = colorama.Style.BRIGHT + colorama.Fore.CYAN  # ? DETECT HIT
BLU = colorama.Style.BRIGHT + colorama.Fore.BLUE  # ? DETECT MISS
BLD = colorama.Style.BRIGHT
RST = colorama.Style.RESET_ALL


class PlayerBuildException(Exception):
    pass


class InvalidActionException(Exception):
    pass


class TurnManager:
    def __init__(self, commanders, iterations) -> None:
        # ? print("-" * 40)
        # ? print("Comienza la prueba de los comandantes")
        # ? print("-" * 40)
        self.player_1 = commanders[0].Commander()
        self.player_2 = commanders[1].Commander()
        self.players = [self.player_1, self.player_2]

        self.winner: str | None = None
        self.prints: bool = False if iterations != 1 else True

        self.troops = {}

        self.reportes = {
            self.player_1.nombre: Report(),
            self.player_2.nombre: Report(),
        }

        self.turno = 1
        self.muertos = {self.player_1.nombre: {}, self.player_2.nombre: {}}
        self.ids_detectados_turno = []
        self.pos_bajas = []
        self.movimiento: tuple[int, str]
        self.posiciones_detectadas = []
        self.exception_counter = {
            self.player_1.nombre: 0,
            self.player_2.nombre: 0,
        }
        self.por_turno: bool = False
        self.exception_break: bool = False
        self.invalid_action_break: bool = False

    def start(self):
        for player in self.players:
            try:
                # print(f" {player.name} esta montando su tablero\n")
                self.build_player(player)
            except PlayerBuildException as e:
                print(
                    f"Commander {player.nombre} tuvo un error montando el tablero: {e}"
                )
                return self.win(self.get_enemy(player))
            except Exception as e:
                print(f"Commander {player.nombre} tuvo un error montando el tablero")
                print_exception(e)
                return self.win(self.get_enemy(player))
            if self.prints:
                print()

            # ? print(f" Verificando tablero de {player.name} \n")
            # ? print(self.verifyTablero(self.troops[player.name]))
            # ? print("-"*40)
            # ? print("-" * 40)

        if self.prints:
            self.menu_modo_juego()
        else:
            self.run()

    def get_enemy(self, player):
        """
        Returns the enemy of a player
        """
        return self.player_2 if player == self.player_1 else self.player_1

    def build_player(self, player):
        troops_dict = {}

        max_quantities = AVAILABLE_TROOPS.copy()

        player_troops = player.montar_tropas()

        if not isinstance(player_troops, list):
            raise PlayerBuildException(
                "Formato inválido, no retorno una lista con las tropas"
            )
        if len(player_troops) != CANTIDAD_TOTAL_TROPAS:
            raise PlayerBuildException(
                f"Cantidad de tropas inválida, se esperaban {CANTIDAD_TOTAL_TROPAS} y se recibieron {len(player_troops)}"
            )
        for troop in player_troops:
            if len(troop) != 3:
                raise PlayerBuildException(
                    f"Tropa con un formato inválido, {troop} debe tener la forma [id, tipo, pos]"
                )
            _id, tipo, pos = troop
            if not isinstance(_id, int):
                raise PlayerBuildException(
                    f"Id inválida, la id {_id} de tipo {type(_id)} debe ser un int"
                )
            if not isinstance(tipo, str) or tipo not in AVAILABLE_TROOPS.keys():
                raise PlayerBuildException(
                    f"Tipo de tropa inválido, el tipo {tipo} debe ser un string y estar en {AVAILABLE_TROOPS.keys()}"
                )
            if not isinstance(pos, str) or pos not in COORD_TO_TUPLE.keys():
                raise PlayerBuildException(
                    f"Posición inválida, la posición {pos} de tipo {type(pos)} debe ser un str y estar en el tablero"
                )

        for _id, tipo, pos in player_troops:
            if tipo == SOLDIER:
                troops_dict[_id] = troops.Soldier(_id, pos)
            elif tipo == GAUSS:
                troops_dict[_id] = troops.Gauss(_id, pos)
            elif tipo == SCOUT:
                troops_dict[_id] = troops.Scout(_id, pos)
            elif tipo == TOWER:
                troops_dict[_id] = troops.Tower(_id, pos)
            elif tipo == HIMARS:
                troops_dict[_id] = troops.Himars(_id, pos)
            max_quantities[tipo] -= 1

        # ? for troop in troops_dict.values():
        # ?     print(f" - {troop}")

        ids = [troop.id for troop in troops_dict.values()]
        if len(ids) != len(set(ids)):
            raise PlayerBuildException(f"Ids inválidas, hay tropas con ids repetidas")
        positions = [troop.pos for troop in troops_dict.values()]
        if len(positions) != len(set(positions)):
            raise PlayerBuildException(
                f"Posiciones inválidas, hay tropas en posiciones repetidas"
            )
        if any((quantity < 0 for quantity in max_quantities.values())):
            raise PlayerBuildException(
                f"Cantidad de tropas inválida, hay tropas de un tipo que exceden el máximo permitido"
            )

        self.troops[player.nombre] = troops_dict

    def menu_modo_juego(self):
        """
        Prints the menu
        """
        print(f"\n{BLD}Seleccione una opción {RST}")
        print("1. Jugar corrido")
        print("2. Jugar por turno")
        print("3. Frenar en excepciones")
        print("4. Frenar en acciones inválidas")
        opcion = input(f"\n{BLD}Ingrese una opción: {RST}")
        if opcion == "1":
            self.run()
        elif opcion == "2":
            self.por_turno = True
            self.run()
        elif opcion == "3":
            self.exception_break = True
            self.run()
        elif opcion == "4":
            self.invalid_action_break = True
            self.run()
        else:
            print("\nOpción inválida")
            self.menu_modo_juego()

    def run(self):
        for player in cycle(self.players):
            if self.prints:
                print(
                    f"{BLD}\n------------------ Turno {self.turno} ------------------\n{RST}"
                )
            if self.turno == 1000:
                return self.find_timeout_winner()
            enemy = self.get_enemy(player)
            reporte = self.reportes[player.nombre]
            reporte_enemigo = self.turn_into_enemy_report(
                enemy, self.ids_detectados_turno
            )
            try:
                accion = player.jugar_turno(reporte, reporte_enemigo)
                self.reset_turn(player)
                self.exception_counter[player.nombre] = 0
            except Exception as e:
                if self.prints:
                    print(f"El jugador {player} levantó una excepción en su codigo:")
                    print_exception(e)
                if self.exception_break:
                    break
                if self.handle_exception(player):
                    return self.win(enemy)
                self.pasar_turno()
                continue

            try:
                self.validate_action(accion, player)
            except InvalidActionException as e:
                if self.prints:
                    print(f"EL jugador {player} mandó una acción inválida: {e}")
                if self.invalid_action_break:
                    break
                self.pasar_turno()
                continue

            accion = self.convertir_accion(accion)

            acc, _id, pos = accion["action"], accion["id"], accion["pos"]
            tropa = self.troops[player.nombre][_id]
            if acc == ATACAR:
                self.handle_attack(tropa, reporte, player, enemy, pos)
            elif acc == MOVER:
                self.handle_movement(tropa, reporte, player, pos)
            if self.prints:
                self.print_game(player)
            if self.game_finished(enemy):
                self.win(player)
                break
            self.pasar_turno()
            if self.por_turno:
                input(f"\n{BLD}Presione enter para continuar{RST}")

    def pasar_turno(self):
        self.turno += 1

    def convertir_accion(self, accion: list) -> dict:
        _id, action, pos = accion
        return {"id": _id, "action": action, "pos": pos}

    def reset_turn(self, player):
        self.ids_detectados_turno = []
        self.pos_bajas = []
        self.posiciones_detectadas = []
        self.clear_report(player)

    def validate_action(self, action: list, player):
        """
        Validates a action sent by the player
        """
        if not isinstance(action, list):
            raise InvalidActionException(
                f"Formato de acción inválido, la acción {action} de tipo {type(action)} debe ser una lista"
            )
        if len(action) != 3:
            raise InvalidActionException(
                f"Formato de acción inválido, la acción {action} debe tener 3 elementos [id, acción, pos]"
            )
        _id, acc, pos = action
        if acc not in ACCIONES:
            raise InvalidActionException(
                f"Tipo de acción inválida, la acción {acc} debe ser {MOVER} o {ATACAR}"
            )
        if _id not in self.troops[player.nombre].keys():
            raise InvalidActionException(
                f"Id de tropa inválida, la id {_id} no está viva o no existe"
            )
        if not isinstance(pos, str) or pos not in COORD_TO_TUPLE.keys():
            raise InvalidActionException(
                f"Posición inválida, la posición {pos} de tipo {type(pos)} debe ser un str y estar en el tablero"
            )
        tropa = self.troops[player.nombre][_id]
        if acc == ATACAR and tropa.type == GAUSS:
            fila = COORD_TO_TUPLE[tropa.pos][0]
            fila_ataque = COORD_TO_TUPLE[pos][0]
            if fila != fila_ataque:
                raise InvalidActionException(
                    f"La tropa Gauss solo puede atacar en la misma fila"
                )
        elif acc == MOVER:
            can_move = tropa.move(pos)
            if not can_move:
                self.reportes[player.nombre].movimiento = Movement(False, tropa.id, pos)
                raise InvalidActionException(
                    f"Movimiento inválido, la tropa de id {tropa.id} y tipo {tropa.type} no puede moverse a la posición {pos}"
                )
            if not self.pos_is_empty(player, pos):
                self.reportes[player.nombre].movimiento = Movement(False, tropa.id, pos)
                raise InvalidActionException(
                    f"Movimiento inválido, la posición {pos} está ocupada"
                )

    def clear_report(self, player):
        """
        Clears a report at the end of the turn
        """
        self.reportes[player.nombre].ataques = []
        self.reportes[player.nombre].detecciones = []
        self.reportes[player.nombre].movimiento = None

    def game_finished(self, enemy) -> bool:
        """
        Returns true if the game is finished
        """
        return not self.troops[enemy.nombre]

    def find_timeout_winner(self):
        """
        Finds the winner in case of timeout
        """
        if len(self.troops[self.player_1.nombre]) > len(
            self.troops[self.player_2.nombre]
        ):
            return self.win(self.player_1)
        elif len(self.troops[self.player_1.nombre]) < len(
            self.troops[self.player_2.nombre]
        ):
            return self.win(self.player_2)
        return self.win(random.choice(self.players))

    def win(self, player):
        """
        Prints the winner
        """
        self.winner = player.nombre
        if self.prints:
            print(f"El comandante {player.nombre} ganó!")

    def turn_into_enemy_report(self, player, ids_detectados: list[int]) -> Report:
        """
        Turns a player report into an enemy report
        """
        reporte = self.reportes[player.nombre]
        new_reporte = Report(ataques=reporte.ataques)
        new_reporte.eliminaciones = list(
            self.muertos[self.get_enemy(player).nombre].keys()
        )
        new_reporte.detecciones = ids_detectados
        return new_reporte

    def handle_exception(self, player) -> bool:
        self.reset_turn(player)
        self.exception_counter[player.nombre] += 1
        if self.exception_counter[player.nombre] == 10:
            print(f"El jugador {player} levantó 10 excepciones seguidas")
            return True
        return False

    def handle_attack(
        self,
        tropa: troops.BaseTroop,
        reporte: Report,
        player,
        enemy,
        pos: str,
    ) -> None:
        if tropa.type == SCOUT:
            self.posiciones_detectadas = tropa.attack(pos)
            (
                self.pos_bajas,
                pos_detectados,
                self.ids_detectados_turno,
            ) = self.scout(enemy, pos, self.posiciones_detectadas)
            reporte.ataques = [pos]
            reporte.detecciones = pos_detectados
        else:
            posiciones = tropa.attack(pos)
            self.pos_bajas = self.attack(enemy, posiciones)
            reporte.ataques = posiciones
        self.reportes[player.nombre].eliminaciones = [
            tropa.type for tropa in self.muertos[enemy.nombre].values()
        ]

    def attack(self, enemy, posiciones: list[str]) -> list[str]:
        """
        Performs the attack and returns the list of eliminated troop types and its ids
        """
        pos_bajas = []
        for pos in posiciones:
            for id, troop in self.troops[enemy.nombre].items():
                if troop.pos == pos:
                    pos_bajas.append(pos)
                    self.muertos[enemy.nombre][id] = self.troops[enemy.nombre].pop(id)
                    break
        return pos_bajas

    def scout(
        self, enemy, pos: str, posiciones_detectadas: list[str]
    ) -> tuple[list[str], list[str], list[int]]:
        """
        Performs the scout action and returns the list of eliminated and detected troop types and ids
        """
        posiciones = self.attack(enemy, [pos])
        pos_detectados = []
        ids_detectados = []
        for pos in posiciones_detectadas:
            for id, troop in self.troops[enemy.nombre].items():
                if troop.pos == pos:
                    pos_detectados.append(pos)
                    ids_detectados.append(id)
                    break
        return posiciones, pos_detectados, ids_detectados

    def handle_movement(
        self, tropa: troops.BaseTroop, reporte: Report, player, pos: str
    ):
        self.movimiento = (tropa.id, tropa.pos)
        tropa.pos = pos
        reporte.movimiento = Movement(True, tropa.id, pos)

    def pos_is_empty(self, player, pos: str) -> bool:
        """
        Returns true if the position is empty
        """
        for troop in self.troops[player.nombre].values():
            if troop.pos == pos:
                return False
        return True

    def print_game(self, current_player):
        """
        Prints the game
        """
        reporte = self.reportes[current_player.nombre]
        ataques = reporte.ataques
        boards = []
        for i, player in enumerate(self.players, 1):
            board = [["." for _ in range(10)] for _ in range(10)]
            for tropa in self.troops[player.nombre].values():
                pos = COORD_TO_TUPLE[tropa.pos]
                board[pos[0]][pos[1]] = (
                    tropa.type[0]
                    if tropa.type not in (GAUSS, SCOUT)
                    else tropa.type[0].upper()
                )
            if current_player != player:
                for ataque in ataques:
                    pos = COORD_TO_TUPLE[ataque]
                    board[pos[0]][pos[1]] = f"{YEL}X{RST}"
                for pos in self.pos_bajas:
                    pos = COORD_TO_TUPLE[pos]
                    board[pos[0]][pos[1]] = f"{RED}X{RST}"
                for pos in self.posiciones_detectadas:
                    pos = COORD_TO_TUPLE[pos]
                    objeto = board[pos[0]][pos[1]]
                    if objeto == ".":
                        board[pos[0]][pos[1]] = f"{BLU}X{RST}"
                    else:
                        board[pos[0]][pos[1]] = f"{CYA}{objeto}{RST}"
            elif reporte.movimiento:
                if reporte.movimiento.resultado:
                    _id, old_pos = self.movimiento
                    old_pos = COORD_TO_TUPLE[old_pos]
                    board[old_pos[0]][old_pos[1]] = f"{GRN}.{RST}"
                    pos = COORD_TO_TUPLE[self.troops[player.nombre][_id].pos]
                    board[pos[0]][pos[1]] = f"{GRN}{board[pos[0]][pos[1]]}{RST}"
            if player == self.player_2:
                self.mirror_board(board)
            boards.append(board)
        x_axis = [chr(i) for i in range(ord("A"), ord("K"))]
        y_axis = [str(i) for i in range(10)]
        print("  " + " ".join(x_axis) + "   " + " ".join(reversed(x_axis)))
        for i, rows in enumerate(zip(*boards)):
            row1, row2 = rows
            print(
                y_axis[i]
                + " "
                + " ".join(row1)
                + "   "
                + " ".join(row2)
                + " "
                + y_axis[i]
            )
        print("      Player 1                Player 2")
        print()
        self.print_summary()

    def print_summary(self):
        for i, player in enumerate(self.players, 1):
            print(f"Eliminaciones player {i}:")
            for elim in self.reportes[player.nombre].eliminaciones:
                print(f" - {elim}")

    def mirror_board(self, board: list[list[str]]):
        """
        Mirrors a board
        """
        for row in board:
            row.reverse()
