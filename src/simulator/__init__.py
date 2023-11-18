# pylint: disable=missing-docstring, W0212, W1510

import argparse
import importlib.util
import itertools
import os
import random
import subprocess
import sys


def prett(text, mode: str = "t"):
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
    import attrs
    import colorama
    import pyfiglet
    import tqdm

    colorama.init(convert=True)

    from src.simulator.turn_manager import TurnManager

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
BLD = colorama.Style.RESET_ALL + colorama.Style.BRIGHT
CLEAR = "cls" if os.name == "nt" else "clear"
ALL_COLORS = BLU, CYA, GRE, YEL, RED, MAG
RST = colorama.Style.RESET_ALL

COLOR_SAMPLE = random.sample(ALL_COLORS, 4)


def logo(commander1_name, commander2_name) -> None:
    _ = subprocess.run([CLEAR], shell=True)
    font = "cosmic"
    color1, color2, color3, _ = COLOR_SAMPLE
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
            f"{commander1_name}\nvs\n{commander2_name}",
            font=font,
            justify="center",
            width=os.get_terminal_size().columns,
        ),
        end="",
    )

    print(color1 + "_" * os.get_terminal_size().columns, end=RST)


bots = {"JorGeneral", "SoloAtaque", "SoloMover", "SoloScout"}

bot_files = [
    f"- {f}" for f in os.listdir(os.path.join('commanders')) if f in bots]
bot_files[bot_files.index('- JorGeneral')] += ' (default)'

commander_files = [
    f"- {f}" for f in os.listdir('commanders') if f != '.gitkeep' and f not in bots]
max_bot_length = max(len(f) for f in bot_files) + 3

formatted_files = "\n".join(f"{b.ljust(max_bot_length)} {c}" for b, c in itertools.zip_longest(
    bot_files, commander_files, fillvalue=''))

epilog = f"{MAG}Bots:{' ' * (max_bot_length - 4)}Players:\n{formatted_files}"

parser = argparse.ArgumentParser(
    description=BLD + "enfrenta dos comandantes." + YEL + " [] -> opcional.",
    epilog=epilog,
    formatter_class=argparse.RawTextHelpFormatter
)
parser._optionals.title = CYA + "syntax"
parser.add_argument(
    "-c1", "--commander1", help="nombre comandante 1", required=True
)
parser.add_argument(
    "-c2", "--commander2", help="nombre comandante 2", required=False
)
parser.add_argument(
    "-i", "--iterations", help="numero de iteraciones (> 1)", required=False, type=int, default=1,
)
if len(sys.argv) == 1:
    print(GRE)
    parser.print_help()
    print(RST)
    sys.exit()

args = parser.parse_args()

if args.iterations < 1:
    print(RED)
    print(
        prett(f"[!] {args.iterations} is not a valid number of iterations", mode="n"))
    print(GRE)
    parser.print_help()
    print()
    sys.exit()

if not args.commander2:
    args.commander2 = 'JorGeneral'

if args.commander1 == args.commander2:
    print(RED)
    print(
        prett(f"[!] {args.commander1} is already selected", mode="n"))
    print(GRE)
    parser.print_help()
    print()
    sys.exit()

valid_commanders = os.listdir('commanders')

CHECK = True
for commander in (args.commander1, args.commander2):
    if commander not in valid_commanders:
        print(RED)
        print(
            prett(f"[!] {commander} is not a valid commander", mode="n"))
        CHECK = False

if not CHECK:
    print(GRE)
    parser.print_help()
    print()
    sys.exit()

logo(args.commander1, args.commander2)
print()

commanders = []

for commander in (args.commander1, args.commander2):
    pyFile = commander + '.py'
    path = 'commanders'

    pyPath = os.path.join(path, commander, pyFile)

    module_spec = importlib.util.spec_from_file_location(
        commander, pyPath)
    module = importlib.util.module_from_spec(module_spec)  # type: ignore
    module_spec.loader.exec_module(module)  # type: ignore
    commanders.append(module.Commander())

wins = {commander: 0 for commander in (args.commander1, args.commander2)}


if args.iterations == 1:
    turn_manager = TurnManager(commanders, 1)
    turn_manager.start()

else:
    pbar = tqdm.tqdm(
        iterable=range(args.iterations),
        ascii=True,
        bar_format=COLOR_SAMPLE[3] + "{bar}" + RST,
    )

    for _ in pbar:
        turn_manager = TurnManager(commanders, args.iterations)
        turn_manager.start()

        wins[str(turn_manager.winner)] += 1

    win_rates = {player: f"{wins/args.iterations:.0%}" for player,
                 wins in wins.items()}

    win_rates = dict(sorted(
        win_rates.items(), key=lambda item: item[1], reverse=True))

    print()
    print(prett("Resultados:"))
    print()
    print(
        GRE + prett(f"{list(win_rates.keys())[0]}: {list(win_rates.values())[0]}", mode="n"))
    print(
        RED + prett(f"{list(win_rates.keys())[1]}: {list(win_rates.values())[1]}", mode="n"))
    print(RST)
