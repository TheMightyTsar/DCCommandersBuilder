from commanders.v.troops.soldier import Soldier 
from commanders.v.troops.scout import Scout 
from commanders.v.troops.gauss import Gauss 
from commanders.v.troops.tower import Tower 
from commanders.v.troops.grenadier import Grenadier 

class Commander:
    def __init__(self):
        self.name ='v'


    def montar_tropas(self):
        tropas = [[]]

        return(tropas)

    def jugar_turno(self, informe, informeEnemigo):
        orden = []

        return(orden)

    def __repr__(self):
        return(self.name)