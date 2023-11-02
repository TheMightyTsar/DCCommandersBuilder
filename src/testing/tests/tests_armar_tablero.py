'''
Testea armar_tablero:
1. Formato de return -> lista
2. Formato de cada elemento -> lista de largo 3
3. Largo de return -> n
'''

from importlib import import_module


def test_armar_tablero_1(commanderName: str):
    user_module = import_module(
        f"created_commanders.{commanderName}.commander"
    )

    commander = user_module.Commander()

    return_list = commander.armar_tablero()

    n = 10

    # 1. Formato de return -> lista
    if not isinstance(return_list, list):
        raise TypeError("armar_tablero no retorna lista")

    # 2. Formato de cada elemento -> lista de largo 3
    for element in return_list:
        if not isinstance(element, list):
            raise TypeError("armar_tablero retorna lista con elementos que no son listas")
        if len(element) != 3:
            raise ValueError("armar_tablero retorna lista con elementos de largo incorrecto")

    # 3. Largo de return -> n
    if len(return_list) != n:
        raise ValueError("armar_tablero retorna lista de largo incorrecto")

    return True


tests = [test_armar_tablero_1]
