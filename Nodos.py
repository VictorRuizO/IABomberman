#Autores:   -Victor Duvan Ruiz Ochoa    -1664060
#           -Sebastian Giron Arcila     -1550180
#Fecha creacion: 12 de Julio de 2019
class Nodo:

    def __init__(self,matriz,papa,player,most,profundidad):
        self.ma = matriz
        self.papa = papa
        self.playerPos=player
        self.mosterPos=most
        self.profundidad=profundidad
    def getPapa(self):

        return self.papa

    def getMatriz(self):

        return self.ma

    def getPos(self):
        return self.playerPos

    def getMos(self):
        return  self.mosterPos

    def getProfundidad(self):
        return self.profundidad