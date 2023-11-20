# pylint: disable=missing-docstring, W0212, W1510

import argparse
import importlib.util
import itertools
import os
import random
import subprocess
import sys

import colorama
import pyfiglet
import tqdm

from src.base_files.utils import prett
from src.review.reviewHandler import check_code
from src.simulator.turn_manager import TurnManager

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
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 160
    print(color1 + "_" * width, end="\n" * 2)
    print(
        color2
        + pyfiglet.figlet_format(
            "DCCommanders",
            font=font,
            justify="center",
            width=width,
        ),
        end="",
    )
    print(color1 + "_" * width, end="\n" * 2 + RST)
    print(
        color3
        + pyfiglet.figlet_format(
            f"{commander1_name}\nvs\n{commander2_name}",
            font=font,
            justify="center",
            width=width,
        ),
        end="",
    )

    print(color1 + "_" * width, end=RST)


bots = {"JorGeneral", "SoloAtaque", "SoloMover", "SoloScout"}

bot_files = [f"- {f}" for f in os.listdir(os.path.join("commanders")) if f in bots]
bot_files[bot_files.index("- JorGeneral")] += " (default)"

commander_files = [
    f"- {f}" for f in os.listdir("commanders") if f != ".gitkeep" and f not in bots
]
max_bot_length = max(len(f) for f in bot_files) + 3

formatted_files = "\n".join(
    f"{b.ljust(max_bot_length)} {c}"
    for b, c in itertools.zip_longest(bot_files, commander_files, fillvalue="")
)

epilog = f"{MAG}Bots:{' ' * (max_bot_length - 4)}Players:\n{formatted_files}"

parser = argparse.ArgumentParser(
    description=BLD + "enfrenta dos comandantes.".title() + YEL + " [] -> opcional.",
    epilog=epilog,
    formatter_class=argparse.RawTextHelpFormatter,
)
parser._optionals.title = CYA + "syntax"
parser.add_argument("-c1", "--commander1", help="nombre comandante 1", required=True)
parser.add_argument("-c2", "--commander2", help="nombre comandante 2", required=False)
parser.add_argument(
    "-i",
    "--iterations",
    help="numero de iteraciones (> 1)",
    required=False,
    type=int,
    default=1,
)
if len(sys.argv) not in (3, 5, 7):
    print(GRE)
    parser.print_help()
    print(RST)
    sys.exit()

args = parser.parse_args()

if args.iterations < 1:
    print(RED)
    print(prett(f"[!] {args.iterations} is not a valid number of iterations", mode="n"))
    print(GRE)
    parser.print_help()
    print()
    sys.exit()

if not args.commander2:
    args.commander2 = "JorGeneral"

if args.commander1 == args.commander2:
    print(RED)
    print(prett(f"[!] {args.commander1} is already selected", mode="n"))
    print(GRE)
    parser.print_help()
    print()
    sys.exit()

valid_commanders = os.listdir("commanders")

CHECK = True
for commander in (args.commander1, args.commander2):
    if commander not in valid_commanders:
        print(RED)
        print(prett(f"[!] {commander} is not a valid commander", mode="n"))
        CHECK = False

if not CHECK:
    print(GRE)
    parser.print_help()
    print()
    sys.exit()

if not check_code(args.commander1):
    sys.exit()
if not check_code(args.commander2):
    sys.exit()

logo(args.commander1, args.commander2)
print()

commanders = []

for commander in (args.commander1, args.commander2):
    pyFile = commander + ".py"
    path = "commanders"

    pyPath = os.path.join(path, commander, pyFile)

    module_spec = importlib.util.spec_from_file_location(commander, pyPath)
    module = importlib.util.module_from_spec(module_spec)  # type: ignore
    module_spec.loader.exec_module(module)  # type: ignore
    commanders.append(module)


wins = {commander: 0 for commander in (args.commander1, args.commander2)}


try:
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

        win_rates = {
            player: f"{wins/args.iterations:.0%}" for player, wins in wins.items()
        }

        win_rates = dict(
            sorted(win_rates.items(), key=lambda item: item[1], reverse=True)
        )

        print()
        print(prett("Resultados:"))
        print()
        print(
            GRE
            + prett(
                f"{list(win_rates.keys())[0]}: {list(win_rates.values())[0]}", mode="n"
            )
        )
        print(
            RED
            + prett(
                f"{list(win_rates.keys())[1]}: {list(win_rates.values())[1]}", mode="n"
            )
        )
        print(RST)

except KeyboardInterrupt:
    print()
    print(RED + prett("[!] keyboard interrupt"))
    print(RST)
    sys.exit()
