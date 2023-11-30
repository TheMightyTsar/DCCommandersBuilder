"""Commander file for himars."""
import itertools
import random

from commanders.Cocommander.clasesBase import (BaseCommander, Gauss, Himars,
                                               Scout, Soldier, Tower)
from commanders.Cocommander.parametros import (ATACAR, GAUSS, HIMARS, MOVER,
                                               SCOUT, SOLDIER, TOWER)


class Commander(BaseCommander):
    """Commander Cocommander."""

    def __init__(self):
        super().__init__(nombre="Cocommander")
        self.lista_tropas = []
        self.gauss_1 = True
        self.gauss_2 = True
        self.torre = True
        self.scout_bool = True
        self.reset = False
        self.attacked_cells = set()
        # Define aquí atributos adicionales para tu comandante

    def montar_tropas(self):
        # Define aquí las posciciones iniciales de tus tropas

        self.Soldier0 = Soldier('A2')
        self.lista_tropas.append(self.Soldier0)

        self.Soldier1 = Soldier('D3')
        self.lista_tropas.append(self.Soldier1)

        self.Soldier2 = Soldier('G4')
        self.lista_tropas.append(self.Soldier2)

        self.Soldier3 = Soldier('I7')
        self.lista_tropas.append(self.Soldier3)

        self.Soldier4 = Soldier('D6')
        self.lista_tropas.append(self.Soldier4)

        self.Scout0 = Scout('E1')
        self.lista_tropas.append(self.Scout0)

        self.Scout1 = Scout('I5')
        self.lista_tropas.append(self.Scout1)

        self.Himars0 = Himars('B4')
        self.lista_tropas.append(self.Himars0)

        self.Himars1 = Himars('F8')
        self.lista_tropas.append(self.Himars1)

        self.Gauss0 = Gauss('C9')
        self.lista_tropas.append(self.Gauss0)

        self.Gauss1 = Gauss('H0')
        self.lista_tropas.append(self.Gauss1)

        self.Torre0 = Tower('J2')
        self.lista_tropas.append(self.Torre0)

        # p = random.sample(self.coordenadas_validas, 12)

        # self.Soldier0 = Soldier(p[0])
        # self.lista_tropas.append(self.Soldier0)

        # self.Soldier1 = Soldier(p[1])
        # self.lista_tropas.append(self.Soldier1)

        # self.Soldier2 = Soldier(p[2])
        # self.lista_tropas.append(self.Soldier2)

        # self.Soldier3 = Soldier(p[3])
        # self.lista_tropas.append(self.Soldier3)

        # self.Soldier4 = Soldier(p[4])
        # self.lista_tropas.append(self.Soldier4)

        # self.Scout0 = Scout(p[5])
        # self.lista_tropas.append(self.Scout0)

        # self.Scout1 = Scout(p[6])
        # self.lista_tropas.append(self.Scout1)

        # self.Himars0 = Himars(p[7])
        # self.lista_tropas.append(self.Himars0)

        # self.Himars1 = Himars(p[8])
        # self.lista_tropas.append(self.Himars1)

        # self.Gauss0 = Gauss(p[9])
        # self.lista_tropas.append(self.Gauss0)

        # self.Gauss1 = Gauss(p[10])
        # self.lista_tropas.append(self.Gauss1)

        # self.Torre0 = Tower(p[11])
        # self.lista_tropas.append(self.Torre0)

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

        self.tropas = {
            SOLDIER: [self.Soldier0, self.Soldier1, self.Soldier2, self.Soldier3, self.Soldier4],
            HIMARS: [self.Himars0, self.Himars1],
            SCOUT: [self.Scout0, self.Scout1],
            GAUSS: [self.Gauss0, self.Gauss1],
            TOWER: [self.Torre0],
        }

        self.coordenadas_scout = itertools.cycle(
            ['C2', 'C7', 'H7', 'H2', 'E4'])
        self.coordenadas_torre = itertools.cycle(
            ['A4', 'J5', 'B5', 'I4', 'F8', 'E1', 'D5', 'G5', 'C3', 'H6'])
        self.coordenadas_scout_2 = itertools.cycle(
            ['B8', 'F9', 'E6', 'I8', 'H6', 'B5', 'E3', 'I4', 'I1', 'E0', 'B2', 'C2', 'C7', 'H7', 'H2', 'E4'])

        self.columnas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.filas = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.coordenadas = list(itertools.product(self.columnas, self.filas))
        for cord in self.coordenadas:
            ''.join(cord)

        self.priority_list = [HIMARS, TOWER, SOLDIER, SCOUT]

        return orden

    def coordenada_mas_lejana(self, coord1, coord2, coord_posibles, rango):
        # Crear un diccionario para mapear letras de columna a índices numéricos
        columna_a_indice = {chr(ord('A') + i): i for i in range(10)}

        # Convertir las coordenadas de entrada en índices numéricos
        fila1, col1 = int(coord1[1]), columna_a_indice[coord1[0]]
        fila2, col2 = int(coord2[1]), columna_a_indice[coord2[0]]

        # Definir todas las direcciones posibles de movimiento
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        max_distancia = -1
        coordenada_mas_lejana = None

        # Recorrer todas las direcciones y distancias posibles
        for dx, dy in direcciones:
            for i in range(1, rango + 1):  # Máximo 3 movimientos
                nueva_fila = fila1 + i * dx
                nueva_col = col1 + i * dy

                # Verificar si la nueva fila y columna están dentro del rango del tablero
                if 0 <= nueva_fila < 10 and 0 <= nueva_col < 10:
                    # Calcular la distancia desde la nueva coordenada a coord2
                    d = abs(nueva_fila - fila2) + abs(nueva_col - col2)

                    if d > max_distancia:
                        max_distancia = d
                        coordenada_mas_lejana = (
                            chr(ord('A') + nueva_col), nueva_fila)
                        if coordenada_mas_lejana[0]+str(coordenada_mas_lejana[1]) in coord_posibles:
                            record = coordenada_mas_lejana[0] + \
                                str(coordenada_mas_lejana[1])

        return record

    def coordenada_con_menos_vecinos(self, coordenadas_set):
        # Convertir las coordenadas al formato (columna, fila)
        def convertir_coordenada(coordenada):
            columnas = "ABCDEFGHIJ"
            columna = columnas.index(coordenada[0])
            fila = int(coordenada[1])
            return (columna, fila)

        conjunto_convertido = {
            convertir_coordenada(c) for c in coordenadas_set}

        # Función para obtener los vecinos en forma de rombo de una coordenada
        def obtener_vecinos_rombo_correcto(coordenada):
            vecinos = []

            # Coordenadas directamente a la izquierda y derecha
            for i in [-2, 2]:
                c = coordenada[0] + i
                if 0 <= c < 10:
                    vecinos.append((c, coordenada[1]))

            # Coordenadas directamente arriba y abajo
            for i in [-2, 2]:
                f = coordenada[1] + i
                if 0 <= f < 10:
                    vecinos.append((coordenada[0], f))

            # Coordenadas diagonales y adyacentes
            for i in range(-1, 2):  # -1, 0, 1
                for j in range(-1, 2):  # -1, 0, 1
                    if i == 0 and j == 0:
                        continue  # Ignorar la coordenada central
                    c = coordenada[0] + i
                    f = coordenada[1] + j
                    if 0 <= c < 10 and 0 <= f < 10:
                        vecinos.append((c, f))

            return vecinos

        # Si el conjunto tiene todas las celdas menos una, retornar esa celda
        if len(conjunto_convertido) == 99:
            for columna in range(10):
                for fila in range(10):
                    if (columna, fila) not in conjunto_convertido:
                        columnas = "ABCDEFGHIJ"
                        return f"{columnas[columna]}{fila}"

        # Contar los vecinos no presentes en el conjunto para cada coordenada del tablero
        max_vecinos_no_presentes = -1
        coordenada_seleccionada = None

        for columna in range(10):
            for fila in range(10):
                coordenada_actual = (columna, fila)
                if coordenada_actual not in conjunto_convertido:
                    vecinos = obtener_vecinos_rombo_correcto(coordenada_actual)
                    vecinos_no_presentes = sum(
                        1 for v in vecinos if v not in conjunto_convertido)

                    if vecinos_no_presentes > max_vecinos_no_presentes:
                        max_vecinos_no_presentes = vecinos_no_presentes
                        coordenada_seleccionada = coordenada_actual

        # Convertir la coordenada seleccionada de vuelta al formato original
        if coordenada_seleccionada:
            columnas = "ABCDEFGHIJ"
            columna_letra = columnas[coordenada_seleccionada[0]]
            fila_numero = coordenada_seleccionada[1]
            return f"{columna_letra}{fila_numero}"
        else:
            return "No hay coordenadas disponibles"

    def coordenada_con_menos_vecinos_soldier(self, coordenadas_set):
        # Convertir las coordenadas al formato (columna, fila)
        def convertir_coordenada(coordenada):
            columnas = "ABCDEFGHIJ"
            columna = columnas.index(coordenada[0])
            fila = int(coordenada[1])
            return (columna, fila)

        conjunto_convertido = {
            convertir_coordenada(c) for c in coordenadas_set}

        # Función para obtener las tres casillas detrás de una coordenada
        def obtener_tres_atras(coordenada):
            tres_atras = []
            columna_anterior = coordenada[0] - 1
            if columna_anterior >= 0:  # Asegurarse de que no esté fuera del tablero
                for i in range(-1, 2):  # -1, 0, 1
                    fila = coordenada[1] + i
                    if 0 <= fila < 10:
                        tres_atras.append((columna_anterior, fila))
            return tres_atras

        # Contar los vecinos no presentes en el conjunto para cada coordenada del tablero
        max_vecinos_no_presentes = -1
        coordenada_seleccionada = None

        for columna in range(10):
            for fila in range(10):
                coordenada_actual = (columna, fila)
                if coordenada_actual not in conjunto_convertido:
                    tres_atras = obtener_tres_atras(coordenada_actual)
                    vecinos_no_presentes = sum(
                        1 for v in tres_atras if v not in conjunto_convertido)

                    if vecinos_no_presentes > max_vecinos_no_presentes:
                        max_vecinos_no_presentes = vecinos_no_presentes
                        coordenada_seleccionada = coordenada_actual

        # Convertir la coordenada seleccionada de vuelta al formato original
        if coordenada_seleccionada:
            columnas = "ABCDEFGHIJ"
            columna_letra = columnas[coordenada_seleccionada[0]]
            fila_numero = coordenada_seleccionada[1]
            return f"{columna_letra}{fila_numero}"
        else:
            return "No hay coordenadas disponibles"

    def coordenada_con_menos_vecinos_misma_columna(self, coordenadas_set):
        # Convertir las coordenadas al formato (columna, fila)
        def convertir_coordenada(coordenada):
            columnas = "ABCDEFGHIJ"
            columna = columnas.index(coordenada[0])
            fila = int(coordenada[1])
            return (columna, fila)

        conjunto_convertido = {
            convertir_coordenada(c) for c in coordenadas_set}

        # Función para obtener los vecinos en la misma columna de una coordenada
        def obtener_vecinos_misma_columna(coordenada):
            vecinos = []
            columna = coordenada[0]
            for fila in range(10):
                if fila != coordenada[1]:  # Excluir la coordenada actual
                    vecinos.append((columna, fila))
            return vecinos

        # Contar los vecinos no presentes en el conjunto para cada coordenada del tablero
        max_vecinos_no_presentes = -1
        coordenada_seleccionada = None

        for columna in range(10):
            for fila in range(10):
                coordenada_actual = (columna, fila)
                if coordenada_actual not in conjunto_convertido:
                    vecinos = obtener_vecinos_misma_columna(coordenada_actual)
                    vecinos_no_presentes = sum(
                        1 for v in vecinos if v not in conjunto_convertido)

                    if vecinos_no_presentes > max_vecinos_no_presentes:
                        max_vecinos_no_presentes = vecinos_no_presentes
                        coordenada_seleccionada = coordenada_actual

        # Convertir la coordenada seleccionada de vuelta al formato original
        if coordenada_seleccionada:
            columnas = "ABCDEFGHIJ"
            columna_letra = columnas[coordenada_seleccionada[0]]
            fila_numero = coordenada_seleccionada[1]
            return f"{columna_letra}{fila_numero}"
        else:
            return "No hay coordenadas disponibles"

    def jugar_turno(self, reporte, reporte_enemigo) -> list[int | str]:
        self.attacked_cells.update(reporte.ataques)
        # Completa tu código aquí
        self.eliminar_tropas(reporte_enemigo)

        self.mover_tropas(reporte)

        if len(self.attacked_cells) == 100:
            self.attacked_cells = set()

        # Movemos HIMARS si lo scoutean
        if self.tropas_detectadas(reporte_enemigo):
            coord_scout = reporte_enemigo.ataques[0]

            if self.Himars0.id in self.tropas_detectadas(reporte_enemigo):
                posibles = self.Himars0.mover()
                # ojala mover maximo posible
                pos = self.coordenada_mas_lejana(
                    self.Himars0.coord, coord_scout, posibles, 2)
                return [self.Himars0.id, MOVER, pos]

            elif self.Himars1.id in self.tropas_detectadas(reporte_enemigo):
                posibles = self.Himars1.mover()
                # ojala mover maximo posible
                pos = self.coordenada_mas_lejana(
                    self.Himars1.coord, coord_scout, posibles, 2)
                return [self.Himars1.id, MOVER, pos]

            else:
                if len(self.tropas[SOLDIER]) < 1:
                    for soldier in self.tropas[SOLDIER]:
                        if soldier.id in self.tropas_detectadas:
                            sol = soldier
                            posibles = sol.mover()
                            pos = self.coordenada_mas_lejana(
                                sol.coord, coord_scout, posibles, 3)
                            return [sol.id, MOVER, pos]

        if self.gauss_1 or self.gauss_2:
            if self.gauss_1 and self.Gauss0 in self.tropas[GAUSS]:
                self.gauss_1 = False
                return [self.Gauss0.id, ATACAR, self.Gauss0.coord]

            elif self.gauss_2 and self.Gauss1 in self.tropas[GAUSS]:
                self.gauss_2 = False
                return [self.Gauss1.id, ATACAR, self.Gauss1.coord]

        if self.torre and self.Torre0 in self.tropas[TOWER]:
            pos = next(self.coordenadas_torre)
            if pos == 'H6':
                self.torre = False
            return [self.Torre0.id, ATACAR, pos]

        if reporte.detecciones:
            coor = random.choice(reporte.detecciones)
            if 'A' in coor or 'J' in coor:
                if self.Torre0 in self.tropas[TOWER]:
                    return [self.Torre0.id, ATACAR, coor]
            elif self.Himars0 in self.tropas[HIMARS]:
                return [self.Himars0.id, ATACAR, coor]
            elif self.Himars1 in self.tropas[HIMARS]:
                return [self.Himars1.id, ATACAR, coor]
            else:
                if len(self.tropas[SOLDIER]) > 0:
                    return [self.tropas[SOLDIER][0].id, ATACAR, coor]
                elif len(self.tropas[SCOUT]) > 0:
                    pos = filter(
                        lambda x: x not in self.attacked_cells,
                        self.coordenadas_validas,
                    )
                    pos = random.choice(list(pos))
                    return [self.tropas[SCOUT][0].id, ATACAR, pos]
                else:
                    return [self.tropas[GAUSS][0].id, ATACAR, self.tropas[GAUSS][0].coord]

        for priority in self.priority_list:

            if priority == TOWER:
                if len(self.tropas[priority]) > 0:
                    pos = self.coordenada_con_menos_vecinos_misma_columna(
                        self.attacked_cells)
                    return [self.Torre0.id, ATACAR, pos]

            elif priority == HIMARS:
                if len(self.tropas[HIMARS]) > 0:
                    pos = self.coordenada_con_menos_vecinos(
                        self.attacked_cells)
                    return [self.tropas[HIMARS][0].id, ATACAR, pos]

            elif priority == SOLDIER:
                if len(self.tropas[SOLDIER]) > 0:
                    pos = self.coordenada_con_menos_vecinos_soldier(
                        self.attacked_cells)
                    return [self.tropas[SOLDIER][0].id, ATACAR, pos]

            elif priority == SCOUT:
                if len(self.tropas[SCOUT]) > 0:
                    pos = self.coordenada_con_menos_vecinos(
                        self.attacked_cells)
                    return [self.tropas[SCOUT][0].id, ATACAR, pos]

        return [self.tropas[GAUSS][0].id, ATACAR, self.tropas[GAUSS][0].coord]
