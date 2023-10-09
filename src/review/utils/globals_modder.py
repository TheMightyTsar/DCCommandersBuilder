from os import path


def add_globals_to_file(commanderName):
    '''
    Revisa las líneas originales del archivo, las guarda, y sobreescribe el
    archivo con ellas más la función get_globals.

    Retorna las líneas originales del archivo.
    '''

    original_lines = []

    with open(path.join("created_commanders", f"{commanderName}", "commander.py"), encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            original_lines.append(line)

    with open(path.join("created_commanders", f"{commanderName}", "commander.py"), "w", encoding='utf-8') as f:
        for line in original_lines:
            f.write(line)

        f.write("\n\n")
        f.write("def get_globals():\n")
        f.write("    return globals()\n")

    return original_lines


def delete_extra_lines(commanderName, original_lines):
    '''
    Mantiene únicamente las líneas originales del archivo entregado.
    '''

    with open(path.join("created_commanders", f"{commanderName}", "commander.py"), "w", encoding='utf-8') as f:
        for line in original_lines:
            f.write(line)
