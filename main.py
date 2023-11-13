"""Starts the builder or battle sim depending on the arguments passed to it."""

# ! NO IMPORTAR NADA DE src.prueba AQUI.
# ! SOLO VALIDO AL FINAL DEL ARCHIVO.

import sys

if __name__ == "__main__":

    if len(sys.argv) == 1:
        import src.builderMaster
        src.builderMaster.start()
    else:
        import src.prueba
