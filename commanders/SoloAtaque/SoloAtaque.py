"""Commander file for SoloAtaque."""


import random

from src.base_files.base_classes import BaseCommander
from src.base_files.parametros import (ATACAR, GAUSS, HIMARS, MOVER, SCOUT,
                                       SOLDIER, TOWER)


class Commander(BaseCommander):
    """Commander for SoloAtaque."""

    def __init__(self):
        super().__init__(nombre="SoloAtaque")
        # Define aquí atributos adicionales para tu comandante
        self.attacked_cells = set()

    def montar_tropas(self):
        # Define aquí las posciciones iniciales de tus tropas

        p = random.sample(self.coordenadas_validas, 12)

        tropas = {
            SOLDIER: [p[0], p[1], p[2], p[3], p[4]],

            HIMARS: [p[5], p[6]],

            SCOUT: [p[7], p[8]],

            GAUSS: [p[9], p[10]],

            TOWER: [p[11]],
        }

        my_troops, troop_list = self.instanciar_tropas(tropas)

        self.tropas = my_troops

        return troop_list

    def jugar_turno(self, reporte, reporte_enemigo):
        # Completa tu código aquí

        self.attacked_cells.update(reporte.ataques)
        for _id, tropa in self.tropas.items():
            if _id in reporte_enemigo.eliminaciones:
                continue
            if tropa.tipo == GAUSS:
                return [tropa.id, ATACAR, tropa.coord]
            return [tropa.id, ATACAR, self.obtener_posicion()]

    # Define aquí tus funciones adicionales

    def obtener_posicion(self):
        for pos in self.coordenadas_validas:
            if pos not in self.attacked_cells:
                return pos

        self.attacked_cells.clear()
        return random.choice(list(self.coordenadas_validas))
