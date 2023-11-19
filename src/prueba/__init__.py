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



def logo(player1_name, player2_name) -> None:
    _ = subprocess.run([CLEAR], shell=True)
    font = "cosmic"
    color1, color2, color3 = random.sample(COLORS, k=3)
    print(color1 + "_" * os.get_terminal_size().columns, end="\n" * 2)
    print(
        color2
        + pyfiglet.figlet_format(
            "DCCommanders",
            font=font,
            justify="center",
            width=os.get_terminal_size().columns,
        ),
        end="",
    )
    print(color1 + "_" * os.get_terminal_size().columns, end="\n" * 2 + RST)
    print(
        color3
        + pyfiglet.figlet_format(
            f"{player1_name} vs {player2_name}",
            font=font,
            justify="center",
            width=os.get_terminal_size().columns,
        ),
        end="",
    )
    print(color1 + "_" * os.get_terminal_size().columns, end=RST)



