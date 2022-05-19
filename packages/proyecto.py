from actividad import *
from relacion import *
from fechas import *
from database.actividaddata import *
from database.relaciondata import *
from database.proyectodata import *


class Proyecto:
    def __init__(self, nombre: str, descripcion: str, fechaInicio, identificador = 0) -> None:
        self.identificador = identificador
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio
        
        self.actividades = []
        self.relaciones = []

        self.final = 0


    def crear_actividad(self):
        #identificador = len(self.actividades) + 1
        nombre = input("Ingrese nombre:\t")
        duracion = int(input("Ingrese duración en días:\t"))
        actividad = Actividad(nombre, duracion)
        self.actividades.append(actividad)

        return actividad
        ### Crear algún tipo de control para que ! self.actividades > 99

    def crear_relacion(self):
        #identificador = len(self.relaciones) + 1
        actividadPrecedente = int(input("Ingrese actividad precedente:\t"))
        actividadSiguiente = int(input("Ingrese actividad siguiente:\t"))
        relacion = Relacion(actividadPrecedente, actividadSiguiente)
        self.relaciones.append(relacion)

        return relacion

    def actualizar_bd(self):
        
        self.actividades = []
        for (a,b,c,d,e,f) in get_actividades(self.identificador):
            act = Actividad(b,c,a,e,f)
            self.actividades.append(act)

        self.relaciones = []
        for (a,b,c,d) in get_relaciones(self.identificador):
            rel = Relacion(b,c,a)
            self.relaciones.append(rel)

        for actividad in self.actividades:
            actividad.precedentes = [y.identificador for y in self.actividades if y.identificador in [x.actividadPrecedente for x in self.relaciones if x.actividadSiguiente == actividad.identificador]]
        
    def nodo_inicio(self):
        for actividad in self.actividades:
            if actividad.precedentes == []:
                actividad.fechaInicioTemprano = self.fechaInicio
                
                actividad.fechaInicioTardio = self.fechaInicio
                actividad.fechaFinTardio = sumardias(actividad.fechaInicioTardio, actividad.duracion)

                return actividad

    def calculo_Tardio(self, actividad):
        siguientes = [act for act in self.actividades if actividad.identificador in act.precedentes]

        if not siguientes:
            self.final = actividad
            self.final.fechaFinTemprano = self.final.fechaFinTardio
            self.final.fechaInicioTemprano = restardias(self.final.fechaFinTemprano, self.final.duracion)
            

        else:

            for siguiente in siguientes:
                if(compfechas(siguiente.fechaInicioTardio, actividad.fechaFinTardio) == 1):
                    siguiente.fechaInicioTardio = actividad.fechaFinTardio
                    siguiente.fechaFinTardio = sumardias(siguiente.fechaInicioTardio, siguiente.duracion)
                    self.calculo_Tardio(siguiente)

            
        
    def calculo_Temprano(self, actividad):
        if not actividad.precedentes:
            pass
        else:
            precs = [act for act in self.actividades if act.identificador in actividad.precedentes]
            for precedente in precs:
                if compfechas(precedente.fechaFinTemprano, actividad.fechaInicioTemprano) == -1:
                    precedente.fechaFinTemprano = actividad.fechaInicioTemprano
                    precedente.fechaInicioTemprano = restardias(precedente.fechaFinTemprano, precedente.duracion)
                    self.calculo_Temprano(precedente)
    
        



###################     Funciones externas referidas a proyecto

def crear_proyecto():
    ### identificador a definir formato !!!

    nombre = input("Ingrese un nombre para el nuevo proyecto:\t")
    descripcion = input("Descripcion:\t")
    fechaInicio = input("Fecha de Inicio? (aaaa/mm/dd):\t")

    return Proyecto(nombre, descripcion, fechaInicio)

   





