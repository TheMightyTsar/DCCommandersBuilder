from commanders.SoloAtaque.troops.baseTroop import BaseTroop


class Himars(BaseTroop):
    # Clase HIMARS

    def __init__(self, pos):
        super().__init__()
        self.type = 'grenadier'
        self.pos = pos

    def mover(self):
        pass

    def atacar(self):
        pass
