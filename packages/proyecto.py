from pyvis.network import Network



from datetime import *
import pandas as pd
import numpy as np

import matplotlib as mp
from pyvis import *

from actividaddata import *

from relaciondata import *
from feriadodata import *

class Proyecto:
    def __init__(self, nombre: str, descripcion: str, fechaInicio, fechaFin=0, identificador = 0, noLaborales = [5, 6]) -> None:
        self.identificador = identificador
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        
        self.actividades = []   # Lista vacia para rellenar en el proceso
        self.relaciones = []

        self.final = 0          # Contenedor de nodo final (Tipo: Actividad)
        
        self.noLaborales = noLaborales
        self.feriados = []      # Para traer luego de la database
        self.dias_laborales = []    # Cálculo


    def imprimir_proyecto(self):
        print(f"""Nombre: {self.nombre}
        Descripcion: {self.descripcion}
        Fecha de inicio: {self.fechaInicio}
        Fecha fin: {self.fechaFin}
        Id: {self.identificador}
        Laborales: {self.noLaborales}
            """)

### Versión anterior

    def crear_actividad(self):
        """Versión primitiva de crear actividad"""
        #identificador = len(self.actividades) + 1
        nombre = input("Ingrese nombre:\t")
        duracion = int(input("Ingrese duración en días:\t"))
        actividad = Actividad(nombre, duracion)
        self.actividades.append(actividad)

        return actividad

    def crear_relacion(self):
        #identificador = len(self.relaciones) + 1
        actividadPrecedente = int(input("Ingrese actividad precedente:\t"))
        actividadSiguiente = int(input("Ingrese actividad siguiente:\t"))
        relacion = Relacion(actividadPrecedente, actividadSiguiente)
        self.relaciones.append(relacion)

        return relacion

### 


    def actualizar_bd(self):
        """Trae los cambios desde la base de datos al programa"""

        self.actividades = []
        for act in get_actividades(self.identificador):     # Rellena la lista de actividades de un proyecto.   
            self.actividades.append(act)

        self.relaciones = []
        for rel in get_relaciones(self.identificador):      # Rellena la lista de relaciones de un proyecto desde la base de datos
            self.relaciones.append(rel)

        for actividad in self.actividades:
            actividad.precedentes = [x.actividadPrecedente for x in self.relaciones if x.actividadSiguiente == actividad.identificador]
            # lista de actividades de las que depende cada actividad (Tipo: Identificador)
        for actividad in self.actividades: 
            actividad.siguientes = [act for act in self.actividades if actividad.identificador in act.precedentes]
            # lista de actividades que dependen de cada actividad. (Tipo: Actividad)
        
        self.feriados = get_feriados_date()     # Recupera los feriados de la base de datos

        for i in range(0,365):                  # Para cada día desde hoy hasta un año posterior
            dia = date.fromisoformat(self.fechaInicio) + timedelta(days = i)  # Dias del año en date
            if(date.weekday(dia) not in self.noLaborales and   # Si ese día no es un dia no laboral o un feriado
                sin_anho(dia) not in self.feriados):

                self.dias_laborales.append(date.isoformat(dia))    # Se añaden a dias_laborales
            

        
    def nodo_inicio(self):
        """Calcular con qué nodo empieza el camino"""
        for actividad in self.actividades:      # Para cada actividad en la lista de actividades del proyecto
            if actividad.precedentes == []:     # Si esa actividad no tiene precedentes, es un nodo inicio.

                actividad.fechaInicioTemprano = self.dias_laborales[0]
                actividad.fechaInicioTardio = self.dias_laborales[0]
                actividad.fechaFinTardio = self.dias_laborales[self.dias_laborales.index(actividad.fechaInicioTardio) + actividad.duracion]

                return actividad

    def calculo_Tardio(self, actividad):
        

        if not actividad.siguientes:
            self.final = actividad
            self.final.fechaFinTemprano = self.final.fechaFinTardio
            self.final.fechaInicioTemprano = self.dias_laborales[self.dias_laborales.index(actividad.fechaFinTemprano) - actividad.duracion]
            self.fechaFin = self.final.fechaFinTemprano

        else:
            for siguiente in actividad.siguientes:
                if siguiente.fechaInicioTardio == "" or siguiente.fechaInicioTardio == '0' or date.fromisoformat(siguiente.fechaInicioTardio) <= date.fromisoformat(actividad.fechaFinTardio):
                    siguiente.fechaInicioTardio = actividad.fechaFinTardio
                    siguiente.fechaFinTardio = self.dias_laborales[self.dias_laborales.index(siguiente.fechaInicioTardio) + siguiente.duracion]
                self.calculo_Tardio(siguiente)

            
        
    def calculo_Temprano(self, actividad):
        if not actividad.precedentes:
            pass
        else:
            precs = [act for act in self.actividades if act.identificador in actividad.precedentes]
            for precedente in precs:
                if precedente.fechaFinTemprano == "" or precedente.fechaFinTemprano == None or date.fromisoformat(precedente.fechaFinTemprano) >= date.fromisoformat(actividad.fechaInicioTemprano) :
                    precedente.fechaFinTemprano = actividad.fechaInicioTemprano
                    precedente.fechaInicioTemprano = self.dias_laborales[self.dias_laborales.index(precedente.fechaFinTemprano) - precedente.duracion]
                self.calculo_Temprano(precedente)

    def actividades_criticas(self):
        for actividad in self.actividades:
            if actividad.fechaInicioTemprano != '':
                if date.fromisoformat(actividad.fechaInicioTemprano) == date.fromisoformat(actividad.fechaInicioTardio):
                    actividad.critico = True

    def mostrar_grafo(self):
        
        rels = [[a.actividadPrecedente,a.actividadSiguiente] for a in self.relaciones]
        relsnombres = []
        for a in range(len(rels)):
            c = [e.nombre for e in self.actividades if e.identificador == rels[a][0]]
            d = [f.nombre for f in self.actividades if f.identificador == rels[a][1]]
            relsnombres.append((c[0], d[0]))


        g = Network(directed=True)
        nombres = [a.nombre for a in self.actividades]
        identificadores = [a.identificador for a in self.actividades]
        identificadores = list(map(str,identificadores))
        colores = ["#00ff1e" if a.critico else '' for a in self.actividades ]

        print(nombres)
        print(colores)
        for i in range(len(nombres)):
            if colores[i] == "#00ff1e":
                g.add_node(nombres[i], label = identificadores[i], title = nombres[i], color = colores[i])
            else:
                g.add_node(nombres[i], label = identificadores[i], title = nombres[i])
        g.add_edges(relsnombres)
        g.show("tmp.html")

        

    def actualizarCsv(self):
        self.calculo_Tardio(self.nodo_inicio())
        self.calculo_Temprano(self.final)
        self.actividades_criticas()

        matrix = []
        for actividad in self.actividades:
            matrix.append([actividad.nombre, actividad.fechaInicioTemprano, actividad.fechaFinTemprano, actividad.duracion, "Y" if actividad.critico else "N"])
            modify_actividad(actividad.identificador, actividad, self.identificador)
        
        arr = np.asarray(matrix)
        pd.DataFrame(arr).to_csv('data.csv', index_label = "Index", header  = ['Tarea', 'Inicio', 'Fin', 'Duracion', 'Critico'])


    # def calcularFechaFin(self):
    #     update_fecha_fin(self.identificador, self.fechaFin)
        

        

###################     Funciones externas referidas a proyecto

def crear_proyecto():
    ### identificador a definir formato !!!

    nombre = input("Ingrese un nombre para el nuevo proyecto:\t")
    descripcion = input("Descripcion:\t")
    fechaInicio = input("Fecha de Inicio? (aaaa-mm-dd):\t")

    return Proyecto(nombre, descripcion, fechaInicio)

def entre_fechas(fechainicio: date, fechafin: date, actual: date):
    if(actual >= fechainicio and actual <= fechafin):
        return True
    return False

def sin_anho(fecha: date):
    #print(fecha)
    return fecha.replace(year = 2020)