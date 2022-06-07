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
    relaciones = cur.fetchall()

    return list(map(
        lambda relacion:
        Relacion(relacion[1], relacion[2], relacion[0]),
        relaciones
    ))

def create_relacion(rel: Relacion, proyecto_id):
    relacion = (rel.actividadPrecedente, rel.actividadSiguiente, proyecto_id)
    #controlar la cantidad de relaciones
    if(not max_relaciones(proyecto_id)):
        return "404"

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
    aux = cur.fetchone()
    if (aux != None):
        return Relacion(aux[1], aux[2], aux[0])
    
    return "404"

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
                "actividadPrecedente": rel.actividadPrecedente,
                "actividadSiguiente": rel.actividadSiguiente,
                "proyecto_id": proyecto_id
            }
        )

def delete_all_relaciones(proyecto_id):
    with connection:
        cur.execute("""DELETE from relaciones 
        WHERE proyecto_id = :proyecto_id""",
        {
            "proyecto_id": proyecto_id
        })

def max_relaciones(proyecto_id):
    """Controlar que la cantidad maxima de
    relaciones sea 149"""
    with connection:
        cur.execute("SELECT COUNT(*) FROM relaciones where proyecto_id = :proyecto_id",
        {
            "proyecto_id": proyecto_id
        })
        number = cur.fetchone()[0]
    
    if(number == 149):
        return False

    return True

connection.commit()


