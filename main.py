"""Inicia el Builder de DCCommanders"""

import sys

from installer import install_dependencies

install_dependencies()

if len(sys.argv) == 1:
    import src.builderMaster

    src.builderMaster.start()
else:
    import src.simulator
