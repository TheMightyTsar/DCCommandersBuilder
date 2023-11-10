"""Cointains all troop classes."""

import random

from base_classes import BaseTroop
from dicts import COORD_TO_TUPLE as ct
from dicts import TUPLE_TO_COORD as tc


class Common(BaseTroop):
    """Common class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = "common"

    def move(self, pos: str):
        """Moves 1 cell in cross pattern."""

        possible = []

        for i in range(-1, 2):
            possible.append((ct[self.pos][0] + i, ct[self.pos][1]))
            possible.append((ct[self.pos][0], ct[self.pos][1] + i))

        try:
            if ct[pos] in possible:
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
            possible.append((ct[self.pos][0] + i, ct[self.pos][1]))

        try:
            if ct[pos] in possible:
                return True
        except KeyError:
            return False

        return False

    def attack(self, pos: str):
        """Attcks targeted position and 4 cells behind."""

        if pos[1] != self.pos[1]:
            return []

        # affected = [
        #     tc[(ct[pos][0] - i, ct[pos][1])]
        #     for i in range(5) if
        #     ct[pos][0] - i in range(0, 10)
        # ]

        affected = [tc[(ct[pos][0], i)] for i in range(10)]

        return affected


class Scouter(BaseTroop):
    """Scouter class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = "scouter"

    def move(self, pos: str):
        """Moves 2 cells in cross pattern."""

        possible = []

        for i in range(-1, 2):
            possible.append((ct[self.pos][0] + i, ct[self.pos][1]))
            possible.append((ct[self.pos][0], ct[self.pos][1] + i))

        try:
            if ct[pos] in possible:
                return True
        except KeyError:
            return False

        return False

    def attack(self, pos: str):
        """Attcks targeted position and 8 cells around."""

        affected = [
            tc[(ct[pos][0] + i, ct[pos][1] + j)]
            for i in range(-1, 2) for j in range(-1, 2) if
            ct[pos][0] + i in range(0, 10) and
            ct[pos][1] + j in range(0, 10)
        ]

        return affected


class ATC(BaseTroop):
    """Air Traffic Control class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = "aircraft_control_tower"

    def move(self, pos: str):
        """Doesn't move."""

        return False

    def attack(self, pos: str):
        """Attcks targeted position and 4 random cells in the same row."""

        affected = [
            tc[(i, ct[pos][1])]
            for i in range(10)
        ]

        affected.remove(pos)

        return [pos] + random.sample(affected, 4)


class Grenadier(BaseTroop):
    """Grenadier class."""

    def __init__(self, id, pos):
        super().__init__(id, pos)
        self.type = "grenadier"

    def move(self, pos: str):
        """Moves 1 cell in cross pattern."""

        possible = []

        for i in range(-1, 2):
            possible.append((ct[self.pos][0] + i, ct[self.pos][1]))
            possible.append((ct[self.pos][0], ct[self.pos][1] + i))

        try:
            if ct[pos] in possible:
                return True
        except KeyError:
            return False

        return False

    def attack(self, pos: str):
        """Attcks targeted position and 4 random cells around."""

        affected = [
            tc[(ct[pos][0] + i, ct[pos][1] + j)]
            for i in range(-1, 2) for j in range(-1, 2) if
            ct[pos][0] + i in range(0, 10) and
            ct[pos][1] + j in range(0, 10)
        ]

        affected.remove(pos)

        return [pos] + random.sample(affected, min(len(affected), 4))


if __name__ == '__main__':
    pass
