from os import mkdir, path


def buildCommander(commanderName):
    printMessage('Creando directorios del jugador')
    relativePath = 'commanders/'
    folderPath = path.join(relativePath, commanderName)
    mkdir(folderPath)

    printMessage('Creados directorio')
    printMessage('Creando modulo')

    commanderPath = 'commanders/'+commanderName+'/'
    commanderFile = commanderPath + commanderName + '.py'
    textPath = 'src/creator/modules/commanders.txt'

    with open(commanderFile, 'w') as cFile:

        with open(textPath) as baseFile:
            for line in baseFile:

                if "{commander_name}" in line:
                    line = line.replace("{commander_name}", commanderName)

                cFile.write(line)
    printMessage('Creado el modulo de comandante')


def printMessage(msg):
    print('...')
    print(msg + '...')
    print('...')
