# from database.proyectodata import create_proyecto, create_table
from database.proyectodata import get_proyectos
from feriadodata import *
from proyecto import *
import sys
sys.path.append('database')
from actividaddata import *
from relaciondata import *
from proyectodata import *
from datetime import *
import pandas as pd
import numpy as np

def prueba():
    a = get_proyecto_by_id(29)
    if (a != "404"):
        a.imprimir_proyecto()
    else:
        print("funciona porfis")


def menu_principal():

    print("Planificador de proyectos (alpha)")
    x = ""
    while(x != "0"):
        
        print("\t1: Crear Proyecto")
        print("\t2: Cargar Proyecto")
        print("\t0: Salir")
        x = input("Ingrese una opción:\t")

        if(x == "1"):
            proy = crear_proyecto()
            create_proyecto(proy)
            

        elif(x == "2"):
            print("\nCargar Proyectos:")
            proys = get_proyectos()
            print("Identificador".ljust(15), "Nombre".ljust(20), "Descripción".ljust(40), "Fecha de Inicio".ljust(20))
            for proy in proys:
                print(f"{proy.identificador}".ljust(15), f"{proy.nombre}".ljust(20), f"{proy.descripcion}".ljust(40), f"{proy.fechaInicio}".ljust(20))
            print("-" * 100)
            user = int(input("Ingrese el identificador del proyecto a cargar:\t"))
            proy = get_proyecto_by_id(user)
            
            menu_proyecto(proy)

        

def menu_proyecto(proy: Proyecto):

    
    
    x = ""
    while(x != "0"):
        proy.actualizar_bd()

        print()
        print("-" * 100)
        print(f"Proyecto = {proy.nombre}")
        print("Identificador".ljust(15), "Activity Description".ljust(50), "Required Predecessor".ljust(50), "Duration (Days)".ljust(50))
        for actividad in proy.actividades:
            print(
                f"{actividad.identificador}".ljust(15),
                f"{actividad.nombre}".ljust(50),
                f"{actividad.precedentes}".ljust(50),
                f"{actividad.duracion}"
                )
        print("-" * 100)
        print()
        print("\t1: Crear Actividad")
        print("\t2: Crear Relacion")
        print("\t3: Actualizar Cálculos")
        print("\t4: Ver grafo")
        print("\t0: Salir")
        x = input("Ingrese una opción:\t")

        if(x == "1"):
            act = proy.crear_actividad()
            create_actividad(act, proy.identificador)
        elif(x == "2"):
            rel = proy.crear_relacion()
            create_relacion(rel, proy.identificador)
        elif(x == "3"):
            proy.calculo_Tardio(proy.nodo_inicio())
            proy.calculo_Temprano(proy.final)
            proy.actividades_criticas()
            print()
            print("-" * 100)
            print("Nombre".ljust(20), "Duracion".ljust(15), "Fecha Inicio Temprano".ljust(15), "Fecha Fin Temprano".ljust(15), "Precedentes".ljust(15))
            for actividad in proy.actividades:
                print(
                    f"{actividad.nombre}".ljust(20),
                    f"{actividad.duracion}".ljust(15),
                    f"{actividad.fechaInicioTemprano}".ljust(15),
                    f"{actividad.fechaFinTemprano}".ljust(15),
                    f"{actividad.precedentes}".ljust(15)
                    )
            print("-" * 100)
            print("Nombre".ljust(20), "Duracion".ljust(15), "Fecha Inicio Tardío".ljust(15), "Fecha Fin Tardío".ljust(15), "Precedentes".ljust(15))
            for actividad in proy.actividades:
                print(
                    f"{actividad.nombre}".ljust(20),
                    f"{actividad.duracion}".ljust(15),
                    f"{actividad.fechaInicioTardio}".ljust(15),
                    f"{actividad.fechaFinTardio}".ljust(15),
                    f"{actividad.precedentes}".ljust(15)
                    )
            print("-" * 100)
            print()
            matrix = []
            for actividad in proy.actividades:
                matrix.append([actividad.nombre, actividad.fechaInicioTemprano, actividad.fechaFinTemprano, actividad.duracion, "Y" if actividad.critico else "N"])
            
            arr = np.asarray(matrix)
            pd.DataFrame(arr).to_csv('data.csv', index_label = "Index", header  = ['Tarea', 'Inicio', 'Fin', 'Duracion', 'Critico'])  
        
        elif(x == '4'):
            proy.mostrar_grafo()

print("cantidad de relaciones: ", max_relaciones(8))