import os


def prett(text, mode: str = "t"):
    if mode == "n":
        return text.center(os.get_terminal_size().columns)

    return text.title().center(os.get_terminal_size().columns)
