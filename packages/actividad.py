import datetime as date

class Actividad:
    def __init__(self, identificador: int, nombre: str, duracion: int, fechaInicioTemprano, fechaIniciotardio) -> None:
        self.identificador = identificador
        self.nombre = nombre
        self.duracion = duracion
        self.fechaInicioTemprano = fechaInicioTemprano
        self.fechaInicioTardio = fechaIniciotardio
