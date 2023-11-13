validPOS = ['A0', 'B0', 'C0', 'D0', 'E0', 'F0', 'G0', 'H0', 'I0', 'J0',
            'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1',
            'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2',
            'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3', 'J3',
            'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4', 'J4',
            'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5', 'J5',
            'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6', 'J6',
            'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7', 'J7',
            'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8', 'J8',
            'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9', 'J9']

validTipos = ['soldier', 'scout', 'tower', 'gauss', 'grenadier']

def verifyTablero():
    import importlib.util


    from os import listdir, path
    print(listdir('commanders'))
    message = ''
    commanderName = input('Ingresa el nombre de tu Commander: ')
    if commanderName in listdir('commanders'):
        pyFile = commanderName + '.py'

        pyPath = path.join('commanders', commanderName, pyFile)

        module_spec = importlib.util.spec_from_file_location(
            commanderName, pyPath)

        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        tablero = module.Commander().montar_tropas()
        message = '| Verificacion al Montar Tablero |\n'
        if isinstance(tablero, list):
            message += 'Lista de Tropas: TRUE \n'
            listaDeListas = True
            listID = []
            listPOS = []
            numSoldier = 0
            numGauss = 0
            numTower = 0
            numScout = 0
            numGrenadier = 0
            if len(tablero) == 13:

                for unit in tablero:
                    if not isinstance(unit, list):
                        message += f'ERROR: montar_tropas no devuelve una lista de listas ' \
                                   f'entregaste {unit}\n'
                    else:

                        if len(unit) != 3:
                            message += f'ERROR: las sublistas no tienen los 3 ' \
                                       f'elementos pedidos {unit}  \n'
                        else:
                            message += f'===============================================\n'
                            message += f'{unit}\n'
                            if not isinstance(unit[0], int):
                                message += f'ERROR: el ID entregado no es un integer: {unit} \n'
                            else:
                                if unit[0] in listID:
                                    message += f'ERROR: el ID entregado no es unico: {unit[0]}\n'
                                else:
                                    listID.append(unit[0])
                                    message += f'ID {unit[0]}: Valido y Unico \n'
                                    if not isinstance(unit[1], str):
                                        message += f'ERROR: el Tipo de tropa entregado no es un string: {unit[1]}\n'
                                    else:
                                        message += 'Tipo de Tropa es un string: TRUE \n'
                                        if unit[1] not in validTipos:
                                            message += f'ERROR: el Tipo de tropa entregado no es valido: \n' \
                                                       f'entregaste {unit[1]}\n' \
                                                       f'debes entregar uno de los siguientes valores {validTipos}\n'
                                        else:
                                            if unit[2] not in validPOS:
                                                message += f'ERROR: No has entregado una posicion valida {unit}'
                                            else:
                                                if unit[2] in listPOS:
                                                    message += f'ERROR: Has colocado dos tropas en la ' \
                                                               f'posicion {unit[2]}'
                                                else:
                                                    listPOS.append(unit[2])
                                                    message += f'Posicion {unit[2]}: Valida \n'

                                                    if unit[1] == 'soldier':
                                                        if numSoldier < 5:
                                                            numSoldier += 1
                                                        else:
                                                            message += f'ERROR: Has entregado más de 5 Soldiers'
                                                    elif unit[1] == 'scout':
                                                        if numScout < 2:
                                                            numScout += 1
                                                        else:
                                                            message += f'ERROR: Has entregado más de 2 Scout'
                                                    elif unit[1] == 'gauss':
                                                        if numGauss < 2:
                                                            numGauss += 1
                                                        else:
                                                            message += f'ERROR: Has entregado más de 1 Gauss'
                                                    elif unit[1] == 'grenadier':
                                                        if numGrenadier < 3:
                                                            numGrenadier += 1
                                                        else:
                                                            message += f'ERROR: Has entregado más de 2 Grenadier'
                                                    elif unit[1] == 'tower':
                                                        if numTower < 1:
                                                            numTower += 1
                                                        else:
                                                            message += f'ERROR: Has entregado más de 1 Tower'



            else:
                message += f'ERROR: Has entregado un numero invalido de tropas: entregaste {len(tablero)} \n'
        else:
            message += 'ERROR: montar_tropas no devuelve una lista \n'

        if 'ERROR' in message:
            message += '\n'
            message += '\n'
            message += 'TABLERO: invalido, tienes errores'
            message += '\n'
            message += '\n'
        else:
            message += '\n'
            message += '\n'
            message += 'TABLERO: Valido, felicidades :D'
            message += '\n'
            message += '\n'
    elif commanderName == 'v':
        print()
    else:
        message = 'Entregaste un nombre de un Commander que no existe ....'

    message += '\n \n [v] volver al menu .... \n [s] para salir ...'
    print(message)