import sqlite3
import sys
sys.path.append('packages')
from actividad import Actividad


#Establecemos la conexion con la base de datos de proyectos
connection = sqlite3.connect("database.db")

#Creamos un cursor para poder añadir, eliminar, actualizar datos de la base de datos
cur = connection.cursor()

"""
create table lq hace es crear una tabla, if not exists crea solo si
la tabla todavia no existe
primary key sirve para destacar la columna y tiene un valor not null siempre
"""
with connection:
    cur.execute("""CREATE TABLE IF NOT EXISTS actividades(
        identificador integer primary key autoincrement,
        nombre text,
        duracion integer,
        proyecto_id integer)
        """)


"""
el select lo que hace es seleccionar de acuerdo a los parametros que le damos,
por ejemplo, ahi decimos select where proyecto_id es igual al parametro que
definimos en la funcion, eso significa que trae todos los elementos que tengan ese
proyecto_id dentro de la tabla actividades.
"""
def get_actividades(proyecto_id):
    """Devuelve un array de tuplas con todas las actividades de un cierto proyecto"""
    cur.execute("SELECT * FROM actividades WHERE proyecto_id = :proyecto_id", 
    {"proyecto_id": proyecto_id})
    return cur.fetchall() #el fetchall trae todos los valores que cumplan las condiciones dadas


"""
el insert lq hace es buscar la tabla que damos como nombre
e insertar los valores que pasamos ahi
"""
def create_actividad(act: Actividad, proyecto_id):
    """Pasar el objeto de actividad y el proyecto_id relacionado con la actividad"""
    if ( act_max(proyecto_id) ):
        actividad = (act.nombre, act.duracion, proyecto_id)
        with connection:
            cur.execute("""INSERT INTO actividades(
                nombre, 
                duracion, 
                proyecto_id
                )
            VALUES (?, ?, ?)""", actividad)
    else:
        print("Se ha alcanzado la cantidad máxima de actividades.")


def get_actividad_by_id(id, proyecto_id):
    """Pasar el id del proyecto. Retorna la actividad"""
    cur.execute("""SELECT * FROM actividades 
    WHERE identificador = :identificador AND proyecto_id = :proyecto_id""",
        {
            "identificador": id,
            "proyecto_id": proyecto_id
        }
    )
    return cur.fetchall()


"""
el delete busca la fila que cumpla con las condiciones dadas y elimina esa fila,
en este caso, busca el id de la actividad y el id del proyecto relacionado con 
esa actividad para poder eliminar la actividad correcta
"""
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
        duracion = :duracion
        WHERE :identificador = identificador AND :proyecto_id = proyecto_id""",
            {
                "identificador": id,
                "nombre": act.nombre,
                "duracion": act.duracion,
                "proyecto_id": proyecto_id
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
