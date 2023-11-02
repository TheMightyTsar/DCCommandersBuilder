from commanders.jeanpipe.troops.baseTroop import BaseTroop 
class Scout(BaseTroop):
    # Clase Scout

    def __init__(self, pos):
        super().__init__()
        self.type = 'soldier'
        self.pos = pos

    def moverse(self):
        pass

    def atacar(self):
        pass