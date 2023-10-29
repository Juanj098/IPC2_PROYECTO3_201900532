from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from django.http import HttpResponse, JsonResponse
import requests
from datetime import datetime
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
            return HttpResponse(str(e), status = 500)
    return render(request, 'index.html')

def resumenTweets(request):
    try:
        response = requests.get('http://127.0.0.1:4000/resumenTweets')
        response.raise_for_status()
        print(f'solicitud exitosa:- {response.status_code}')
        response_data = response.json()
        return JsonResponse(response_data)
    except Exception as e:
        return HttpResponse(str(e), status = 500)

def resumenConfi(request):
    try:
        response = requests.get('http://127.0.0.1:4000/resumenEmociones')
        response.raise_for_status()
        response_data = response.json()
        print(f'solicitud exitosa: **{response.status_code}')
        return JsonResponse(response_data)
    except Exception as e:
        return HttpResponse(str(e), status = 500)

def Hashtags(request,dateMin,dateMax):
    try:
        dateMin = dateMin.split('-')
        dateMin = f'{dateMin[2]}.{dateMin[1]}.{dateMin[0]}'
        dateMax = dateMax.split('-')
        dateMax = f'{dateMax[2]}.{dateMax[1]}.{dateMax[0]}'
        response = requests.get(f'http://127.0.0.1:4000/Hashtags/{dateMin}_{dateMax}')
        response.raise_for_status()
        response_data = response.json()
        print(f'solicitud exitosa: {response.status_code}')
        return JsonResponse(response_data)
    except Exception as e:
        return HttpResponse(str(e), status = 500)

def Users(request, dateMin,dateMax):
    try:
        dateMin = dateMin.split('-')
        dateMin = f'{dateMin[2]}.{dateMin[1]}.{dateMin[0]}'
        dateMax = dateMax.split('-')
        dateMax = f'{dateMax[2]}.{dateMax[1]}.{dateMax[0]}'
        response = requests.get(f'http://127.0.0.1:4000/menciones/{dateMin}_{dateMax}')
        response.raise_for_status()
        response_data = response.json()
        print(f'solicitud exitosa: {response.status_code}')
        return JsonResponse(response_data)
    except Exception as e:
        return HttpResponse(str(e),status = 500)

def emociones(request,dateMin,dateMax):
    try:
        dateMin = dateMin.split('-')
        dateMin = f'{dateMin[2]}.{dateMin[1]}.{dateMin[0]}'
        dateMax = dateMax.split('-')
        dateMax = f'{dateMax[2]}.{dateMax[1]}.{dateMax[0]}'
        response = requests.get(f'http://127.0.0.1:4000/Emociones/{dateMin}_{dateMax}')
        response.raise_for_status()
        response_data = response.json()
        print(f'solicitud exitosa:{response.status_code}')
        return JsonResponse(response_data)
    except Exception as e:
        return HttpResponse(str(e),status = 500)

def ClearList(request):
    try:
        response = requests.get('http://127.0.0.1:4000/Clear')
        response.raise_for_status()
        response_data = response.json()
        print(f'solicitud exitosa:{response.status_code}')
        return JsonResponse(response_data)
    except Exception as e:
        return HttpResponse(str(e),status = 500)