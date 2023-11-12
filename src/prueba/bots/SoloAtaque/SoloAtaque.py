import random

from src.prueba.bots.SoloAtaque.troops.gauss import Gauss
from src.prueba.bots.SoloAtaque.troops.grenadier import Grenadier
from src.prueba.bots.SoloAtaque.troops.scout import Scout
from src.prueba.bots.SoloAtaque.troops.soldier import Soldier
from src.prueba.bots.SoloAtaque.troops.tower import Tower
from src.prueba.parametros import ATACAR, ATACK, BAJAS
from src.prueba.parametros import COORD_TO_TUPLE as ct
from src.prueba.parametros import (DETECT, GAUSS, GRENADIER, MOV_SUCCESS,
                                   MOVER, SCOUT, SOLDIER, TOWER)
from src.prueba.parametros import TUPLE_TO_COORD as tc


class Commander:
    def __init__(self):
        self.name = 'SoloAtaque'
        self.tropas = {}

    def montar_tropas(self):
        tropas = []

        granadero = Grenadier("A5")
        tower = Tower("A6")
        soldado = Soldier("D8")

        self.tropas[granadero.id] = granadero
        self.tropas[tower.id] = tower
        self.tropas[soldado.id] = soldado

        tropas.append([granadero.id, granadero.type, granadero.pos])
        tropas.append([tower.id, tower.type, tower.pos])
        tropas.append([soldado.id, soldado.type, soldado.pos])

        return tropas

    def jugar_turno(self, informe: dict, informe_enemigo: dict):
        for id_tropa in self.tropas:
            if id_tropa in informe[BAJAS]:
                continue
            tropa = self.tropas[id_tropa]
            if tropa.type == GRENADIER:
                return [tropa.id, ATACAR, self.obtener_posicion()]
            elif tropa.type == TOWER:
                return [tropa.id, ATACAR, self.obtener_posicion()]
            elif tropa.type == SOLDIER:
                return [tropa.id, ATACAR, self.obtener_posicion()]

    def obtener_posicion(self):
        fil, col = random.choice(list(tc.keys()))
        return tc[(fil, col)]

    def __repr__(self) -> str:
        return self.name
