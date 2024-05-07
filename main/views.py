from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from main.models import Contact,Lecture
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
def page(request):
    theme = request.GET.get('theme', None)
    lecture = Lecture.objects.filter(name = theme).first()
    resources = lecture.resource.all()
    if request.method == 'POST':
        all = list(Lecture.objects.all().values('id','name','fee','image'))
        data = []
        chapter = lecture.chapter.split('\n')
        resource_ = []
        for resource in resources:
            dict = {}
            dict['name'] = resource.name
            dict['url'] = resource.url
            resource_.append(dict)
        return JsonResponse({'errno':0,'chapter':chapter,'resource':resource_,"all":all})
    return render(request,'more.html',locals())

@csrf_exempt
def load_lecture(request):
    lectures = Lecture.objects.all()
    data = []
    for lecture in lectures:
        data.append(lecture.name)
    return JsonResponse({'lecture':data})
