# pylint: disable=E0401, C0103, C0114, C0115, C0116

import random

from src.prueba.bots.SoloMover.troops.gauss import Gauss
from src.prueba.bots.SoloMover.troops.grenadier import Grenadier
from src.prueba.bots.SoloMover.troops.scout import Scout
from src.prueba.bots.SoloMover.troops.soldier import Soldier
from src.prueba.bots.SoloMover.troops.tower import Tower
from src.prueba.parametros import (BAJAS, DETECT, GAUSS, GRENADIER, MOVER,
                                   SCOUT, SOLDIER, TOWER)
from src.prueba.parametros import TUPLE_TO_COORD as TC


class Commander:
    def __init__(self):
        self.name = 'SoloMover'
        self.tropas: dict[int, Soldier | Gauss |
                          Scout | Tower | Grenadier] = {}

    def montar_tropas(self):
        possible = [TC[(i, j)] for i in range(10) for j in range(10)]
        possible = random.sample(possible, 13)

        tropas = []

        for i in range(5):
            tropa = Soldier(possible[i])
            self.tropas[tropa.id] = tropa
            tropas.append([tropa.id, SOLDIER, possible[i]])
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

        return tropas

    def jugar_turno(self, reporte, reporte_enemigo):

        for _id in reporte[BAJAS]:
            if _id in self.tropas:
                del self.tropas[_id]

        my_troop_pos = self.get_pos()

        if reporte_enemigo[DETECT]:

            for _id in random.sample(reporte_enemigo[DETECT], len(reporte_enemigo[DETECT])):

                tropa = self.tropas[_id]

                if isinstance(tropa, Tower):
                    continue

                posibles = tropa.mover()

                for pos in posibles:
                    if pos in my_troop_pos:
                        continue

                    self.tropas[_id].pos = pos
                    return [_id, MOVER, pos]

            # ! RETURNS NONE WHEN ONLY TOWER IS DETECTED

        else:

            tropas = random.sample(
                list(self.tropas.values()), len(self.tropas))

            for tropa in tropas:

                if isinstance(tropa, Tower):
                    continue

                posibles = tropa.mover()

                for pos in posibles:

                    if pos in my_troop_pos:
                        continue

                    self.tropas[tropa.id].pos = pos
                    return [tropa.id, MOVER, pos]

    def get_pos(self):
        positions = []
        for troop in self.tropas.values():
            positions.append(troop.pos)

        return positions

    def __repr__(self) -> str:
        return self.name
