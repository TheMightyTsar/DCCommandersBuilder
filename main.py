from src import builderMaster
from src.prueba import turn_manager
import importlib.util

from os import listdir, path



if __name__ == '__main__':
    commanderName = 'JefeJorge'
    pyFile = commanderName + '.py'

    pyPath = path.join('commanders', commanderName, pyFile)

    module_spec = importlib.util.spec_from_file_location(
        commanderName, pyPath)

    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)


    turn_manager.TurnManager([module, module])
    #builderMaster.start()

