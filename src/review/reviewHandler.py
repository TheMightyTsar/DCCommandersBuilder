import importlib
from src.review.utils.globals_modder import (
    add_globals_to_file,
    delete_extra_lines
)
import sys
from src.review.reviewExceptions import ModuloNoPermitido


def check_code(commanderName):
    # debe retornar True si el codigo es Valido
    try:
        check_imported_modules(commanderName)

    except ModuloNoPermitido as error:
        print("Código commander.py inválido")
        print(f"Motivo: {error.args[0]}")
        error.imprimir_modulos_invalidos()
        return False

    return True


# Definir tester de modulos importados
def check_imported_modules(commanderName):
    '''
    Revisa si los módulos importadoes en el código del usuario son válidos.
    En caso de encontrar módulos inválidos, levanta una excepción con los
    nombres de los módulos no permitido.
    En caso contrario, no retorna nada.
    '''

    modules_whitelist = list(sys.modules).copy()
    modules_whitelist.extend(["math", "random", "time"])

    # Modificar archivo commander.py para agregar función get_globals
    original_lines = add_globals_to_file(commanderName)

    # commanderName -> Referencia a un directorio -> En su interior commander
    # Importar archivo creado por usuario con commanderName
    user_module = importlib.import_module(f"created_commanders.{commanderName}.commander")
    modules_whitelist.append(f"created_commanders.{commanderName}.commander")
    modules_whitelist.append(f"created_commanders.{commanderName}")
    modules_whitelist.append("created_commanders")

    # Obtener todos los módulos importados
    all_globals = user_module.get_globals()
    merge(globals(), all_globals)

    modules = []
    for name, val in all_globals.items():
        # Filtra solo aquellas variables que son modulos
        if isinstance(val, type(sys)):
            modules.append(name)

    # Eliminar líneas agregadas a commander.py
    delete_extra_lines(commanderName, original_lines)

    invalid_modules = []
    for module in modules:
        # print(module)
        if module not in modules_whitelist:
            # Problemas
            invalid_modules.append(module)
    if invalid_modules:
        raise ModuloNoPermitido(
            invalid_modules, "Se han encontrado módulos no permitidos:")


def merge(dict1: dict, dict2: dict):
    dict2.update(dict1)
