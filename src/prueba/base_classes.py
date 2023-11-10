"""Contains base classes for the game."""

# pylint: disable=missing-docstring
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Dict, List

from src.prueba.clases_jugador import ATC, Common, Gauss, Grenadier, Scouter


class Acciones(Enum):
    """Constants for actions."""
    ATACAR = "atacar"
    MOVER = "mover"


class Troops(Enum):
    """Constants for troops."""
    COMMON = "common"
    GAUSS = "gauss"
    SCOUTER = "scouter"
    ATC = "atc"
    GRENADIER = "grenadier"


class BaseTroop(metaclass=ABCMeta):
    """Base class for all troops."""

    def __init__(self, id, pos) -> None:
        self.pos: str = pos
        self.type: str
        self.id = id

    @abstractmethod
    def move(self, pos: str) -> bool:
        """Verify if the troop can move to the given position."""

    @abstractmethod
    def attack(self, pos: str) -> List[str]:
        """Returns a list of positions affected by the attack."""

    def __repr__(self) -> str:
        return f"Id: {str(self.id).center(2)} \
        Position: {self.pos.center(3)} \
        Type: {self.type}"





if __name__ == "__main__":
    pass
