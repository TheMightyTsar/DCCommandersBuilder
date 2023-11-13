



import sys

if __name__ == "__main__":

    if len(sys.argv) == 1:
        import src.builderMaster
        src.builderMaster.start()
    import src.prueba

'''if __name__ == '__main__':
    commanderName = 'Sweeper'
    pyFile = commanderName + '.py'

    pyPath = path.join('commanders', commanderName, pyFile)

    module_spec = importlib.util.spec_from_file_location(
        commanderName, pyPath)

    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)


    turn_manager.TurnManager([module, module])
    # builderMaster.start()'''


