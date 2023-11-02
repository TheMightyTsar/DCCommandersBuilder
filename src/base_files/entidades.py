from __future__ import annotations  # Enable postponed evaluation of type annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

# Parametros


class Direccion(Enum):
    ARRIBA = (0, -1)
    ABAJO = (0, 1)
    DERECHA = (1, 0)
    IZQUIERDA = (-1, 0)


class Arma(Enum):
    TORPEDO = 1
    RADAR = 2


class Defensa(Enum):
    MOVER = 1
    REPARAR = 2
    ESCUDO = 3


# Metodos de envio info del usuario al handler


@dataclass
class Ataque:
    tipo: Arma  # Tipo de ataque
    posicion: tuple[int, int]  # Posicion del ataque


@dataclass
class Neutro:
    tipo: Defensa  # Tipo de defensa
    direccion: Direccion


# Metodos de envio info del handler al usuario


@dataclass
class Torpedo:
    posicion: tuple[int, int]
    barco_afectado: Barco | None | True


@dataclass
class Radar:
    posicion: tuple[int, int]
    barcos_afectados: list[Barco] | None


@dataclass
class Mover:
    direccion: tuple[int, int]
    pos_original: tuple[int, int]
    pos_final: tuple[int, int]
    barco: Barco


@dataclass
class Turno:
    """
    Clase que almacena la información de un turno
    """
    jugador: int  # Jugador 1 o 2
    accion: Torpedo | Radar | Mover | None  # Ataque o defensa


# Clases abstractas que deberá programar el usuario


class Barco(ABC):
    """
    Clase base de barco, los usuarios deben definir su metodo de accion
    """

    def __init__(
            self,
            nombre: str,
            tamano: int,
            direccion: Direccion,
            posicion: tuple[int, int]
    ) -> None:
        self.nombre = nombre
        self.tamano = tamano
        self.direccion = direccion
        self.posicion = posicion

    @abstractmethod
    def accion(self, historial_turnos: list[Turno]) -> Ataque | Neutro:
        """
        Define la forma de actuar del barco

        Parameters:
        -----------
        historial_turnos : list[Turno]
            Una lista de objetos Turno que representan el historial de turnos del juego.

        Returns:
        --------
        Ataque | Neutro
            Un objeto Ataque si el jugador decide atacar en este turno, o un objeto Neutro si el jugador decide defenderse.
        """
        pass

    def usar_arma(self, arma: Arma, posicion: tuple[int, int]) -> Ataque:
        """
        Utiliza el arma indicada en la posicion indicada
        """
        return Ataque(arma, posicion)

    def mover(self, direccion: Direccion) -> Neutro:
        """
        Desplaza el barco en la direccion indicada
        """
        return Neutro(Defensa.MOVER, direccion)

    def __str__(self) -> str:
        return self.nombre[:2]


class Almirante(ABC):
    """
    Clase base de almirante, los usuarios deben definir su metodo de administrar flota y agregar los barcos
    """

    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.barcos: list[Barco] = []
        self.agregar_flota()

    @abstractmethod
    def administrar_flota(
        self, historial_turnos: list[Turno], historial_enemigo: list[Turno]
    ) -> Ataque | Neutro:
        """
        Decide que barco actuara en el turno actual, recibe el historial de turnos y devuelve un ataque o una defensa
        """
        pass

    @abstractmethod
    def agregar_flota(self) -> None:
        """
        Agrega los barcos a la flota
        """
        pass


from utils import verificar_tablero
from random import randint


class BarcoRadar(Barco):
    def accion(self, historial_turnos) -> Ataque | Neutro:
        # Prioriza siempre radar sobre y no se mueve nunca (a menos que lo indique el almirante)
        # Por ejemplo iterar sobre  las ultimas posiciones disparadas, evaluar que paso
        # y disparar un radar a una distinta
        ultimos = historial_turnos[-6:]
        for turno in ultimos:
            if isinstance(turno.accion, Torpedo) and turno.accion.barco_afectado:
                return self.usar_arma(Arma.RADAR, turno.accion.posicion)
        else:
            return self.usar_arma(Arma.RADAR, (randint(0, 9), randint(0, 9)))


class BarcoTorpedo(Barco):
    def accion(self, historial_turnos: list[Turno]) -> Ataque | Neutro:
        # Prioriza siempre torpedo sobre radar y se mueve si en los ultimos 3 turnos no se ha movido
        # Al moverse elige la ultima posicion disparada por el enemigo
        ultimos = historial_turnos[-6:]
        for turno in ultimos:
            if turno.jugador == 1 and isinstance(turno.accion, Mover):
                break
        else:
            return self.mover(Direccion.ARRIBA)
        return self.usar_arma(Arma.TORPEDO, (randint(0, 9), randint(0, 9)))
