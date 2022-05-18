import sqlite3

#-----------------------------------Creamos una clase de prueba-----------------------------------------------
class Empleado:
    def __init__(self, nombre, sueldo) -> None:
        self.nombre = nombre
        self.sueldo = sueldo
    
    def imprimir_empleado(self):
        print("Empleado: ")
        print(f"Nombre: {self.nombre}\nSueldo: {self.sueldo}")

def crear_empleados():
    print("BIENVENIDO A BASE DE DATOS DE PRUEBA")
    while(True):
        x = input("Desea crear un empleado nuevo? (Y/N)")
        if(x == 'n' or x == 'N'):
            break
        
        nombre = input("Ingrese el nombre del empleado: ")
        sueldo = int(input("Ingrese el sueldo del empleado: "))
        empleado = Empleado(nombre, sueldo)
        crear_empleado(empleado)

def obtener_empleados():
    empleados = get_empleados()
    print(empleados)
        
#----------------------------Todo lo relacionado a la base de datos-----------------------------------------------

#Para conectarnos a una base de datos
#sqlite3.connect("nombre de la base de datos")
#Lo que hace es crear una archivo de base de datos donde vamos a almacenar todo
conn = sqlite3.connect("empleado.db")

#Creamos un cursor que nos permite hacer cosas en el archivo bd que creamos
cur = conn.cursor()

#Para crear una tabla usamos lo siguiente
#solo hay que crear una vez
try:
    cur.execute("""CREATE TABLE empleados(
        id integer primary key  autoincrement,
        nombre text,
        sueldo integer
        )""")
except:
    pass

def crear_empleado(emp: Empleado):
    empleado = (emp.nombre, emp.sueldo)
    with conn:
        cur.execute("INSERT INTO empleados (nombre, sueldo) VALUES (?, ?)", empleado)

def get_empleados():
    cur.execute("SELECT * FROM empleados"
    )
    return cur.fetchall()



crear_empleados()
obtener_empleados()

#basicamente, guarda los cambios
#siempre al final del archivo
conn.commit()
conn.close()    