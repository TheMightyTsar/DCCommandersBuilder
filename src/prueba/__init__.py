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

    from src.prueba.turn_manager import TurnManager

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
            PASSED = True
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
            "DCComanders",
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


def parse_args():
    bot_files = [
        f"- {f}" for f in os.listdir(os.path.join('src', 'prueba', 'bots'))]
    bot_files[bot_files.index('- JorGeneral')] = '- JorGeneral (default)'
    commander_files = [
        f"- {f}" for f in os.listdir('commanders') if f != '.gitkeep']
    max_bot_length = max(len(f) for f in bot_files) + 3
    formatted_files = "\n".join(f"{b.ljust(max_bot_length)} {c}" for b, c in itertools.zip_longest(
        bot_files, commander_files, fillvalue=''))
    epilog = f"{RST}Bots:{' ' * (max_bot_length - 4)}Players:\n{formatted_files}"
    parser = argparse.ArgumentParser(
        description=RST + "enfrenta dos comandantes.".title() + YEL +
        " [] -> opcional.".title(),
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser._optionals.title = CYA + "syntax".title()
    parser.add_argument(
        "-p1", "--player1", help="nombre comandante 1".title(), required=True
    )
    parser.add_argument(
        "-p2", "--player2", help="nombre comandante 2".title(), required=False
    )
    if len(sys.argv) not in (3, 5):
        print(GRE)
        parser.print_help()
        print()
        sys.exit()
    return parser.parse_args()


args = parse_args()

if not args.player2:
    args.player2 = 'JorGeneral'

logo(args.player1, args.player2)

commanders = []

for commander in (args.player1, args.player2):
    pyFile = commander + '.py'
    path = 'commanders'

    if commander in ('SoloAtaque', 'SoloMover', 'SoloScout', 'JorGeneral'):
        path = os.path.join('src', 'prueba', 'bots')

    pyPath = os.path.join(path, commander, pyFile)

    module_spec = importlib.util.spec_from_file_location(
        commander, pyPath)
    module = importlib.util.module_from_spec(module_spec)  # type: ignore
    module_spec.loader.exec_module(module)  # type: ignore
    commanders.append(module)

TurnManager(commanders)


def start():
    pass
