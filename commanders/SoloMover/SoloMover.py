# pylint: disable=E0401, C0103, C0114, C0115, C0116

import random

from commanders.SoloMover.troops.gauss import Gauss
from commanders.SoloMover.troops.grenadier import Grenadier
from commanders.SoloMover.troops.scout import Scout
from commanders.SoloMover.troops.soldier import Soldier
from commanders.SoloMover.troops.tower import Tower
from commanders.SoloMover.parametros import (BAJAS, DETECT, GAUSS, GRENADIER, MOVER,
                                   SCOUT, SOLDIER, TOWER)
from commanders.SoloMover.parametros import TUPLE_TO_COORD as TC


class Commander:
    def __init__(self):
        """
        Aqui se inicializan las variables que se utilizaran durante la simulacion.\n
        El nombre del comandante es asignado automaticamente por el builder.\n
        Se pueden crear mas variables en caso de ser necesario.
        """
        self.name = 'SoloMover'

        # Se crea un diccionario para almacenar las tropas de manera conveniente
        # El diccionario tiene como llave el id de la tropa y como valor la instancia de la tropa
        self.tropas: dict[int, Soldier | Gauss |
                          Scout | Tower | Grenadier] = {}

    def montar_tropas(self):
        """
        Este metodo es llamado por el simulador al inicio de la simulacion.\n
        Debe retornar una lista de listas, donde cada lista interna representa una tropa.\n
        El formato de cada lista interna debe ser el siguiente:\n
                                        [id, tipo, posicion]
        """

        # Se eligen 13 posiciones aleatorias utilizando el diccionario TC, el cual
        # tiene como llave una tupla e.g. (0,0) y como valor un posicion e.g. "A0"
        possible = list(TC.values())
        possible = random.sample(possible, 13)

        # Se crea una lista vacia a la cual se le agregaran las tropas en el formato pedido
        tropas = []

        # Comienza creando los 5 soldados
        for i in range(5):
            # Se crea una instancia de Soldier, la cual genera un id unico automaticamente
            tropa = Soldier(possible[i])
            # Se agrega la instancia al diccionario coneveniente, utilizando su id como llave
            self.tropas[tropa.id] = tropa
            # Se agrega la tropa a la lista de listas que el metodo debe devolver
            tropas.append([tropa.id, SOLDIER, possible[i]])

        # Se repite el proceso para cada tipo de tropa
        for i in range(5, 7):
            tropa = Gauss(possible[i])
            self.tropas[tropa.id] = tropa
            tropas.append([tropa.id, GAUSS, possible[i]])

        for i in range(7, 9):
            tropa = Scout(possible[i])
            self.tropas[tropa.id] = tropa
            tropas.append([tropa.id, SCOUT, possible[i]])

        for i in range(9, 10):
            tropa = Tower(possible[i])
            self.tropas[tropa.id] = tropa
            tropas.append([tropa.id, TOWER, possible[i]])

        for i in range(10, 13):
            tropa = Grenadier(possible[i])
            self.tropas[tropa.id] = tropa
            tropas.append([tropa.id, GRENADIER, possible[i]])

        # Se retorna la lista de listas, la cual sera verificada por el simulador
        return tropas

    def jugar_turno(self, reporte, reporte_enemigo):
        """Este metodo es llamado por el simulador cada turno."""

        # Se verifican las bajas del comandante
        for _id in reporte[BAJAS]:

            # Si el id de la tropa esta en el diccionario (esta viva), se elimina
            if _id in self.tropas:
                del self.tropas[_id]

        # Se crea una lista con las posiciones actuales de las tropas del comandante
        # Esto se realiza mediante la funcion get_pos(), definida mas abajo
        my_troop_pos = self.get_pos()

        # Se verifica si el enemigo detecto alguna tropa
        if reporte_enemigo[DETECT]:

            # Se randomiza el orden de los id de las tropas detectadas y se itera sobre estos
            for _id in random.sample(reporte_enemigo[DETECT], len(reporte_enemigo[DETECT])):

                # Se obtiene la instancia de la tropa detectada
                tropa = self.tropas[_id]

                # Si la tropa es una torre, se ignora ya que no se puede mover
                if isinstance(tropa, Tower):
                    continue

                # Se obtienen las posiciones a las que se puede mover la tropa
                # El metodo mover() retorna una lista de posiciones, definido en cada clase de tropa
                # Para mas informacion, ver el archivo de cada tropa en la carpeta troops
                posibles = tropa.mover()

                # Se itera sobre las posiciones posibles
                for pos in posibles:

                    # Si la posicion esta ocupada por una tropa aliada, se ignora
                    if pos in my_troop_pos:
                        continue

                    # Si la posicion no esta ocupada, se guarda la nueva posicion de la tropa
                    # ! ES IMPORTANTE ASEGURARSE QUE EL MOVIMIENTO SEA VALIDO
                    # ! EL SIMULADOR HACE LA VERIFICACION Y SI EL MOVIMIENTO NO ES VALIDO
                    # ! SE PUEDE PERDER LA POSICION REAL DE LA TROPA
                    self.tropas[_id].pos = pos

                    # Se retorna la accion realizada en el formato pedido
                    return [_id, MOVER, pos]

            # ! SI SOLO LA TORRE ES DETECTADA, EL COMANDANTE NO HACE NADA

        # Si no se detecto ninguna tropa...
        else:

            # Se randomiza el orden de las tropas del comandante
            tropas = random.sample(
                list(self.tropas.values()), len(self.tropas))

            # Se itera sobre las tropas
            for tropa in tropas:

                # Si la tropa es una torre, se ignora ya que no se puede mover
                if isinstance(tropa, Tower):
                    continue

                # Se obtienen las posiciones a las que se puede mover la tropa
                posibles = tropa.mover()

                # Se itera sobre las posiciones posibles
                for pos in posibles:

                    # Si la posicion esta ocupada por una tropa aliada, se ignora
                    if pos in my_troop_pos:
                        continue

                    # Si la posicion no esta ocupada, se guarda la nueva posicion de la tropa
                    self.tropas[tropa.id].pos = pos

                    # Se retorna la accion realizada en el formato pedido
                    return [tropa.id, MOVER, pos]

    def get_pos(self):
        positions = []
        for troop in self.tropas.values():
            positions.append(troop.pos)

        return positions

    def __repr__(self) -> str:
        return self.name
