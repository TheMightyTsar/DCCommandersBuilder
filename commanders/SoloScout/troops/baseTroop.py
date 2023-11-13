from abc import ABC, abstractmethod


class BaseTroop(ABC):
    _id = 0

    def __init__(self):
        self.id = self._id
        BaseTroop._id += 1
        self.type = 'base'
        self.pos: str = 'A0'

    @abstractmethod
    def mover(self):
        # decide donde moverse
        pass

    @abstractmethod
    def atacar(self):
        # decide donde ataca
        pass
