class Relacion:
    def __init__(self, actividadPrecedente: int, actividadSiguiente: int, identificador = 0) -> None:
        self.identificador = identificador
        self.actividadPrecedente = actividadPrecedente
        self.actividadSiguiente = actividadSiguiente