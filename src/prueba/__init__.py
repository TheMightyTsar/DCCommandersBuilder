# pylint: disable=missing-docstring, W0212, W1510

import argparse
import importlib.util
import itertools
import os
import random
import subprocess
import sys


def prett(text, mode: str = "t"):
    """
    Centers text scaled to terminal size.
    mode: t = title, n = normal
    """
    if mode == "n":
        return text.center(os.get_terminal_size().columns)

    return text.title().center(os.get_terminal_size().columns)


COMMANDS = [
    ["pip", "install", "-r", "requirements.txt"],
    ["pip3", "install", "-r", "requirements.txt"],
    ["py", "-m", "pip", "install", "-r", "requirements.txt"],
    ["py", "-m", "pip3", "install", "-r", "requirements.txt"],
    ["python", "-m", "pip", "install", "-r", "requirements.txt"],
    ["python", "-m", "pip3", "install", "-r", "requirements.txt"],
    ["python3", "-m", "pip", "install", "-r", "requirements.txt"],
    ["python3", "-m", "pip3", "install", "-r", "requirements.txt"]
]


try:
    import colorama
    import pyfiglet

    colorama.init(convert=True)

    from src.prueba.turn_manager import simulationManager

except ModuleNotFoundError:

    print(
        "\x1b[1m\x1b[31m"
        + prett("[!] Missing dependencies, installing them now...")
        + "\x1b[0m"
    )

    for cmd in COMMANDS:
        print("\x1b[1m\x1b[33m" +
              prett(f"[*] trying: {' ' .join(cmd)}", mode="n") + "\x1b[0m")
        try:
            subprocess.check_output(cmd)
            print("\x1b[1m\x1b[92m" + prett("[+] dependencies installed"))
            print("\x1b[1m\x1b[92m" + prett("[+] run the program again"))
            sys.exit("\x1b[0m")

        except subprocess.CalledProcessError:

            print(
                "\x1b[1m\x1b[31m"
                + prett("[!] failed.")
                + '\033[0m\n'
            )

            if cmd == COMMANDS[-1]:
                print(
                    "\x1b[1m\x1b[31m" +
                    prett("[!] an error occured while installing dependencies")
                )
                print(
                    "\x1b[1m\x1b[34m" +
                    prett(
                        "[?] Maybe pip isn't installed or requirements.txt is missing?\n", mode="n")
                )

            continue

    sys.exit("\x1b[0m")


BLU = colorama.Style.BRIGHT + colorama.Fore.BLUE
CYA = colorama.Style.BRIGHT + colorama.Fore.CYAN
GRE = colorama.Style.BRIGHT + colorama.Fore.GREEN
YEL = colorama.Style.BRIGHT + colorama.Fore.YELLOW
RED = colorama.Style.BRIGHT + colorama.Fore.RED
MAG = colorama.Style.BRIGHT + colorama.Fore.MAGENTA
CLEAR = "cls" if os.name == "nt" else "clear"
COLORS = BLU, CYA, GRE, YEL, RED, MAG
RST = colorama.Style.RESET_ALL



print(f'Comandantes disponibles: \n')
for C in os.listdir('commanders'):
    if C in ('SoloAtaque', 'SoloMover', 'SoloScout'):
        print(f'{C} - [BOT] creado para poner a prueba tu Commander')
    else:
        print(f'{C} - Tu Commander')
running = True
while running:
    valid = True
    p1 = input('Ingresa el nombre del Commander 1: ')
    p2 = input('Ingresa el nombre del Commander 2: ')
    commanders = []
    for commander in (p1, p2):
        pyFile = commander + '.py'
        path = 'commanders'

        if commander in os.listdir('commanders'):

            pyPath = os.path.join(path, commander, pyFile)

            module_spec = importlib.util.spec_from_file_location(
                commander, pyPath)
            module = importlib.util.module_from_spec(module_spec)  # type: ignore
            module_spec.loader.exec_module(module)  # type: ignore
            commanders.append(module)
        else:
            print('Has ingresado mal el Nombre de un commander')
            valid = False
    if valid:
        simulationManager(commanders)
