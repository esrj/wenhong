from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
import json
from main.models import Profile,Course,Student
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# 登入視圖
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
                        Profile.objects.filter(user = user).first()
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

# course_list 依賴函式
def collect_data(data,permission):
    ele = {}
    ele['meet'] = data.meet
    ele['id'] = data.id
    ele['teacher'] = data.teacher.user.username
    ele['name'] = data.name
    if data.photo:
        ele['photo'] = data.photo.name
    else:
        ele['photo'] = 'course/course-lg.jpg'
    if permission == 2:
        students = []
        for student in list(data.mystudent.all()):
            students.append(student.profile.user.username)
        ele['your_student'] = students
    return ele

# page視圖依賴函式
def course_list(datas,permission,name):
    courses = []
    for data in datas:
        courses.append(collect_data(data,permission))
    if name == None:
        # 待更改 courses[0] 可能有error
        try:
            return courses, courses[0]
        except:
            return courses,'no course'
    # 尚未完成的功能
    else:
        main_course = Course.objects.filter(name = name).first()
        if main_course:
            course = []
            course.append(collect_data(main_course,permission))
            return courses, course[0]
        else :
            return courses,'no permission'

# page視圖依賴函式
def document_list(documents):
    doc = []
    for document in list(documents):
        ele = {}
        ele['title'] = document.title
        ele['path'] = str(document.title.encode('utf-8')).replace("\\", "").replace('\'', '')
        doc.append(ele)
    return doc

# page視圖依賴函式
def load_document(course):
    documents = course.document.order_by('-date').all()
    doc = document_list(documents)

# 加載入課程以及課程文件
# errno = 0 學生頁面
# errno = 1 所有使用者 在無課程時
# errno = 2 教師或admin頁面
# errno = 3 缺乏權限
# permission = 1 學生
# permission = 2 老師
# profile.permission == 1 學生
# profile.permission == 1 老師
@login_required(login_url='/learning/login/')
@csrf_exempt
def page(request):
    name = request.GET.get('name', None)
    if request.method == 'GET':
        return render(request,'learning.html')
    if request.method == 'POST':
        user = request.user
        try:
            profile = Profile.objects.filter(user = user).first()
        except :
            return HttpResponse()
        if user.is_superuser :
            datas = Course.objects.all()  # superuser 可以查看所有課程
            courses,main = course_list(datas,2,name)
            if main == 'no course':
                return JsonResponse({'errno': 1})
            elif main == 'no permission':
                return JsonResponse({'errno': 3, 'courses': courses})
            if name == None:
                documents = datas[0].document.order_by('-date').all()
            else:
                course = Course.objects.filter(name=name).first()
                documents = course.document.order_by('-date').all()
            doc = document_list(documents)
            print(courses,main)
            return JsonResponse({'errno': 2, 'courses': courses, 'document': doc,'main':main})
        # 學生權限
        if profile.permission == 1:
            students = Student.objects.filter(profile = profile).all()
            datas = []
            for student in students:
                datas.append(student.course)
            courses,main = course_list(datas,1,name)
            if main == 'no course':
                return JsonResponse({'errno':1})
            elif main == 'no permission':
                return JsonResponse({'errno': 3, 'courses': courses})
            if name == None:
                documents = datas[0].document.order_by('-date').all()
            else:
                course = Course.objects.filter(name = name).first()
                documents = course.document.order_by('-date').all()
            doc = document_list(documents)
            return JsonResponse({'errno':0,'courses':courses,'document':doc,'main':main})
        # 教師權限
        elif profile.permission == 3:
            datas = Course.objects.filter(teacher = profile).all()
            courses,main = course_list(datas,2,name)
            if main == 'no course':
                return JsonResponse({'errno':1})
            elif main == 'no permission':
                return JsonResponse({'errno': 3, 'courses': courses})
            if name == None:
                documents = datas[0].document.order_by('-date').all()
            else:
                course = Course.objects.filter(name = name).first()
                documents = course.document.order_by('-date').all()
            doc = document_list(documents)
            return JsonResponse({'errno': 2, 'courses': courses, 'document': doc, 'main':main})

@login_required(login_url='/learning/login/')
@csrf_exempt
def search(request):
    req = json.loads(request.body)
    name = req['name']
    courses = Course.objects.filter(name__contains=name).all()
    profile = Profile.objects.filter(user = request.user).first()
    datas = []
    if request.user.is_superuser:
        for course in courses:
            data = {}
            data['name'] = course.name
            if course.photo.name:
                data['photo'] = course.photo.name
            else:
                data['photo'] = 'course/course-lg.jpg'
            data['teacher'] = course.teacher.user.username
            datas.append(data)
    elif profile.permission == 1:
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
                    datas.append(data)
    elif profile.permission == 3:
        for course in courses:
            if course.teacher.user == request.user:
                data = {}
                data['name'] = course.name
                if course.photo.name:
                    data['photo'] = course.photo.name
                else:
                    data['photo'] = 'course/course-lg.jpg'
                data['teacher'] = course.teacher.user.username
                datas.append(data)
    return JsonResponse({"errno":0,'datas':datas})
