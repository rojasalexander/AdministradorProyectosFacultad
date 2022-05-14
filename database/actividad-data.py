import sqlite3
import sys
sys.path.append('packages')
from actividad import *


#Establecemos la conexion con la base de datos de proyectos
connection = sqlite3.connect("database.db")

#Creamos un cursor para poder añadir, eliminar, actualizar datos de la base de datos
cur = connection.cursor()

try:
    cur.execute("""
        CREATE TABLE actividades(
        identificador integer,
        nombre text,
        duracion integer,
        proyecto_id integer,
        fechaInicioTemprano text,
        fechaInicioTardio text
        )
    """)
except:
    pass

def get_actividades(proyecto_id):
    """Devuelve un array de tuplas con todas las actividades de un cierto proyecto"""
    cur.execute("SELECT * FROM actividades WHERE proyecto_id = :proyecto_id", 
    {"proyecto_id": proyecto_id})
    return cur.fetchall()

def create_actividad(act: Actividad, proyecto_id):
    id = len(get_actividades()) + 1
    with connection:
        cur.execute("""INSERT INTO actividades VALUES 
        (:identificador, 
        :nombre, 
        :duracion, 
        :proyecto_id,
        :fechaInicioTemprano,
        :fechaInicioTardio)""",
            {
                "identificador": id,
                "nombre": act.nombre,
                "duracion": act.duracion,
                "proyecto_id": proyecto_id,
                "fechaInicioTemprano": (act.fechaInicioTemprano, '')[act.fechaInicioTemprano != None],
                "fechaInicioTardio": (act.fechaInicioTardio, '')[act.fechaInicioTardio != None]
            }
        )

def get_actividad_by_id(id, proyecto_id):
    """Pasar el id del proyecto. Retorna la actividad"""
    cur.execute("SELECT * FROM relaciones WHERE identificador = :identificador AND proyecto_id = :proyecto_id",
        {
            "identificador": id,
            "proyecto_id": proyecto_id
        }
    )
    return cur.fetchall()

def delete_actividad(id, proyecto_id):
    """Pasar el id del proyecto a ser eliminado"""
    with connection:
        cur.execute("DELETE from actividades WHERE identificador = :identificador AND proyecto_id = :proyecto_id", 
            {
                "identificador": id,
                "proyecto_id": proyecto_id
            }
        )

def modify_actividad(id, act: Actividad, proyecto_id):
    with connection:
        cur.execute("""UPDATE actividades SET 
        nombre = :nombre, 
        duracion = :duracion, 
        fechaInicioTemprano = :fechaInicioTemprano,
        fechaInicioTardio = :fechaInicioTardio
        WHERE :identificador = identificador AND :proyecto_id = proyecto_id""",
            {
                "identificador": id,
                "nombre": act.nombre,
                "duracion": act.duracion,
                "proyecto_id": proyecto_id,
                "fechaInicioTemprano": (act.fechaInicioTemprano, '')[act.fechaInicioTemprano != None],
                "fechaInicioTardio": (act.fechaInicioTardio, '')[act.fechaInicioTardio != None]
            }
        )