class tweet:
    def __init__(self,fecha,txt) -> None:
        self.Date = fecha
        self.txt  = txt
        self.menciones = []
        self.Hash = []


class Palabra:
    def __init__(self, palabra, emocion) -> None:
        self.palabra = palabra
        self.sentimiento = emocion

