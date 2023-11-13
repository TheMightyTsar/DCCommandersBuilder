from commanders.v.troops.baseTroop import BaseTroop 
class Scout(BaseTroop):
    # Clase Scout

    def __init__(self, pos):
        super().__init__()
        self.type = 'scout'
        self.pos = pos

    def mover(self):
        pass

    def atacar(self):
        pass