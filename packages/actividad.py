import datetime as date

class Actividad:
    def __init__(self, 
    nombre: str, 
    duracion: int, 
    identificador = 0, 
    fechaInicioTemprano = '', 
    fechaInicioTardio = '',
    fechaFinTemprano = '',
    fechaFinTardio = '',
    critico = False) -> None:
        self.identificador = identificador
        self.nombre = nombre
        self.duracion = duracion

        self.fechaInicioTemprano = fechaInicioTemprano
        self.fechaInicioTardio = fechaInicioTardio

        self.fechaFinTemprano = fechaFinTemprano
        self.fechaFinTardio = fechaFinTardio

        self.precedentes = []       # Guarda las actividades de las que depende (Tipo: identificador)
        self.siguientes = []        # Guarda las actividades que dependen de él (Tipo: Actividad)

        self.critico = critico
        
        # self.completado = False
        # self.enCurso = False
    
    def setId(self, id):
        """Modifica el id al que traemos de la base de datos"""
        self.identificador = id     

