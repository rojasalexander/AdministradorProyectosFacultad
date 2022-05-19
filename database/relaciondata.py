import sqlite3
import sys
sys.path.append('packages')
from relacion import Relacion

#Establecemos la conexion con la base de datos de proyectos
connection = sqlite3.connect("database.db")

#Creamos un cursor para poder añadir, eliminar, actualizar datos de la base de datos
cur = connection.cursor()


cur.execute("""
    CREATE TABLE IF NOT EXISTS relaciones(
    identificador integer primary key autoincrement,
    actividadPrecedente integer,
    actividadSiguiente integer,
    proyecto_id integer
    )
""")

def get_relaciones(proyecto_id):
    """Devuelve un array de tuplas con todas las relaciones de un proyecto"""
    cur.execute("SELECT * FROM relaciones WHERE proyecto_id = :proyecto_id", 
    {"proyecto_id": proyecto_id})
    return cur.fetchall()

def create_relacion(rel: Relacion, proyecto_id):
    relacion = (rel.actividadPrecedente, rel.actividadSiguiente, proyecto_id)
    with connection:
        cur.execute("""INSERT INTO relaciones(
            actividadPrecedente, 
            actividadSiguiente, 
            proyecto_id) VALUES (?, ?, ?)""", relacion)

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
                "nombre": rel.nombre,
                "duracion": rel.duracion,
                "proyecto_id": proyecto_id,
                "fechaInicioTemprano": (rel.fechaInicioTemprano, '')[rel.fechaInicioTemprano != None],
                "fechaInicioTardio": (rel.fechaInicioTardio, '')[rel.fechaInicioTardio != None]
            }
        )

def delete_all_relaciones(proyecto_id):
    with connection:
        cur.execute("""DELETE from relaciones 
        WHERE proyecto_id = :proyecto_id""",
        {
            "proyecto_id": proyecto_id
        })

connection.commit()