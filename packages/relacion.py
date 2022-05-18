class Relacion:
    def __init__(self, identificador: int, actividadPrecedente: int, actividadSiguiente: int) -> None:
        self.identificador = identificador
        self.actividadPrecedente = actividadPrecedente
        self.actividadSiguiente = actividadSiguiente