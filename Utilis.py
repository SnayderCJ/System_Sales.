import os

#colores para la impresion de texto
green_color = '\033[32m'
blue_color = '\033[34m'
purple_color = '\033[35m'
reset_color = '\033[0m'
red_color = '\033[31m'

def BorrarPantalla():
    os.system('cls')

def linea(longitud, color):
    print(f"{color}{longitud * '-'}{reset_color}")

class Menu:
    def __init__(self, titulo="", opciones=[], color="\033[97m", color_numeros="\033[97m"):  
        self.titulo = titulo
        self.opciones = opciones
        self.color = color
        self.color_numeros = color_numeros
        
    def menu(self):
        print(f"{self.color}{self.titulo}{reset_color}")
        for index, opcion in enumerate(self.opciones, start=1):
            print(f"{self.color_numeros}{index}. {self.color}{opcion}{reset_color}")
        opc = input(f"{self.color_numeros}Elija opción [1...{len(self.opciones)}]: {self.color}") 
        return opc
    
def gotoxy(x, y):
    print(f"\033[{y};{x}H", end="")

def mensaje(msg,f,c):
    pass
