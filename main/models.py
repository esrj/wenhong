from django.db import models
from django.contrib.auth.models import User
import os
from django.contrib.auth.models import AbstractUser



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # permission = 1 為學生  3 為老師
    permission = models.IntegerField(default = 0)



# 客戶聯絡
class Contact(models.Model):
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    text = models.TextField()
    phone = models.CharField(max_length = 20,null = True,blank = True )
    date = models.DateTimeField(auto_now_add = True)
    is_contact = models.BooleanField(default = False)
    is_sign = models.BooleanField(default = False)

# 課程資訊
class Course(models.Model):
    teacher = models.ForeignKey(Profile,on_delete = models.CASCADE)
    meet = models.TextField(null=True,blank=True)
    name = models.TextField()
    photo = models.ImageField(upload_to='course', height_field=None, width_field=None, max_length=100,null=True,blank=True)

# 學生和課程間 多對多模型
class Student(models.Model):
    course = models.ForeignKey(Course,on_delete = models.CASCADE,related_name = 'mystudent')
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE,related_name = 'mycourse')

# 學生資源(講義，文件)
class Document(models.Model):
    title = models.TextField()
    upload = models.FileField(upload_to = 'file',null = True,blank = True)
    date = models.DateField(auto_now_add =True)
    course = models.ForeignKey(Course,on_delete =models.CASCADE,null = True,blank=True,related_name = 'document')



#公開資源(課程)資訊
class Lecture(models.Model):
    name = models.CharField(max_length=30)
    introduce = models.TextField()
    outline = models.TextField()
    chapter = models.TextField(null = True,blank = True)
    fee = models.IntegerField()
    image = models.ImageField(upload_to = 'lecture',default = 'lecture/course2.jpg')
    teacher = models.CharField(max_length=30,null = True,blank = True)
    teacher_info = models.TextField(null = True,blank = True)
    teacher_email = models.CharField(max_length=30,null = True,blank = True)

# 公開資源(課程)文件
class Resource(models.Model):
    name = models.TextField()
    file = models.FileField(upload_to = 'file',null = True,blank = True)
    lecture = models.ForeignKey(Lecture,on_delete = models.CASCADE , related_name = "resource")

