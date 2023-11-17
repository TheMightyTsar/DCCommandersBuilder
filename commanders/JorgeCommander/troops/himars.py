from commanders.JorgeCommander.troops.baseTroop import BaseTroop 
class HIMARS(BaseTroop):
    # Clase HIMARS

    def __init__(self, pos):
        super().__init__()
        self.type = 'himars'
        self.pos = pos

    def mover(self):
        pass

    def atacar(self):
        pass