import datetime as date

class Actividad:
    def __init__(self, identificador: int, nombre: str, duracion: int) -> None:
        self.identificador = identificador
        self.nombre = nombre
        self.duracion = duracion

        self.completado = False
        self.enCurso = False

        self.fechaInicioTemprano = 0
        self.fechaInicioTardio = 0
