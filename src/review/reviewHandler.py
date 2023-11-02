import importlib
import types
from os import path

from src.review.utils.globals_modder import (
    add_globals_to_file,
    delete_extra_lines
)
from src.review.utils.print_styles import (
    print_test_pass,
    print_test_fail
)

import sys
from src.review.reviewExceptions import ModuloNoPermitido, FuncionNoPermitida
from src.review.utils.mock_vars import mock_informe_1


def check_code(commanderName):
    # debe retornar True si el codigo es Valido
    print(f"Validando commander.py de {commanderName}... ")
    try:
        print("- Test funciones prohibidas...", end="")
        check_forbidden_builtins(commanderName)
        print_test_pass()

        print("- Test sintaxis...", end="")
        user_module = importlib.import_module(
            f"created_commanders.{commanderName}.commander"
        )
        print_test_pass()

        print("- Test modulos importados...", end="")
        check_imported_modules(commanderName, user_module)
        print_test_pass()

        print("- Test estructura...", end="")
        check_commander_structure(user_module)
        print_test_pass()

    except FuncionNoPermitida as error:
        print_test_fail()
        print("Código commander.py inválido")
        print(f"Motivo: {error.args[0]}")
        error.imprimir_funciones_invalidas()
        return False

    except ModuloNoPermitido as error:
        print_test_fail()
        print("Código commander.py inválido")
        print(f"Motivo: {error.args[0]}")
        error.imprimir_modulos_invalidos()
        return False

    except (NameError, AttributeError, TypeError) as error:
        print_test_fail()
        print("Código commander.py inválido")
        print(f"Motivo: {error.args[0]}")
        return False

    except SyntaxError as error:
        print_test_fail()
        print("Código commander.py inválido")
        print("Motivo: Error de sintaxis")
        print("----")
        print(f"Línea: {error.lineno}\n")
        print(error.text, end="")
        print((error.offset - 1) * " " + "^\n")
        print("SyntaxError:", error.msg)
        return False

    return True


def check_forbidden_builtins(commanderName):
    # Leer archivo commander.py en busca de " exec("" o " eval("
    # Si se encuentra, levantar excepción

    lines = []

    with open(path.join("created_commanders", f"{commanderName}", "commander.py"), encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        msg = []
        if ' exec(' in line or line[0:5] == 'exec(':
            msg.append("exec")
        if ' eval(' in line or line[0:5] == 'eval(':
            msg.append("eval")
        if msg:
            raise FuncionNoPermitida(
                msg, "Se han encontrado funciones no permitidas:")


# Definir tester de modulos importados
def check_imported_modules(commanderName, user_module):
    '''
    Revisa si los módulos importadoes en el código del usuario son válidos.
    En caso de encontrar módulos inválidos, levanta una excepción con los
    nombres de los módulos no permitido.
    En caso contrario, no retorna nada.
    '''

    modules_whitelist = [
        "itertools", "importlib", "sys", "math", "random", "time"
    ]

    functions_blacklist = [
        "rmdir", "mkdir"
    ]

    # Modificar archivo commander.py para agregar función get_globals
    original_lines = add_globals_to_file(commanderName)

    # Re-importar modulo usuario
    user_module = importlib.import_module(
        f"created_commanders.{commanderName}.commander"
    )
    user_module = importlib.reload(user_module)
    modules_whitelist.append(f"created_commanders.{commanderName}.commander")
    modules_whitelist.append(f"created_commanders.{commanderName}")
    modules_whitelist.append("created_commanders")

    # Obtener todos los módulos importados
    all_globals = user_module.get_globals()

    modules = []
    functions = []
    for name, val in all_globals.items():
        # Filtra solo aquellas variables que son modulos
        if isinstance(val, type(sys)):
            modules.append(name)
        elif isinstance(val, types.BuiltinFunctionType):
            functions.append(name)

    # Eliminar líneas agregadas a commander.py
    delete_extra_lines(commanderName, original_lines)

    invalid_modules = []
    for module in modules:
        if module not in modules_whitelist:
            # Problemas
            invalid_modules.append(module)

    for func in functions:
        if func in functions_blacklist:
            invalid_modules.append(func)

    if invalid_modules:
        raise ModuloNoPermitido(
            invalid_modules, "Se han encontrado módulos no permitidos:")


def check_commander_structure(user_module):
    '''
    Revisa si el código para la clase Commander es válido o no.
    Debe poder instanciarse con los argumentos requeridos, y deben existir
    los métodos necesarios.
    '''

    # Importar archivo creado por usuario con commanderName

    try:
        commander = user_module.Commander()
    except (NameError, AttributeError):
        raise NameError(
            "No se ha encontrado la clase Commander en commander.py.")
    except TypeError:
        raise TypeError(
            "La clase Commander no debe recibir argumentos.")

    # Revisar si la clase Commander tiene los atributos necesarios
    try:
        commander.atr1
    except AttributeError:
        raise AttributeError(
            "No se ha encontrado el atributo atr1 en la clase Commander.")

    # Revisar si la clase Commander tiene los métodos necesarios
    try:
        commander.set_troops()
    except AttributeError:
        raise AttributeError(
            "No se ha encontrado el método obligatorio \"armar_tablero\" en la clase Commander.")

    try:
        commander.admin_troops(mock_informe_1)
    except AttributeError:
        raise AttributeError(
            "No se ha encontrado el método obligatorio \"armar_tablero\" en la clase Commander.")
