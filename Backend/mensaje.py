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
    def __init__(self,user,menciones,date) -> None:
        self.user = user
        self.fecha = date
        self.menciones = int(menciones)
    
    def __str__(self) -> str:
        return f'user: {self.user}, menciones: {self.menciones}'
class Hashtags:
    def __init__(self,hashtag,contador,date) -> None:
        self.Hashtag = hashtag
        self.date = date
        self.contador = int(contador)
    
    def __str__(self) -> str:
        return f'Hashtags: {self.Hashtag}, Contador: {self.contador} '

class MencionesFecha:
    def __init__(self,fecha) -> None:
        self.date = fecha
        self.menciones = []

class HashtagsFecha:
    def __init__(self,date) -> None:
        self.date = date
        self.Hashtags = []

class Emociones:
    def __init__(self,date) -> None:
        self.date = date
        self.positivo = 0
        self.negativo = 0
        self.neutro = 0

    def __str__(self) -> str:
        return f'<Fecha:{self.date}>: Positivas-{self.positivo}, Negativas-{self.negativo}, Neutro-{self.neutro}'
class resumenTweet:
    def __init__(self, date) -> None:
        self.date = date
        self.recibidos = 0
        self.users = 0
        self.hash = 0

    def __str__(self) -> str:
        return f'<fecha:{self.date}>, cont_Mensajes: {self.recibidos}, cont_Menciones:{self.users}, cont_Hashtags:{self.hash}'
    
class resumenEmociones:
    def __init__(self) -> None:
        self.positivas = 0
        self.positivas_rechazadas = 0
        self.negativas = 0
        self.negativas_rechazadas = 0
    
    def __str__(self) -> str:
        return f'positivas: {self.positivas}, P_rechazadas: {self.positivas_rechazadas}, negativas: {self.negativas}, N_rechazadas: {self.negativas_rechazadas}'
         