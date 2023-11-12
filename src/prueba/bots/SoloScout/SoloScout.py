import random

from src.prueba.bots.SoloScout.troops.gauss import Gauss
from src.prueba.bots.SoloScout.troops.grenadier import Grenadier
from src.prueba.bots.SoloScout.troops.scout import Scout
from src.prueba.bots.SoloScout.troops.soldier import Soldier
from src.prueba.bots.SoloScout.troops.tower import Tower
from src.prueba.parametros import ATACAR, ATACK, BAJAS
from src.prueba.parametros import COORD_TO_TUPLE as ct
from src.prueba.parametros import (DETECT, GAUSS, GRENADIER, MOV_SUCCESS,
                                   MOVER, SCOUT, SOLDIER, TOWER)
from src.prueba.parametros import TUPLE_TO_COORD as tc


class Commander:
    def __init__(self):
        self.name = 'SoloScout'
        self.tropas = {}

    def montar_tropas(self):
        tropas = []

        scout1 = Scout("A5")
        scout2 = Scout("D7")

        self.tropas[scout1.id] = scout1
        self.tropas[scout2.id] = scout2

        tropas.append([scout1.id, scout1.type, scout1.pos])
        tropas.append([scout2.id, scout2.type, scout2.pos])

        return tropas

    def jugar_turno(self, informe: dict, informe_enemigo: dict):
        for id_tropa in self.tropas:
            if id_tropa in informe[BAJAS]:
                continue
            tropa = self.tropas[id_tropa]
            return [tropa.id, ATACAR, self.obtener_posicion()]

    def obtener_posicion(self):
        fil, col = random.choice(list(tc.keys()))
        return tc[(fil, col)]

    def __repr__(self) -> str:
        return self.name
