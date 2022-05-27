import datetime as date

class Actividad:
    def __init__(self, 
    nombre: str, 
    duracion: int, 
    identificador = 0, 
    fechaInicioTemprano = 0, 
    fechaInicioTardio = 0,
    fechaFinTemprano = 0,
    fechaFinTardio = 0,
    critico = False) -> None:
        self.identificador = identificador
        self.nombre = nombre
        self.duracion = duracion

        self.fechaInicioTemprano = fechaInicioTemprano
        self.fechaInicioTardio = fechaInicioTardio

        self.fechaFinTemprano = fechaFinTemprano
        self.fechaFinTardio = fechaFinTardio

        self.precedentes = []

        self.critico = critico
        # self.completado = False
        # self.enCurso = False
    
    def setId(self, id):
        self.identificador = id

