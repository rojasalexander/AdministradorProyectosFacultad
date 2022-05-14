import sqlite3
import sys
sys.path.append('packages')
from proyecto import Proyecto



#Establecemos la conexion con la base de datos de proyectos
connection = sqlite3.connect("database.db")

#Creamos un cursor para poder añadir, eliminar, actualizar datos de la base de datos
cur = connection.cursor()

try:
    cur.execute("""
        CREATE TABLE proyectos(
        identificador integer,
        nombre text,
        fecha text,
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
        cur.execute("INSERT INTO proyectos VALUES (:identificador, :nombre, :fecha, :descripcion)",
            {
                "identificador": id,
                "nombre": proy.nombre, 
                "fecha": proy.fechaInicio,
                "descripcion": proy.descripcion
            }
        )

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



