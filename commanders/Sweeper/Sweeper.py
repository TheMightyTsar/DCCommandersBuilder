import random

from commanders.Sweeper.troops.baseTroop import BaseTroop
from commanders.Sweeper.troops.gauss import Gauss
from commanders.Sweeper.troops.grenadier import Grenadier
from commanders.Sweeper.troops.scout import Scout
from commanders.Sweeper.troops.soldier import Soldier
from commanders.Sweeper.troops.tower import Tower
from commanders.Sweeper.parametros import (ATACAR, BAJAS, GAUSS, GRENADIER, MOVER,
                                           SCOUT, SOLDIER, TOWER)
from commanders.Sweeper.parametros import TUPLE_TO_COORD as TC


class Commander:
    def __init__(self) -> None:
        super().__init__()
        self.name = "Sweeper"
        self.tropas: dict[int, BaseTroop] = {}
        self.attack_priority_list = [GRENADIER, TOWER, SOLDIER]
        self.last_action = "move"
        self.wiped = set()
        self.attacked = set()
        self.reverse = False

    def montar_tropas(self) -> list[list]:
        possible = [TC[(i, j)] for i in range(10) for j in range(0, 5)]
        possible = random.sample(possible, 13)

        tropas = []

        gauss_1 = Gauss("I0")
        self.tropas[gauss_1.id] = gauss_1
        tropas.append([gauss_1.id, GAUSS, "I0"])

        gauss_2 = Gauss("H9")
        self.tropas[gauss_2.id] = gauss_2
        tropas.append([gauss_2.id, GAUSS, "H9"])

        for i in range(5):
            tropa = Soldier(possible[i])
            self.tropas[tropa.id] = tropa
            tropas.append([tropa.id, SOLDIER, possible[i]])
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

    def jugar_turno(self, reporte: dict, reporte_enemigo: dict):
        for _id in reporte[BAJAS]:
            if _id in self.tropas:
                if isinstance(self.tropas[_id], Gauss):
                    self.last_action = "move"
                del self.tropas[_id]

        my_toops = self.get_ids()

        if my_toops[GAUSS]:
            gauss = my_toops[GAUSS][0]

            if self.tropas[gauss].pos in ("I9", "H0"):
                self.reverse = True

            if self.tropas[gauss].pos in ("I0", "H9"):
                self.reverse = False

            if self.tropas[gauss].pos.startswith("I"):
                if not self.reverse:
                    move_dir = +1
                else:
                    move_dir = -1

            else:
                if not self.reverse:
                    move_dir = -1
                else:
                    move_dir = +1

            match self.last_action:
                case "move":
                    self.last_action = "atk"
                    self.wiped.add(self.tropas[gauss].pos[1])
                    return [gauss, ATACAR, self.tropas[gauss].pos]
                case "atk":
                    self.last_action = "move"
                    self.tropas[gauss].pos = self.tropas[gauss].pos[0] + \
                                             str(int(self.tropas[gauss].pos[1]) + move_dir)
                    return [gauss, MOVER, self.tropas[gauss].pos]

        for priority in self.attack_priority_list:
            if my_toops[priority]:
                for _id in my_toops[priority]:
                    pos = filter(
                        lambda x: x[1] not in self.wiped and x not in self.attacked, TC.values())
                    pos = random.choice(list(pos))
                    self.attacked.add(pos)
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

    def __repr__(self) -> str:
        return self.name


if __name__ == "__main__":
    pass
