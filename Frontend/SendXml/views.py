from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
# Create your views here.

server = 'http://127.0.0.1:4000/'

def index(request):
    if request.method == 'GET':
        hola = 'Get'
        # response = requests.get('http://127.0.0.1:4500/ping')
        return render(request,'index.html',{'hello':hola})
    elif request.method == 'POST':
        doc = request.FILES['document']
        data = doc.read()
        print(data)
        return redirect('index')

def testXml(request, nameDoc):
    return HttpResponse(f'the doc is {nameDoc}')