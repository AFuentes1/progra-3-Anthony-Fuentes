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
from tkinter import *
import random
import sys
from tkinter import *
from tkinter import simpledialog

frame=Tk()
frame.resizable(0,0)
frame.geometry("1080x1080")
frame.title("SUDOKU FUENTES")
menu=Menu(frame)
file=Menu(menu)
file.add_command(label="Salir", command=frame.quit)
file.add_command(label="Nivel Facil", command=lambda:easyLvl())
file.add_command(label="Nivel Facil Resuelto", command=lambda:easyLvlSolved())
file.add_command(label="Nivel Dificil", command=lambda:hardLvl())
file.add_command(label="Nivel Dificil Resuelto", command=lambda:hardLvlSolved())


menu.add_cascade(label="Niveles (Facil o Dificil)", menu=file)
frame.config(menu=menu)
listofnumbers0=[0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0]

hardUnsolved=[8,0,0,0,0,0,0,0,0,
    0,0,3,6,0,0,0,0,0,
    0,7,0,0,9,0,2,0,0,
    0,5,0,0,0,7,0,0,0,
    0,0,0,0,4,5,7,0,0,
    0,0,0,1,0,0,0,3,0,
    0,0,1,0,0,0,0,6,8,
    0,0,8,5,0,0,0,1,0,
    0,9,0,0,0,0,4,0,0]

hardSolved=[8, 1, 2, 7, 5, 3, 6, 4, 9,
9, 4, 3, 6, 8, 2, 1, 7, 5,
6, 7, 5, 4, 9, 1, 2, 8, 3,
1, 5, 4, 2, 3, 7, 8, 9, 6,
3, 6, 9, 8, 4, 5, 7, 2, 1,
2, 8, 7, 1, 6, 9, 5, 3, 4,
5, 2, 1, 9, 7, 4, 3, 6, 8,
4, 3, 8, 5, 2, 6, 9, 1, 7,
7, 9, 6, 3, 1, 8, 4, 5, 2]

easyUnsolved=[5,1,7,6,0,0,0,3,4,
               2,8,9,0,0,4,0,0,0,
               3,4,6,2,0,5,0,9,0,
               6,0,2,0,0,0,0,1,0,
               0,3,8,0,0,6,0,4,7,
               0,0,0,0,0,0,0,0,0,
               0,9,0,0,0,0,0,7,8,
               7,0,3,4,0,0,5,6,0,
               0,0,0,0,0,0,0,0,0]
easySolved=[5,1,7,6,9,8,2,3,4,
             2,8,9,1,3,4,7,5,6,
             3,4,6,2,7,5,8,9,1,
             6,7,2,8,4,9,3,1,5,
             1,3,8,5,2,6,9,4,7,
             9,5,4,7,1,3,6,8,2,
             4,9,5,3,6,2,1,7,8,
             7,2,3,4,8,1,5,6,9,
             8,6,1,9,5,7,4,2,3]
i=0
q=0
thelist=[listofnumbers0,easyUnsolved, easySolved,hardUnsolved, hardSolved]

def easyLvl():
    global q
    q=1
    grid = jugar()


def easyLvlSolved():
    global q
    q=2
    jugar()

def hardLvl():
    global q
    q=3
    jugar()
def hardLvlSolved():
    global q
    q=4
    jugar()

def btnCommand(x):
    if x==0:
        x=x+1





colourTxt="black"
#-----------------------------Codigo principal------------------
#En esta parte desarrollamos lo que va en la ventana principal
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

    global bg_color, color, gridcell
    for rowindex in range(9):
        for colindex in range(9):

            if (rowindex in (0, 1, 2, 6, 7, 8) and colindex in (3, 4, 5) or \
                    (rowindex in (3, 4, 5) and colindex in (0, 1, 2, 6, 7, 8))):
                colour = "light blue"
            else:
                colour = "white"

            global i
            x = thelist[q][i]
            i = i + 1
            if i == 81:
                i = 0

            if x == 0:
                colourTxt = "black"
            else:
                colourTxt = "black"
            btn = Button(gameArea, width=6, height=3, bg=colour, text=x, fg=colourTxt, command=lambda: btnCommand(x))
            btn.grid(row=rowindex, column=colindex)



    gameArea.grid()
    gameArea.place(x=70, y = 90)


    Nombre = Label(canvasPantalla, text= "JUGADOR: ", bg="cyan2",font=("Bodoni Font", 15) )
    Nombre.place(x=800, y=60)
    entrada_nombre = StringVar()
    entrada_widget = Entry(canvasPantalla, width=30, textvariable=entrada_nombre, justify=CENTER)
    entrada_widget.place(x=765, y=90)

    cont = 1
    for i in range(3):
        for j in range(3):
            numeral = Button(gameArea2, width= 10, height=5, bg="white", text = cont)
            numeral.grid(row=i, column=j)
            cont += 1
    gameArea2.grid()
    gameArea2.place(x=730, y=200)






jugar()
frame.mainloop()