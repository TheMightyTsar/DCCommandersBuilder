from abc import ABC, abstractmethod


class BaseTroop(ABC):
    _id = 0

    def __init__(self, _type, pos):
        self.id = self._id
        BaseTroop._id += 1
        self.type = _type
        self.pos: str = pos

    @abstractmethod
    def mover(self):
        """Decides where to move"""

    @abstractmethod
    def atacar(self):
        """Decides where to attack"""


class Common(BaseTroop):
    def __init__(self, pos):
        super().__init__(_type="common", pos=pos)

    def mover(self):
        pass

    def atacar(self):
        pass


class Gauss(BaseTroop):
    def __init__(self, pos):
        super().__init__(_type="gauss", pos=pos)

    def mover(self):
        pass

    def atacar(self):
        pass


class Scouter(BaseTroop):
    def __init__(self, pos):
        super().__init__(_type="scouter", pos=pos)

    def mover(self):
        pass

    def atacar(self):
        pass


class ATC(BaseTroop):
    def __init__(self, pos):
        super().__init__(_type="atc", pos=pos)

    def mover(self):
        pass

    def atacar(self):
        pass


class Grenadier(BaseTroop):
    def __init__(self, pos):
        super().__init__(_type="grenadier", pos=pos)

    def mover(self):
        pass

    def atacar(self):
        pass
