"""Commander file for CommanderHimars."""


from commanders.CommanderHimars.clasesBase import BaseCommander, Soldier, Scout, Gauss, Himars, Tower
from commanders.CommanderHimars.parametros import (ATACAR, GAUSS, HIMARS, MOVER, SCOUT, SOLDIER, TOWER)
import random


class Commander(BaseCommander):
    """Commander CommanderHimars."""

    def __init__(self):
        super().__init__(nombre="CommanderHimars")
        self.tropas = []
        self.scout = 0
        self.soldado = 0
        self.himars = 0
        self.torre_c = 0
        self.coordenadas_scout = ["C2", "H2", "C7", "H7", "F5", "E1", "I0", "B4", "E9", "A8", "J9", "J4", "A0"]
        self.coordenadas_soldado = ["A1", "C1", "E1", "G1", "I1",
                                    "B3", "D3", "F3", "H3",
                                    "A5", "C5", "E5", "G5", "I5",
                                    "B7", "D7", "F7", "H7",
                                    "A9", "C9", "E9", "G9", "I9",
                                    "J3", "J7", "A7", "A3", "B0", "D0", "F0",
                                    "H0", "J0"]
        self.coordenadas_himars = []
        self.coordenadas_torre = []
        #["B1", "I1", "F2", "C4", "H5", "A7", "C9", "E7", "I8"]
        self.gauss = False
        self.torre = False
        self.escanear = False
        self.canones = []
        self.turno = 0
        self.casillas_atacadas = []
        self.casillas_detectadas = []

        self.destruidos_anteriores = []
        self.turno_anterior = ""
        self.ataque_anterior = ""

        self.letras = "ABCDEFGHIJ"
        for i in range(1, 8, 3):
            for j in range(0, len(self.letras), 2):
                self.coordenadas_soldado.append(self.letras[j] + str(i))
        
        for i in range(0, len(self.letras), 2):
            self.coordenadas_soldado.append(self.letras[i] + "9")

        # for i in range(0, len(self.coordenadas_soldado), 2):
        #     self.coordenadas_himars.append(self.coordenadas_soldado[i])
        self.coordenadas_himars = self.coordenadas_scout.copy()

        for i in range(len(self.letras)):
            self.coordenadas_torre.append(self.letras[i] + "4")

    def montar_tropas(self):
        # Define aquí las posciciones iniciales de tus tropas

        self.Soldier0 = Soldier('H3')
        self.tropas.append(self.Soldier0)

        self.Soldier1 = Soldier('H6')
        self.tropas.append(self.Soldier1)

        self.Soldier2 = Soldier('D7')
        self.tropas.append(self.Soldier2)

        self.Soldier3 = Soldier('F8')
        self.tropas.append(self.Soldier3)

        self.Soldier4 = Soldier('A8')
        self.tropas.append(self.Soldier4)

        self.Scout0 = Scout('B0')
        self.tropas.append(self.Scout0)

        self.Scout1 = Scout('I9')
        self.tropas.append(self.Scout1)

        self.Himars0 = Himars('E1')
        self.tropas.append(self.Himars0)

        self.Himars1 = Himars('G5')
        self.tropas.append(self.Himars1)

        self.Gauss0 = Gauss('J2')
        self.tropas.append(self.Gauss0)
        self.canones.append(self.Gauss0)

        self.Gauss1 = Gauss('A6')
        self.tropas.append(self.Gauss1)
        self.canones.append(self.Gauss1)

        self.Torre0 = Tower('C4')
        self.tropas.append(self.Torre0)


        orden = [
                [self.Soldier0.id, self.Soldier0.tipo, self.Soldier0.coord],
                [self.Soldier1.id, self.Soldier1.tipo, self.Soldier1.coord],
                [self.Soldier2.id, self.Soldier2.tipo, self.Soldier2.coord],
                [self.Soldier3.id, self.Soldier3.tipo, self.Soldier3.coord],
                [self.Soldier4.id, self.Soldier4.tipo, self.Soldier4.coord],
                [self.Scout0.id, self.Scout0.tipo, self.Scout0.coord],
                [self.Scout1.id, self.Scout1.tipo, self.Scout1.coord],
                [self.Himars0.id, self.Himars0.tipo, self.Himars0.coord],
                [self.Himars1.id, self.Himars1.tipo, self.Himars1.coord],
                [self.Gauss0.id, self.Gauss0.tipo, self.Gauss0.coord],
                [self.Gauss1.id, self.Gauss1.tipo, self.Gauss1.coord],
                [self.Torre0.id, self.Torre0.tipo, self.Torre0.coord]
                ]

        return orden

    def jugar_turno(self, reporte, reporte_enemigo):

        enemigos_destruidos = self.enemigos_destruidos(reporte_enemigo)
        # if(self.turno_anterior == "respuesta" and enemigos_destruidos != self.destruidos_anteriores):
        #     self.casillas_detectadas.remove(self.ataque_anterior)

        self.turno += 1
        self.dar_de_baja_tropas(reporte_enemigo)
        self.mover_tropas(reporte)
        self.diccionario_tropas()
        self.casillas_detectadas += self.enemigos_detectados(reporte)
        tropas_detectadas = self.tropas_detectadas(reporte_enemigo)
        casillas_atacadas = self.ataque_realizado(reporte)
        enemigo_atacadas = self.ataque_recibido(reporte_enemigo)
        

        por_atacar = list(set(self.casillas_detectadas) - set(self.casillas_atacadas))

        tropas_vivas = self.tropas_vivas(reporte_enemigo)

        if(len(tropas_detectadas) > 0):
            tropa_peligro_id = tropas_detectadas[random.randint(0, len(tropas_detectadas) - 1)]
            for i in tropas_detectadas:
                for j in self.tropas:
                    if(j.id == i):
                        if(j.tipo == SCOUT):
                            tropa_peligro_id = j.id
                        elif(j.tipo == HIMARS):
                            tropa_peligro_id = j.id
                        elif(j.tipo == SOLDIER):
                            tropa_peligro_id = j.id
            for tropa in self.tropas:
                if(tropa.id == tropa_peligro_id):
                    tropa_peligro = tropa
            
            if(tropa_peligro.tipo != GAUSS and tropa_peligro.tipo != TOWER):
                coordenadas_validas = tropa_peligro.mover()
                if(chr(ord(tropa_peligro.coord[0]) - 1) + tropa_peligro.coord[1] in set(coordenadas_validas)):
                    coordenada = chr(ord(tropa_peligro.coord[0]) - 1) + tropa_peligro.coord[1]
                elif(chr(ord(tropa_peligro.coord[0]) + 1) + tropa_peligro.coord[1] in set(coordenadas_validas)):
                    coordenada = chr(ord(tropa_peligro.coord[0]) + 1) + tropa_peligro.coord[1]
                else:
                    coordenada = coordenadas_validas[random.randint(0, len(coordenadas_validas) - 1)]

                self.destruidos_anteriores = enemigos_destruidos.copy()
                self.turno_anterior = ""
                return [tropa_peligro_id, MOVER, coordenada]
            
        else:
            torre = self.comprobar_tipo(tropas_vivas, TOWER)
            if(len(por_atacar) > 0):
                himars = self.comprobar_tipo(tropas_vivas, HIMARS)
                soldado = self.comprobar_tipo(tropas_vivas, SOLDIER)
                if(self.comprobar_gauss(0, reporte_enemigo) and por_atacar[0][1] == "2"):
                    coordenadas_validas = self.Gauss0.atacar()
                    self.turno_anterior = "respuesta"
                    self.casillas_atacadas.append(por_atacar[0])
                    self.ataque_anterior = por_atacar[0]
                    return [self.Gauss0.id, ATACAR, por_atacar[0]]
                
                elif(self.comprobar_gauss(1, reporte_enemigo) and por_atacar[0][1] == "6"):
                    coordenadas_validas = self.Gauss1.atacar()
                    self.turno_anterior = "respuesta"
                    self.casillas_atacadas.append(por_atacar[0])
                    self.ataque_anterior = por_atacar[0]
                    return [self.Gauss1.id, ATACAR, por_atacar[0]]

                elif(himars != False):
                    coordenadas_validas = set(himars.atacar())
                    if(por_atacar[0] in coordenadas_validas):
                        self.destruidos_anteriores = enemigos_destruidos.copy()
                        self.turno_anterior = "respuesta"
                        self.casillas_atacadas.append(por_atacar[0])
                        self.ataque_anterior = por_atacar[0]
                        return [himars.id, ATACAR, por_atacar[0]]
                
                elif(torre != False):
                    coordenadas_validas = torre.atacar()
                    if(por_atacar[0] in coordenadas_validas):
                        self.destruidos_anteriores = enemigos_destruidos.copy()
                        self.turno_anterior = "respuesta"
                        self.casillas_atacadas.append(por_atacar[0])
                        self.ataque_anterior = por_atacar[0]
                        return [torre.id, ATACAR, por_atacar[0]]
                
                # elif(soldado != False):
                #     coordenadas_validas = soldado.atacar()
                #     if(por_atacar[0] in coordenadas_validas):
                #         self.destruidos_anteriores = enemigos_destruidos.copy()
                #         self.turno_anterior = "respuesta"
                #         self.casillas_atacadas.append(por_atacar[0])
                #         self.ataque_anterior = por_atacar[0]
                #         return [soldado.id, ATACAR, por_atacar[0]]

            elif(self.gauss and self.comprobar_gauss(1, reporte_enemigo) != False):
                coordenadas_validas = self.Gauss1.atacar()
                self.gauss = False
                self.destruidos_anteriores = enemigos_destruidos.copy()
                self.turno_anterior = ""
                self.casillas_atacadas.append(coordenadas_validas[0])
                return [self.Gauss1.id, ATACAR, coordenadas_validas[0]]
            
            elif(self.torre and torre != False):
                self.torre = False
                self.destruidos_anteriores = enemigos_destruidos.copy()
                self.turno_anterior = ""
                return [self.Torre0.id, ATACAR, "J5"]

            else:
                himars = self.comprobar_tipo(tropas_vivas, HIMARS)
                torre = self.comprobar_tipo(tropas_vivas, TOWER)
                scout = self.comprobar_tipo(tropas_vivas, SCOUT)
                if(scout != False  and (himars != False or torre != False)):
                    self.scout += 1
                    if(self.scout > 13):
                        self.scout = 0
                    elif(self.scout == 13):
                        self.gauss = True
                        self.torre = True
                    
                    if(not self.comprobar_tipo(tropas_vivas, SOLDIER) and 
                       not self.comprobar_tipo(tropas_vivas, TOWER) and 
                       not self.comprobar_tipo(tropas_vivas, HIMARS)):
                        coordenadas_validas = scout.atacar()
                        return [scout.id, ATACAR, coordenadas_validas[random.randint(0, len(coordenadas_validas) - 1)]]
                    self.destruidos_anteriores = enemigos_destruidos.copy()
                    self.turno_anterior = "scout"
                    self.casillas_atacadas.append(self.coordenadas_scout[self.scout - 1])
                    return [scout.id, ATACAR, self.coordenadas_scout[self.scout - 1]]
                
                else:
                    soldado = self.comprobar_tipo(tropas_vivas, SOLDIER)
                    himars = self.comprobar_tipo(tropas_vivas, HIMARS)
                    torre = self.comprobar_tipo(tropas_vivas, TOWER)
                    
                    if(torre != False):
                        self.torre_c += 1
                        if(self.torre_c == 10):
                            self.torre_c = 0
                        self.destruidos_anteriores = enemigos_destruidos.copy()
                        self.turno_anterior = "torre"
                        self.casillas_atacadas.append(self.coordenadas_torre[self.torre_c - 1])
                        return [torre.id, ATACAR, self.coordenadas_torre[self.torre_c - 1]]
                    
                    elif(himars != False):
                        self.himars += 1
                        if(self.himars == 13):
                            self.himars = 0
                        self.destruidos_anteriores = enemigos_destruidos.copy()
                        self.turno_anterior = "himars"
                        self.casillas_atacadas.append(self.coordenadas_himars[self.himars - 1])
                        return [himars.id, ATACAR, self.coordenadas_himars[self.himars - 1]]

                    elif(soldado != False):
                        self.soldado += 1
                        if(self.soldado == len(self.coordenadas_soldado)):
                            self.soldado = 0
                        self.destruidos_anteriores = enemigos_destruidos.copy()
                        self.turno_anterior = "soldado"
                        self.casillas_atacadas.append(self.coordenadas_soldado[self.soldado - 1])
                        return [soldado.id, ATACAR, self.coordenadas_soldado[self.soldado - 1]]
                
        coordenadas_validas = tropas_vivas[0].atacar()
        for i in self.casillas_atacadas:
            if(i in set(coordenadas_validas)):
                coordenadas_validas.remove(i)
        self.destruidos_anteriores = enemigos_destruidos.copy()
        self.turno_anterior = ""
        return [tropas_vivas[0].id, ATACAR, coordenadas_validas[random.randint(0, len(coordenadas_validas) - 1)]]

    def diccionario_tropas(self):
        self.dict_tropas = {}
        for i in range(len(self.tropas)):
            self.dict_tropas[self.tropas[i].id] = self.tropas[i]

    def tropas_vivas(self, reporte_enemigo):
        tropas_eliminadas = reporte_enemigo.eliminaciones
        set_tropas = {i.id for i in self.tropas}
        vivas = []

        for tropa in tropas_eliminadas:
            if(tropa in set_tropas):
                set_tropas.remove(tropa)

        for i in list(set_tropas):
            vivas.append(self.dict_tropas[i])

        return vivas
    
    def comprobar_tipo(self, vivas, tipo):
        for tropa in vivas:
            if(tropa.tipo == tipo):
                return tropa
        return False
    
    def comprobar_gauss(self, indice, reporte_enemigo):
        tropas_eliminadas = reporte_enemigo.eliminaciones
        if(self.canones[indice].id in set(tropas_eliminadas)):
            return False
        return True