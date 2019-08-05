#Autores:   -Victor Duvan Ruiz Ochoa    -1664060
#           -Sebastian Giron Arcila     -1550180
#Fecha creacion: 03 de Julio de 2019

import numpy as np
import random as r
from AgenteMonster import *
from AgenteJugador import *
import threading
import time
import pygame,sys
from collections import deque
from pygame.locals import *
from tkinter import ttk
from tkinter import *

#Funcion que genera la puera aleatoriamente en el tablero
def generarPuerta(ma,n):
    while (1):
        x = r.randrange(1, n + 1)
        y = r.randrange(1, n + 1)
        if ma[x][y] == 0 or ma[x][y] ==2:
            ma[x][y] = 9
            puerta = (x,y)
            return  puerta
            break

#Funcion que genera de manera aleatoria al agente jugador en el tablero
def generarJugador(ma,n):
    while(1):
        x = r.randrange(1, n + 1)
        y = r.randrange(1, n + 1)
        if ma[x][y] == 0:
            ma[x][y] = 4
            age = AgenteJugador(x, y)
            return age
            break

#Funcion que genera de manera aleatoria al agente mostruo en el tablero
def generarMonster(ma,n):
    while(1):
        x=r.randrange(1,n+1)
        y =r.randrange(1, n + 1)
        if ma[x][y]==0:
            ma[x][y]=3
            age = AgenteMonster(x,y)
            return age
            break

#Esta funcion el la ejecutada por un hilo que crea y refresca el juego
def pintar():
    pygame.init()
    #pygame.mixer.music.load('song.mp3')
    #pygame.mixer.music.play(0)
    venta = pygame.display.set_mode((32 * (n + 2), 32 * (n + 2)))
    pygame.display.set_caption("Bomberman")


    while True:

        venta.fill((79,160,1))
        xx = 0
        yy = 0
        piedra = pygame.image.load("piedra.PNG")
        ladri = pygame.image.load("ladrillo.PNG")
        monster = pygame.image.load("moustruo.png")
        jugador = pygame.image.load("player.png")
        puerta = pygame.image.load("puerta.png")
        bomba = pygame.image.load("bomba.png")
        for i in range(0, n + 2):
            for j in range(0, n + 2):
                if ma[i][j] == 1:
                    venta.blit(piedra, (xx, yy))
                elif ma[i][j] == 2 or ma[i][j] == 9:
                    venta.blit(ladri, (xx, yy))
                elif ma[i][j] == 3:
                    venta.blit(monster, (xx, yy))
                elif ma[i][j] == 4:
                    venta.blit(jugador, (xx, yy))
                elif ma[i][j] == 5:
                    venta.blit(puerta, (xx, yy))
                elif ma[i][j] == 6:
                    venta.blit(bomba, (xx, yy))
                xx = xx + 32
            xx = 0
            yy = yy + 32


        for even in pygame.event.get():
            if even.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

#Funcion que genera la matriz tablero, con sus respectivas piedras, y
#con generacion de ladrillos aleatoriamente
def generarMundo(n):
    blo = 3
    ma = np.zeros((n+2, n+2))
    for i in range(0,n+2):
        for j in range(0,n+2):
            if i==0 or i==(n+1):
                ma[i][j]=1
            if j==0 or j==(n+1):
                ma[i][j] = 1
            if i%2==0 and j%2==0:
                ma[i][j]=1

            ran = r.randrange(0,10,1)
            if ran>7 and ma[i][j]!=1 and blo>0:
                ma[i][j]=2
                blo-=1
        blo=3

    return ma
    print(ma)

#Funcion utilizada para la lectura del tablero desde el archivo Entrada.txt
def LeerArchivo(k):

    archivo = open("Entrada.txt","r")
    lineas = archivo.readlines()
    n= len(lineas)
    k=n-2
    mat = np.zeros((n,n))
    i=0
    for linea in lineas:
        results = list(map(int,linea.split()))
        mat[i]=results
        i+=1


    archivo.close()
    return mat,k

#Accion del evento del boton jugar
def botonAccion():
    n = comboTablero.get()
    nMoster = comboEnemies.get()
    gui.quit()


#####Flujo principal de la aplicacion#####

#creacion de la GUI
gui = Tk()
gui.title("BOMBERMAN")
gui.resizable(width=False, height=False)
C = Canvas(gui, bg="blue", height=420, width=575)
filename = PhotoImage(file = "logo.png")
background_label = Label(gui, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
C.pack()

varCheck= IntVar()
#labels de la GUI
Label(gui,text="Tamaño tablero:",bg='black',fg='white').place(x=100,y=300)
Label(gui,text="Numero enemigos:",bg='black',fg='white').place(x=100,y=330)
Label(gui,text="Tipo busqueda:",bg='black',fg='white').place(x=100,y=360)

#ComboBox de la GUI
comboTablero = ttk.Combobox(gui,values=[3,5,7,9],state="readonly")
comboTablero.place(x=230,y=300)
comboTablero.current(0)

comboEnemies = ttk.Combobox(gui,values=[1,2,3],state="readonly")
comboEnemies.place(x=230,y=330)
comboEnemies.current(0)

comboBusq = ttk.Combobox(gui,values=["Amplitud","Profundidad"],state="readonly")
comboBusq.place(x=230,y=360)
comboBusq.current(0)

checkTipo = Checkbutton(gui, text="Importar tablero desde archivo",variable=varCheck)
checkTipo.place(x=150,y=390)

#Boton jugar
boton = Button(gui, text ="Play!", command = botonAccion,height=4,width=10)
boton.place(x=420,y=300)

gui.mainloop
gui.mainloop()

#Parametros utilizados para la creacion del tablero
n = 0
nMoster = 0

age = np.array([])
pla = None
pue = None

if varCheck.get()==0: leer=False
else: leer=True
k=0

#Condicion que identifica si es generacion del tablero o si se imperta desde archivo
if leer:
    ma,n=LeerArchivo(k)

    for i in range(0,n+2):
        for j in range(0, n + 2):
            if ma[i][j]==3:
                age=np.append(age,AgenteMonster(i,j))
            elif ma[i][j]==4:
                pla=AgenteJugador(i,j)
else:
    n = int(comboTablero.get())
    nMoster = int(comboEnemies.get())
    ma = generarMundo(n)
    #print(nMoster)
    for i in range(0,nMoster): age=np.append(age,generarMonster(ma, n))
    pla = generarJugador(ma, n)
    pue = generarPuerta(ma, n)


busquedad = int(comboBusq.current())
gui.destroy()

#print(pla)
t = threading.Thread(target=pintar)
t.start()

#Se identifica el algortmo de busqueda que se va a utilizar
if busquedad==0:
    pila = pla.movePorAmplitud(ma, age)
else:
    pila = pla.movePorProfundidad(ma,age)


#Ciclo para pintar la ruta de la busqueda
tam = pila.size
for i in range(0,tam):
    elem=pila[tam-i-1].getMatriz()
    ma=elem
    print(ma)
    time.sleep(1)










