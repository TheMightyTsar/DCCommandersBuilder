"""Commander file for SoloScout."""

import random

from src.base_files.base_classes import BaseCommander
from src.base_files.parametros import (
    ATACAR,
    GAUSS,
    HIMARS,
    MOVER,
    SCOUT,
    SOLDIER,
    TOWER,
)


class Commander(BaseCommander):
    """Commander SoloScout."""

    def __init__(self):
        super().__init__(nombre="SoloScout")
        # Define aquí atributos adicionales para tu comandante

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
        for _id, tropa in self.tropas.items():
            if _id in reporte_enemigo.eliminaciones:
                continue
            if tropa.tipo == SCOUT:
                return [tropa.id, ATACAR, self.obtener_posicion()]
            # Si no quedan scouts, el comandante enviara acciones invalidas

    # Define aquí tus funciones adicionales
    def obtener_posicion(self):
        return random.choice(list(self.coordenadas_validas))
