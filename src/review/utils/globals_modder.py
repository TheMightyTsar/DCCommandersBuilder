from os import path


def add_globals_to_file(commanderName):

    lineas = []

    with open(path.join("created_commanders", f"{commanderName}", "commander.py"), encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            lineas.append(line)

    lineas.append("\n\n")
    lineas.append("def get_globals():\n")
    lineas.append("    return globals()\n")

    with open(path.join("created_commanders", f"{commanderName}", "commander.py"), "w", encoding='utf-8') as f:
        for line in lineas:
            f.write(line)
