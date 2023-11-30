def coordenada_mas_lejana(coord1, coord2, coord_posibles, rango):
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
                    coordenada_mas_lejana = (chr(ord('A') + nueva_col), nueva_fila)
                    if coordenada_mas_lejana in coord_posibles:
                        record = coordenada_mas_lejana

    return record

# Ejemplo de uso:
# coord1 = ('C', '3')
# coord2 = ('D', '4')
# coordenada_lejana = coordenada_mas_lejana(coord1, coord2)
# print(coordenada_lejana)  # Debería imprimir la coordenada más lejana posible desde ('C', '3') a ('H', '7')

def coordenada_con_menos_vecinos(coordenadas_set):
    # Convertir las coordenadas al formato (columna, fila)
    def convertir_coordenada(coordenada):
        columnas = "ABCDEFGHIJ"
        columna = columnas.index(coordenada[0])
        fila = int(coordenada[1])
        return (columna, fila)

    conjunto_convertido = {convertir_coordenada(c) for c in coordenadas_set}

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
                vecinos_no_presentes = sum(1 for v in vecinos if v not in conjunto_convertido)

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

# Ejemplo de uso con un set casi completo
# ejemplo_set_casi_completo_columnas_letras = {f"{letra}{numero}" for letra in "ABCDEFGHIJ" for numero in range(10) if (letra, numero) != ('E', 5)}
# coordenada_con_menos_vecinos_rombo_set_modificada_columnas_letras(ejemplo_set_casi_completo_columnas_letras)


# Ejemplo de uso con un set casi completo
# ejemplo_set_casi_completo = {f"{letra}{numero}" for letra in "ABCDEFGHIJ" for numero in range(10) if (letra, numero) != ('E', 5)}
set = set({'A4', 'A7', 'A9', 'B3', 'B4', 'B6', 'B9', 'C2', 'C5', 'C7', 'D1', 'D2', 'D9', 'E0', 'E2', 'E3', 'E5', 'E7', 'E9', 'F1', 'F3', 'F6', 'G1', 'G2', 'G7', 'H0', 'H3', 'H4', 'H5', 'H6', 'H8', 'H9', 'I2', 'I6', 'I7', 'I9', 'J3', 'J4', 'J5', 'J6'}
)
print(coordenada_con_menos_vecinos(set))

