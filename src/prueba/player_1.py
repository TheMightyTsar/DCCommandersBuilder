import random

from base_classes import Acciones as A
from base_classes import BaseCommander
from base_classes import Troops as T
from dicts import TUPLE_TO_COORD as tc
# // from icecream import ic
from parametros import ATACK, BAJAS, DETECT, MOV_SUCCESS
from troops import *


class MyCommander(BaseCommander):
    def __init__(self) -> None:
        super().__init__()
        self.nombre = "DCCapallo"
        self.attack_priority_list = [
            T.GRENADIER.value, T.ATC.value, T.COMMON.value, T.GAUSS.value]

    def set_troops(self) -> list[tuple[int, str, str]]:
        possible = [tc[(i, j)] for i in range(10) for j in range(10)]
        possible = random.sample(possible, 13)
        dictt = {
            T.COMMON: possible[0:5],
            T.GAUSS: possible[5:7],
            T.SCOUTER: possible[7:9],
            T.ATC: possible[9:10],
            T.GRENADIER: possible[10:13],
        }
        # // ic(dictt)
        tropas = self.instantiate_troops(dictt)
        return tropas

    def admin_troops(self, reporte: dict, reporte_enemigo: dict):
        for _id in reporte[BAJAS]:
            if _id in self.tropas:
                del self.tropas[_id]

        my_toops = self.get_ids()

        # // if reporte_enemigo[DETECT]:
        # //     tropa = random.choice(reporte_enemigo[DETECT])
        # //     for coord in tc.values():
        # //         if self.tropas[tropa].pos == coord:
        # //             continue
        # //         if self.can_i_move(tropa, coord):
        # //             for troops in self.tropas.values():
        # //                 if troops.pos == coord:
        # //                     continue
        # //             return self.accion(tropa, A.MOVER, coord)

        # // else:

        if reporte[DETECT]:
            for _id in my_toops[T.GAUSS.value]:
                if self.tropas[_id].pos[0] in [pos[0] for pos in reporte[DETECT]]:
                    return self.accion(_id, A.ATACAR, self.tropas[_id].pos)

            for priority in self.attack_priority_list:
                if my_toops[priority]:
                    for _id in my_toops[priority]:
                        pos = random.choice(reporte[DETECT])
                        return self.accion(_id, A.ATACAR, pos)
                else:
                    continue

        if not reporte[DETECT]:
            if my_toops[T.SCOUTER.value]:
                for _id in my_toops[T.SCOUTER.value]:
                    pos = random.choice(list(tc.values()))
                    return self.accion(_id, A.ATACAR, pos)
            else:
                for priority in self.attack_priority_list:
                    if priority == T.GAUSS.value:
                        for _id in my_toops[T.GAUSS.value]:
                            return self.accion(_id, A.ATACAR, self.tropas[_id].pos)
                    if my_toops[priority]:
                        for _id in my_toops[priority]:
                            pos = random.choice(list(tc.values()))
                            return self.accion(_id, A.ATACAR, pos)
                    else:
                        continue

    def can_i_move(self, _id: int, pos: str):
        if self.tropas[_id].type == T.COMMON.value:
            return Common(0, self.tropas[_id].pos).move(pos)
        if self.tropas[_id].type == T.GAUSS.value:
            return Gauss(0, self.tropas[_id].pos).move(pos)
        if self.tropas[_id].type == T.SCOUTER.value:
            return Scouter(0, self.tropas[_id].pos).move(pos)
        if self.tropas[_id].type == T.ATC.value:
            return ATC(0, self.tropas[_id].pos).move(pos)
        if self.tropas[_id].type == T.GRENADIER.value:
            return Grenadier(0, self.tropas[_id].pos).move(pos)

    def get_ids(self):
        troops = {
            T.COMMON.value: [],
            T.GAUSS.value: [],
            T.SCOUTER.value: [],
            T.ATC.value: [],
            T.GRENADIER.value: [],
        }
        for troop in self.tropas.values():
            troops[troop.type].append(troop.id)

        return troops


if __name__ == "__main__":
    pass
