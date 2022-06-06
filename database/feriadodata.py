import sqlite3

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
    with connection:
        cur.execute("INSERT INTO feriados(fecha) values(?)", fecha)

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
        return cur.fetchall()

connection.commit()