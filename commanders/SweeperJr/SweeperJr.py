"""Commander file for SweeperJr."""


import itertools

import numpy as np
from icecream import ic

from commanders.SweeperJr.clasesBase import (BaseCommander, Gauss, Himars,
                                             Report, Scout, Soldier, Tower)
from commanders.SweeperJr.parametros import (ATACAR, GAUSS, HIMARS, SCOUT,
                                             SOLDIER, TOWER)
from commanders.SweeperJr.parametros import TUPLE_TO_COORD as T2C


class Commander(BaseCommander):
    """Commander SweeperJr."""

    def __init__(self):
        super().__init__(nombre="SweeperJr")
        self.tropas = []
        # Define aquí atributos adicionales para tu comandante
        self.gauss_0_status = "idle"
        self.gauss_1_status = "idle"
        self.tower = itertools.cycle("JAIBHCGDFE")
        self.attacked: set[str] = set()
        self.enemy_attacks: dict[str, int] = {
            coord: 0 for coord in T2C.values()}
        self.attacked_map = np.zeros((10, 10), dtype=int)
        self.density_map = np.zeros((12, 12), dtype=float)

    def montar_tropas(self):
        # Define aquí las posciciones iniciales de tus tropas

        self.Soldier0 = Soldier("C3")
        self.tropas.append(self.Soldier0)

        self.Soldier1 = Soldier("B6")
        self.tropas.append(self.Soldier1)

        self.Soldier2 = Soldier("F1")
        self.tropas.append(self.Soldier2)

        self.Soldier3 = Soldier("F8")
        self.tropas.append(self.Soldier3)

        self.Soldier4 = Soldier("E4")
        self.tropas.append(self.Soldier4)

        self.Scout0 = Scout("D1")
        self.tropas.append(self.Scout0)

        self.Scout1 = Scout("G8")
        self.tropas.append(self.Scout1)

        self.Himars0 = Himars('H2')
        self.tropas.append(self.Himars0)

        self.Himars1 = Himars('C7')
        self.tropas.append(self.Himars1)

        self.Gauss0 = Gauss('J1')
        self.tropas.append(self.Gauss0)

        self.Gauss1 = Gauss('J8')
        self.tropas.append(self.Gauss1)

        self.Torre0 = Tower('H5')
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
                [self.Torre0.id, self.Torre0.tipo, self.Torre0.coord]
        ]

        return orden

    def jugar_turno(self, reporte, reporte_enemigo):
        # Completa tu código aquí
        self.dar_de_baja_tropas(reporte_enemigo)
        self.attacked.update(reporte.ataques)

        if self.attacked == 100:
            self.attacked = set()

        self.update_attacked_map(reporte.ataques)
        my_troops = self.obtener_ids(self.tropas)

        if my_troops[GAUSS]:
            if self.gauss_0_status == "idle":
                self.gauss_0_status = "done"
                return [self.Gauss0.id, ATACAR, self.Gauss0.coord]

            if self.gauss_1_status == "idle":
                self.gauss_1_status = "done"
                return [self.Gauss1.id, ATACAR, self.Gauss1.coord]

        if my_troops[TOWER]:
            col = next(self.tower)
            if any(map(lambda x: x.startswith(col), self.attacked)):
                row = [i for i in range(
                    10) if f"{col}{i}" not in self.attacked][0]
            else:
                max_index = np.where(self.density_map ==
                                     np.amin(self.density_map))
                row = max_index[0][0]

            return [self.Torre0.id, ATACAR, f"{col}{row}"]

        if my_troops[HIMARS]:
            max_index = np.where(self.density_map == np.amin(self.density_map))
            row, column = max_index[0][0], max_index[1][0]
            coord = T2C[(row, column)]
            return [my_troops[HIMARS][0], ATACAR, coord]

        if my_troops[SOLDIER]:
            max_index = np.where(self.density_map == np.amin(self.density_map))
            row, column = max_index[0][0], max_index[1][0]
            coord = T2C[(row, column)]
            return [my_troops[SOLDIER][0], ATACAR, coord]

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
            if tropa.condicion != "destruida":
                ids[tropa.tipo].append(tropa.id)
        return ids

    def update_attacked_map(self, attacks: list[str]) -> None:
        """Actualiza el mapa de ataques."""
        for attack in attacks:
            self.attacked_map[int(attack[1]), ord(attack[0]) - 65] += 1

        padded_attacked_map = np.pad(self.attacked_map, 2, constant_values=1)
        padded_density_map = np.zeros((14, 14), dtype=float)

        weights: np.ndarray = np.array(
            [
                [1, 2, 4, 2, 1],
                [2, 3, 6, 3, 2],
                [3, 4, 67, 4, 3],
                [2, 3, 6, 3, 2],
                [1, 2, 4, 2, 1],
            ],
            dtype=float
        ) / 133

        for i in range(2, 12):
            for j in range(2, 12):

                segment = padded_attacked_map[i - 2: i + 3, j - 2: j + 3]
                padded_density_map[i, j] = np.sum(segment * weights)

        self.density_map = padded_density_map[2:12, 2:12]
