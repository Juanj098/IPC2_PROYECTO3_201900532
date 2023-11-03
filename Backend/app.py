from flask import Flask,jsonify,request
import xml.etree.ElementTree as ET
from flask_cors import CORS
from analizadores import Analizador_Lexico, Analisis_Emocion
import re   
from datetime import datetime 
import xml.dom.minidom
import base64

from mensaje import tweet,User,Hashtags,MencionesFecha,HashtagsFecha,Emociones,resumenTweet,resumenEmociones

HFecha = []
EFecha = []
resumenTw = []
MFecha = []
usuarios = []
Hashs = []
mensajes = []
tweet_Json = []
emos_Json = []
twets =[]

diccionario_palabras = {'Negativas': [],'Positivas': [],'rechazadas_P':[], 'rechazadas_N':[]}

def sort_list(list):
    pass

app = Flask(__name__)

CORS(app)

@app.route('/ping')
def ping():
    return jsonify({'respuesta':'pong!'})

@app.route('/Clear')
def Clear():
    mensajes.clear()
    tweet_Json.clear()
    diccionario_palabras['Negativas'].clear()
    diccionario_palabras['Positivas'].clear()
    diccionario_palabras['rechazadas_P'].clear()
    diccionario_palabras['rechazadas_N'].clear()

    path1 = 'DB_tweets.xml'
    tree = ET.parse(path1)
    root1 = tree.getroot()
    for elm in root1.findall('MENSAJE'):
        root1.remove(elm)

    path2 = 'DB_Emociones.xml'
    tree = ET.parse(path2)
    root2 = tree.getroot()
    for elm in root2.findall('sentimientos_positivos'):
        root2.remove(elm)
    for elm in root2.findall('sentimientos_negativos'):
        root2.remove(elm)
    return jsonify({'info':'Listas vacias'})

@app.route('/Xml_tweets', methods =['POST'])
def Xml_tweets():
    if 'file' not in request.files:
        return jsonify({'error':'intente enviar de nuevo el documento'})
    file = request.files['file']
    if file:
        xmlDoc = file.read().decode('utf-8')
        try:
            root = ET.fromstring(xmlDoc)
            for mensaje in root.findall('MENSAJE'):
                fecha = mensaje.find('FECHA').text
                text = mensaje.find('TEXTO').text
                text = text.strip()
                newtweet = tweet(fecha,text)
                Analizador_Lexico(newtweet.txt,newtweet.Hash,newtweet.menciones)
                if len(diccionario_palabras['Positivas']) > 0 and len(diccionario_palabras['Negativas'])>0:
                    newtweet.emocion = Analisis_Emocion(newtweet.txt,diccionario_palabras)
                mensajes.append(newtweet)
            
            path = 'DB_tweets.xml'
            regex = r'\d+\/\d+\/\d+'
            tree = ET.parse(path)
            root = tree.getroot()
            for elm in root.findall('MENSAJE'):
                root.remove(elm)
            
            for mensaje in mensajes:
                message = ET.Element('MENSAJE')
                date = ET.SubElement(message,'FECHA')
                date.text = re.search(regex,mensaje.Date).group()
                txt = ET.SubElement(message,'TEXTO')
                txt.text = mensaje.txt
                root.append(message)

            root = ET.tostring(root,encoding='utf-8')
            root = xml.dom.minidom.parseString(root)
            root = root.toprettyxml(indent='    ')
            with open('DB_tweets.xml','w',encoding='utf-8') as xmlFile:
                xmlFile.write(root)

            return jsonify({'xml':'archivo xml procesado con exito..'})
        except Exception as e:
            return jsonify({'error':str(e)})
    else:
        return jsonify({'info':'no selecciono ningun archivo'})

@app.route('/Xml_Palabras', methods = ['POST'])
def Xml_Palabras():
    if 'file' not in request.files:
        return jsonify({'error':'intente enviar de nuevo el documento'})
    file = request.files['file']
    if file:
        xmlD = file.read().decode('utf-8')
        try:
            root = ET.fromstring(xmlD)
            for Positivos in root.findall('sentimientos_positivos'):
                for palabra in Positivos.findall('palabra'):
                    Palabra = palabra.text
                    diccionario_palabras['Positivas'].append(Palabra)
            for Negativos in root.findall('sentimientos_negativos'):
                for palabra in Negativos.findall('palabra'):
                    Palabra = palabra.text
                    diccionario_palabras['Negativas'].append(Palabra)
            if len(mensajes) > 0:
                for tweet in mensajes:
                    tweet.emocion = Analisis_Emocion(tweet.txt,diccionario_palabras)
                
            path = 'DB_Emociones.xml'
            tree = ET.parse(path)
            root = tree.getroot()
            for elm in root.findall('sentimientos_positivos'):
                root.remove(elm)
            for elm in root.findall('sentimientos_negativos'):
                root.remove(elm)

            for key, valors in diccionario_palabras.items():
                if key == 'Positivas':
                    sP = ET.Element('sentimientos_positivos')
                    for value in valors:
                        palab = ET.SubElement(sP,'palabra')
                        palab.text = value
                    root.append(sP)
                if key == 'Negativas':
                    sN = ET.Element('sentimientos_negativos')
                    for value in valors:
                        palab = ET.SubElement(sN,'palabra')
                        palab.text = value
                    root.append(sN)

            root = ET.tostring(root, encoding='utf-8')
            root = xml.dom.minidom.parseString(root)
            root = root.toprettyxml(indent='    ')
            with open('DB_Emociones.xml','w',encoding='utf-8') as xmlFile:
                xmlFile.write(root)

            return jsonify({'info':'archivo xml procesado con exito...'})
        except Exception as e:
            return jsonify({'error': e})
    else:
        return jsonify({'info':'no selecciono ningun archivo'})

@app.route('/tweets')
def tweets():
    if len(mensajes) > 0:
        return jsonify({'tweets':[tweet.__dict__ for tweet in mensajes]})
    else:
        return jsonify({'info':'lista vacia'})
    
@app.route('/emociones')
def emociones():
    if (len(diccionario_palabras['Negativas']) > 0) or (len(diccionario_palabras['Positivas']) > 0):
        for clave,valor in diccionario_palabras.items():
            for emocion in valor:
                emo = {'emocion':clave,'palabra':emocion}
                emos_Json.append(emo)
        return jsonify(emos_Json)
    else:
        return jsonify({'info':'lista vacia'})
    
@app.route('/Analizar')
def Analizar():
    if mensajes:
        return jsonify({'info':'lista ocupada'})
    else:
        return jsonify({'info':'lista vacia'})
    
@app.route('/menciones/<string:dateMin>_<string:dateMax>', methods = ['GET'])
def date(dateMin,dateMax):
    try:
        MFecha.clear()
        twets.clear()
        date = ''
        regex = r'\d+\/\d+\/\d+'
        dateMin = dateMin.replace('.','/')
        dateMax = dateMax.replace('.','/')
    
        dateMin = datetime.strptime(dateMin,'%d/%m/%Y')
        dateMax = datetime.strptime(dateMax,'%d/%m/%Y')
    
        # filtra por rango de fechas
        if len(mensajes) > 0:
            for tweet in mensajes:
                date = re.search(regex,tweet.Date).group()
                date =datetime.strptime(date,'%d/%m/%Y')
                if dateMin <= date  and date <= dateMax:
                    twets.append(tweet)
        else:
            return jsonify({'info':'lista vacia'})
        
        # busca usuarios iguales o crea nuevos y cuenta las menciones
        if len(twets) > 0:
            usuarios.clear()
            fechas_menciones = []
            cont = 1
            for tw in twets:

                date = tw.Date
                date = re.search(regex,date).group()
                date = datetime.strptime(date,'%d/%m/%Y')
                date = date.strftime('%d/%m/%Y')

                for us in tw.menciones:
                    user_exist = False
                    for usuario in usuarios:
                        if usuario.user == us and usuario.fecha == date:
                            usuario.menciones+=1
                            user_exist = True
                            break
                    if not user_exist:
                        user = User(us,cont,date)
                        usuarios.append(user)

            for tw in twets:
                mf_exist = False

                date = tw.Date
                date = re.search(regex,date).group()
                date = datetime.strptime(date,'%d/%m/%Y')
                date = date.strftime('%d/%m/%Y')

                for mf in MFecha:
                    if mf.date == date:
                        mf_exist = True
                        break                    
                if not mf_exist:
                    mf = MencionesFecha(date)
                    MFecha.append(mf)

            for mf in MFecha:
                for usuario in usuarios:
                    if mf.date == usuario.fecha:
                        mf.menciones.append(usuario)

            for mf in MFecha:
                newObj = {
                    'fecha':mf.date,
                    'menciones':[]
                }
                for user in mf.menciones:
                    mencion = {
                        'user': user.user,
                        'contador':str(user.menciones)
                    }
                    newObj['menciones'].append(mencion)
                fechas_menciones.append(newObj)

            return jsonify({'info':fechas_menciones})
        else:
            return jsonify({'info':'lista vacia'})
    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/Hashtags/<string:dateMin>_<string:dateMax>', methods = ['GET'])
def Hash(dateMin,dateMax):
    try:    
        twets.clear()
        HFecha.clear()
        fechas_Hashtag = []
        regex = r'\d+\/\d+\/\d+'
        dateMin = dateMin.replace('.','/')
        dateMax = dateMax.replace('.','/')
        
        dateMin = datetime.strptime(dateMin,'%d/%m/%Y')
        dateMax = datetime.strptime(dateMax,'%d/%m/%Y')
        
        if len(mensajes) > 0:
            for mensaje in mensajes:
                date = re.search(regex,mensaje.Date).group()
                date = datetime.strptime(date,'%d/%m/%Y')
                if date >= dateMin and date <= dateMax:
                    twets.append(mensaje)
        else:
            return jsonify({'info':'lista vacia'})    
        
        if len(twets) > 0:
            Hashs.clear()
            for tw in twets:

                date = tw.Date
                date = re.search(regex,date).group()
                date = datetime.strptime(date,'%d/%m/%Y')
                date = date.strftime('%d/%m/%Y')

                for hash in tw.Hash:
                    Hash_exist = False
                    for Hash in Hashs:
                        if Hash.Hashtag == hash and Hash.date == date:
                            Hash.contador+=1
                            Hash_exist = True
                            break
                    if not Hash_exist:
                        hs = Hashtags(hash,1,date)
                        Hashs.append(hs)

            for tw in twets:
                hf_exist = False
            
                date = tw.Date
                date = re.search(regex,date).group()
                date = datetime.strptime(date,'%d/%m/%Y')
                date = date.strftime('%d/%m/%Y')

                for hf in HFecha:
                    if hf.date == date:
                        hf_exist = True
                        break
                if not hf_exist:
                    hf = HashtagsFecha(date)
                    HFecha.append(hf)
                
            for hf in HFecha:
                for has in Hashs:
                    if hf.date == has.date:
                        hf.Hashtags.append(has)
                
            for hf in HFecha:
                newObj = {
                    'fecha': hf.date,
                    'Hashtags':[]
                }
                for has in hf.Hashtags:
                    Hash_obj = {
                        'Hashtag': has.Hashtag,
                        'contador': str(has.contador)
                    }
                    newObj['Hashtags'].append(Hash_obj)                        
                fechas_Hashtag.append(newObj)
                

            return jsonify({'info':fechas_Hashtag})
        else:
            return jsonify({'error':'lista vacia'})
        
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/Emociones/<string:fechaInicial>_<string:fechaMaxima>' ,methods =['GET'])
def Emos(fechaInicial,fechaMaxima):
    try:
        fecha_E = []
        EFecha.clear()
        tempEmo = []
        regex = r'\d+\/\d+\/\d+'
        fechaInicial = fechaInicial.replace('.','/')
        fechaInicial = datetime.strptime(fechaInicial,'%d/%m/%Y')
        fechaMaxima = fechaMaxima.replace('.','/')
        fechaMaxima = datetime.strptime(fechaMaxima,'%d/%m/%Y')
        if len(mensajes) > 0 and (len(diccionario_palabras['Positivas']) > 0 or len(diccionario_palabras['Negativas']) > 0):
            for mensaje in mensajes:
                date = mensaje.Date
                date = re.search(regex,date).group()
                date = datetime.strptime(date,'%d/%m/%Y')
                if (date >= fechaInicial) and (date <= fechaMaxima):
                    date = date.strftime('%d/%m/%Y')
                    tempEmo.append(mensaje)

            if len(tempEmo) > 0:
                for temporal in tempEmo:
                    E_exist = False
                    date = temporal.Date
                    date = re.search(regex,date).group()
                    for Ef in EFecha:
                        if Ef.date == date:
                            E_exist = True
                            break
                    if not E_exist:
                        newEmo = Emociones(date)
                        EFecha.append(newEmo)

                for Ef in EFecha:
                    for temporal in tempEmo:
                        dateTem = temporal.Date
                        dateTem = re.search(regex,dateTem).group()
                        if dateTem == Ef.date:
                            if temporal.emocion == 'Positivo':
                                Ef.positivo+=1
                            elif temporal.emocion == 'Negativo':
                                Ef.negativo+=1
                            elif temporal.emocion =='Neutro':
                                Ef.neutro+=1
                            else:
                                pass
                
                for Ef in EFecha:
                    newObj ={
                        'fecha':Ef.date,
                        'M_positivos':Ef.positivo,
                        'M_negativos':Ef.negativo,
                        'M_neutros':Ef.neutro
                    }
                    fecha_E.append(newObj)

                return jsonify({'info':fecha_E})
            else:
                return jsonify({'info':'no se encontraron mensajes en este rango de fecha'})
        else:
            return jsonify({'info':'listas vacias (palabras y tweets)'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/resumenTweets', methods = ['GET'])
def resTweets():
    resumenTw.clear()
    tempMensajes = []
    regex = r'\d+\/\d+\/\d+'
    if len(mensajes) > 0:
        for mensaje in mensajes:
            temp_exist = False
            date = mensaje.Date
            date = re.search(regex,date).group()
            for temporal in tempMensajes:
                if temporal.date == date:
                    temp_exist = True
                    break
            if not temp_exist:
                newResumen = resumenTweet(date)
                tempMensajes.append(newResumen)
        
        for mensaje in mensajes:
            date = mensaje.Date
            date = re.search(regex,date).group()

            for temporal in tempMensajes:
                if temporal.date == date:
                    temporal.recibidos+=1
                    temporal.users += len(mensaje.menciones)
                    temporal.hash += len(mensaje.Hash)

        root = ET.Element('MENSAJES_RECIBIDOS')
        for temporal in tempMensajes:
            time = ET.SubElement(root,'TIEMPO')
            fecha = ET.SubElement(time,'FECHA')
            fecha.text = temporal.date
            msj = ET.SubElement(time,'MSJ_RECIBIDOS')
            msj.text = str(temporal.recibidos)
            users = ET.SubElement(time,'USR_MENCIONADOS')
            users.text = str(temporal.users)
            hash = ET.SubElement(time,'HASH_INCLUIDOS')
            hash.text = str(temporal.hash)
        root = ET.tostring(root,encoding='utf-8')
        root = xml.dom.minidom.parseString(root).toprettyxml(indent="   ")
        return jsonify({'info':root})
    else:
        return jsonify({'info':'ingrese documento de mensajes'})

@app.route('/resumenEmociones', methods = ['GET'])
def resumenEmos():
    if len(diccionario_palabras['Positivas']) > 0 and len(diccionario_palabras['Negativas']) > 0:
        newResumen = resumenEmociones()
        for keys,value in diccionario_palabras.items():
            if keys == 'Positivas':
               newResumen.positivas += len(value)
            if keys == 'Negativas':
                newResumen.negativas += len(value)
        
        root = ET.Element('CONFIG_RECIBIDA')
        positivas = ET.SubElement(root,'PALABRAS_POSITIVAS')
        positivas.text = str(newResumen.positivas)
        p_rechazadas = ET.SubElement(root,'PALABRAS_POSITIVAS_RECHAZADAS')
        p_rechazadas.text = str(newResumen.positivas_rechazadas)
        negativas = ET.SubElement(root,'PALABRAS_NEGATIVAS')
        negativas.text = str(newResumen.negativas)
        n_rechazadas = ET.SubElement(root,'PALABRAS_NEGATIVAS_RECHAZADAS')
        n_rechazadas.text = str(newResumen.negativas_rechazadas)
        root = ET.tostring(root,encoding='utf-8')
        root = xml.dom.minidom.parseString(root).toprettyxml(indent="   ")
        return jsonify({'info':root})
    else:
        return jsonify({'info':'ingrese doc. XML emociones'}) 


# @app.route('search/emociones/<string:emocion>', methods = ['GET'])
# def searchEmo(emocion):
#     pass

# @app.route('search/user/<string:user>', methods = ['GET'])
# def searchUser(user):
#     pass

# @app.route('search/Hash/<string:hashtag>', methods = ['GET'])p
# def searchHash(Hashtag):
#     pass

if __name__ == '__main__':
    app.run(debug = True,port = 4000)