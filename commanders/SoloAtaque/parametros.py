"""Contains all the constants used in the game."""

# Acciones del usuario
ATACAR = "atacar"
MOVER = "mover"
ACCIONES = [ATACAR, MOVER]

# Tipos de tropas
SOLDIER = "soldier"
GAUSS = "gauss"
SCOUT = "scout"
TOWER = "tower"
GRENADIER = "grenadier"

# Llaves reportes
ATACK = "ataks"
DETECT = "detectados"
BAJAS = "bajas"
MOV_SUCCESS = "success"

COORD_TO_TUPLE: dict[str, tuple[int, int]] = {
    'A0': (0, 0),
    'A1': (1, 0),
    'A2': (2, 0),
    'A3': (3, 0),
    'A4': (4, 0),
    'A5': (5, 0),
    'A6': (6, 0),
    'A7': (7, 0),
    'A8': (8, 0),
    'A9': (9, 0),

    'B0': (0, 1),
    'B1': (1, 1),
    'B2': (2, 1),
    'B3': (3, 1),
    'B4': (4, 1),
    'B5': (5, 1),
    'B6': (6, 1),
    'B7': (7, 1),
    'B8': (8, 1),
    'B9': (9, 1),

    'C0': (0, 2),
    'C1': (1, 2),
    'C2': (2, 2),
    'C3': (3, 2),
    'C4': (4, 2),
    'C5': (5, 2),
    'C6': (6, 2),
    'C7': (7, 2),
    'C8': (8, 2),
    'C9': (9, 2),

    'D0': (0, 3),
    'D1': (1, 3),
    'D2': (2, 3),
    'D3': (3, 3),
    'D4': (4, 3),
    'D5': (5, 3),
    'D6': (6, 3),
    'D7': (7, 3),
    'D8': (8, 3),
    'D9': (9, 3),

    'E0': (0, 4),
    'E1': (1, 4),
    'E2': (2, 4),
    'E3': (3, 4),
    'E4': (4, 4),
    'E5': (5, 4),
    'E6': (6, 4),
    'E7': (7, 4),
    'E8': (8, 4),
    'E9': (9, 4),

    'F0': (0, 5),
    'F1': (1, 5),
    'F2': (2, 5),
    'F3': (3, 5),
    'F4': (4, 5),
    'F5': (5, 5),
    'F6': (6, 5),
    'F7': (7, 5),
    'F8': (8, 5),
    'F9': (9, 5),

    'G0': (0, 6),
    'G1': (1, 6),
    'G2': (2, 6),
    'G3': (3, 6),
    'G4': (4, 6),
    'G5': (5, 6),
    'G6': (6, 6),
    'G7': (7, 6),
    'G8': (8, 6),
    'G9': (9, 6),

    'H0': (0, 7),
    'H1': (1, 7),
    'H2': (2, 7),
    'H3': (3, 7),
    'H4': (4, 7),
    'H5': (5, 7),
    'H6': (6, 7),
    'H7': (7, 7),
    'H8': (8, 7),
    'H9': (9, 7),

    'I0': (0, 8),
    'I1': (1, 8),
    'I2': (2, 8),
    'I3': (3, 8),
    'I4': (4, 8),
    'I5': (5, 8),
    'I6': (6, 8),
    'I7': (7, 8),
    'I8': (8, 8),
    'I9': (9, 8),

    'J0': (0, 9),
    'J1': (1, 9),
    'J2': (2, 9),
    'J3': (3, 9),
    'J4': (4, 9),
    'J5': (5, 9),
    'J6': (6, 9),
    'J7': (7, 9),
    'J8': (8, 9),
    'J9': (9, 9)
}


TUPLE_TO_COORD: dict[tuple[int, int], str] = {
    tup: coord for coord, tup in COORD_TO_TUPLE.items()}


AVAILABLE_TROOPS = {
    SOLDIER: 5,
    GAUSS: 2,
    SCOUT: 2,
    TOWER: 1,
    GRENADIER: 3,
}

if __name__ == "__main__":
    ...
