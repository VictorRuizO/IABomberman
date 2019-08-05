#Autores:   -Victor Duvan Ruiz Ochoa    -1664060
#           -Sebastian Giron Arcila     -1550180
#Fecha creacion: 12 de Junlo de 2019

from Nodos import *
from AgenteMonster import *
import collections
import numpy as np

class AgenteJugador:

    def __init__(self,posX,posY):
        self.x = posX
        self.y = posY


    #Metodo para hacer explotar bombas en la matriz tablero
    def explotarBomba(self, ma,pos):

        if ma[pos[0]-1][pos[1]]==2:
            ma[pos[0] - 1][pos[1]] = 0
        if ma[pos[0]+1][pos[1]]==2:
            ma[pos[0] + 1][pos[1]] =0
        if ma[pos[0]][pos[1]-1]==2:
            ma[pos[0]][pos[1]-1] = 0
        if ma[pos[0]][pos[1]+1]==2:
            ma[pos[0]][pos[1]+1] = 0

        if ma[pos[0]-1][pos[1]]==9:
            ma[pos[0] - 1][pos[1]] = 5
        if ma[pos[0]+1][pos[1]]==9:
            ma[pos[0] + 1][pos[1]] = 5
        if ma[pos[0]][pos[1]-1]==9:
            ma[pos[0]][pos[1]-1] = 5
        if ma[pos[0]][pos[1]+1]==9:
            ma[pos[0]][pos[1]+1] = 5

        ma[pos[0]][pos[1]]=0

    # Mover por amplitud
    def movePorAmplitud(self,ma,enemies):
        #print(len(enemies))
        eneCoor=np.zeros((len(enemies),2))
        for i in range(0, len(enemies)):
            eneCoor[i]=enemies[i].getPos()
        nodo = Nodo(ma,None,(self.x,self.y),eneCoor,0)
        enemy=AgenteMonster(0,0)
        cola = collections.deque()
        cola.append(nodo)

        #ciclo principal
        while True:
            elem=cola.popleft()
            xx=elem.getPos()[0]
            yy = elem.getPos()[1]
            explota=False
            #print(elem.getMatriz())
            #time.sleep(0.01)
            if elem.getMatriz()[xx][yy]==5:
                return self.win(elem)
                break
           # print(elem.getMos(),xx,yy,elem.getPos())
            abue=elem.getPapa()
            if abue!=None:
                abue=abue.getPapa()
                if abue!=None:
                    abue = abue.getPapa()
                    if abue!=None and abue.getMatriz()[abue.getPos()[0]][abue.getPos()[1]]==6:
                        explota=True


            #Rama mover a la izquierda
            if elem.getMatriz()[xx-1][yy]==0 or elem.getMatriz()[xx-1][yy]==5:
                mima=self.copiar(elem.getMatriz())
                if explota : self.explotarBomba(mima,elem.getPapa().getPapa().getPapa().getPos())
                miMos = np.zeros((len(enemies),2))

                for i in range(0, len(enemies)):
                    enemy.setPos(elem.getMos()[i][0], elem.getMos()[i][1])
                    enemy.move(mima, xx, yy)
                    miMos[i] = enemy.getPos()
                if elem.getMatriz()[xx-1][yy]==0:
                    mima[xx-1][yy]=4
                if elem.getPapa()==None or mima[xx][yy]==4:
                    mima[xx][yy]=0

                nodo2=Nodo(mima,elem,(xx-1,yy),miMos,0)
                cola.append(nodo2)

            #Rama mover a la derecha
            if elem.getMatriz()[xx+1][yy]==0 or elem.getMatriz()[xx+1][yy]==5:
                mima=self.copiar(elem.getMatriz())
                if explota : self.explotarBomba(mima,elem.getPapa().getPapa().getPapa().getPos())
                miMos = np.zeros((len(enemies),2))
                for i in range(0, len(enemies)):
                    enemy.setPos(elem.getMos()[i][0], elem.getMos()[i][1])
                    #print(enemy.getPos())
                    enemy.move(mima, xx, yy)
                    miMos[i] = enemy.getPos()
                if elem.getMatriz()[xx+1][yy]==0:
                    mima[xx+1][yy]=4
                if elem.getPapa() == None or mima[xx][yy] == 4:
                    mima[xx][yy] = 0

                nodo2=Nodo(mima,elem,(xx+1,yy),miMos,0)
                cola.append(nodo2)

            #rama mover hacia arriba
            if elem.getMatriz()[xx][yy-1]==0 or elem.getMatriz()[xx][yy-1]==5:
                mima=self.copiar(elem.getMatriz())
                if explota : self.explotarBomba(mima,elem.getPapa().getPapa().getPapa().getPos())
                miMos = np.zeros((len(enemies),2))
                for i in range(0, len(enemies)):
                    enemy.setPos(elem.getMos()[i][0], elem.getMos()[i][1])
                    enemy.move(mima, xx, yy)
                    miMos[i] = enemy.getPos()
                if elem.getMatriz()[xx][yy-1]==0:
                    mima[xx][yy-1]=4
                if elem.getPapa() == None or mima[xx][yy] == 4:
                    mima[xx][yy] = 0

                nodo2=Nodo(mima,elem,(xx,yy-1),miMos,0)
                cola.append(nodo2)

            #rama mover hacia abajo
            if elem.getMatriz()[xx][yy+1]==0 or elem.getMatriz()[xx][yy+1]==5:
                mima=self.copiar(elem.getMatriz())
                if explota : self.explotarBomba(mima,elem.getPapa().getPapa().getPapa().getPos())
                miMos = np.zeros((len(enemies),2))
                #print(miMos)
                for i in range(0, len(enemies)):
                    enemy.setPos(elem.getMos()[i][0], elem.getMos()[i][1])
                    enemy.move(mima, xx, yy)
                    miMos[i] = enemy.getPos()
                if elem.getMatriz()[xx][yy+1]==0:
                    mima[xx][yy+1]=4
                if elem.getPapa() == None or mima[xx][yy] == 4:
                    mima[xx][yy] = 0

                nodo2=Nodo(mima,elem,(xx,yy+1),miMos,0)
                cola.append(nodo2)

            #Rama poner bomba
            if not (elem.getPapa() != None and elem.getPapa().getMatriz()[xx][yy] == 6):
                if (elem.getMatriz()[xx-1][yy]==2 or
                    elem.getMatriz()[xx + 1][yy] == 2 or
                    elem.getMatriz()[xx][yy-1] == 2 or
                    elem.getMatriz()[xx][yy+1] == 2 or
                    elem.getMatriz()[xx - 1][yy] == 9 or
                    elem.getMatriz()[xx + 1][yy] == 9 or
                    elem.getMatriz()[xx][yy - 1] == 9 or
                    elem.getMatriz()[xx][yy + 1] == 9) :



                        mima=self.copiar(elem.getMatriz())
                        if explota : self.explotarBomba(mima,elem.getPapa().getPapa().getPapa().getPos())
                        miMos = np.zeros((len(enemies),2))
                        for i in range(0, len(enemies)):
                            enemy.setPos(elem.getMos()[i][0], elem.getMos()[i][1])
                            enemy.move(mima, xx, yy)
                            miMos[i] = enemy.getPos()
                        mima[xx][yy] = 6
                        nodo2 = Nodo(mima, elem, (xx, yy),miMos,0)
                        cola.append(nodo2)

            explota=False
            #print(elem.getMos())

    #Mover por profundidad
    def movePorProfundidad(self,ma,enemies):
        #print(len(enemies))
        eneCoor=np.zeros((len(enemies),2))
        for i in range(0, len(enemies)):
            eneCoor[i]=enemies[i].getPos()
        nodo = Nodo(ma,None,(self.x,self.y),eneCoor,0)
        enemy=AgenteMonster(0,0)
        cola = collections.deque()
        cola.append(nodo)
        n = len(ma[0])
        #print(n)

        #ciclo principal
        while True:
            elem=cola.popleft()
            xx=elem.getPos()[0]
            yy = elem.getPos()[1]
            explota=False
            #print(elem.getMatriz())
            #time.sleep(0.01)
            if elem.getMatriz()[xx][yy]==5:
                return self.win(elem)
                break
            if elem.getProfundidad()>=n*n:
                continue;
           # print(elem.getMos(),xx,yy,elem.getPos())
            abue=elem.getPapa()
            if abue!=None:
                abue=abue.getPapa()
                if abue!=None:
                    abue = abue.getPapa()
                    if abue!=None and abue.getMatriz()[abue.getPos()[0]][abue.getPos()[1]]==6:
                        explota=True

            # Rama mover hacia la derecha
            if elem.getMatriz()[xx+1][yy]==0 or elem.getMatriz()[xx+1][yy]==5:
                mima=self.copiar(elem.getMatriz())
                if explota : self.explotarBomba(mima,elem.getPapa().getPapa().getPapa().getPos())
                miMos = np.zeros((len(enemies),2))
                for i in range(0, len(enemies)):
                    enemy.setPos(elem.getMos()[i][0], elem.getMos()[i][1])
                    #print(enemy.getPos())
                    enemy.move(mima, xx, yy)
                    miMos[i] = enemy.getPos()
                if elem.getMatriz()[xx+1][yy]==0:
                    mima[xx+1][yy]=4
                if elem.getPapa() == None or mima[xx][yy] == 4:
                    mima[xx][yy] = 0

                nodo2=Nodo(mima,elem,(xx+1,yy),miMos,elem.getProfundidad()+1)
                cola.appendleft(nodo2)

            # Rama mover hacia la izquierda
            if elem.getMatriz()[xx-1][yy]==0 or elem.getMatriz()[xx-1][yy]==5:
                mima=self.copiar(elem.getMatriz())
                if explota : self.explotarBomba(mima,elem.getPapa().getPapa().getPapa().getPos())
                miMos = np.zeros((len(enemies),2))

                for i in range(0, len(enemies)):
                    enemy.setPos(elem.getMos()[i][0], elem.getMos()[i][1])
                    enemy.move(mima, xx, yy)
                    miMos[i] = enemy.getPos()
                if elem.getMatriz()[xx-1][yy]==0:
                    mima[xx-1][yy]=4
                if elem.getPapa()==None or mima[xx][yy]==4:
                    mima[xx][yy]=0

                nodo2=Nodo(mima,elem,(xx-1,yy),miMos,elem.getProfundidad()+1)
                cola.appendleft(nodo2)

            # Rama mover hacia arriba
            if elem.getMatriz()[xx][yy-1]==0 or elem.getMatriz()[xx][yy-1]==5:
                mima=self.copiar(elem.getMatriz())
                if explota : self.explotarBomba(mima,elem.getPapa().getPapa().getPapa().getPos())
                miMos = np.zeros((len(enemies),2))
                for i in range(0, len(enemies)):
                    enemy.setPos(elem.getMos()[i][0], elem.getMos()[i][1])
                    enemy.move(mima, xx, yy)
                    miMos[i] = enemy.getPos()
                if elem.getMatriz()[xx][yy-1]==0:
                    mima[xx][yy-1]=4
                if elem.getPapa() == None or mima[xx][yy] == 4:
                    mima[xx][yy] = 0

                nodo2=Nodo(mima,elem,(xx,yy-1),miMos,elem.getProfundidad()+1)
                cola.appendleft(nodo2)

            # Rama mover hacia abajo
            if elem.getMatriz()[xx][yy+1]==0 or elem.getMatriz()[xx][yy+1]==5:
                mima=self.copiar(elem.getMatriz())
                if explota : self.explotarBomba(mima,elem.getPapa().getPapa().getPapa().getPos())
                miMos = np.zeros((len(enemies),2))
                #print(miMos)
                for i in range(0, len(enemies)):
                    enemy.setPos(elem.getMos()[i][0], elem.getMos()[i][1])
                    enemy.move(mima, xx, yy)
                    miMos[i] = enemy.getPos()
                if elem.getMatriz()[xx][yy+1]==0:
                    mima[xx][yy+1]=4
                if elem.getPapa() == None or mima[xx][yy] == 4:
                    mima[xx][yy] = 0

                nodo2=Nodo(mima,elem,(xx,yy+1),miMos,elem.getProfundidad()+1)
                cola.appendleft(nodo2)

            # Rama poner bomba
            if not (elem.getPapa() != None and elem.getPapa().getMatriz()[xx][yy] == 6):
                if (elem.getMatriz()[xx-1][yy]==2 or
                    elem.getMatriz()[xx + 1][yy] == 2 or
                    elem.getMatriz()[xx][yy-1] == 2 or
                    elem.getMatriz()[xx][yy+1] == 2 or
                    elem.getMatriz()[xx - 1][yy] == 9 or
                    elem.getMatriz()[xx + 1][yy] == 9 or
                    elem.getMatriz()[xx][yy - 1] == 9 or
                    elem.getMatriz()[xx][yy + 1] == 9) :

                        mima=self.copiar(elem.getMatriz())
                        if explota : self.explotarBomba(mima,elem.getPapa().getPapa().getPapa().getPos())
                        miMos = np.zeros((len(enemies),2))
                        for i in range(0, len(enemies)):
                            enemy.setPos(elem.getMos()[i][0], elem.getMos()[i][1])
                            enemy.move(mima, xx, yy)
                            miMos[i] = enemy.getPos()
                        mima[xx][yy] = 6
                        nodo2 = Nodo(mima, elem, (xx, yy),miMos,elem.getProfundidad()+1)
                        cola.appendleft(nodo2)

            explota=False
            #print(elem.getMos())

    #metodo que retorna el arreglo con la ruta de la solucion de la busqueda
    def win(self,nodo):
        minodo=nodo
        pila=np.array([])
        #print(pila)
        while minodo!=None:
            pila=np.append(pila,minodo)
            minodo=minodo.getPapa()

        return pila

    #Metodo para hacer copias de la matris del tablero
    def copiar(self,mat):
        n=mat[0].size
        nueva=np.zeros((n,n))
        for i in range(0,n):
            for j in range(0,n):
                nueva[i][j]=mat[i][j]


        return  nueva
