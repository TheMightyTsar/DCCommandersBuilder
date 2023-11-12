import random

from src.prueba.bots.SoloAtaque.troops.grenadier import Grenadier
from src.prueba.bots.SoloAtaque.troops.soldier import Soldier
from src.prueba.bots.SoloAtaque.troops.tower import Tower
from src.prueba.parametros import ATACAR, BAJAS
from src.prueba.parametros import TUPLE_TO_COORD as TC


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

        for _id, tropa in self.tropas.items():
            if _id in informe[BAJAS]:
                continue
            return [tropa.id, ATACAR, self.obtener_posicion()]

    def obtener_posicion(self):
        return random.choice(list(TC.values()))

    def __repr__(self) -> str:
        return self.name
