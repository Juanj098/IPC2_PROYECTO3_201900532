
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

# Analizador_Lexico('#info# hola @juan @Abirl y @paula bienvenidos a # @usacenlinea #SoyUSAC# #Ingenieria# @juanj098 #juanjo#')
# print(usuarios)
# print(hash)