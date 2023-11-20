"""Commander file for SoloMover."""

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
    """Commander SoloMover."""

    def __init__(self):
        super().__init__(nombre="SoloMover")
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

        # Se verifican las bajas del comandante
        # Esto se realiza mediante la funcion eliminar_tropas() de BaseCommander
        self.eliminar_tropas(reporte_enemigo)

        # Se mueven las tropas del comandante cuya solicitud de movimiento fue aceptada
        # Esto se realiza mediante la funcion mover_tropas() de BaseCommander
        self.mover_tropas(reporte)

        # Se crea una lista con las posiciones actuales de las tropas del comandante
        # Esto se realiza mediante la funcion obtener_posciciones() de BaseCommander
        my_troop_pos = self.obtener_posiciones()

        # Se verifica si el enemigo detecto alguna tropa
        if reporte_enemigo.detecciones:
            # Se randomiza el orden de los id de las tropas detectadas y se itera sobre estos
            for _id in random.sample(
                reporte_enemigo.detecciones, len(reporte_enemigo.detecciones)
            ):
                # Se obtiene la instancia de la tropa detectada
                tropa = self.tropas[_id]

                # Si la tropa es una torre o gauss, se ignora ya que no se puede mover
                if tropa.tipo in [TOWER, GAUSS]:
                    continue

                # Se obtienen las posiciones a las que se puede mover la tropa
                # El metodo mover() retorna una lista de posiciones, definido en cada clase de tropa

                posibles = tropa.mover()
                random.shuffle(posibles)

                # Se itera sobre las posiciones posibles
                for pos in posibles:
                    # Si la posicion esta ocupada por una tropa aliada, se ignora
                    if pos in my_troop_pos:
                        continue

                    # Si la posicion no esta ocupada, se retorna la accion
                    return [_id, MOVER, pos]

            # ! SI SOLO UNA TORRE O UN GAUSS ES DETECTADO, EL COMANDANTE NO HACE NADA

        # Si no se detecto ninguna tropa...
        else:
            # Se randomiza el orden de las tropas del comandante
            tropas = random.sample(list(self.tropas.values()), len(self.tropas))

            # Se itera sobre las tropas
            for tropa in tropas:
                # Si la tropa es una torre o gauss, se ignora ya que no se puede mover
                if tropa.tipo in [TOWER, GAUSS]:
                    continue

                # Se obtienen las posiciones a las que se puede mover la tropa
                posibles = tropa.mover()

                random.shuffle(posibles)

                # Se itera sobre las posiciones posibles
                for pos in posibles:
                    # Si la posicion esta ocupada por una tropa aliada, se ignora
                    if pos in my_troop_pos:
                        continue

                    # Si la posicion no esta ocupada, se retorna la accion
                    return [tropa.id, MOVER, pos]

    # Define aquí tus funciones adicionales
