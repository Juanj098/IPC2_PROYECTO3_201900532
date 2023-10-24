from flask import Flask,jsonify,request
import xml.etree.ElementTree as ET
from flask_cors import CORS
from analizadores import Analizador_Lexico, Analisis_Emocion
import re   
from datetime import datetime 

from mensaje import tweet,User,Hashtags,MencionesFecha,HashtagsFecha,Emociones

HFecha = []
EFecha = []
MFecha = []
usuarios = []
Hashs = []
mensajes = []
tweet_Json = []
emos_Json = []
twets =[]

diccionario_palabras = {'Negativas': [],'Positivas': []}

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
    return jsonify({'info':'Listas vacias'})

@app.route('/Xml_tweets', methods =['POST'])
def Xml_tweets():
    xml = request.data
    try:
        root = ET.fromstring(xml)
        ET.dump(root)
        for mensaje in root.findall('MENSAJE'):
            fecha = mensaje.find('FECHA').text
            text = mensaje.find('TEXTO').text
            text = text.strip()
            newtweet = tweet(fecha,text)
            Analizador_Lexico(newtweet.txt,newtweet.Hash,newtweet.menciones)
            if len(diccionario_palabras['Positivas']) > 0 and len(diccionario_palabras['Negativas'])>0:
                newtweet.emocion = Analisis_Emocion(newtweet.txt,diccionario_palabras)
            else:
                pass
            mensajes.append(newtweet)
            
        return jsonify({'xml':request.method})
    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/Xml_Palabras', methods = ['POST'])
def Xml_Palabras():
    xml = request.data
    try:
        root = ET.fromstring(xml)
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
        return jsonify({'info':'registro exitoso'})
    except Exception as e:
        return jsonify({'error': e})

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
                print(mf.date)
                for mencion in mf.menciones:
                    print(mencion)

            return jsonify({'mensaje':'se contaron las menciones'})
        else:
            return jsonify({'info':'lista vacia'})
    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/Hashtags/<string:dateMin>_<string:dateMax>', methods = ['GET'])
def Hash(dateMin,dateMax):
    try:    
        twets.clear()
        HFecha.clear()
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
                print(hf.date)
                for hashtag in hf.Hashtags:
                    print(hashtag)


            return jsonify({'Hashtags':'registrados'})
        else:
            return jsonify({'error':'lista vacia'})
        
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/Emociones/<string:fechaInicial>_<string:fechaMaxima>' ,methods =['GET'])
def Emos(fechaInicial,fechaMaxima):
    try:
        EFecha.clear()
        tempEmo = []
        regex = r'\d+\/\d+\/\d+'
        fechaInicial = fechaInicial.replace('.','/')
        fechaInicial = datetime.strptime(fechaInicial,'%d/%m/%Y')
        fechaMaxima = fechaMaxima.replace('.','/')
        fechaMaxima = datetime.strptime(fechaMaxima,'%d/%m/%Y')
        if len(mensajes) > 0 and (len(diccionario_palabras['Positivas']) > 0 or len(diccionario_palabras['Negativas'] > 0)):
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
                    print(Ef)
                return jsonify({'info':'se procesaron emociones con exito :3'})
            else:
                return jsonify({'info':'no se encontraron mensajes en este rango de fecha'})
        else:
            return jsonify({'info':'listas vacias (palabras y tweets)'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/resumenTweets', methods = ['GET'])
def resTweets():
    return jsonify({'info':'Xml_generando...'})

if __name__ == '__main__':
    app.run(debug = True,port = 4000)