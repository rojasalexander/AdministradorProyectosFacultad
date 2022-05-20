import datetime as date

class Actividad:
    def __init__(self, nombre: str, duracion: int, identificador = 0, fechaInicioTemprano = 0, fechaInicioTardio = 0) -> None:
        self.identificador = identificador
        self.nombre = nombre
        self.duracion = duracion

        self.fechaInicioTemprano = fechaInicioTemprano
        self.fechaInicioTardio = fechaInicioTardio

        self.fechaFinTemprano = "3000-01-01"
        self.fechaFinTardio = ""

        self.precedentes = []

        self.critico = False
        # self.completado = False
        # self.enCurso = False

