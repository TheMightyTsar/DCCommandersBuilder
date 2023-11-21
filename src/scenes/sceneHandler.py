menus = {
    "welcome": {
        "0": "input_commander_name",
        "1": "input_review_code",
        "2": "manual",
        "3": "verificar_montarTablero",
        "4": "test",
    },
    "input_commander_name": {"0": "building_commander", "v": "welcome"},
    "input_review_code": {"0": "review_code", "v": "welcome"},
    "manual": {"v": "welcome"},
    "test": {"v": "welcome"},
    "verificar_montarTablero": {"v": "welcome"},
}

message = "Usaste caracteres no validos, no ocupes caracteres NO alfanumericos"


def showScene(scene):
    file_name = "src/scenes/" + scene + ".txt"
    with open(file_name) as escena:
        print(escena.read())
        pass
    pass


def changeScene(scene, option):
    nextScene = menus[scene].get(option, scene)

    if scene == "input_commander_name":
        verificacionNombre = verifyCommanderName(option)
        if verificacionNombre:
            nextScene = menus[scene].get("0", scene)
    if nextScene == "input_review_code" and option != "v":
        nextScene = menus[nextScene].get("0", scene)

    return nextScene


def verifyCommanderName(name):
    name = name.strip()
    notification = f"Saludos comandante {name}"
    valid = True

    valid = name.isalnum()

    if len(name) == 0:
        notification = message
        valid = False

    if not valid:
        notification = message

    print("-" * 10)
    print(notification)
    print("-" * 10)

    return valid
