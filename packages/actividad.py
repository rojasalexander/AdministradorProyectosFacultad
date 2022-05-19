import datetime as date

class Actividad:
    def __init__(self, nombre: str, duracion: int) -> None:
        self.identificador = 0
        self.nombre = nombre
        self.duracion = duracion

        self.fechaInicioTemprano = 0
        self.fechaInicioTardio = 0

        # self.completado = False
        # self.enCurso = False

