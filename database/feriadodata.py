import sqlite3
from datetime import *

#Establecemos la conexion con la base de datos de proyectos
connection = sqlite3.connect("database.db")

#Creamos un cursor para poder añadir, eliminar, actualizar datos de la base de datos
cur = connection.cursor()

with connection:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS feriados(
            fecha text
        )
    """)

def create_feriado(fecha):
    fechaAux = fecha.split("-")
    fechaAux = fechaAux[1] + "-" + fechaAux[2]
    if(in_feriados(fechaAux)):
        return "404"

    with connection:
        cur.execute("INSERT INTO feriados(fecha) values(:fecha)", {"fecha": fechaAux})

def delete_feriado(fecha):
    with connection:
        cur.execute("DELETE from feriados WHERE fecha = :fecha",
        {
            "fecha": fecha
        }
        )

def get_feriados():
    with connection:
        cur.execute("SELECT * FROM feriados")
        fechas = cur.fetchall()
        
        return list(map(lambda fecha: fecha[0], fechas))

def get_feriados_date():
    with connection:
        cur.execute("SELECT * FROM feriados")
        fechas = get_feriados()
        
        return list(map(map_to_feriados, fechas))

connection.commit()

def in_feriados(fecha):
    return fecha in get_feriados()


def map_to_feriados(fecha:str):
    fechaAux = fecha.split("-")
    return date(2020, int(fechaAux[0]), int(fechaAux[1]))
    