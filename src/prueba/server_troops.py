"""Cointains all troop classes used by the 'server'."""

import random
from abc import ABC, abstractmethod

from src.prueba.parametros import COORD_TO_TUPLE as CT
from src.prueba.parametros import TUPLE_TO_COORD as TC


class BaseTroop(ABC):
    """Base class for all troops."""

    def __init__(self, _id, pos) -> None:
        self.pos: str = pos
        self.type: str
        self.id = _id

    @abstractmethod
    def move(self, pos: str) -> bool:
        """Verify if the troop can move to the given position."""

    @abstractmethod
    def attack(self, pos: str) -> list[str]:
        """Returns a list of positions affected by the attack."""

    def __repr__(self) -> str:
        return f"Id: {str(self.id).center(2)} \
        Position: {self.pos.center(3)} \
        Type: {self.type}"


class Soldier(BaseTroop):
    """Soldier class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = "soldier"

    def move(self, pos: str):
        """Moves 1 cell in cross pattern."""

        possible = []

        for i in range(-1, 2):
            possible.append((CT[self.pos][0] + i, CT[self.pos][1]))
            possible.append((CT[self.pos][0], CT[self.pos][1] + i))

        try:
            if CT[pos] in possible:
                return True
        except KeyError:
            return False

        return False

    def attack(self, pos: str):
        """Attcks targeted position."""

        return [pos]


class Gauss(BaseTroop):
    """Gauss class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = "gauss"

    def move(self, pos: str):
        """Moves 1 cell only between columns."""

        possible = []

        for i in range(-1, 2):
            possible.append((CT[self.pos][0] + i, CT[self.pos][1]))

        try:
            if CT[pos] in possible:
                return True
        except KeyError:
            return False

        return False

    def attack(self, pos: str):
        """Attcks targeted position and 4 cells behind."""

        if pos[1] != self.pos[1]:
            return []

        affected = [TC[(CT[pos][0], i)] for i in range(10)]

        return affected


class Scout(BaseTroop):
    """Scout class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = "scout"

    def move(self, pos: str):
        """Moves 2 cells in cross pattern."""

        possible = []

        for i in range(-2, 3):
            possible.append((CT[self.pos][0] + i, CT[self.pos][1]))
            possible.append((CT[self.pos][0], CT[self.pos][1] + i))

        try:
            if CT[pos] in possible:
                return True
        except KeyError:
            return False

        return False

    def attack(self, pos: str):
        """Attcks targeted position and 8 cells around."""

        affected = [
            TC[(CT[pos][0] + i, CT[pos][1] + j)]
            for i in range(-1, 2) for j in range(-1, 2) if
            CT[pos][0] + i in range(0, 10) and
            CT[pos][1] + j in range(0, 10)
        ]

        return affected


class Tower(BaseTroop):
    """Air Traffic Control class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = "tower"

    def move(self, pos: str):
        """Doesn't move."""

        return False

    def attack(self, pos: str):
        """Attcks targeted position and 4 random cells in the same row."""

        affected = [
            TC[(i, CT[pos][1])]
            for i in range(10)
        ]

        affected.remove(pos)

        return [pos] + random.sample(affected, 4)


class Grenadier(BaseTroop):
    """HIMARS class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = "grenadier"

    def move(self, pos: str):
        """Moves 1 cell in cross pattern."""

        possible = []

        for i in range(-1, 2):
            possible.append((CT[self.pos][0] + i, CT[self.pos][1]))
            possible.append((CT[self.pos][0], CT[self.pos][1] + i))

        try:
            if CT[pos] in possible:
                return True
        except KeyError:
            return False

        return False

    def attack(self, pos: str):
        """Attcks targeted position and 4 random cells around."""

        affected = [
            TC[(CT[pos][0] + i, CT[pos][1] + j)]
            for i in range(-1, 2) for j in range(-1, 2) if
            CT[pos][0] + i in range(0, 10) and
            CT[pos][1] + j in range(0, 10)
        ]

        affected.remove(pos)

        return [pos] + random.sample(affected, min(len(affected), 4))


if __name__ == '__main__':
    pass
