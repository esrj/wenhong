from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
import json
from main.models import Profile,Contact,Course,Student,Msg
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request,'login_.html')
    if request.method == 'POST':
        req = json.loads(request.body)
        username = req['username']
        password = req['password']
        if username and password :
            user = authenticate(username= username,password = password)
            if user is not None:
                if user.is_active:
                    try :
                        profile = Profile.objects.filter(user = user).first()
                    except:
                        auth.logout(request)
                        return render(request,'login_.html')
                    auth.login(request,user)
                    return JsonResponse({'errno':0})
            else:
                return JsonResponse({'errno':1})
        else:
            return JsonResponse({"errno":1})
    else:
        return JsonResponse({"errno":2})


@login_required(login_url='/learning/login/')
@csrf_exempt
def page(request):
    if request.method == 'GET':
        return render(request,'page.html')
    if request.method == 'POST':
        user = request.user
        try:
            profile = Profile.objects.filter(user = user).first()
        except :
            return JsonResponse({'errno': 1})
        if user.is_superuser :
            datas = Course.objects.all()
            courses = []
            for data in datas:
                ele = {}
                ele['meet'] = data.meet
                ele['id'] = data.id
                ele['teacher'] = data.teacher.user.username
                ele['name'] = data.name
                if data.photo:
                    ele['photo'] = data.photo.name
                else:
                    ele['photo'] = 'course/course-lg.jpg'
                courses.append(ele)
            documents = datas[0].document.order_by('-date').all()
            doc = []
            for document in list(documents):
                ele = {}
                ele['title'] = document.title
                ele['path'] = str(document.title.encode('utf-8')).replace("\\", "").replace('\'', '')
                doc.append(ele)
            id = datas[0].id
            return JsonResponse({'errno': 0, 'courses': courses, 'document': doc, 'id': id})
        if profile.permission == 1:
            datas = Student.objects.filter(profile = profile).all()
            courses=[]
            for data in datas:
                ele = {}
                ele['meet'] = data.course.meet
                ele['id'] = data.course.id
                ele['teacher'] = data.course.teacher.user.username
                ele['name'] = data.course.name
                if data.course.photo :
                    ele['photo'] = data.course.photo.name
                else:
                    ele['photo'] = 'course/course-lg.jpg'
                courses.append(ele)
            documents = datas[0].course.document.order_by('-date').all()
            doc = []
            for document in list(documents):
                ele = {}
                ele['title'] = document.title
                ele['path'] = str(document.title.encode('utf-8')).replace("\\", "").replace('\'', '')
                doc.append(ele)
            id = datas[0].course.id
            return JsonResponse({'errno':0,'courses':courses,'document':doc,'id':id})
        elif profile.promission == 2:
            datas = Course.objects.filter(teacher = profile).all()
            courses = []
            for data in datas:
                ele = {}
                ele['meet'] = data.meet
                ele['id'] = data.id
                ele['teacher'] = data.teacher.user.username
                ele['name'] = data.name
                if data.photo:
                    ele['photo'] = data.photo.name
                else:
                    ele['photo'] = 'course/course-lg.jpg'
                courses.append(ele)
            documents = datas[0].document.order_by('-date').all()
            doc = []
            for document in list(documents):
                ele = {}
                ele['title'] = document.title
                ele['path'] = str(document.title.encode('utf-8')).replace("\\", "").replace('\'', '')
                doc.append(ele)
            id = datas[0].id
            return JsonResponse({'errno': 0, 'courses': courses, 'document': doc, 'id': id})


@login_required(login_url='/learning/login/')
@csrf_exempt
def load(request,id):
    course = Course.objects.filter(id=id).first()
    data = []
    ele={}
    ele['meet'] = course.meet
    ele['id'] = course.id
    ele['teacher'] = course.teacher.user.username
    ele['name'] = course.name
    if course.photo:
        ele['photo'] = course.photo.name
    else:
        ele['photo'] = 'course/course-lg.jpg'
    data.append(ele)
    documents = course.document.order_by('-date').all()
    doc =[]
    for document in list(documents):
        ele={}
        ele['title'] = document.title
        ele['path'] = str(document.title.encode('utf-8')).replace("\\","").replace('\'','')
        doc.append(ele)
    id = course.id
    return JsonResponse({'errno':0,'courses':data,'document':doc,'id':id})

@csrf_exempt
def chat(request,id):
    course = Course.objects.filter(id=id).first()
    profile = Profile.objects.filter(user = request.user).first()
    if request.method == 'GET':
        return render(request,'chat.html',locals())
    if request.method == 'POST':
        req = json.loads(request.body)
        content = req['content']
        if content == "":
            return JsonResponse({'errno': 1})
        else:
            msg = Msg.objects.create(msg = content,auth = course,sender = profile)
            msg.save()
            return JsonResponse({'errno': 0, 'msg': msg.msg})


@csrf_exempt
def load_msg(request,id):
    course = Course.objects.filter(id=id).first()
    msgs = Msg.objects.filter(auth=course).order_by('date').all()
    data = []
    for ele in msgs:
        d = dict()
        d['date'] = ele.date.strftime('%H:%M')
        if ele.msg != '':
            d['msg'] = ele.msg
            d['pic'] = False
        else:
            d['msg'] = ele.photo.name
            d['pic'] = True
        d['sender'] = ele.sender.user.username
        if ele.sender.user == request.user:
            d['self'] = True
        else:
            d['self'] = False
        if ele.sender.permission == 3:
            d['is_admin'] = True
        else:
            d['is_admin'] = False
        data.append(d)
    return JsonResponse({'errno': 0, 'data': data})


@csrf_exempt
def picture(request,id):
    profile = Profile.objects.filter(user = request.user).first()
    file = request.FILES.get('file')
    course = Course.objects.filter(id=id).first()
    photo = file.name
    msg = Msg.objects.create(msg = "", auth=course, sender=profile,photo = file)
    msg.save()
    return JsonResponse({'errno': 0,'photo':photo})

@csrf_exempt
def search(request):
    req = json.loads(request.body)
    name = req['name']
    if request.user.is_superuser:
        courses = Course.objects.filter(name__contains=name).all()
        datas = []
        for course in courses:
            data = {}
            data['name'] = course.name
            if course.photo.name:
                data['photo'] = course.photo.name
            else:
                data['photo'] = 'course/course-lg.jpg'
            data['teacher'] = course.teacher.user.username
            data['id'] = course.id
            datas.append(data)
        return JsonResponse({"errno": 0, 'datas': datas})
    else:
        courses = Course.objects.filter(name__contains = name).all()
        datas=[]
        for course in courses:
            list = course.mystudent.all()
            for l in list:
                if l.profile.user == request.user:
                    data={}
                    data['name'] = course.name
                    if course.photo.name:
                        data['photo'] = course.photo.name
                    else:
                        data['photo'] = 'course/course-lg.jpg'
                    data['teacher'] = course.teacher.user.username
                    data['id'] = course.id
                    datas.append(data)
        return JsonResponse({"errno":0,'datas':datas})
