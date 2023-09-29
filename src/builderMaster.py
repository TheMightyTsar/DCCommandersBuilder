from src.creator import commanderBuilder
from src.scenes import sceneHandler
from src.review import reviewHandler

def start():
    running = True
    scene = 'welcome'
    sceneHandler.showScene(scene)


    while running:
        option = input('')
        scene = sceneHandler.changeScene(scene, option)
        sceneHandler.showScene(scene)



    pass