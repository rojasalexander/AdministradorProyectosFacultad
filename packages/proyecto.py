from packages.actividad import *
from packages.relacion import *

class Proyecto:
    def __init__(self, nombre: str, descripcion: str, fechaInicio, identificador = 0) -> None:
        self.identificador = identificador
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio
        
        self.actividades = []
        self.relaciones = []


    def crear_actividad(self):
        identificador = len(self.actividades) + 1
        nombre = input("Ingrese nombre:\t")
        duracion = int(input("Ingrese duración en días:\t"))

        self.actividades.append(Actividad(identificador, nombre, duracion))

        ### Crear algún tipo de control para que ! self.actividades > 99

    def crear_relacion(self):
        identificador = len(self.relaciones) + 1
        actividadPrecedente = int(input("Ingrese actividad precedente:\t"))
        actividadSiguiente = int(input("Ingrese actividad siguiente:\t"))

        self.relaciones.append(Relacion(identificador, actividadPrecedente, actividadSiguiente))

###################     Funciones externas referidas a proyecto

def crear_proyecto():
    ### identificador a definir formato !!!

    nombre = input("Ingrese un nombre para el nuevo proyecto:\t")
    descripcion = input("Descripcion:\t")
    fechaInicio = input("Fecha de Inicio? (aaaa/mm/dd):\t")

    return Proyecto(nombre, descripcion, fechaInicio)

   





