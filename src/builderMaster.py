# pylint: disable=W1510

import os
import subprocess
import sys
import threading

from src.creator.commanderBuilder import buildCommander
from src.review import reviewHandler
from src.scenes import sceneHandler
from src.tableroVerification.verificar import verifyTablero


def start():
    clear = "cls" if os.name == "nt" else "clear"
    _ = subprocess.run(clear, shell=True, check=True)

    running = True
    scene = "welcome"
    sceneHandler.showScene(scene)
    message = "opcion :"
    while running:

        option = input(message)
        message = "opcion :"
        if option.lower() != "s":
            scene = sceneHandler.changeScene(scene, option)
            sceneHandler.showScene(scene)

            if scene == "input_commander_name":
                message = "Introduce el nombre de tu nuevo Commander: "


            if scene == "building_commander":


                buildThread = threading.Thread(target=buildCommander, args=(option,))

                buildThread.start()
                buildThread.join()
                running = False

            if scene == "review_code":
                commander_name = input("Nombre del Commander: ")
                reviewHandler.check_code(commander_name)

                scene = "welcome"
                sceneHandler.showScene(scene)

            if scene == "verificar_montarTablero":
                option = verifyTablero()
                if option == "s":
                    running = False
                    sys.exit()
                scene = "welcome"
                sceneHandler.showScene(scene)

            if scene == "test":
                c1 = input()

                try:
                    if (
                        subprocess.run(
                            ["python", "main.py", "-c1", c1], shell=True
                        ).returncode
                        == 0
                    ):
                        pass

                    elif (
                        subprocess.run(
                            ["python3", "main.py", "-c1", c1], shell=True
                        ).returncode
                        == 0
                    ):
                        pass

                except KeyboardInterrupt:
                    pass

                finally:
                    input("Presiona enter para volver al menú.")

                    scene = "welcome"
                    sceneHandler.showScene(scene)

        else:
            running = False
