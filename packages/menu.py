# from database.proyectodata import create_proyecto, create_table
from proyecto import *
import sys
sys.path.append('database')
from actividaddata import *
from relaciondata import *
from proyectodata import *

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
            menu_proyecto(proy)
            

        elif(x == "2"):
            pass

        

def menu_proyecto(proy: Proyecto):
    
    x = ""
    while(x != "0"):
        print()
        print("\t1: Crear Actividad")
        print("\t2: Cargar Relacion")
        print("\t0: Salir")

        x = input("Ingrese una opción:\t")

        if(x == "1"):
            act = proy.crear_actividad()
            create_actividad(act, proy.identificador)
        elif(x == "2"):
            proy.crear_relacion()
        
        print()
        print("-" * 100)
        print(f"Proyecto = {proy.nombre}")
        print(f"Actividades = {[x.nombre for x in proy.actividades]}")
        print(f"Relaciones = {[x.identificador for x in proy.relaciones]}")
        print("-" * 100)
        print()

menu_principal()