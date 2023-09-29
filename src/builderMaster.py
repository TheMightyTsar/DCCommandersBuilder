from src.creator import commanderBuilder
from src.scenes import sceneHandler
from src.review import reviewHandler


def start():

    pass
    review_result = reviewHandler.check_code("testercommander")
    if review_result:
        print("Código válido")
