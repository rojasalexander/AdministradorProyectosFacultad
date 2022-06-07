from calendar import weekday
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
        self.fechaFin = date.fromisoformat(fechaInicio) + timedelta(days = 365) if fechaFin == 0 else fechaFin
        
        
        self.actividades = []
        self.relaciones = []

        self.final = 0
        
        # provisional
        self.noLaborales = noLaborales
        self.feriados = []
        self.dias_laborales = []


    def imprimir_proyecto(self):
        print(f"""Nombre: {self.nombre}
        Descripcion: {self.descripcion}
        Fecha de inicio: {self.fechaInicio}
        Fecha fin: {self.fechaFin}
        Id: {self.identificador}
        Laborales: {self.noLaborales}
            """)

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
        for act in get_actividades(self.identificador):
            self.actividades.append(act)

        self.relaciones = []
        for rel in get_relaciones(self.identificador):
            self.relaciones.append(rel)

        for actividad in self.actividades:
            actividad.precedentes = [y.identificador for y in self.actividades if y.identificador in
                [x.actividadPrecedente for x in self.relaciones if x.actividadSiguiente == actividad.identificador]]
        for actividad in self.actividades: 
            actividad.siguientes = [act for act in self.actividades if actividad.identificador in act.precedentes]
        
        self.feriados = get_feriados_date()

        for i in range(0,365):
            dia = date.fromisoformat(self.fechaInicio) + timedelta(days = i)
            if(date.weekday(dia) not in self.noLaborales and 
                sin_anho(dia) not in self.feriados):

                self.dias_laborales.append(date.isoformat(dia))
            

        
    def nodo_inicio(self):
        for actividad in self.actividades:
            if actividad.precedentes == []:
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

        # print(rels)
        # print(relsnombres)
        
        
        # G = nx.DiGraph()
        # G.add_edges_from(relsnombres)

        # pos = nx.spring_layout(G)

        # nx.draw_networkx_nodes(G,pos, node_size = 500)
        # nx.draw_networkx_edges(G,pos, edgelist = G.edges(), edge_color= "black", arrowsize=15)
        # nx.draw_networkx_labels(G,pos)

        # mp.pyplot.show()


        g = Network(directed=True)
        g.add_nodes([a.nombre for a in self.actividades])
        g.add_edges(relsnombres)
        #g.show_buttons(filter_=True)
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