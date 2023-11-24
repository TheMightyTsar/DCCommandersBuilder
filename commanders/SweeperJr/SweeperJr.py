# pylint: disable=C0103, W0201, W0611

"""Commander file for SweeperJr."""


import random

from commanders.SweeperJr.clasesBase import (
    BaseCommander,
    Gauss,
    Himars,
    Scout,
    Soldier,
    Tower,
)
from commanders.SweeperJr.parametros import (
    ATACAR,
    GAUSS,
    HIMARS,
    MOVER,
    SCOUT,
    SOLDIER,
    TOWER,
)


class Commander(BaseCommander):
    """Commander SweeperJr."""

    def __init__(self):
        super().__init__(nombre="SweeperJr")
        self.tropas: list[Soldier | Scout | Himars | Gauss | Tower] = []
        # Define aquí atributos adicionales para tu comandante
        self.prio: list[str] = [HIMARS, TOWER, SOLDIER]
        self.attacked: set[str] = set()
        self.ataques_pendientes: int = 0
        self.por_atacar: list[str] = []
        self.cantidad_eliminadas: int = 0

    def montar_tropas(self):
        # Define aquí las posciciones iniciales de tus tropas

        p = random.sample(self.coordenadas_validas, 12)

        self.Soldier0 = Soldier(p[0])
        self.tropas.append(self.Soldier0)

        self.Soldier1 = Soldier(p[1])
        self.tropas.append(self.Soldier1)

        self.Soldier2 = Soldier(p[2])
        self.tropas.append(self.Soldier2)

        self.Soldier3 = Soldier(p[3])
        self.tropas.append(self.Soldier3)

        self.Soldier4 = Soldier(p[4])
        self.tropas.append(self.Soldier4)

        self.Scout0 = Scout(p[5])
        self.tropas.append(self.Scout0)

        self.Scout1 = Scout(p[6])
        self.tropas.append(self.Scout1)

        self.Himars0 = Himars(p[7])
        self.tropas.append(self.Himars0)

        self.Himars1 = Himars(p[8])
        self.tropas.append(self.Himars1)

        self.Gauss0 = Gauss(p[9])
        self.tropas.append(self.Gauss0)

        self.Gauss1 = Gauss(p[10])
        self.tropas.append(self.Gauss1)

        self.Torre0 = Tower(p[11])
        self.tropas.append(self.Torre0)

        orden = [
            [self.Soldier0.id, self.Soldier0.tipo, self.Soldier0.coord],
            [self.Soldier1.id, self.Soldier1.tipo, self.Soldier1.coord],
            [self.Soldier2.id, self.Soldier2.tipo, self.Soldier2.coord],
            [self.Soldier3.id, self.Soldier3.tipo, self.Soldier3.coord],
            [self.Soldier4.id, self.Soldier4.tipo, self.Soldier4.coord],
            [self.Scout0.id, self.Scout0.tipo, self.Scout0.coord],
            [self.Scout1.id, self.Scout1.tipo, self.Scout1.coord],
            [self.Himars0.id, self.Himars0.tipo, self.Himars0.coord],
            [self.Himars1.id, self.Himars1.tipo, self.Himars1.coord],
            [self.Gauss0.id, self.Gauss0.tipo, self.Gauss0.coord],
            [self.Gauss1.id, self.Gauss1.tipo, self.Gauss1.coord],
            [self.Torre0.id, self.Torre0.tipo, self.Torre0.coord],
        ]

        return orden

    def jugar_turno(self, reporte, reporte_enemigo):
        # Completa tu código aquí
        self.dar_de_baja_tropas(reporte_enemigo)
        self.mover_tropas(reporte)

        self.attacked.update(reporte.ataques)

        if len(self.attacked) == 100:
            self.attacked.clear()

        if reporte.detecciones:
            self.cantidad_eliminadas = len(reporte.eliminaciones)
            self.por_atacar = reporte.detecciones
            self.ataques_pendientes = max(1, len(reporte.detecciones) - 1)

        if self.ataques_pendientes:
            self.attack_mode(self.por_atacar, self.ataques_pendientes)
        else:
            self.hunt_mode()

    # Define aquí tus funciones adicionales
    def obtener_ids(
        self, tropas: list[Soldier | Scout | Himars | Gauss | Tower]
    ) -> dict[str, list[int]]:
        """Obtiene los ids de las tropas por tipo."""
        ids: dict[str, list[int]] = {
            SOLDIER: [],
            SCOUT: [],
            HIMARS: [],
            GAUSS: [],
            TOWER: [],
        }
        for tropa in tropas:
            ids[tropa.tipo].append(tropa.id)
        return ids

    def obtener_posciciones(
        self, tropas: list[Soldier | Scout | Himars | Gauss | Tower]
    ) -> list[str]:
        """Obtiene las posciciones de las tropas por id."""
        return [tropa.coord for tropa in tropas]

    def attack_mode(self, detecciones: list[str], ataques_pendientes: int):
        """Ataca a las tropas enemigas hasta eliminar len(detecciones) o len(detecciones) -1 turnos."""

    def hunt_mode(self):
        """Busca las tropas enemigas."""

    def random_mode(self):
        """Ataca una vez que no hay scouts."""
