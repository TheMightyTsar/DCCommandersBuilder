from src.creator import commanderBuilder
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
            waitThread = threading.Thread(target=forceWait())
            commanderBuilder.buildCommander(option)

            waitThread.start()
            waitThread.join()
            running = False



    pass

def forceWait():
    for i in range(0, 10):
        print('...')
        time.sleep(0.5)