import sqlite3
import sys
sys.path.append('packages')
from actividad import Actividad
from relaciondata import *


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
        fechaInicioTemprano text,
        fechaInicioTardio text,
        fechaFinTemprano text,
        fechaFinTardio text,
        critico integer,
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
    aux = cur.fetchall()

    if (len(aux) != 0):
        return list(map(
            lambda actividad:
            Actividad(actividad[1], 
            actividad[2], 
            actividad[0], 
            fechaInicioTemprano=actividad[3],
            fechaInicioTardio=actividad[4],
            fechaFinTemprano=actividad[5],
            fechaFinTardio=actividad[6],
            critico= True if actividad[7] == 1 else False 
            ),
            aux)
        )

    return []

"""
el insert lq hace es buscar la tabla que damos como nombre
e insertar los valores que pasamos ahi
"""
def create_actividad(act: Actividad, proyecto_id):
    """Pasar el objeto de actividad y el proyecto_id relacionado con la actividad"""
    if (act_max(proyecto_id)):
        actividad = (act.nombre, act.duracion, "", "", "", "", proyecto_id)
        with connection:
            cur.execute("""INSERT INTO actividades(
                nombre, 
                duracion,
                fechaInicioTemprano,
                fechaInicioTardio,
                fechaInicioTemprano,
                fechaFinTardio,
                proyecto_id
                )
            VALUES (?, ?, ?, ?, ?, ?, ?)""", actividad)
    else:
        return "404"


def get_actividad_by_id(id, proyecto_id):
    """Pasar el id del proyecto. Retorna la actividad"""
    cur.execute("""SELECT * FROM actividades 
    WHERE identificador = :identificador AND proyecto_id = :proyecto_id""",
        {
            "identificador": id,
            "proyecto_id": proyecto_id
        }
    )
    aux = cur.fetchone()
    if (aux == None):
        return "404"
    
    return Actividad(
        aux[1], 
        aux[2], 
        aux[0], 
        fechaInicioTemprano=aux[3],
        fechaInicioTardio=aux[4],
        fechaFinTemprano=aux[5],
        fechaFinTardio=aux[6],
        critico= True if aux[7] == 1 else False 
        )



"""
el delete busca la fila que cumpla con las condiciones dadas y elimina esa fila,
en este caso, busca el id de la actividad y el id del proyecto relacionado con 
esa actividad para poder eliminar la actividad correcta
"""
def delete_actividad_2(id, proyecto_id):
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
        fechaInicioTardio = :fechaInicioTardio,
        fechaFinTemprano = :fechaFinTemprano,
        fechaFinTardio = :fechaFinTardio,
        critico = :critico
        WHERE :identificador = identificador AND :proyecto_id = proyecto_id""",
            {
                "identificador": id,
                "nombre": act.nombre,
                "duracion": act.duracion,
                "fechaInicioTemprano": act.fechaInicioTemprano,
                "fechaInicioTardio": act.fechaInicioTardio,
                "fechaFinTemprano": act.fechaFinTemprano,
                "fechaFinTardio": act.fechaFinTardio,
                "critico": act.critico,
                "proyecto_id": proyecto_id,
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

def delete_actividad(id, proy):
    proy.actualizar_bd()
    actividad = [a for a in proy.actividades if id == a.identificador]
    print(actividad)
    if actividad:
        actividad = actividad[0]
        
        
        for precedente in actividad.precedentes:
            rel_id = [a.identificador for a in proy.relaciones if 
                a.actividadPrecedente == precedente and a.actividadSiguiente == actividad.identificador]
            delete_relacion(rel_id[0], proy.identificador)

        for siguiente in actividad.siguientes:
            
            rel_id = [a.identificador for a in proy.relaciones if 
                a.actividadPrecedente == actividad.identificador and a.actividadSiguiente == siguiente.identificador]

            print(rel_id)
            delete_relacion(rel_id[0], proy.identificador)

        delete_actividad_2(id, proy.identificador)
    

connection.commit()
