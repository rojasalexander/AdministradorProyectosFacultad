from actividad import *
from relacion import *
from database.actividaddata import *
from database.relaciondata import *
from database.proyectodata import *
from datetime import *
import networkx as nx
import matplotlib as mp

class Proyecto:
    def __init__(self, nombre: str, descripcion: str, fechaInicio, fechaFin=0, identificador = 0) -> None:
        self.identificador = identificador
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        
        self.actividades = []
        self.relaciones = []

        self.final = 0

    def imprimir_proyecto(self):
        print(f"""Nombre: {self.nombre}
        Descripcion: {self.descripcion}
        Fecha de inicio: {self.fechaInicio}
        Fecha fin: {self.fechaFin}
        Id: {self.identificador}
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
                actividad.fechaFinTardio = date.isoformat(date.fromisoformat(actividad.fechaInicioTardio) + timedelta(days = actividad.duracion))

                return actividad

    def calculo_Tardio(self, actividad):
        siguientes = [act for act in self.actividades if actividad.identificador in act.precedentes]

        if not siguientes:
            self.final = actividad
            self.final.fechaFinTemprano = self.final.fechaFinTardio
            self.final.fechaInicioTemprano = date.isoformat(date.fromisoformat(self.final.fechaFinTemprano) - timedelta(days = self.final.duracion)) 
            

        else:

            for siguiente in siguientes:
                if siguiente.fechaInicioTardio == "" or date.fromisoformat(siguiente.fechaInicioTardio) < date.fromisoformat(actividad.fechaFinTardio):
                    siguiente.fechaInicioTardio = actividad.fechaFinTardio
                    siguiente.fechaFinTardio = date.isoformat(date.fromisoformat(siguiente.fechaInicioTardio) + timedelta(days = siguiente.duracion))
                    self.calculo_Tardio(siguiente)

            
        
    def calculo_Temprano(self, actividad):
        if not actividad.precedentes:
            pass
        else:
            precs = [act for act in self.actividades if act.identificador in actividad.precedentes]
            for precedente in precs:
                if precedente.fechaFinTemprano == "" or date.fromisoformat(precedente.fechaFinTemprano) > date.fromisoformat(actividad.fechaInicioTemprano) :
                    precedente.fechaFinTemprano = actividad.fechaInicioTemprano
                    precedente.fechaInicioTemprano = date.isoformat(date.fromisoformat(precedente.fechaFinTemprano) - timedelta(precedente.duracion))
                    self.calculo_Temprano(precedente)

    def actividades_criticas(self):
        for actividad in self.actividades:
            if date.fromisoformat(actividad.fechaInicioTemprano) == date.fromisoformat(actividad.fechaInicioTardio):
                actividad.critico = True

    def mostrar_grafo(self):
        
        rels = [[a.actividadPrecedente,a.actividadSiguiente] for a in self.relaciones]
        relsnombres = []
        for a in range(len(rels)):
            c = [e.nombre for e in self.actividades if e.identificador == rels[a][0]]
            d = [f.nombre for f in self.actividades if f.identificador == rels[a][1]]
            relsnombres.append((c[0], d[0]))

        print(rels)
        print(relsnombres)
        
        
        G = nx.DiGraph()
        G.add_edges_from(relsnombres)

        pos = nx.spring_layout(G)

        nx.draw_networkx_nodes(G,pos, node_size = 500)
        nx.draw_networkx_edges(G,pos, edgelist = G.edges(), edge_color= "black", arrowsize=15)
        nx.draw_networkx_labels(G,pos)

        mp.pyplot.show()
        



###################     Funciones externas referidas a proyecto

def crear_proyecto():
    ### identificador a definir formato !!!

    nombre = input("Ingrese un nombre para el nuevo proyecto:\t")
    descripcion = input("Descripcion:\t")
    fechaInicio = input("Fecha de Inicio? (aaaa-mm-dd):\t")

    return Proyecto(nombre, descripcion, fechaInicio)

   