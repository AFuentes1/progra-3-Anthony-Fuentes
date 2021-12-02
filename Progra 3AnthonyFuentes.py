#Progra 3
"""
Sudoku es un pasatiempo que se popularizó internacionalmente después del año 2000
cuando diversos periódicos empezaron a publicarlo en la sección de pasatiempos.
Consiste en llenar con dígitos del 1 al 9 cada una de las casillas de una cuadrícula que tiene
un total de 9 x 9 casillas.
La cuadrícula la podemos ver como una matriz de 9 filas y 9
columnas. A la vez esta cuadrícula se divide en subcuadrículas de 3 x 3 casillas. Para
empezar a jugar hay algunos dígitos fijos en la cuadrícula, lo cual determina el nivel de
dificultad del juego. Aunque usualmente se usan dígitos, lo que interesa es que sean grupos
de 9 elementos diferentes: por ejemplo 9 letras, 9 colores, 9 frutas, etc.
La regla de este juego es que un mismo elemento no se puede repetir:
- En una misma fila (casillas horizontales)
- En una misma columna (casillas verticales)
- En las subcuadrículas (3x3)
Además, los elementos que aparecen al inicio del juego quedan fijos, no se pueden cambiar.
"""
import time
from tkinter import *
import tkinter as tk
import random
import sys
from tkinter import *
from tkinter import messagebox
from Sudoku import *
from jugadas import *
from reloj import *
import threading
import json
import os


#Se inicia el juego
def start():
    global ingame, dicConfiguracion

    if ingame:
        return
    ingame = True
    if entrada_nombre.get == "":
        messagebox.showinfo("Error", "Introduce un nombre")
        ingame = False
        return

    dicConfiguracion = CargarConfiguracion()

    if dicConfiguracion["opcionG"] == 1:
        hilo = threading.Thread(target=CorrerTiempo, args=(False,)).start()
    elif dicConfiguracion["opcionG"] == 3:
        hilo = threading.Thread(target=CorrerTiempo, args=(True,)).start()
    else:
        reloj.config(text="Tiempo: Sin tiempo")

    if dicConfiguracion["opcionP"] == 1:
        sudoku.Easy()
    elif dicConfiguracion["opcionP"] == 2:
        sudoku.Medium()
    elif dicConfiguracion["opcionP"] == 3:
        sudoku.Hard()
    else:
        sudoku.GenerateFixed()

    for i in range(len(board)):
        for j in range(len(board[i])):
            board[i][j].config(text = str(sudoku.board[i][j]))

#Funcion que borra el juego
def BorrarJuego():
    if ingame:

        for i in range(len(board)):
            for j in range(len(board[i])):

                flag = False

                for k in sudoku.fixedPositions:
                    if i == k[0] and j == k[1]:
                        flag = True

                if not flag:

                    board[i][j].config(text = str(0))
                    sudoku.board[i][j] = 0


#Funcion para el top
def TopX():

    global ingame, sudoku, listaJugadas

    if ingame:
        sudoku.Solve()

        for i in range(len(board)):
            for j in range(len(board[i])):

                board[i][j].config(text = str(sudoku.board[i][j]))

        messagebox.showinfo("Completa", "Se ha completado el sudoku automanticamente")

        ingame = False
        Tiempo = tiempo()
        listaJugadas = Jugadas()

#Funcion para rehacer jugado
def RehacerJugada():
    if ingame:
        numeros = listaJugadas.Rehacer()
        if numeros != None:
            posi, posj, num = numeros
            board[posi][posj].config(text = str(num))
            sudoku.board[posi][posj] = num

#deshace la jugada
def deshacerjugada():
    if ingame:
        numeros = listaJugadas.Deshacer()
        if numeros != None:
            posi, posj = numeros
            board[posi][posj].config(text=str(0))
            sudoku.board[posi][posj] = 0

#Funcion para terminar juego
def TerminarJuego():

    global ingame, sudoku, listaJugadas

    if ingame:
        opcion = messagebox.askquestion("Terminar", "Quieres terminar el juego?")

        if opcion == "yes":
            Tiempo = tiempo()
            ingame = False
            sudoku = SudokuGame()
            for i in range(len(board)):
                for j in range(len(board[i])):
                    board[i][j].config(text = str(sudoku.board[i][j]))
            listaJugadas = Jugadas()

def GuardarJuego():
    if ingame:

        tablero = sudoku.board
        casillas = sudoku.fixedPositions
        deshacerlista = listaJugadas.jugadasDeshacer
        rehacerlista = listaJugadas.jugadasRehacer
        nombre = entrada_nombre.get()
        hora = Tiempo.hora
        minuto = Tiempo.minuto
        segundo = Tiempo.segundo
        modo = dicConfiguracion["opcionG"]

        dicJuego = {"tablero": tablero, "casillas": casillas, "deshacerlista": deshacerlista, "rehacerlista": rehacerlista, "nombre": nombre, "hora": hora, "minuto": minuto, "segundo": segundo, "modo": modo}

        archivo = open('sudokujuegoactual.json', 'w')
        archivo.write(json.dumps(dicJuego))
        archivo.close()

def CargarJuego():

    global ingame, sudoku, listaJugadas, Tiempo

    ingame = True

    if ingame:

        dicJuego = {}
        try:

            archivo = open('sudokujuegoactual.json', 'r')
            dicJuego = json.load(archivo)
            archivo.close()

        except:
            pass

        ingame = True

        sudoku.board = dicJuego["tablero"]
        sudoku.fixedPositions = dicJuego["casillas"]
        listaJugadas.jugadasDeshacer = dicJuego["deshacerlista"]
        listaJugadas.jugadasRehacer = dicJuego["rehacerlista"]
        entrada_nombre.set(dicJuego["nombre"])
        Tiempo.hora = dicJuego["hora"]
        Tiempo.minuto = dicJuego["minuto"]
        Tiempo.segundo = dicJuego["segundo"]
        dicConfiguracion["opcionG"] = dicJuego["modo"]

        if dicConfiguracion["opcionG"] == 1:
            hilo = threading.Thread(target=CorrerTiempo, args=(False,)).start()
        elif dicConfiguracion["opcionG"] == 3:
            hilo = threading.Thread(target=CorrerTiempo, args=(True,)).start()
        else:
            reloj.config(text="Tiempo: Sin tiempo")

        for i in range(len(board)):
            for j in range(len(board[i])):
                board[i][j].config(text = str(sudoku.board[i][j]))


def btnCommand(i, j):

    global posi, posj

    if ingame:
        board[posi][posj].config(bg = "light blue")
        posi, posj = i, j
        board[i][j].config(bg = "red")


def btnCommand2(num):

    global ingame,listaJugadas, Tiempo

    if ingame:

        action = sudoku.Add(posi, posj, num)

        if action == True:

            board[posi][posj].config(bg="light blue")
            listaJugadas.AgregarDeshacer(posi, posj, num)
            board[posi][posj].config(text=str(num))
            sudoku.Print()

            if sudoku.Valid():

                Tiempo = tiempo()
                listaJugadas = Jugadas()
                messagebox.showinfo("Felicidades", "Felicidades has ganado")
                ingame = False
                return

        elif action == 1:

            messagebox.showinfo("Error", "Este numero ya esta en la fila")

        elif action == 2:

            messagebox.showinfo("Error", "Este numero ya esta en la columna")

        elif action == 3:

            messagebox.showinfo("Error", "Este numero ya esta en la subcuadrícula")

        elif action == 4:

            messagebox.showinfo("Error", "Este numero es casilla fija")

def CorrerTiempo(flag):

    global dicConfiguracion, ingame

    if flag:

        Tiempo.hora = dicConfiguracion["horas"]
        Tiempo.minuto = dicConfiguracion["minutos"]
        Tiempo.segundo = dicConfiguracion["segundos"]


    while ingame:

        if flag:

            if Tiempo.hora == 0 and Tiempo.minuto == 0 and Tiempo.segundo == 0:
                messagebox.showinfo("Tiempo", "Se ha acabado el tiempo")
                ingame = False
                return

            Tiempo.contraReloj()
        else:
            Tiempo.reloj()

        reloj.config(text="Tiempo: " + str(Tiempo.hora) + ":" + str(Tiempo.minuto) + ":" + str(Tiempo.segundo))

        time.sleep(1)

def GuardarConfiguracion(h,m,s,opcionG,opcionP):

    global dicConfiguracion

    try:
        #convertimos las variables a enteros
        h = int(h)
        m = int(m)
        s = int(s)

        #verificamos que los valores sean correctos
        if h < 0 or h > 99 and m < 0 or m > 59 and s < 0 or s > 59:
            messagebox.showerror("Error", "Error al guardar la configuracion")
            return

        #guardamos la configuracion
        archivo = open('sudoku2021configuracion.json', 'w')
        archivo.write(json.dumps({"horas":h,"minutos":m,"segundos":s,"opcionG":opcionG,"opcionP":opcionP}))
        archivo.close()

        dicConfiguracion = CargarConfiguracion()

        messagebox.showinfo("Guardado", "Configuracion guardada")

    except:

        messagebox.showerror("Error", "Error al guardar la configuracion")

def CargarConfiguracion():

    try:
        #cargarmos la configuracion para retornarla
        archivo = open('sudoku2021configuracion.json', 'r')
        dic = json.load(archivo)
        archivo.close()

        return dic

    except:

        pass

def Configuracion():


    #Generamos la interfaz grafica para la zona de configuracion


    canvasPantalla = Canvas()
    canvasPantalla.place(x=0, y=0)
    canvasPantalla.config(bg="cyan2")
    canvasPantalla.config(width="1010", height="740")
    canvasPantalla.config(bd=35)
    canvasPantalla.config(relief="groove")

    canvasPantalla.place(x=0, y=0)


    titulo = Label(canvasPantalla, text="Configuración", font=("Arial", 20), bg="cyan2", fg="Black")
    titulo.place(x=470, y=100)

    opcionGame = IntVar()

    canvasOpciones = Canvas(canvasPantalla, width=200, height=200, bg="White",highlightcolor = "black", highlightbackground = "black")
    canvasOpciones.place(x=350, y=200)

    radioTimer = Radiobutton(canvasOpciones, text="Timer", variable=opcionGame, value=1, bg ="White")
    radioTimer.grid(row=0, column=0,padx=7,pady=7)
    radioNoTimer = Radiobutton(canvasOpciones, text="No Timer", variable=opcionGame, value=2, bg ="White")
    radioNoTimer.grid(row=1, column=0,padx=7,pady=7)
    radioContra = Radiobutton(canvasOpciones, text="Contra Reloj", variable=opcionGame, value=3, bg ="White")
    radioContra.grid(row=2, column=0,padx=7,pady=7)

    labelHoras = Label(canvasOpciones, text="Horas:", bg ="White")
    labelHoras.grid(row=0, column=1,padx=7,pady=7)
    entryHoras = Entry(canvasOpciones, width=5, bg ="White")
    entryHoras.insert(0,"0")
    entryHoras.grid(row=0, column=2,padx=7,pady=7)
    labelMinutos = Label(canvasOpciones, text="Minutos:", bg ="White")
    labelMinutos.grid(row=1, column=1,padx=7,pady=7)
    entryMinutos = Entry(canvasOpciones, width=5, bg ="White")
    entryMinutos.grid(row=1, column=2,padx=7,pady=7)
    entryMinutos.insert(0,"0")
    labelSegundos = Label(canvasOpciones, text="Segundos:", bg ="White")
    labelSegundos.grid(row=2, column=1,padx=7,pady=7)
    entrySegundos = Entry(canvasOpciones, width=5, bg ="White")
    entrySegundos.grid(row=2, column=2,padx=7,pady=7)
    entrySegundos.insert(0,"0")

    opcionDif = IntVar()

    labelFacil = Label(canvasOpciones, text="Facil", bg ="White")
    labelFacil.grid(row=0, column=3,padx=7,pady=7)

    radioFacil = Radiobutton(canvasOpciones, text="Facil", variable=opcionDif, value=1, bg ="White")
    radioFacil.grid(row=0, column=4,padx=7,pady=7)

    labelMedio = Label(canvasOpciones, text="Medio", bg ="White")
    labelMedio.grid(row=1, column=3,padx=7,pady=7)

    radioMedio = Radiobutton(canvasOpciones, text="Medio", variable=opcionDif, value=2, bg ="White")
    radioMedio.grid(row=1, column=4,padx=7,pady=7)

    labelDificil = Label(canvasOpciones, text="Dificil", bg ="White")
    labelDificil.grid(row=2, column=3,padx=7,pady=7)

    radioDificil = Radiobutton(canvasOpciones, text="Dificil", variable=opcionDif, value=3, bg ="White")
    radioDificil.grid(row=2, column=4,padx=7,pady=7)

    labelAutomatico = Label(canvasOpciones, text="Automatico", bg ="White")
    labelAutomatico.grid(row=3, column=3,padx=7,pady=7)

    radioAutomatico = Radiobutton(canvasOpciones, text="Automatico", variable=opcionDif, value=4, bg ="White")
    radioAutomatico.grid(row=3, column=4,padx=7,pady=7)

    botonAceptar = Button(canvasOpciones, text="Aceptar", bg="White", command = lambda : GuardarConfiguracion(entryHoras.get(), entryMinutos.get(), entrySegundos.get(), opcionGame.get(), opcionDif.get()))
    botonAceptar.grid(row=4, column=0,padx=7,pady=7)

    frame.mainloop()


def jugar():

    global ingame, board, entrada_nombre, reloj, canvasPantalla, gameArea, pause, gameArea2

    canvasPantalla = Canvas()
    canvasPantalla.place(x=0, y=0)
    canvasPantalla.config(bg="cyan2")
    canvasPantalla.config(width="1010", height="740")
    canvasPantalla.config(bd=35)
    canvasPantalla.config(relief="groove")
    Sudoku = Label(canvasPantalla, text="SUDOKU", font=("Bodoni Font", 23))
    Sudoku.place(x=500, y=40)
    Sudoku.config(bg="cyan2")

    board = []

    gameArea = Frame(canvasPantalla, bg="pale turquoise")
    gameArea2 = Frame(canvasPantalla, bg="pale turquoise")

    colour = "light blue"
    colour2 = "white"

    boton00 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(0, 0))
    boton00.grid(row=0, column=0)

    boton01 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(0, 1))
    boton01.grid(row=0, column=1)

    boton02 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(0, 2))
    boton02.grid(row=0, column=2)

    boton03 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(0, 3))
    boton03.grid(row=0, column=3)

    boton04 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(0, 4))
    boton04.grid(row=0, column=4)

    boton05 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(0, 5))
    boton05.grid(row=0, column=5)

    boton06 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(0, 6))
    boton06.grid(row=0, column=6)

    boton07 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(0, 7))
    boton07.grid(row=0, column=7)

    boton08 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(0, 8))
    boton08.grid(row=0, column=8)

    boton10 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(1, 0))
    boton10.grid(row=1, column=0)

    boton11 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(1, 1))
    boton11.grid(row=1, column=1)

    boton12 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(1, 2))
    boton12.grid(row=1, column=2)

    boton13 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(1, 3))
    boton13.grid(row=1, column=3)

    boton14 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(1, 4))
    boton14.grid(row=1, column=4)

    boton15 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(1, 5))
    boton15.grid(row=1, column=5)

    boton16 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(1, 6))
    boton16.grid(row=1, column=6)

    boton17 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(1, 7))
    boton17.grid(row=1, column=7)

    boton18 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(1, 8))
    boton18.grid(row=1, column=8)

    boton20 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(2, 0))
    boton20.grid(row=2, column=0)

    boton21 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(2, 1))
    boton21.grid(row=2, column=1)

    boton22 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(2, 2))
    boton22.grid(row=2, column=2)

    boton23 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(2, 3))
    boton23.grid(row=2, column=3)

    boton24 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(2, 4))
    boton24.grid(row=2, column=4)

    boton25 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(2, 5))
    boton25.grid(row=2, column=5)

    boton26 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(2, 6))
    boton26.grid(row=2, column=6)

    boton27 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(2, 7))
    boton27.grid(row=2, column=7)

    boton28 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(2, 8))
    boton28.grid(row=2, column=8)

    boton30 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(3, 0))
    boton30.grid(row=3, column=0)

    boton31 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(3, 1))
    boton31.grid(row=3, column=1)

    boton32 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(3, 2))
    boton32.grid(row=3, column=2)

    boton33 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(3, 3))
    boton33.grid(row=3, column=3)

    boton34 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(3, 4))
    boton34.grid(row=3, column=4)

    boton35 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(3, 5))
    boton35.grid(row=3, column=5)

    boton36 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(3, 6))
    boton36.grid(row=3, column=6)

    boton37 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(3, 7))
    boton37.grid(row=3, column=7)

    boton38 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(3, 8))
    boton38.grid(row=3, column=8)

    boton40 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(4, 0))
    boton40.grid(row=4, column=0)

    boton41 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(4, 1))
    boton41.grid(row=4, column=1)

    boton42 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(4, 2))
    boton42.grid(row=4, column=2)

    boton43 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(4, 3))
    boton43.grid(row=4, column=3)

    boton44 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(4, 4))
    boton44.grid(row=4, column=4)

    boton45 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(4, 5))
    boton45.grid(row=4, column=5)

    boton46 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(4, 6))
    boton46.grid(row=4, column=6)

    boton47 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(4, 7))
    boton47.grid(row=4, column=7)

    boton48 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(4, 8))
    boton48.grid(row=4, column=8)

    boton50 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(5, 0))
    boton50.grid(row=5, column=0)

    boton51 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(5, 1))
    boton51.grid(row=5, column=1)

    boton52 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(5, 2))
    boton52.grid(row=5, column=2)

    boton53 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(5, 3))
    boton53.grid(row=5, column=3)

    boton54 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(5, 4))
    boton54.grid(row=5, column=4)

    boton55 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(5, 5))
    boton55.grid(row=5, column=5)

    boton56 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(5, 6))
    boton56.grid(row=5, column=6)

    boton57 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(5, 7))
    boton57.grid(row=5, column=7)

    boton58 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(5, 8))
    boton58.grid(row=5, column=8)

    boton60 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(6, 0))
    boton60.grid(row=6, column=0)

    boton61 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(6, 1))
    boton61.grid(row=6, column=1)

    boton62 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(6, 2))
    boton62.grid(row=6, column=2)

    boton63 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(6, 3))
    boton63.grid(row=6, column=3)

    boton64 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(6, 4))
    boton64.grid(row=6, column=4)

    boton65 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(6, 5))
    boton65.grid(row=6, column=5)

    boton66 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(6, 6))
    boton66.grid(row=6, column=6)

    boton67 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(6, 7))
    boton67.grid(row=6, column=7)

    boton68 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(6, 8))
    boton68.grid(row=6, column=8)

    boton70 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(7, 0))
    boton70.grid(row=7, column=0)

    boton71 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(7, 1))
    boton71.grid(row=7, column=1)

    boton72 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(7, 2))
    boton72.grid(row=7, column=2)

    boton73 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(7, 3))
    boton73.grid(row=7, column=3)

    boton74 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(7, 4))
    boton74.grid(row=7, column=4)

    boton75 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(7, 5))
    boton75.grid(row=7, column=5)

    boton76 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(7, 6))
    boton76.grid(row=7, column=6)

    boton77 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(7, 7))
    boton77.grid(row=7, column=7)

    boton78 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(7, 8))
    boton78.grid(row=7, column=8)

    boton80 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(8, 0))
    boton80.grid(row=8, column=0)

    boton81 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(8, 1))
    boton81.grid(row=8, column=1)

    boton82 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(8, 2))
    boton82.grid(row=8, column=2)

    boton83 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(8, 3))
    boton83.grid(row=8, column=3)

    boton84 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(8, 4))
    boton84.grid(row=8, column=4)

    boton85 = Button(gameArea, width=6, height=3, bg=colour, text="0", fg=colourTxt, command=lambda: btnCommand(8, 5))
    boton85.grid(row=8, column=5)

    boton86 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(8, 6))
    boton86.grid(row=8, column=6)

    boton87 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(8, 7))
    boton87.grid(row=8, column=7)

    boton88 = Button(gameArea, width=6, height=3, bg=colour2, text="0", fg=colourTxt, command=lambda: btnCommand(8, 8))
    boton88.grid(row=8, column=8)

    gameArea.grid()
    gameArea.place(x=70, y=90)

    fila0 = [boton00, boton01, boton02, boton03, boton04, boton05, boton06, boton07, boton08]
    fila1 = [boton10, boton11, boton12, boton13, boton14, boton15, boton16, boton17, boton18]
    fila2 = [boton20, boton21, boton22, boton23, boton24, boton25, boton26, boton27, boton28]
    fila3 = [boton30, boton31, boton32, boton33, boton34, boton35, boton36, boton37, boton38]
    fila4 = [boton40, boton41, boton42, boton43, boton44, boton45, boton46, boton47, boton48]
    fila5 = [boton50, boton51, boton52, boton53, boton54, boton55, boton56, boton57, boton58]
    fila6 = [boton60, boton61, boton62, boton63, boton64, boton65, boton66, boton67, boton68]
    fila7 = [boton70, boton71, boton72, boton73, boton74, boton75, boton76, boton77, boton78]
    fila8 = [boton80, boton81, boton82, boton83, boton84, boton85, boton86, boton87, boton88]

    board = [fila0,fila1,fila2,fila3,fila4,fila5,fila6,fila7,fila8]

    gameArea.grid()
    gameArea.place(x=70, y = 90)


    Nombre = Label(canvasPantalla, text= "JUGADOR: ", bg="cyan2",font=("Bodoni Font", 15) )
    Nombre.place(x=800, y=60)
    entrada_nombre = StringVar()
    entrada_widget = Entry(canvasPantalla, width=30, textvariable=entrada_nombre, justify=CENTER)
    entrada_widget.place(x=765, y=90)

    numeral1 = Button(gameArea2, width=10, height=5, bg="white", text="1", fg="black", command=lambda: btnCommand2(1))
    numeral1.grid(row=0, column=0)

    numeral2 = Button(gameArea2, width=10, height=5, bg="white", text="2", fg="black", command=lambda: btnCommand2(2))
    numeral2.grid(row=0, column=1)

    numeral3 = Button(gameArea2, width=10, height=5, bg="white", text="3", fg="black", command=lambda: btnCommand2(3))
    numeral3.grid(row=0, column=2)

    numeral4 = Button(gameArea2, width=10, height=5, bg="white", text="4", fg="black", command=lambda: btnCommand2(4))
    numeral4.grid(row=1, column=0)

    numeral5 = Button(gameArea2, width=10, height=5, bg="white", text="5", fg="black", command=lambda: btnCommand2(5))
    numeral5.grid(row=1, column=1)

    numeral6 = Button(gameArea2, width=10, height=5, bg="white", text="6", fg="black", command=lambda: btnCommand2(6))
    numeral6.grid(row=1, column=2)

    numeral7 = Button(gameArea2, width=10, height=5, bg="white", text="7", fg="black", command=lambda: btnCommand2(7))
    numeral7.grid(row=2, column=0)

    numeral8 = Button(gameArea2, width=10, height=5, bg="white", text="8", fg="black", command=lambda: btnCommand2(8))
    numeral8.grid(row=2, column=1)

    numeral9 = Button(gameArea2, width=10, height=5, bg="white", text="9", fg="black", command=lambda: btnCommand2(9))
    numeral9.grid(row=2, column=2)

    gameArea2.grid()
    gameArea2.place(x=730, y=200)

    #botones
    canvasBotones = Canvas(canvasPantalla, bg="cyan2",bd=0, highlightthickness=0)
    canvasBotones.place(x=100, y=620)

    botonIniciarPartida = Button(canvasBotones, text= "Iniciar Partida", command=lambda: start(), bg = "SlateGray2", width=12)
    botonIniciarPartida.grid(row=0, column=1, padx=10, pady=10)

    botonDeshacer = Button(canvasBotones, text = "Deshacer Jugada", command=lambda: deshacerjugada(), bg="SlateGray2", width=12)
    botonDeshacer.grid(row=0, column=2, padx=10, pady=10)

    botonBorrar = Button(canvasBotones, text="Borrar Juego", command=lambda: BorrarJuego(), bg="slateGray2", width=12)
    botonBorrar.grid(row=1, column=1, padx=10, pady=10)

    botonTopx = Button(canvasBotones, text="Resolver", command=lambda: TopX(), bg="slateGray2", width=12)
    botonTopx.grid(row=0, column=3, padx=10, pady=10)

    botonRehacer = Button(canvasBotones, text="Rehacer Jugada", command=lambda: RehacerJugada(), bg="slateGray2", width=12)
    botonRehacer.grid(row=1, column=2, padx=10, pady=10)

    botonTerminar = Button(canvasBotones, text = "Terminar Juego", command=lambda: TerminarJuego(),bg="slateGray2", width=12)
    botonTerminar.grid(row=1, column=3, padx=10, pady=10)

    botonGuardar = Button(canvasBotones, text="Guardar Juego", command=lambda: GuardarJuego(),bg="slateGray2", width=12)
    botonGuardar.grid(row=2, column=2, padx=10, pady=10)

    botonCargarJuego = Button(canvasBotones, text="Cargar Juego", command=lambda: CargarJuego(), bg="slateGray2", width=12)
    botonCargarJuego.grid(row=2, column=3, padx=10, pady=10)

    reloj = Label(canvasPantalla, text="Tiempo: ",bg = "cyan2")
    reloj.place(x=450, y=630)

def About():

    canvasPantalla = Canvas()
    canvasPantalla.place(x=0, y=0)
    canvasPantalla.config(bg="cyan2")
    canvasPantalla.config(width="1010", height="740")
    canvasPantalla.config(bd=35)
    canvasPantalla.config(relief="groove")

    canvasPantalla.place(x=0, y=0)

    canvasOpciones = Canvas(canvasPantalla, width=200, height=200, bg="White", highlightcolor="black",
                           highlightbackground="black")
    canvasOpciones.place(x=250, y=170)

    titulo = Label(canvasOpciones, text="Acerca de", font=("Arial", 15), bg="white", fg="Black", anchor='n')
    titulo.grid(row=0, column=0, padx=7, pady=7)

    texto = Label(canvasOpciones, text="Juego 2048", font=("Arial", 15), bg="white", fg="Black", anchor='center')
    texto.grid(row=1, column=0, padx=7, pady=7)

    autor = Label(canvasOpciones, text="Autor: Anthony", font=("Arial", 15), bg="white", fg="Black", anchor='center')
    autor.grid(row=2, column=0, padx=7, pady=7)

    version = Label(canvasOpciones, text="Version: 1.0", font=("Arial", 15), bg="white", fg="Black", anchor='center')
    version.grid(row=3, column=0, padx=7, pady=7)

    texto2 = Label(canvasOpciones, text="Este juego fue creado para el curso de Taller de programación",
                   anchor='center', font=("Arial", 15), bg="white", fg="Black")
    texto2.grid(row=4, column=0, padx=7, pady=7)

    texto3 = Label(canvasOpciones, text="Tecnologico de Costa Rica", font=("Arial", 15), bg="white", fg="Black",
                   anchor='center')
    texto3.grid(row=5, column=0, padx=7, pady=7)

    fecha = Label(canvasOpciones, text="Fecha: 1/12/2021", font=("Arial", 15), bg="white", fg="Black", anchor='center')
    fecha.grid(row=6, column=0, padx=7, pady=7)


frame=Tk()
frame.resizable(0,0)
frame.geometry("1080x1080")
frame.title("SUDOKU FUENTES")

barraMenu = Menu(frame)

mnuJugar = Menu(barraMenu)
mnuConfigurar = Menu(barraMenu)
mnuAbout = Menu(barraMenu)
mnuManual = Menu(barraMenu)
mnuSalir = Menu(barraMenu)

barraMenu.add_command(label="Jugar", command = lambda : jugar())
barraMenu.add_command(label="Configurar", command= lambda  : Configuracion())
barraMenu.add_command(label="Manual", command= lambda  : os.popen("aquivaelnombre.pdf"))
barraMenu.add_command(label="About", command= lambda  : About())
barraMenu.add_command(label="Salir", command= lambda  : frame.destroy())

frame.config(menu=barraMenu)

dicConfiguracion = CargarConfiguracion()

ingame = False
sudoku = SudokuGame()
Tiempo = tiempo()
posi, posj = 0,0
colourTxt="black"
board = []
listaJugadas = Jugadas()

jugar()
frame.mainloop()
