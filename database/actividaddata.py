import sqlite3
import sys
sys.path.append('packages')
from actividad import Actividad


#Establecemos la conexion con la base de datos de proyectos
connection = sqlite3.connect("database.db")

#Creamos un cursor para poder añadir, eliminar, actualizar datos de la base de datos
cur = connection.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS actividades(
    identificador integer primary key autoincrement,
    nombre text,
    duracion integer,
    proyecto_id integer,
    fechaInicioTemprano text,
    fechaInicioTardio text
    )
""")


def get_actividades(proyecto_id):
    """Devuelve un array de tuplas con todas las actividades de un cierto proyecto"""
    cur.execute("SELECT * FROM actividades WHERE proyecto_id = :proyecto_id", 
    {"proyecto_id": proyecto_id})
    return cur.fetchall()

def create_actividad(act: Actividad, proyecto_id):
    """Pasar el objeto de actividad y el proyecto_id relacionado con la actividad"""
    if ( act_max(proyecto_id) ):
        with connection:
            actividad = (act.nombre, act.duracion, proyecto_id, 
            (act.fechaInicioTemprano, '')[act.fechaInicioTemprano != None], 
            (act.fechaInicioTardio, '')[act.fechaInicioTardio != None])
            with connection:
                cur.execute("""INSERT INTO actividades(
                    nombre, 
                    duracion, 
                    proyecto_id, 
                    fechaInicioTemprano, 
                    fechaInicioTardio)
                VALUES (?, ?, ?, ?, ?)""", actividad)
    else:
        print("Se ha alcanzado la cantidad máxima de actividades.")


def get_actividad_by_id(id, proyecto_id):
    """Pasar el id del proyecto. Retorna la actividad"""
    cur.execute("""SELECT * FROM relaciones 
    WHERE identificador = :identificador AND proyecto_id = :proyecto_id""",
        {
            "identificador": id,
            "proyecto_id": proyecto_id
        }
    )
    return cur.fetchall()

def delete_actividad(id, proyecto_id):
    """Pasar el id de la actividad a ser eliminada y el id del proyecto relacionado con esa actividad"""
    with connection:
        cur.execute("""DELETE from actividades 
        WHERE identificador = :identificador AND proyecto_id = :proyecto_id""", 
            {
                "identificador": id,
                "proyecto_id": proyecto_id
            }
        )

def modify_actividad(id, act: Actividad, proyecto_id):
    """Pasar el id de la actividad que se va a modificar, 
    el objeto de la actividad modificada y el proyecto_id"""
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

def delete_all_actividades(proyecto_id):
    with connection:
        cur.execute("""DELETE from actividades 
        WHERE proyecto_id = :proyecto_id""",
        {
            "proyecto_id": proyecto_id
        })


def act_max(proyecto_id):
    if(not(len(get_actividades(proyecto_id)) == 99)):
        return True
    return False


connection.commit()
