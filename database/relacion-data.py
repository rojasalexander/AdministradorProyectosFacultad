import sqlite3
import sys
sys.path.append('packages')
from relacion import *

#Establecemos la conexion con la base de datos de proyectos
connection = sqlite3.connect("database.db")

#Creamos un cursor para poder añadir, eliminar, actualizar datos de la base de datos
cur = connection.cursor()

try:
    cur.execute("""
        CREATE TABLE relaciones(
        identificador integer,
        actividadPrecedente integer,
        actividadSiguiente integer,
        proyecto_id integer
        )
    """)
except:
    pass

def get_relaciones(proyecto_id):
    """Devuelve un array de tuplas con todas las relaciones de un proyecto"""
    cur.execute("SELECT * FROM relaciones WHERE proyecto_id = :proyecto_id", 
    {"proyecto_id": proyecto_id})
    return cur.fetchall()

def create_relacion(rel: Relacion, proyecto_id):
    id = len(get_relaciones()) + 1
    with connection:
        cur.execute("""INSERT INTO relaciones VALUES 
        (:identificador, 
        :actividadPrecedente, 
        :actividadSiguiente, 
        :proyecto_id
        )""",
            {
                "identificador": rel.identificador,
                "actividadPrecedente": rel.actividadPrecedente,
                "actividadSiguiente": rel.actividadSiguiente,
                "proyecto_id": proyecto_id
            }
        )

def get_relacion_by_id(id, proyecto_id):
    """Pasar el id del proyecto. Retorna el proyecto"""
    cur.execute("SELECT * FROM relaciones WHERE identificador = :identificador AND proyecto_id = :proyecto_id",
        {
            "identificador": id,
            "proyecto_id": proyecto_id
        }
    )
    return cur.fetchall()

def delete_relacion(id, proyecto_id):
    """Pasar el id del proyecto a ser eliminado"""
    with connection:
        cur.execute("DELETE from relaciones WHERE identificador = :identificador AND proyecto_id = :proyecto_id", 
            {
                "identificador": id,
                "proyecto_id": proyecto_id
            }
        )

def modify_relacion(id, rel: Relacion, proyecto_id):
    with connection:
        cur.execute("""UPDATE relaciones SET 
        identificador = :identificador, 
        actividadPrecedente = :actividadPrecedente, 
        actividadSiguiente = :actividadSiguiente, 
        proyecto_id = :proyecto_id
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
