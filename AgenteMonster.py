#Autores:   -Victor Duvan Ruiz Ochoa    -1664060
#           -Sebastian Giron Arcila     -1550180
#Fecha creacion: 07 de Junlo de 2019
class AgenteMonster:

    def __init__(self,posX,posY):
        self.x = posX
        self.y = posY

    #Metodo para mover al agente Mostruo (basado en metas)
    def move(self,ma,desx,desy):
        #print(self.x,self.y,desx,desy)
        dis=[100000,100000,100000,100000]
        if ma[self.x+1][self.y] in (0,9):
            dis[0]=abs(self.x+1-desx)+abs(self.y-desy)


        if ma[self.x][self.y+1]in (0,9):
            dis[1]=abs(self.x-desx)+abs(self.y+1-desy)

        if ma[self.x-1][self.y]in (0,9):
            dis[2]=abs(self.x-1-desx)+abs(self.y-desy)

        if ma[self.x][self.y-1]in (0,9):
            dis[3]=abs(self.x-desx)+abs(self.y-1-desy)

       # print(dis)
        may =100000
        pos=-1
        for i in range(0,4):
            if dis[i]<may:
                may=dis[i]
                pos=i

        ma[self.x][self.y]=0
        if pos==0:
            self.x+=1
        elif pos==1:
            self.y+=1
        elif pos==2:
            self.x-=1
        elif pos==3:
            self.y-=1
        ma[self.x][self.y] = 3

    #setiar la posicion del agente
    def setPos(self,posX,posY):
        self.x = int(posX)
        self.y = int (posY)

    #obtener la posicion del agente
    def getPos(self):
        return (self.x,self.y)