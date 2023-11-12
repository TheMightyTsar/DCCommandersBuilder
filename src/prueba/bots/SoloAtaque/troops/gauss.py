from src.prueba.bots.SoloAtaque.troops.baseTroop import BaseTroop


class Gauss(BaseTroop):
    # Clase Gauss

    def __init__(self, pos):
        super().__init__()
        self.type = "gauss"
        self.pos = pos

    def mover(self):
        pass

    def atacar(self):
        pass
