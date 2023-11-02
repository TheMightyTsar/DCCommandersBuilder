from src.creator.commanderBuilder import buildCommander
from src.scenes import sceneHandler
from src.review import reviewHandler
import threading
import time


def start():

    running = True
    scene = 'welcome'
    sceneHandler.showScene(scene)



    while running:
        option = input('')
        scene = sceneHandler.changeScene(scene, option)
        sceneHandler.showScene(scene)

        if scene == 'building_commander':
            buildThread = threading.Thread(target=buildCommander, args=(option,))

            buildThread.start()
            buildThread.join()
            running = False

        if scene == 'review_code':
            commander_name = input()
            reviewHandler.check_code(commander_name)

            scene = 'welcome'
            sceneHandler.showScene(scene)
