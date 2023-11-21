import os


def prett(text, mode: str = "t"):
    try:
        if mode == "n":
            return text.center(os.get_terminal_size().columns)

        return text.title().center(os.get_terminal_size().columns)
    except OSError:
        return text
