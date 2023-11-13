from commanders.SoloAtaque.troops.baseTroop import BaseTroop


class Soldier(BaseTroop):
    # Clase de Soldado

    def __init__(self, pos):
        super().__init__()
        self.type = 'soldier'
        self.pos: str = pos

    def mover(self):
        pass

    def atacar(self):
        pass
