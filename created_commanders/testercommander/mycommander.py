import random

from base_classes import BaseCommander
from dicts import TUPLE_TO_COORD as tc


class MyCommander(BaseCommander):

    def set_troops(self) -> list[tuple[int, str, str]]:

        possible = [tc[(i, j)] for i in range(10) for j in range(10)]
        possible = random.sample(possible, 13)
        _dict = {
            "common": possible[0:5],
            "gauss": possible[5:7],
            "scouter": possible[7:9],
            "atc": possible[9:10],
            "grenadier": possible[10:13],
        }
        return self.instantiate_troops(_dict)

    def admin_troops(self):
        print("admin player 2")