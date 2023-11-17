from os import mkdir, path


def buildCommander(commanderName):
    printMessage('Creando directorios del jugador')
    relativePath = 'commanders/'
    folderPath = path.join(relativePath, commanderName)
    mkdir(folderPath)

    troopsFolderPath = path.join(folderPath, 'troops')
    mkdir(troopsFolderPath)
    printMessage('Creados los directorios')
    printMessage('Creando modulos')

    commanderPath = 'commanders/'+commanderName+'/'
    commanderFile = commanderPath + commanderName + '.py'
    textPath = 'src/creator/modules/commanders.txt'
    importSoldier = 'from commanders.' + commanderName + '.troops.soldier import Soldier \n'
    importScout = 'from commanders.' + commanderName + '.troops.scout import Scout \n'
    importGauss = 'from commanders.' + commanderName + '.troops.gauss import Gauss \n'
    importTower = 'from commanders.' + commanderName + '.troops.tower import Tower \n'
    importGrenadier = 'from commanders.' + commanderName + '.troops.grenadier import HIMARS \n'

    with open(commanderFile, 'w') as cFile:
        cFile.write(importSoldier)
        cFile.write(importScout)
        cFile.write(importGauss)
        cFile.write(importTower)
        cFile.write(importGrenadier)

        with open(textPath) as baseFile:
            for line in baseFile:
                if 'import' in line:
                    line = line.strip('\n') + commanderName + '.troops' + '\n'
                if 'name =' in line:
                    line = line.strip('\n') + "'" + commanderName + "'" + '\n'
                cFile.write(line)
    printMessage('Creado el modulo de comandante')

    printMessage("creando los modulos de Troops")

    abstractTroopPath = troopsFolderPath + '/baseTroop.py'
    troopsTextPath = 'src/creator/modules/masterTroop.txt'
    typeTroops = ['masterTroop.txt']
    with open(abstractTroopPath, 'w') as tFile:

        with open(troopsTextPath) as baseFile:
            for line in baseFile:
                tFile.write(line)

    printMessage('creando clase Asbtracta de tus tropas')

    importMasterTroop = 'from commanders.' + commanderName + '.troops.baseTroop import BaseTroop \n'
    soldierPath = troopsFolderPath + '/soldier.py'
    soldierTextPath = 'src/creator/modules/soldier.txt'
    escribirTroops(importMasterTroop, soldierPath, soldierTextPath)

    scoutPath = troopsFolderPath + '/scout.py'
    scoutTextPath = 'src/creator/modules/scout.txt'
    escribirTroops(importMasterTroop, scoutPath, scoutTextPath)

    gaussPath = troopsFolderPath + '/gauss.py'
    gaussTextPath = 'src/creator/modules/gauss.txt'
    escribirTroops(importMasterTroop, gaussPath, gaussTextPath)

    towerPath = troopsFolderPath + '/tower.py'
    towerTextPath = 'src/creator/modules/tower.txt'
    escribirTroops(importMasterTroop, towerPath, towerTextPath)

    grenadierPath = troopsFolderPath + '/himars.py'
    grenadierTextPath = 'src/creator/modules/grenadier.txt'
    escribirTroops(importMasterTroop, grenadierPath, grenadierTextPath)




def printMessage(msg):
    print('...')
    print(msg + '...')
    print('...')

def escribirTroops(importPath, pyPath, textPath):
    with open(pyPath, 'w') as pyFile:
        pyFile.write(importPath)
        with open(textPath, 'r') as txt:
            for line in txt:
                pyFile.write(line)
    pass