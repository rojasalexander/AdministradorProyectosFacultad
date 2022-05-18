import sqlite3
import sys
sys.path.append('packages')
from proyecto import Proyecto
from relaciondata import get_relaciones
from actividaddata import get_actividades



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
    with connection:
        cur.execute("""INSERT INTO proyectos(nombre, descripcion, fecha) 
        VALUES (?, ?, ?)""", proyecto)

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

#proyecto = Proyecto("hola", "manhana", "no")
#proyecto = Proyecto("hola", "manhana", "si")

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

def get_actividades_relaciones(proyecto_id):
    return [get_actividades(proyecto_id), get_relaciones(proyecto_id)]
    
    
connection.commit()
connection.close()