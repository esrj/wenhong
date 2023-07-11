from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
from main.models import Contact
from main.models import Contact,Profile,Course,Student,Document
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# 初始介面
@login_required(login_url='/myadmin/login/')
@csrf_exempt
def adminpage(request):
    if request.method == 'GET':
        if request.user.is_staff:
            return render(request, 'adminpage.html')
        else:
            return HttpResponse('權限不足')
    if request.method == 'POST':
        contacts = Contact.objects.order_by('-date').all().values('id','date','email','name','text','phone','is_contact','is_sign')
        datas = list(contacts)
        for data in datas:
            data['date'] = data['date'].strftime('%m/%d')
        return JsonResponse({'errno':0,'data':datas})

@csrf_exempt
def adminlogin(request):
    if request.method == 'GET':
        return render(request, 'adminlogin.html')
    if request.method == 'POST':
        req = json.loads(request.body)
        username = req['username']
        password = req['password']
        if username and password:
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active and user.is_staff:
                    auth.login(request, user)
                    return JsonResponse({'errno':0})
                else:
                    return JsonResponse({'errno': 1})
            else:
                return JsonResponse({'errno':1})
        else:
            return JsonResponse({'errno':2})

@login_required(login_url='/myadmin/login/')
@csrf_exempt
def logout(request):
    auth.logout(request)
    return JsonResponse({'errno': 0})

# adminpage 已聯絡操作
@login_required(login_url='/myadmin/login/')
@csrf_exempt
def contact(request,id):
    contact = Contact.objects.filter(id=id).first()
    if contact.is_contact == True:
        contact.is_contact=False
    else:
        contact.is_contact = True
    contact.save()
    return JsonResponse({'errno':0})

# adminpage 已報名操作
@login_required(login_url='/myadmin/login/')
@csrf_exempt
def sign(request,id):
    contact = Contact.objects.filter(id = id).first()
    if contact.is_sign == True:
        contact.is_sign = False
    else:
        contact.is_sign = True
    contact.save()
    return JsonResponse({'errno':0})


@login_required(login_url='/myadmin/login/')
@csrf_exempt
def single(request,id):
    contact = Contact.objects.filter(id=id).first()
    if request.user.is_staff:
        return render(request, 'single.html', locals())
    else:
        return HttpResponse('權限不足')


@login_required(login_url='/myadmin/login/')
@csrf_exempt
def delete(request,id):
    contact = Contact.objects.filter(id=id).first()
    contact.delete()
    return JsonResponse({'errno':0})


@login_required(login_url='/myadmin/login/')
@csrf_exempt
def create(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        email = req['email']
        if '@' not in email :
            return JsonResponse({'errno':5})
        username = req['username']
        password = req['password']
        password2= req['password2']
        permission = req['permission']
        if password2 == password:
            if username and email and password and password2:
                try:
                    user = User.objects.create_user(username, email, password)
                    user.is_staff = True
                    user.save()
                    profile = Profile.objects.create(user=user,permission = permission)
                    profile.save()
                    return JsonResponse({'errno':0})
                except Exception as e:
                    if e == 'UNIQUE constraint failed: auth_user.username':
                        return JsonResponse({'errno':3})
                    else:
                        return JsonResponse({'errno': 4})
            else:
                return JsonResponse({'errno':1})
        else:
            return JsonResponse({'errno':2})
    if request.method == 'GET':
        if request.user.is_superuser :
            return render(request,'create.html')
        else:
            return HttpResponse('權限不足')

# 新增課程頁面
@login_required(login_url='/myadmin/login/')
@csrf_exempt
def info(request):
    if request.method == "GET":
        if request.user.is_staff:
            return render(request,'info.html')
        else:
            return HttpResponse('權限不足')
    if request.method == "POST":
        Users = Profile.objects.all()
        data=[]
        for user in Users:
            if user.permission == 1:
                ele = dict()
                ele['id'] = user.id
                ele['name'] = user.user.username
                data.append(ele)
        teachers = Profile.objects.filter(permission = 3).all()
        teacher_data = []
        for teacher in teachers:
            ele = dict()
            ele['id'] = teacher.id
            ele['name'] = teacher.user.username
            ele['permission'] = teacher.permission
            teacher_data.append(ele)
        return JsonResponse({'errno':0,'data':data,'teacher':teacher_data})

# 新增課程api
@login_required(login_url='/myadmin/login/')
@csrf_exempt
def post(request):
    try:
        file = request.FILES.get('file')
    except:
        file = None
    meet = request.POST.get('meet')
    students = request.POST.get('student').split(',')
    course = request.POST.get('course_name')
    if meet and students and course:
        if  Course.objects.filter(name = course).first() != None:
            return JsonResponse({'errno': 1})
        teacher = request.POST.get('teacher')
        user_t = User.objects.filter(username = teacher).first()
        profile_t = Profile.objects.filter(user = user_t).first()
        course = Course.objects.create(teacher = profile_t,name = course,photo = file,meet = meet )
        course.save()
        for student in students:
            user_s = User.objects.filter(username = student).first()
            profile_s = Profile.objects.filter(user = user_s).first()
            student_ = Student.objects.create(course = course,profile = profile_s)
            student_.save()
        return JsonResponse({'errno': 0})
    else:
        return JsonResponse({'errno': 2})

# 上傳檔案頁面
@login_required(login_url='/myadmin/login/')
@csrf_exempt
def upload(request):
    if request.method == 'GET':
        if request.user.is_staff:
            return render(request,'upload.html')
        else:
            return HttpResponse('權限不足')
    if request.method == 'POST':
        courses = Course.objects.all().values('name','id')
        courses = list(courses)
        return JsonResponse({'errno':0,'data':courses})

# 上傳檔案api
from django.core.files.base import ContentFile
@login_required(login_url='/myadmin/login/')
@csrf_exempt
def document(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        id = request.POST.get('id')
        if id !='請選擇課程' and file:
            course = Course.objects.filter(id=id).first()
            document = Document.objects.create(title = file.name, course = course)
            full_filename = os.path.join('img','file', str(file.name.encode('utf-8')).replace("\\","").replace('\'',''))
            fout = open(full_filename, 'wb+')
            file_content = ContentFile(request.FILES.get('file').read())
            for chunk in file_content.chunks():
                fout.write(chunk)
            fout.close()
            document.save()
            return JsonResponse({'errno':0,'id':document.id})
        else:
            return JsonResponse({'errno': 1})

@login_required(login_url='/myadmin/login/')
@csrf_exempt
def load_document(request,id):
    course = Course.objects.filter(id = id).first()
    documents = course.document.order_by('-date').all()
    documents = list(documents)
    data = []
    for document in documents:
        ele = {}
        ele['title'] = document.title
        ele['path'] = str(document.title.encode('utf-8')).replace("\\","").replace('\'','')
        ele['id'] = document.id
        data.append(ele)
    return JsonResponse({'errno':0,'documents':data})

# 刪除已上傳的資料
@login_required(login_url='/myadmin/login/')
@csrf_exempt
def delete_(request,id):
    document = Document.objects.filter(id=id).first()
    document.delete()
    return JsonResponse({'errno':0})


