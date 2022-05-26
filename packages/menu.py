# from database.proyectodata import create_proyecto, create_table
from database.proyectodata import get_proyectos
from proyecto import *
import sys
sys.path.append('database')
from database.actividaddata import *
from database.relaciondata import *
from database.proyectodata import *
from datetime import *
import pandas as pd
import numpy as np

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
            for a,b,c,d in proys:
                print(f"{a}".ljust(15), f"{b}".ljust(20), f"{d}".ljust(40), f"{c}".ljust(20))
            print("-" * 100)
            user = int(input("Ingrese el identificador del proyecto a cargar:\t"))
            [(a,b,c,d)] = get_proyecto_by_id(user)
            proy = Proyecto(b,d,c,a)
            
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
            pd.DataFrame(arr).to_excel(excel_writer = f'{proy.nombre}.xlsx', index_label = "Index", header  = ['Nombre', 'Fecha Inicio', 'Fecha Fin', 'Duracion estimada', 'Critico'])  
        
        elif(x == '4'):
            proy.mostrar_grafo()

