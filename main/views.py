from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from main.models import Contact,Lecture,Detail,Resource
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
            phone = req['phone']
            text = req['text']
            if email =='' or name =='':
                return JsonResponse({'errno': 2})
            contact = Contact.objects.create(name = name,phone = phone,email=email,text=text)
            contact.save()
            return JsonResponse({'errno':0})
        except:
            return JsonResponse({'errno':1})

@csrf_exempt
def more(request,id):
    lecture = Lecture.objects.filter(id = id).first()
    details = lecture.detail.all()
    resources = lecture.resource.all()
    lecturer = lecture.teacher
    if request.method == 'POST':
        all = list(Lecture.objects.all().values('id','name','fee','image'))
        data = []
        for detail in details:
            data.append(detail.text)
        resource_ = []
        for resource in resources:
            dict = {}
            dict['name'] = resource.name
            dict['file'] = resource.file.name
            resource_.append(dict)
        return JsonResponse({'errno':0,'data':data,'resource':resource_,"all":all})
    return render(request,'more.html',locals())