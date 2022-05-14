import datetime as date

class Actividad:
    def __init__(self, nombre: str, duracion: int, identificador = 0) -> None:
        self.identificador = identificador
        self.nombre = nombre
        self.duracion = duracion

        self.fechaInicioTemprano = 0
        self.fechaInicioTardio = 0

        # self.completado = False
        # self.enCurso = False

