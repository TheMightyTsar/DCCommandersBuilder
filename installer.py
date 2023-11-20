"""Dependencies installer."""

import subprocess
import sys

from src.base_files.parametros import COMMANDS
from src.base_files.utils import prett


def install_dependencies():
    """Checks if all dependencies are installed and if not, installs them."""
    try:
        import attrs
        import colorama
        import pyfiglet
        import tqdm

        colorama.init(convert=True)

    except ModuleNotFoundError:
        print(
            "\x1b[1m\x1b[31m"
            + prett("[!] Missing dependencies, installing them now...")
            + "\x1b[0m"
        )

        for cmd in COMMANDS:
            print(
                "\x1b[1m\x1b[33m"
                + prett(f"[*] trying: {' ' .join(cmd)}", mode="n")
                + "\x1b[0m"
            )
            if subprocess.run(cmd, shell=True).returncode == 0:
                print("\x1b[1m\x1b[92m" + prett("[+] dependencies installed"))
                print("\x1b[1m\x1b[92m" + prett("[+] run the program again"))
                sys.exit("\x1b[0m")

            else:
                print("\x1b[1m\x1b[31m" + prett("[!] failed.") + "\033[0m\n")

                if cmd == COMMANDS[-1]:
                    print(
                        "\x1b[1m\x1b[31m"
                        + prett("[!] an error occured while installing dependencies")
                    )
                    print(
                        "\x1b[1m\x1b[34m"
                        + prett(
                            "[?] Maybe pip isn't installed or requirements.txt is missing?\n",
                            mode="n",
                        )
                    )

                continue

        sys.exit("\x1b[0m")
