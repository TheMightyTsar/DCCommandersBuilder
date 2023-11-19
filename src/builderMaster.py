import subprocess
import threading

import sys
from src.prueba import turn_manager
from src.creator.commanderBuilder import buildCommander
from src.review import reviewHandler
from src.scenes import sceneHandler
from src.tableroVerification.verificar import verifyTablero


def start():
    running = True
    scene = "welcome"
    sceneHandler.showScene(scene)

    while running:
        option = input('opcion: ')
        if option != 's':





            scene = sceneHandler.changeScene(scene, option)
            sceneHandler.showScene(scene)

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

            if scene == 'verificar_montarTablero':
                option = verifyTablero()
                if option == 's':
                    running = False
                    sys.exit()
                scene = 'welcome'
                sceneHandler.showScene(scene)


            if scene == 'test':
                commander_name = input()

                try:
                    _ = subprocess.run(
                        ['python', 'main.py', '-c1', commander_name], check=True, shell=True)

                    scene = 'welcome'
                    sceneHandler.showScene(scene)

                except FileNotFoundError:
                    _ = subprocess.run(
                        ['python3', 'main.py', '-c1', commander_name], check=True, shell=True)

                    scene = 'welcome'
                    sceneHandler.showScene(scene)

                except KeyboardInterrupt:
                    scene = 'welcome'
                    sceneHandler.showScene(scene)


        else:
            running = False
