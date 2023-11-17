import random

from commanders.JorGeneral.troops.gauss import Gauss
from commanders.JorGeneral.troops.grenadier import Grenadier
from commanders.JorGeneral.troops.scout import Scout
from commanders.JorGeneral.troops.soldier import Soldier
from commanders.JorGeneral.troops.tower import Tower
from parametros import (ATACAR, ATACK, BAJAS, DETECT, GAUSS, GRENADIER, MOVER,
                        SCOUT, SOLDIER, TOWER)
from parametros import TUPLE_TO_COORD as TC


class Commander:
    def __init__(self):
        self.name = "JorGeneral"
        self.tropas: dict[int, Soldier | Gauss |
                          Scout | Tower | Grenadier] = {}
        self.attack_priority_list = [GRENADIER, TOWER, SOLDIER, GAUSS]
        self.attacked = set()

    def montar_tropas(self):
        possible = list(TC.values())
        possible = random.sample(possible, 12)

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
        for i in range(10, 12):
            tropa = Grenadier(possible[i])
            self.tropas[tropa.id] = tropa
            tropas.append([tropa.id, GRENADIER, possible[i]])

        return tropas

    def jugar_turno(self, reporte: dict, reporte_enemigo: dict):
        for _id in reporte[BAJAS]:
            if _id in self.tropas:
                del self.tropas[_id]

        if reporte[ATACK]:
            for pos in reporte[ATACK]:
                self.attacked.add(pos)

        my_toops = self.get_ids()

        my_troop_pos = self.get_pos()

        if reporte_enemigo[DETECT]:
            for _id in random.sample(
                reporte_enemigo[DETECT], len(reporte_enemigo[DETECT])
            ):
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

        if reporte[DETECT]:
            for _id in my_toops[GAUSS]:
                if self.tropas[_id].pos[1] in [pos[1] for pos in reporte[DETECT]]:
                    return [_id, ATACAR, self.tropas[_id].pos]

            for priority in self.attack_priority_list:
                if my_toops[priority]:
                    for _id in my_toops[priority]:
                        pos = random.choice(reporte[DETECT])
                        return [_id, ATACAR, pos]
                else:
                    continue

        if not reporte[DETECT]:
            if my_toops[SCOUT]:
                for _id in my_toops[SCOUT]:
                    pos = filter(lambda x: x not in self.attacked, TC.values())
                    pos = random.choice(list(pos))
                    return [_id, ATACAR, pos]
            else:
                for priority in self.attack_priority_list:
                    if priority == GAUSS:
                        for _id in my_toops[GAUSS]:
                            return [_id, ATACAR, self.tropas[_id].pos]
                    if my_toops[priority]:
                        for _id in my_toops[priority]:
                            pos = filter(
                                lambda x: x not in self.attacked, TC.values())
                            pos = random.choice(list(pos))
                            return [_id, ATACAR, pos]
                    else:
                        continue

    def get_ids(self):
        troops = {
            SOLDIER: [],
            GAUSS: [],
            SCOUT: [],
            TOWER: [],
            GRENADIER: [],
        }
        for troop in self.tropas.values():
            troops[troop.type].append(troop.id)

        return troops

    def get_pos(self):
        positions = []
        for troop in self.tropas.values():
            positions.append(troop.pos)

        return positions

    def __repr__(self):
        return self.name
