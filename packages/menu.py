from packages.proyecto import *
#from proyecto import crear_proyecto

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
            proy.crear_actividad()
        elif(x == "2"):
            proy.crear_relacion()
        
        print()
        print("-" * 100)
        print(f"Proyecto = {proy.nombre}")
        print(f"Actividades = {[x.nombre for x in proy.actividades]}")
        print(f"Relaciones = {[x.identificador for x in proy.relaciones]}")
        print("-" * 100)
        print()