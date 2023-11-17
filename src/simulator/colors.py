"""Colors for the terminal output."""

import colorama

GRN = colorama.Style.BRIGHT + colorama.Fore.GREEN   # ? MOVE
RED = colorama.Style.BRIGHT + colorama.Fore.RED     # ? HIT
YEL = colorama.Style.BRIGHT + colorama.Fore.YELLOW  # ? MISS
CYA = colorama.Style.BRIGHT + colorama.Fore.CYAN    # ? DETECT HIT
BLU = colorama.Style.BRIGHT + colorama.Fore.BLUE    # ? DETECT MISS
BLD = colorama.Style.BRIGHT
RST = colorama.Style.RESET_ALL
