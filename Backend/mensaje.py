class tweet:
    def __init__(self,fecha,txt) -> None:
        self.Date = fecha
        self.txt  = txt
        self.menciones = []
        self.Hash = []
        self.emocion = ''


class Palabra:
    def __init__(self, palabra, emocion) -> None:
        self.palabra = palabra
        self.sentimiento = emocion


class User:
    def __init__(self,user,menciones) -> None:
        self.user = user
        self.menciones = int(menciones)