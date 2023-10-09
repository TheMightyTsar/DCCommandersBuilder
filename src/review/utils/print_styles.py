
# Code by @SimpleBinary on https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal

import os

# System call
os.system("")


# Class of different styles
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


def print_test_pass():
    print(style.GREEN + "OK" + style.RESET)


def print_test_fail():
    print(style.RED + "FAIL" + style.RESET + "\n")
