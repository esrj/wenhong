from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from main.models import Contact
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def index(request):
    if request.method == 'GET':
        return render(request,'index.html')
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            email = req['email']
            name = req['name']
            text = req['text']
            contact = Contact.objects.create(name = name,email=email,text=text)
            contact.save()
            return JsonResponse({'errno':0})
        except:
            return JsonResponse({'errno':1})

