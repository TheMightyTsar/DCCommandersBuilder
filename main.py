
import sys

if __name__ == "__main__":

    if len(sys.argv) == 1:
        import src.builderMaster

        src.builderMaster.start()

    else:
        import src.prueba

