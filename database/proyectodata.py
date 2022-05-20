import sqlite3
import sys
sys.path.append('packages')
<<<<<<< HEAD
from packages.proyecto import *
from database.relaciondata import *
from database.actividaddata import *
=======
from proyecto import Proyecto
>>>>>>> ed7797bbdd8371857cdd19ba2270aad14d7c6ec5



#Establecemos la conexion con la base de datos de proyectos
connection = sqlite3.connect("database.db")

#Creamos un cursor para poder añadir, eliminar, actualizar datos de la base de datos
cur = connection.cursor()


with connection:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS proyectos(
        identificador integer primary key autoincrement,
        nombre text,
        fecha text,
        descripcion text
        )
    """)

def get_proyectos():
    """Devuelve un array de tuplas con todos los proyectos"""
    cur.execute("SELECT * FROM proyectos")
    return cur.fetchall()

def create_proyecto(proy: Proyecto):
    proyecto = (proy.nombre, proy.descripcion, proy.fechaInicio)
    if (proy_max()):
        with connection:
            cur.execute("""INSERT INTO proyectos(nombre, descripcion, fecha) 
            VALUES (?, ?, ?)""", proyecto)
    else:
        print("Se ha alcanzado el numero maximo de proyectos")

def get_proyecto_by_id(id):
    """Pasar el id del proyecto. Retorna el proyecto"""
    cur.execute("SELECT * FROM proyectos WHERE identificador = :identificador",
        {
            "identificador": id
        }
    )
    return cur.fetchall()

def delete_proyecto(id):
    """Pasar el id del proyecto a ser eliminado"""
    with connection:
        cur.execute("DELETE from proyectos WHERE identificador = :identificador", 
            {
                "identificador": id
            }
        )
    delete_all_actividades(id)
    delete_all_relaciones(id)
    

def modify_proyecto(id, proy: Proyecto):
    with connection:
        cur.execute("""UPDATE proyectos SET nombre = :nombre, fecha = :fecha, descripcion = :descripcion
        WHERE :identificador = identificador""",
            {
                "identificador": id,
                "nombre": proy.nombre, 
                "fecha": proy.fechaInicio,
                "descripcion": proy.descripcion
            }
        )

def proy_max():
    if (not(len(get_proyectos()) == 999)):
        return True
    return False

def get_actividades_relaciones(proyecto_id):
    return [get_actividades(proyecto_id), get_relaciones(proyecto_id)]
    
    
connection.commit()
