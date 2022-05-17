import sqlite3
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append('packages')
from proyectos import *

#Establecemos la conexion con la base de datos de proyectos
connection = sqlite3.connect("proyecto.db")

#Creamos un cursor para poder añadir, eliminar, actualizar datos de la base de datos
cur = connection.cursor()

try:
    cur.execute("""
        CREATE TABLE proyectos(
        id_proyecto integer,
        nombre_proyecto text,
        fecha_inicio text,
        descripcion text
        )
    """)
except:
    pass

def get_proyectos():
    """Devuelve un array de tuplas con todos los proyectos"""
    cur.execute("SELECT * FROM proyectos")
    return cur.fetchall()

def create_proyecto(proy: Proyecto):
    id = len(get_proyectos()) + 1
    with connection:
        cur.execute("INSERT INTO proyectos VALUES (:id_proyecto, :nombre_proyecto, :fecha_inicio, :descripcion)",
            {
                "id_proyecto": id,
                "nombre_proyecto": proy.nombre, 
                "fecha_inicio": proy.fechaInicio,
                "descripcion": proy.descripcion
            }
        )

def get_proyecto_by_id(id):
    cur.execute("SELECT * FROM proyectos WHERE id_proyecto = :id_proyecto",
        {
            "id_proyecto": id
        }
    )
    return cur.fetchall()





