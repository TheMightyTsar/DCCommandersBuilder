# pylint: disable=E0401, C0103, C0114, C0115, C0116

from commanders.JorGeneral.troops.baseTroop import BaseTroop


class Tower(BaseTroop):
    # Clase Tower

    def __init__(self, pos):
        super().__init__()
        self.type = "tower"
        self.pos = pos

    def mover(self):
        return []

    def atacar(self):
        pass
