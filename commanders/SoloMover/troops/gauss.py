# pylint: disable=E0401, C0103, C0114, C0115, C0116

from random import sample

from commanders.SoloAtaque.troops.baseTroop import BaseTroop
from src.prueba.parametros import COORD_TO_TUPLE as CT
from src.prueba.parametros import TUPLE_TO_COORD as TC


class Gauss(BaseTroop):
    # Clase Gauss

    def __init__(self, pos):
        super().__init__()
        self.type = "gauss"
        self.pos = pos

    def mover(self):
        possible = []

        for i in (-1, 1):
            possible.append((CT[self.pos][0] + i, CT[self.pos][1]))

        possible = [TC[i] for i in possible if i in TC.keys()]

        return sample(possible, len(possible))

    def atacar(self):
        pass