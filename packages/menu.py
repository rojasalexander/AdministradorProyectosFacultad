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
        print("Index".ljust(15), "Activity Description".ljust(50), "Required Predecessor".ljust(50), "Duration (Days)".ljust(50))
        for actividad in proy.actividades:
            print(
                f"{actividad.identificador}".ljust(15),
                f"{actividad.nombre}".ljust(50),
                f"{[y.identificador for y in proy.actividades if y.identificador in [x.actividadPrecedente for x in proy.relaciones if x.actividadSiguiente == actividad.identificador]]}".ljust(50),
                f"{actividad.duracion}"
                )
        print("-" * 100)
        print()

menu_principal()