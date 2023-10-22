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


    #review_result = reviewHandler.check_code("testercommander")
    #if review_result:
    #   print("Código válido")

