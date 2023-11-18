"""Commander file for SoloScout."""


from src.base_files.base_classes import BaseCommander
from src.base_files.parametros import (ATACAR, GAUSS, HIMARS, MOVER, SCOUT,
                                       SOLDIER, TOWER)


class Commander(BaseCommander):
    """Commander for SoloScout."""

    def __init__(self):
        super().__init__(nombre="SoloScout")
        # Define aquí atributos adicionales para tu comandante

    def montar_tropas(self):
        # Define aquí las posciciones iniciales de tus tropas
        tropas = {
            SOLDIER: ["A0", "A1", "A2", "A3", "A4"],

            HIMARS: ["B0", "B1"],

            SCOUT: ["C0", "C1"],

            GAUSS: ["D0", "D1"],

            TOWER: ["E0"],
        }

        my_troops, troop_list = self.instanciar_tropas(tropas)

        self.tropas = my_troops

        return troop_list

    def jugar_turno(self, reporte, reporte_enemigo):
        # Completa tu código aquí
        ...
