import sys
import threading
import time

from src.creator.commanderBuilder import buildCommander
from src.review import reviewHandler
from src.scenes import sceneHandler


def start():

    running = True
    scene = 'welcome'
    sceneHandler.showScene(scene)

    while running:
        option = input('')

        if option == '3':
            break

        if option != 's':
            print('Scene: ', scene)
            print('Option: ', option)
            scene = sceneHandler.changeScene(scene, option)
            sceneHandler.showScene(scene)

            if scene == 'building_commander':
                buildThread = threading.Thread(
                    target=buildCommander, args=(option,))

                buildThread.start()
                buildThread.join()
                running = False

            if scene == 'review_code':
                reviewHandler.check_code(option)

                scene = 'welcome'
                sceneHandler.showScene(scene)
        else:
            running = False
            sys.exit()
