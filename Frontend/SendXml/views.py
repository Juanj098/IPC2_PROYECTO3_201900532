from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from django.http import HttpResponse, JsonResponse
import requests
# Create your views here.

def sendTweetsyConfi(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'message':'no se ha seleccionado archivo'})
        try:
            files = {"file":(file.name,file.read())}
            xml_cont = files['file'][1]
            xml_cont = xml_cont.decode('utf-8')
            xml_cont = ET.fromstring(xml_cont)
            root = xml_cont.tag
            if root == 'MENSAJES':
                response = requests.post('http://127.0.0.1:4000/Xml_tweets',data={'data':data},files=files)
            elif root =='diccionario':
                response = requests.post('http://127.0.0.1:4000/Xml_Palabras',data={'data':data},files=files)
            response.raise_for_status()
            response_data = response.json()
            print(f'solicitud exitosa: {response.status_code}')
            return JsonResponse(response_data)
        except Exception as e:
            return HttpResponse(str(e), status = 5000)
    return render(request, 'index.html')

def resumenTweets(request):
    try:
        response = requests.get('http://127.0.0.1:4000/resumenTweets')
        response.raise_for_status()
        print(f'solicitud exitosa:- {response.status_code}')
        response_data = response.json()
        return JsonResponse(response_data)
    except Exception as e:
        return HttpResponse(str(e), status = 5000)

def resumenConfi(request):
    try:
        response = requests.get('http://127.0.0.1:4000/resumenEmociones')
        response.raise_for_status()
        response_data = response.json()
        print(f'solicitud exitosa: **{response.status_code}')
        return JsonResponse(response_data)
    except Exception as e:
        return HttpResponse(str(e), status = 5000)
