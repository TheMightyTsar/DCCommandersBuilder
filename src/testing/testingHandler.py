
import testing.tests.tests_armar_tablero as t_armar_tablero
import testing.tests.tests_realizar_accion as t_realizar_accion


def run_tests(commanderName: str):
    for test in t_armar_tablero.tests:
        test(commanderName)
    for test in t_realizar_accion.tests:
        test(commanderName)
