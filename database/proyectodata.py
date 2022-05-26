import sqlite3
import sys
sys.path.append('packages')
sys.path.append('database')
from proyecto import Proyecto
from actividaddata import *
from relaciondata import *
from datetime import *



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
        descripcion text,
        fechaFin text
        )
    """)

def get_proyectos():
    """Devuelve un array de tuplas con todos los proyectos"""
    cur.execute("SELECT * FROM proyectos")
    aux = cur.fetchall()
    print(aux)
    if (len(aux) != 0):
        return list(map(
            lambda proyecto: 
            Proyecto(proyecto[1], 
            proyecto[3], 
            proyecto[2], 
            proyecto[4],
            identificador=proyecto[0])
            , 
            aux
            ))
    
    return []

def create_proyecto(proy: Proyecto):
    """Recibe el objeto proyecto"""
    proyecto = (
        proy.nombre, 
        proy.descripcion, 
        proy.fechaInicio, 
        proy.fechaInicio + timedelta(days=365)

        )

    if (proy_max()):
        with connection:
            cur.execute("""INSERT INTO proyectos(nombre, descripcion, fecha, fechaFin) 
            VALUES (?, ?, ?, ?)""", proyecto)
    else:
        return "404"

def get_proyecto_by_id(id):
    """Pasar el id del proyecto. Retorna el proyecto"""
    cur.execute("SELECT * FROM proyectos WHERE identificador = :identificador",
        {
            "identificador": id
        }
    )
    aux = cur.fetchone()
    if (aux == None):
        return "404"
    else:
        return Proyecto(
            aux[1], 
            aux[3], 
            aux[2], 
            aux[4],
            identificador=aux[0])

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
    fechaFin = proy.fechaInicio + timedelta(days=365)
    with connection:
        cur.execute("""UPDATE proyectos SET nombre = :nombre, fecha = :fecha, descripcion = :descripcion, fechaFin = :fechaFin 
        WHERE :identificador = identificador""",
            {
                "identificador": id,
                "nombre": proy.nombre, 
                "fecha": proy.fechaInicio,
                "descripcion": proy.descripcion,
                "fechaFin": fechaFin
            }
        )

def proy_max():
    if (not(len(get_proyectos()) == 999)):
        return True
    return False

def get_actividades_relaciones(proyecto_id):
    return [get_actividades(proyecto_id), get_relaciones(proyecto_id)]
    
    
connection.commit()

