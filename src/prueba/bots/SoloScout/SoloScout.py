import random

from src.prueba.bots.SoloScout.troops.scout import Scout
from src.prueba.parametros import ATACAR, BAJAS
from src.prueba.parametros import TUPLE_TO_COORD as TC


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

        for _id, tropa in self.tropas.items():
            if _id in informe[BAJAS]:
                continue
            return [tropa.id, ATACAR, self.obtener_posicion()]

    def obtener_posicion(self):
        return random.choice(list(TC.values()))

    def __repr__(self) -> str:
        return self.name
