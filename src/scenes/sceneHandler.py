
menus = {'welcome': {'0': 'input_commander_name', '1': 'review_code'},
         'input_commander_name': {'0': 'building_commander'}}

invalidCharacters = [' ', 'ñ']

message = 'Usaste caracteres no validos, no ocupes espacio, ñ o simbolos raros'

def showScene(scene):
    file_name = 'src/scenes/'+scene+'.txt'
    with open(file_name) as escena:
        print(escena.read())
        pass
    pass


def changeScene(scene, option):
    next_scene = menus[scene].get(option, scene)
    if scene == 'input_commander_name':
        verificacionNombre = verifyCommanderName(option)
        if verificacionNombre:
            next_scene = menus[scene].get('0', scene)


    return next_scene


def verifyCommanderName(name):
    name = name.strip()
    notification = f'Saludos comandante {name}'
    valid = True
    print(len(name))
    if len(name) == 0:
        notification = message
        valid = False

    for char in invalidCharacters:
        if char in name:

            notification = message
            valid = False


    print("")
    print(notification)
    print("")

    return valid
