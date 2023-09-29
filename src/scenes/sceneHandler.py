
menus = {'welcome': {'0': 'input_commander_name', '1': 'review_code'}}

def showScene(scene):
    file_name = 'src/scenes/'+scene+'.txt'
    with open(file_name) as escena:
        print(escena.read())
        pass
    pass


def changeScene(scene, option):


    next_scene = menus[scene].get(option, scene)

    return next_scene

