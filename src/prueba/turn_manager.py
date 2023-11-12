# pylint: disable=missing-docstring, W0718, W719

import random
from itertools import cycle
from traceback import print_exception

import src.prueba.server_troops as troops
from src.prueba.colors import BLD, BLU, CYA, GRN, RED, RST, YEL
from src.prueba.parametros import (ACCIONES, ATACAR, ATACK, AVAILABLE_TROOPS,
                                   BAJAS, COORD_TO_TUPLE, DETECT, GAUSS,
                                   GRENADIER, MOV_SUCCESS, MOVER, SCOUT,
                                   SOLDIER, TOWER)

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

validTipos = ['']


class TurnManager:
    def __init__(self, commanders) -> None:
        # ? print("-" * 40)
        # ? print("Comienza la prueba de los comandantes")
        # ? print("-" * 40)
        self.player_1 = commanders[0].Commander()
        self.player_2 = commanders[1].Commander()
        self.players = [self.player_1, self.player_2]

        self.troops = {}

        self.reportes = {
            self.player_1: {ATACK: [], DETECT: [], BAJAS: [], MOV_SUCCESS: None},
            self.player_2: {ATACK: [], DETECT: [], BAJAS: [], MOV_SUCCESS: None},
        }

        for player in self.players:
            try:
                # print(f" {player.name} esta montando su tablero\n")
                self.build_player(player)
            except Exception:  # ? as e:
                # ? print(
                # ? f"Commander {player.name} tuvo un error montando el tablero: {e}")
                return self.win(self.get_enemy(player))
            print()

            # ? print(f" Verificando tablero de {player.name} \n")
            # ? print(self.verifyTablero(self.troops[player.name]))
            # ? print("-"*40)
            # ? print("-" * 40)

        self.turno = 1
        self.muertos = {self.player_1: {}, self.player_2: {}}
        self.ids_bajas_turno = []
        self.ids_detectados_turno = []
        self.pos_bajas = []
        self.movimiento: tuple[int, str]
        self.posiciones_detectadas = []
        self.exception_counter = {
            self.player_1: 0,
            self.player_2: 0,
        }
        self.por_turno: bool = False
        self.exception_break: bool = False
        self.invalid_action_break: bool = False

        self.menu_modo_juego()

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
            raise Exception(f"{player} did not return a list")
        for troop in player_troops:
            if len(troop) != 3:
                raise Exception(
                    f"{player} sent a troop with an invalid format: {troop} must be [id, tipo, pos]"
                )
            _id, tipo, pos = troop
            if not isinstance(_id, int):
                raise Exception(
                    f"{player} sent a troop with an invalid id, id {_id} of type {type(_id)} must be a integer"
                )
            if not isinstance(tipo, str) or tipo not in AVAILABLE_TROOPS.keys():
                raise Exception(
                    f"{player} sent a troop with an invalid type, type {tipo} must be a string and must be one of the available types"
                )
            if not isinstance(pos, str) or pos not in COORD_TO_TUPLE.keys():
                raise Exception(
                    f"Invalid position, position {pos} is not a string or is not in the board"
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
            elif tipo == GRENADIER:
                troops_dict[_id] = troops.Grenadier(_id, pos)
            else:
                raise Exception(f"{player} sent an invalid troop type")
            max_quantities[tipo] -= 1

        # ? for troop in troops_dict.values():
        # ?     print(f" - {troop}")

        ids = [troop.id for troop in troops_dict.values()]
        if len(ids) != len(set(ids)):
            raise Exception(f"{player} sent troops with the same id")
        positions = [troop.pos for troop in troops_dict.values()]
        if len(positions) != len(set(positions)):
            raise Exception(f"{player} sent troops to the same position")
        if any((quantity < 0 for quantity in max_quantities.values())):
            raise Exception(f"{player} sent more troops than allowed")
        # ? for troop, quantity in max_quantities.items():
        # ?     if quantity > 0:
        # ?         print(
        # ?             f"\nWarning, {player} sent {quantity} less troops of type {troop} than allowed"
        # ?         )

        self.troops[player] = troops_dict

    # ? def verifyTablero(self, tropas):
    # ?     message = '| Verificacion al Montar Tablero |\n'
    # ?     if isinstance(tropas, list):
    # ?         message += 'Lista de Tropas: TRUE \n'
    # ?         listaDeListas = True
    # ?         listID = []
    # ?         listPOS = []
    # ?         numSoldier = 0
    # ?         numGauss = 0
    # ?         numTower = 0
    # ?         numScout = 0
    # ?         numGrenadier = 0
    # ?         if len(tropas) == 13:

    # ?             for unit in tropas:
    # ?                 if not isinstance(unit, list):
    # ?                     message += 'ERROR: montar_tropas no devuelve una lista de listas \n'
    # ?                 else:
    # ?                     if len(unit) != 3:
    # ?                         message += f'ERROR: las sublistas no tienen los 3 ' \
    # ?                                    f'elementos pedidos {unit}  \n'
    # ?                     else:
    # ?                         if not isinstance(unit[0], int):
    # ?                             message += f'ERROR: el ID entregado no es un integer {unit} \n'
    # ?                         else:
    # ?                             if unit[0] in listID:
    # ?                                 message += f'ERROR: el ID entregado no es unico {unit[0]}\n'
    # ?                             else:
    # ?                                 listID.append(unit[0])

    # ?         else:
    # ?             message += 'ERROR: faltan tropas en el tablero \n'
    # ?     else:
    # ?         message += 'ERROR: montar_tropas no devuelve una lista \n'

    # ?     return message

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
            if self.turno == 1000:
                return self.find_timeout_winner()
            enemy = self.get_enemy(player)
            reporte = self.reportes[player]
            reporte_enemigo = self.turn_into_enemy_report(
                enemy, self.ids_detectados_turno
            )
            try:
                accion = player.jugar_turno(reporte, reporte_enemigo)
                self.reset_turn(player)
                self.exception_counter[player] = 0
            except Exception as e:
                if self.exception_break:
                    self.print_exception(player, e)
                    break
                if self.handle_exception(player, e):
                    return self.win(enemy)
                continue

            if not self.validate_action(accion, player):
                if self.invalid_action_break:
                    print(f"Player {player} sent an invalid action")
                    break
                print(f"Player {player} sent an invalid action, skipping turn")
                self.turno += 1
                continue
            accion = self.convertir_accion(accion)

            acc, _id, pos = accion["action"], accion["id"], accion["pos"]
            tropa = self.troops[player][_id]
            if acc == ATACAR:
                self.handle_attack(tropa, reporte, player, enemy, pos)
            elif acc == MOVER:
                self.handle_movement(tropa, reporte, player, pos)
            self.print_game(player)
            if self.game_finished(enemy):
                self.win(player)
                break
            self.turno += 1
            if self.por_turno:
                input(f"\n{BLD}Presione enter para continuar{RST}")

    def convertir_accion(self, accion: list) -> dict:
        _id, action, pos = accion
        return {"id": _id, "action": action, "pos": pos}

    def reset_turn(self, player):
        self.ids_bajas_turno = []
        self.ids_detectados_turno = []
        self.pos_bajas = []
        self.posiciones_detectadas = []
        self.clear_report(player)

    def validate_action(self, action: list, player) -> bool:
        """
        Validates a action sent by the player
        """
        if not isinstance(action, list):
            print(
                f"Invalid action format, action {action} of type {type(action)} must be a list"
            )
            return False
        if len(action) != 3:
            print(
                f"Invalid action format, action {action} must have 3 elements [id, action, pos]"
            )
            return False
        _id, acc, pos = action
        if acc not in ACCIONES:
            print(
                f"Invalid action type, action {acc} must be {MOVER} or {ATACAR}")
            return False
        if _id not in self.troops[player].keys():
            print(
                f"Invalid troop id, id {_id} is not in alive or does not exist")
            return False
        if not isinstance(pos, str) or pos not in COORD_TO_TUPLE.keys():
            print(
                f"Invalid position, position {pos} is not a string or is not in the board"
            )
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

    def handle_exception(self, player, e) -> bool:
        print(f"Player {player} raised an exception")
        print_exception(e)
        self.reset_turn(player)
        self.exception_counter[player] += 1
        if self.exception_counter[player] == 10:
            print(f"Player {player} raised 10 exceptions in a row")
            return True
        return False

    def handle_attack(
        self,
        tropa: troops.BaseTroop,
        reporte: dict,
        player,
        enemy,
        pos: str,
    ) -> None:
        if tropa.type == SCOUT:
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
                enemy, posiciones)
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
                    self.muertos[enemy][id] = self.troops[enemy].pop(id)
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

    def handle_movement(
        self, tropa: troops.BaseTroop, reporte: dict, player, pos: str
    ):
        can_move = tropa.move(pos)
        if can_move and self.pos_is_empty(player, pos):
            self.movimiento = (tropa.id, tropa.pos)
            tropa.pos = pos
            reporte[MOV_SUCCESS] = True
        else:
            reporte[MOV_SUCCESS] = False

    def pos_is_empty(self, player, pos: str) -> bool:
        """
        Returns true if the position is empty
        """
        for troop in self.troops[player].values():
            if troop.pos == pos:
                return False
        return True

    def get_troop_types(self, player):
        return [
            self.muertos[player][id].type for id in self.reportes[player][BAJAS].copy()
        ]

    def print_game(self, current_player):
        """
        Prints the game
        """
        print(
            f"{BLD}\n------------------ Turno {self.turno} ------------------\n{RST}"
        )
        reporte = self.reportes[current_player]
        ataques = reporte[ATACK]
        boards = []
        for i, player in enumerate(self.players, 1):
            board = [["." for _ in range(10)] for _ in range(10)]
            for tropa in self.troops[player].values():
                pos = COORD_TO_TUPLE[tropa.pos]
                board[pos[0]][pos[1]
                              ] = tropa.type[0] if tropa.type != GAUSS else tropa.type[0].upper()
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
                        board[pos[0]][pos[1]
                                      ] = f"{BLU}X{RST}"
                    else:
                        board[pos[0]][pos[1]
                                      ] = f"{CYA}{objeto}{RST}"
            elif reporte[MOV_SUCCESS]:
                _id, old_pos = self.movimiento
                old_pos = COORD_TO_TUPLE[old_pos]
                board[old_pos[0]][old_pos[1]] = f"{GRN}.{RST}"
                pos = COORD_TO_TUPLE[self.troops[player][_id].pos]
                board[pos[0]][pos[1]] = f"{GRN}{board[pos[0]][pos[1]]}{RST}"
            if player == self.player_2:
                self.mirror_board(board)
            boards.append(board)
        x_axis = [chr(i) for i in range(ord("A"), ord("K"))]
        y_axis = [str(i) for i in range(10)]
        print("  " + " ".join(x_axis) + "   " + " ".join(reversed(x_axis)))
        for i, rows in enumerate(zip(*boards)):
            row1, row2 = rows
            print(y_axis[i] + " " + " ".join(row1) +
                  "   " + " ".join(row2) + " " + y_axis[i])
        print("      Player 1                Player 2")
        print()
        self.print_summary()

    def print_summary(self):
        for i, player in enumerate(self.players, 1):
            print(f"Bajas player {i}:")
            for bajas in self.get_troop_types(player):
                print(f" - {bajas}")

    def print_exception(self, player, e):
        print(f"Player {player} raised an exception")
        print_exception(e)

    def mirror_board(self, board: list[list[str]]):
        """
        Mirrors a board
        """
        for row in board:
            row.reverse()


if __name__ == "__main__":
    pass
