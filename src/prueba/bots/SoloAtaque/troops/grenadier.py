from src.prueba.bots.SoloAtaque.troops.baseTroop import BaseTroop


class Grenadier(BaseTroop):
    # Clase Grenadier

    def __init__(self, pos):
        super().__init__()
        self.type = 'grenadier'
        self.pos = pos

    def mover(self):
        pass

    def atacar(self):
        pass
