from os import mkdir, path


def buildCommander(commanderName):
    relativePath = 'commanders/'
    folderPath = path.join(relativePath, commanderName)
    mkdir(folderPath)

    pass
