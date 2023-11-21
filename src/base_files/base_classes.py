"""Contiene todas las clases necesarias para construir un DCCommander."""

from abc import ABC, abstractmethod
from itertools import chain, count

from attrs import define, field, setters, validators

from src.base_files.parametros import AVAILABLE_TROOPS
from src.base_files.parametros import COORD_TO_TUPLE as CTT
from src.base_files.parametros import GAUSS, HIMARS, SCOUT, SOLDIER, TOWER
from src.base_files.parametros import TUPLE_TO_COORD as TTC


class TroopsInSamePosition(Exception):
    """Error para cuando hay tropas en la misma posición."""


class MoreTroopsThanAllowed(Exception):
    """Error para cuando hay más tropas de las permitidas."""


class InvalidPosition(Exception):
    """Error para cuando se intenta utilizar una posicion inexistente."""


@define
class BaseTroop(ABC):
    """
    ABC para todas las tropas.

    Atributos
    ---------
    >>> id : int
    >>> tipo : str
    >>> coord : str
    >>> condicion : str

    Métodos
    -------
    >>> mover()
    >>> atacar()
    """

    id: int = field(init=False, factory=count().__next__, on_setattr=setters.frozen)
    tipo: str = field(kw_only=True, on_setattr=setters.frozen)
    coord: str = field(kw_only=True, validator=validators.in_(CTT))
    condicion: str = field(default="perfecta")

    @abstractmethod
    def mover(self) -> list[str]:
        """
        Obtiene las pocisiones validas para el movimiento de la tropa.

        Retorna
        -------
        * [coordenada, ...]
                * coordenada : str

        ESTE METODO NO MODIFICA LA POSCICION DE LA TROPA.
        -------------------------------------------------
        """

    @abstractmethod
    def atacar(self) -> list[str]:
        """
        Obtiene las pocisiones validas para el ataque de la tropa.

        Retorna
        -------
        * [coordenada, ...]
                * coordenada : str
        """


class Soldier(BaseTroop):
    """
    Tropa Soldier.

    Ataque
    ------
    * Todo el tablero

    Movimiento
    ----------
    * 3 casillas en dirección vertical u horizontal
    """

    def __init__(self, coord: str):
        super().__init__(tipo=SOLDIER, coord=coord)

    def mover(self):
        moves = []

        for i in range(-3, 4):
            moves.append((CTT[self.coord][0] + i, CTT[self.coord][1]))
            moves.append((CTT[self.coord][0], CTT[self.coord][1] + i))

        moves = [TTC[move] for move in moves if move in TTC]

        return sorted(set(moves))

    def atacar(self):
        return list(CTT.keys())


class Gauss(BaseTroop):
    """
    Tropa Gauss.

    Ataque
    ------
    * Misma fila

    Movimiento
    ----------
    * No se puede mover
    """

    def __init__(self, coord: str):
        super().__init__(tipo=GAUSS, coord=coord)

    def mover(self):
        return [self.coord]

    def atacar(self):
        return [coord for coord in CTT if coord[1] == self.coord[1]]


class Scout(BaseTroop):
    """
    Tropa Scout.

    Ataque
    ------
    * Todo el tablero

    Movimiento
    ----------
    * 2 casillas en dirección vertical u horizontal
    """

    def __init__(self, coord: str):
        super().__init__(tipo=SCOUT, coord=coord)

    def mover(self):
        moves = []

        for i in range(-2, 3):
            moves.append((CTT[self.coord][0] + i, CTT[self.coord][1]))
            moves.append((CTT[self.coord][0], CTT[self.coord][1] + i))

        moves = [TTC[move] for move in moves if move in TTC]

        return sorted(set(moves))

    def atacar(self):
        return list(CTT.keys())


class Tower(BaseTroop):
    """
    Tropa Tower.

    Ataque
    ------
    * Todo el tablero

    Movimiento
    ----------
    * No se puede mover
    """

    def __init__(self, coord: str):
        super().__init__(tipo=TOWER, coord=coord)

    def mover(self):
        return [self.coord]

    def atacar(self):
        return list(CTT.keys())


class Himars(BaseTroop):
    """
    Tropa Himars.

    Ataque
    ------
    * Todo el tablero

    Movimiento
    ----------
    * 2 casillas en dirección vertical u horizontal
    """

    def __init__(self, coord: str):
        super().__init__(tipo=HIMARS, coord=coord)

    def mover(self):
        moves = []

        for i in range(-2, 3):
            moves.append((CTT[self.coord][0] + i, CTT[self.coord][1]))
            moves.append((CTT[self.coord][0], CTT[self.coord][1] + i))

        moves = [TTC[move] for move in moves if move in TTC]

        return sorted(set(moves))

    def atacar(self):
        return list(CTT.keys())


@define
class Movement:
    """
    Movimiento de una tropa.

    Atributos
    ---------
    >>> resultado : bool
    >>> id_tropa : int
    >>> coord : str
    """

    resultado: bool
    id_tropa: int
    coord: str


@define
class Report:
    """
    Reporte de un turno.

    Atributos
    ---------
    >>> ataques : list[str]
    >>> eliminaciones : list[int | str]
    >>> detecciones : list[int | str]
    >>> movimiento : Movement | None
    """

    ataques: list[str] = field(factory=list)
    eliminaciones: list = field(factory=list)
    detecciones: list = field(factory=list)
    movimiento: Movement | None = field(default=None)


@define
class BaseCommander(ABC):
    """
    ABC para todos los comandantes.

    Atributos
    ---------
    >>> nombre : str
    >>> tropas : dict[int, BaseTroop]
    >>> coordenadas_validas : list[str]

    Métodos Obligatorios
    -------
    >>> montar_tropas()
    >>> jugar_turno(reporte: Report, reporte_enemigo: Report)

    Métodos Opcionales
    ------------------
    >>> instanciar_tropas(troops_dict: dict[str, list[str]])
    >>> eliminar_tropas(reporte_enemigo: Report)
    >>> mover_tropas(reporte: Report)
    >>> obtener_ids()
    >>> obtener_posiciones()
    """

    nombre: str = field(kw_only=True, on_setattr=setters.frozen)
    tropas: dict[int, BaseTroop] = field(init=False)
    coordenadas_validas: list[str] = field(
        init=False, factory=CTT.keys, on_setattr=setters.frozen
    )

    @abstractmethod
    def montar_tropas(self) -> list[list[int | str]]:
        """
        Función
        -------
        * Define un diccionario con las posiciones de tropas del comandante según el tipo de tropa
                * {tipo_tropa: [coordenada_tropa, ...], ...}
        * Llama al método instanciar_tropas
                * Almacena el primer resultado del método instanciar_tropas en el atributo tropas
                * Retorna el segundo resultado del método instanciar_tropas

        Retorna
        -------
        * [[id_tropa, tipo_tropa, coordenada_tropa], ...]
                * id_tropa : int
                * tipo_tropa : str
                * coordenada_tropa : str
        """

    @abstractmethod
    def jugar_turno(self, reporte: Report, reporte_enemigo: Report) -> list[int | str]:
        """
        Función
        -------
        * Lógica del comandante para jugar un turno.

        Parámetros
        ----------
        * reporte: reporte de tu turno
        * reporte_enemigo: reporte del turno del enemigo

        Estructura Reporte
        ------------------
        * ataques : list[str]
                * lista de coordenadas donde se atacó

        * eliminaciones : varia según el reporte
                * reporte : list[str]
                        * lista de tipo de tropas del oponente eliminadoas
                * reporte_enemigo : list[int]
                        * lista de ids de tus tropas eliminadas

        * detecciones : varia según el reporte
                * reporte : list[str]
                        * lista de coordenadas donde se detectaron tropas enemigas
                * reporte_enemigo : list[int]
                        * lista de ids de tus tropas detectadas

        * movimiento: objeto con los siguientes atributos o None
                * resultado : bool
                        * indica si el movimiento fue exitoso o no
                * id_tropa : int
                        * id de la tropa que se intento mover
                * coord : str
                        * coordenada a la cual se intento mover la tropa

        Retorna
        -------
        * [id_tropa, acción, coordenada]
                * id_tropa : int
                * acción : str
                * coordenada : str
        """

    def instanciar_tropas(
        self, troops_dict: dict[str, list[str]]
    ) -> tuple[dict[int, BaseTroop], list[int | str]]:
        """
        Función
        -------
        * Crea un diccionario con instancias de tropas del comandante
                * {id_tropa: instancia_tropa, ...}
        * Crea una lista con las tropas del comandante para enviar al servidor
                * [[id_tropa, tipo_tropa, coordenada_tropa], ...]

        Parámetros
        ----------
        * troops_dict: diccionario con posiciones de tropas segun su tipo
                * {tipo_tropa: [coordenada_tropa, ...], ...}

        Retorna
        -------
        * {id_tropa: instancia_tropa, ...}
                * id_tropa : int
                * instancia_tropa : BaseTroop
        * [[id_tropa, tipo_tropa, coordenada_tropa], ...]
                * id_tropa : int
                * tipo_tropa : str
                * coordenada_tropa : str
        """

        positions = list(chain.from_iterable(troops_dict.values()))

        if len(set(positions)) != len(positions):
            raise TroopsInSamePosition("Hay tropas en la misma posición")

        if len(positions) > 12:
            raise MoreTroopsThanAllowed("Hay más tropas de las permitidas")

        for troop_type, positions in troops_dict.items():
            if len(positions) > AVAILABLE_TROOPS[troop_type]:
                raise MoreTroopsThanAllowed(
                    f"Hay más tropas {troop_type} de las permitidas"
                )

        my_troops, troop_list = {}, []

        for troop_type, positions in troops_dict.items():
            for position in positions:
                try:
                    match troop_type:
                        case "soldier":
                            troop = Soldier(position)

                            my_troops[troop.id] = troop
                            troop_list.append([troop.id, troop.tipo, troop.coord])

                        case "himars":
                            troop = Himars(position)

                            my_troops[troop.id] = troop
                            troop_list.append([troop.id, troop.tipo, troop.coord])

                        case "scout":
                            troop = Scout(position)

                            my_troops[troop.id] = troop
                            troop_list.append([troop.id, troop.tipo, troop.coord])

                        case "gauss":
                            troop = Gauss(position)

                            my_troops[troop.id] = troop
                            troop_list.append([troop.id, troop.tipo, troop.coord])

                        case "tower":
                            troop = Tower(position)

                            my_troops[troop.id] = troop
                            troop_list.append([troop.id, troop.tipo, troop.coord])

                except ValueError as exc:
                    raise InvalidPosition(
                        f"La posición {position} de {troop_type} no existe"
                    ) from exc

        return my_troops, troop_list

    def eliminar_tropas(self, reporte_enemigo: Report) -> None:
        """
        Función
        -------
        * Elimina las tropas muertas del diccionario tropas

        Parámetros
        ----------
        * reporte_enemigo: reporte del turno del enemigo

        Estructura Reporte
        ------------------
        * eliminaciones : list[int]
                * lista de ids de tropas eliminadas
        """

        if reporte_enemigo.eliminaciones:
            for _id in reporte_enemigo.eliminaciones:
                try:
                    del self.tropas[_id]
                except KeyError:
                    pass

    def mover_tropas(self, reporte: Report) -> None:
        """
        Función
        -------
        * Mueve las tropas cuya solicitud de movimiento haya sido aprobada

        Parámetros
        ----------
        * reporte: reporte de tu turno

        Estructura Reporte
        ------------------
        * movimiento: objeto con los siguientes atributos o None
                * resultado : bool
                        * indica si el movimiento fue exitoso o no
                * id_tropa : int
                        * id de la tropa que se intento mover
                * coord : str
                        * coordenada a la cual se intento mover la tropa
        """

        if reporte.movimiento:
            resultado = reporte.movimiento.resultado
            id_tropa = reporte.movimiento.id_tropa
            posicion = reporte.movimiento.coord

            if resultado is True and id_tropa in self.tropas:
                self.tropas[id_tropa].coord = posicion

    def obtener_ids(self) -> dict[str, list[int]]:
        """
        Función
        -------
        * Obtiene los ids de las tropas del comandante segun su tipo

        Retorna
        -------
        * {tipo_tropa: [id_tropa, ...], ...}
                * tipo_tropa : str
                * id_tropa : int
        """

        troops = {
            SOLDIER: [],
            HIMARS: [],
            SCOUT: [],
            GAUSS: [],
            TOWER: [],
        }

        for troop in self.tropas.values():
            troops[troop.tipo].append(troop.id)

        return troops

    def obtener_posiciones(self) -> list[str]:
        """
        Función
        -------
        * Obtiene las posiciones actuales de todas las tropas

        Retorna
        -------
        * [coordenada_tropa, ...]
                * coordenada_tropa : str
        """

        troops = []

        for troop in self.tropas.values():
            troops.append(troop.coord)

        return troops

    def __repr__(self):
        return f"Commander {self.nombre}"


if __name__ == "__main__":
    pass
