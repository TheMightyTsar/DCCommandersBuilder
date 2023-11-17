"""Cointains all troop classes used by the 'server'."""

import random
from abc import ABC, abstractmethod

from src.base_files.parametros import COORD_TO_TUPLE as ct
from src.base_files.parametros import GAUSS, HIMARS, SCOUT, SOLDIER, TOWER
from src.base_files.parametros import TUPLE_TO_COORD as tc


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
        self.type = SOLDIER

    def move(self, pos: str):
        """Moves 1 cell in cross pattern."""

        possible = []

        for i in range(-3, 4):
            possible.append((ct[self.pos][0] + i, ct[self.pos][1]))
            possible.append((ct[self.pos][0], ct[self.pos][1] + i))

        try:
            if ct[pos] in possible:
                return True
        except KeyError:
            return False

        return False

    def attack(self, pos: str):
        """Attacks targeted position."""
        # Atacks to the right, up and down
        affected = []
        affected.append((ct[pos][0] + 1, ct[pos][1]))
        affected.append((ct[pos][0], ct[pos][1] + 1))
        affected.append((ct[pos][0] - 1, ct[pos][1]))

        return [pos] + [tc[i] for i in affected if i in ct.values()]


class Gauss(BaseTroop):
    """Gauss class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = GAUSS

    def move(self, pos: str):
        """Doesn't move."""

        return False

    def attack(self, pos: str):
        """Attacks targeted position and 4 cells behind."""

        if pos[1] != self.pos[1]:
            return []

        # affected = [
        #     tc[(ct[pos][0] - i, ct[pos][1])]
        #     for i in range(5) if
        #     ct[pos][0] - i in range(0, 10)
        # ]

        affected = [tc[(ct[pos][0], i)] for i in range(10)]

        return affected


class Scout(BaseTroop):
    """Scouter class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = SCOUT

    def move(self, pos: str):
        """Moves 2 cells in cross pattern."""

        possible = []

        for i in range(-2, 3):
            possible.append((ct[self.pos][0] + i, ct[self.pos][1]))
            possible.append((ct[self.pos][0], ct[self.pos][1] + i))

        try:
            if ct[pos] in possible:
                return True
        except KeyError:
            return False

        return False

    def attack(self, pos: str):
        """Attacks targeted position and 8 cells around."""

        affected = [
            (ct[pos][0] + i, ct[pos][1] + j)
            for i in range(-1, 2) for j in range(-1, 2) if
            ct[pos][0] + i in range(0, 10) and
            ct[pos][1] + j in range(0, 10)
        ]

        affected.append((ct[pos][0] + 2, ct[pos][1]))
        affected.append((ct[pos][0], ct[pos][1] + 2))
        affected.append((ct[pos][0] - 2, ct[pos][1]))
        affected.append((ct[pos][0], ct[pos][1] - 2))

        return [tc[i] for i in affected if i in ct.values()]


class Tower(BaseTroop):
    """Air Traffic Control class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = TOWER

    def move(self, pos: str):
        """Doesn't move."""

        return False

    def attack(self, pos: str):
        """Attacks targeted position and 4 random cells in the same row."""

        affected = [
            tc[(i, ct[pos][1])]
            for i in range(10)
        ]

        affected.remove(pos)

        return [pos] + random.sample(affected, 5)


class Grenadier(BaseTroop):
    """Grenadier class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = HIMARS

    def move(self, pos: str):
        """Moves 1 cell in cross pattern."""

        possible = []

        for i in range(-2, 3):
            possible.append((ct[self.pos][0] + i, ct[self.pos][1]))
            possible.append((ct[self.pos][0], ct[self.pos][1] + i))

        try:
            if ct[pos] in possible:
                return True
        except KeyError:
            return False

        return False

    def attack(self, pos: str):
        """Attacks targeted position and 4 random cells around."""

        affected = [
            (ct[pos][0] + i, ct[pos][1] + j)
            for i in range(-1, 2) for j in range(-1, 2)
        ]
        affected.append((ct[pos][0] + 2, ct[pos][1]))
        affected.append((ct[pos][0], ct[pos][1] + 2))
        affected.append((ct[pos][0] - 2, ct[pos][1]))
        affected.append((ct[pos][0], ct[pos][1] - 2))
        affected.remove(ct[pos])

        affected = random.sample(affected, 6)

        affected = [tc[cord] for cord in affected if cord in tc.keys()]

        return [pos] + affected


if __name__ == '__main__':
    ...
