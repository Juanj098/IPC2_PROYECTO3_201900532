from flask import Flask,jsonify,request
import xml.etree.ElementTree as ET
from flask_cors import CORS
from analizadores import Analizador_Lexico


from mensaje import tweet

mensajes = []
tweet_Json = []
emos_Json = []
diccionario_palabras = {'Negativas': [],'Positivas': []}

def Analizador_Emo(text):
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
    diccionario_palabras.clear()
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
            text = text.replace('\n',' ')
            text = text.replace('\t',' ')
            newtweet = tweet(fecha,text)
            Analizador_Lexico(newtweet.txt,newtweet.Hash,newtweet.menciones)
            mensajes.append(newtweet)
        return jsonify({'xml':request.method})
    except:
        return jsonify({'error':'error'})

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
        return jsonify({'info':'registro exitoso'})
    except:
        return jsonify({'error':'error'})

@app.route('/tweets')
def tweets():
    if len(mensajes) > 0:
        # for tweet in mensajes:
        #     tweet_J = {'fecha':tweet.Date,'texto':tweet.txt}
        #     tweet_Json.append(tweet_J)
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
    
    
if __name__ == '__main__':
    app.run(debug = True,port = 4000)