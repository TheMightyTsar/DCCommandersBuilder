import subprocess
import threading

from src.creator.commanderBuilder import buildCommander
from src.review import reviewHandler
from src.scenes import sceneHandler


def start():

    running = True
    scene = 'welcome'
    sceneHandler.showScene(scene)

    while running:
        option = input('')

        if option != 's':
            scene = sceneHandler.changeScene(scene, option)
            sceneHandler.showScene(scene)

            if scene == 'building_commander':
                buildThread = threading.Thread(
                    target=buildCommander, args=(option,))

                buildThread.start()
                buildThread.join()
                running = False

            if scene == 'review_code':
                commander_name = input()
                reviewHandler.check_code(commander_name)

                scene = 'welcome'
                sceneHandler.showScene(scene)

            if scene == 'test':
                commander_name = input()

                try:
                    try:
                        subprocess.run(
                            ['python', 'main.py', '-c1', commander_name], check=True)

                        scene = 'welcome'
                        sceneHandler.showScene(scene)

                    except FileNotFoundError:
                        subprocess.run(
                            ['python3', 'main.py', '-c1', commander_name], check=True)

                        scene = 'welcome'
                        sceneHandler.showScene(scene)

                except KeyboardInterrupt:
                    scene = 'welcome'
                    sceneHandler.showScene(scene)

        else:
            running = False
