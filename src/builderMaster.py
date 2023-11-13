import sys
import threading

from src.prueba import turn_manager
from src.creator.commanderBuilder import buildCommander
from src.review import reviewHandler
from src.scenes import sceneHandler
from src.tableroVerification.verificar import verifyTablero


def start():

    running = True
    scene = 'welcome'
    sceneHandler.showScene(scene)

    while running:

        option = input('opcion: ')
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

            if scene == 'verificar_montarTablero':
                option = verifyTablero()
                if option == 's':
                    running = False
                    sys.exit()
                scene = 'welcome'
                sceneHandler.showScene(scene)
            if scene == 'prueba':
                turn_manager.start()
                print('salio del juego')
                scene = 'welcome'
                sceneHandler.showScene(scene)


        else:
            running = False
            sys.exit()
