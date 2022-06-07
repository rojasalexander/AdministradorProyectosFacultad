import sqlite3
import sys

from numpy import split
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
        fechaFin text,
        noLaborales text
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
            identificador=proyecto[0],
            noLaborales= list(map(lambda x: int(x), list(proyecto[5])))
            )
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
        date.fromisoformat(proy.fechaInicio) + timedelta(days=365),
        "".join(str(x) for x in proy.noLaborales)
        )

    if (proy_max()):
        with connection:
            cur.execute("""INSERT INTO proyectos(nombre, descripcion, fecha, fechaFin, noLaborales) 
            VALUES (?, ?, ?, ?, ?)""", proyecto)
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
            identificador=aux[0],
            noLaborales= list(map(lambda x: int(x), list(aux[5])))
            )

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
    fechaFin = date.fromisoformat(proy.fechaInicio) + timedelta(days=365)
    noLab = "".join(str(x) for x in proy.noLaborales)
    with connection:
        cur.execute("""UPDATE proyectos SET nombre = :nombre, fecha = :fecha, descripcion = :descripcion, fechaFin = :fechaFin, noLaborales = :noLaborales 
        WHERE :identificador = identificador""",
            {
                "identificador": id,
                "nombre": proy.nombre, 
                "fecha": proy.fechaInicio,
                "descripcion": proy.descripcion,
                "fechaFin": proy.fechaFin,
                "noLaborales": noLab
            }
        )

def update_fecha_fin(id, fechaFin):
    with connection:
        cur.execute("""UPDATE proyectos SET fechaFin = :fechaFin
        WHERE :identificador = identificador""", {
            "identificador": id,
            "fechaFin": fechaFin
        })

def proy_max():
    if (not(len(get_proyectos()) == 999)):
        return True
    return False

def get_actividades_relaciones(proyecto_id):
    return [get_actividades(proyecto_id), get_relaciones(proyecto_id)]
    
    
connection.commit()

#Busca el proyecto que tenga como nombre el parametro dado
def buscar_proyectos(word):
    """Pasar una palabra cualquiera"""
    proyectos = get_proyectos()
    result = []
    for proyecto in proyectos:
        if (word.lower() in proyecto.nombre.lower()):
            result.append(proyecto)
    
    return result
