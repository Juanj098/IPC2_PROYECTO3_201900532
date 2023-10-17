
usuarios = []
hash = []

def Analizador_Lexico(text,arrH,arrU):
    text += ' '
    char = ''
    pos = 0
    user = ''
    Hash = ''
    while text and  pos < len(text):
        char = text[pos]
        if char == '@':
            user , text = ArmarUs(text[pos:])
            if user:
                arrU.append(user)
                pos = 0
        if char == '#':
            Hash, text = ArmarHash(text[pos:])
            if Hash:
                arrH.append(Hash)
                pos = 0
            else:
                pos = 0
        pos+=1
    
def ArmarUs(cadena):
    pos = 0
    char = ''
    user = ''
    while cadena and pos < len(cadena):
        char = cadena[pos]
        if char != ' ':
            user+=char
        else:
            return user, cadena[pos:]
        pos+=1
    return None, None

def ArmarHash(cadena):
    pos = 1
    char = ''
    hasht = '#'
    while cadena and pos < len(cadena):
        char = cadena[pos]
        if char != ' ':
            if  char != '#':
                hasht+=char 
            elif char == '#' and len(hasht) > 2:
                hasht+=char
                return hasht, cadena[pos:]   
        else:
            return None, cadena[pos:]
        pos+=1
    return None, None


def Analisis_Emocion(cadena,diccionario):
    palPositivas = 0
    palNegativas = 0
    cadena = cadena.split(' ')
    for key,emociones in diccionario.items():
            for emocion in emociones:
                emocion = emocion.strip()
                for palabra in cadena:
                    if palabra.lower() == emocion.lower() and key == 'Positivas':
                        palPositivas+=1
                    elif palabra.lower() == emocion.lower() and key == 'Negativas':
                        palNegativas+=1
    if palPositivas > palNegativas:
        return f'Positivo'
    elif palNegativas > palPositivas:
        return f'Negativo'
    elif palNegativas == palPositivas:
        return f'Neutro'

# diccionario_palabras = {'Negativas': ['enojo','feo','triste','pesimo','decepcionado','insatisfecho'],'Positivas': ['feliz','bueno','excelente','bienvenidos','cool','satisfecho']}
# emocion = Analisis_Emocion('@Juanj098 Feliz anio #Happy#',diccionario_palabras)
# print(emocion)