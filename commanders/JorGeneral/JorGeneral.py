"""Commander file for JorGeneral."""

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
    """Commander JorGeneral."""

    def __init__(self):
        super().__init__(nombre="JorGeneral")
        # Define aquí atributos adicionales para tu comandante
        self.attacked_cells = set()
        self.attack_priority_list = [TOWER, HIMARS, SOLDIER, GAUSS]

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

        self.eliminar_tropas(reporte_enemigo)

        self.mover_tropas(reporte)

        self.attacked_cells.update(reporte.ataques)

        if len(self.attacked_cells) == 100:
            self.attacked_cells = set()

        ids_actuales = self.obtener_ids()
        posiciones_actuales = self.obtener_posiciones()

        if reporte_enemigo.detecciones:
            for _id in random.sample(
                reporte_enemigo.detecciones, len(reporte_enemigo.detecciones)
            ):
                tropa = self.tropas[_id]

                if tropa.tipo in [TOWER, GAUSS]:
                    continue

                posibles = tropa.mover()

                for pos in posibles:
                    if pos in posiciones_actuales:
                        continue

                    return [_id, MOVER, pos]

        if reporte.detecciones:
            for _id in ids_actuales[GAUSS]:
                for coord in reporte.detecciones:
                    if coord in self.tropas[_id].atacar():
                        return [_id, ATACAR, coord]

            for priority in self.attack_priority_list:
                if ids_actuales[priority]:
                    for _id in ids_actuales[priority]:
                        pos = random.choice(reporte.detecciones)
                        return [_id, ATACAR, pos]

                else:
                    continue

        else:
            if ids_actuales[SCOUT]:
                for _id in ids_actuales[SCOUT]:
                    coord = filter(
                        lambda x: x not in self.attacked_cells, self.coordenadas_validas
                    )
                    pos = random.choice(list(coord))
                    return [_id, ATACAR, pos]

            else:
                for priority in self.attack_priority_list:
                    if priority == GAUSS:
                        for _id in ids_actuales[GAUSS]:
                            return [_id, ATACAR, self.tropas[_id].coord]

                    if ids_actuales[priority]:
                        for _id in ids_actuales[priority]:
                            pos = filter(
                                lambda x: x not in self.attacked_cells,
                                self.coordenadas_validas,
                            )
                            pos = random.choice(list(pos))
                            return [_id, ATACAR, pos]
                    else:
                        continue

    # Define aquí tus funciones adicionales
