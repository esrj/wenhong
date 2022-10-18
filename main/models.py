from django.db import models
from django.contrib.auth.models import User
import os

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    permission = models.IntegerField(default = 0)


class Contact(models.Model):
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    text = models.TextField()
    phone = models.CharField(max_length = 20,null = True,blank = True )
    date = models.DateTimeField(auto_now_add = True)
    is_contact = models.BooleanField(default = False)
    is_sign = models.BooleanField(default = False)



class Course(models.Model):
    teacher = models.ForeignKey(Profile,on_delete = models.CASCADE)
    meet = models.TextField(null=True,blank=True)
    name = models.TextField()
    photo = models.ImageField(upload_to='course', height_field=None, width_field=None, max_length=100,null=True,blank=True)

class Student(models.Model):
    course = models.ForeignKey(Course,on_delete = models.CASCADE,related_name = 'mystudent')
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE,related_name = 'mycourse')

class Document(models.Model):
    title = models.TextField()
    upload = models.FileField(upload_to = 'file',null = True,blank = True)
    date = models.DateField(auto_now_add =True)
    course = models.ForeignKey(Course,on_delete =models.CASCADE,null = True,blank=True,related_name = 'document')


class Msg(models.Model):
    date = models.DateTimeField(auto_now_add = True)
    msg = models.TextField(blank = True , null = True)
    photo = models.ImageField(upload_to='msg', height_field=None, width_field=None, max_length=100,null=True,blank=True)
    auth = models.ForeignKey(Course,on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE)

class Lecturer(models.Model):
    name = models.TextField()
    subject = models.TextField()
    info = models.TextField()
    email = models.TextField()

class Lecture(models.Model):
    name = models.TextField()
    title1 = models.TextField()
    content1 = models.TextField()
    title2 = models.TextField()
    content2 = models.TextField()
    text = models.TextField(null = False,blank = False)
    fee = models.IntegerField()
    image = models.ImageField(upload_to = 'file',null = True,blank = True)
    teacher = models.ForeignKey(Lecturer,on_delete = models.CASCADE,related_name = 'lecture')

#
class Detail(models.Model):
    text = models.TextField()
    lecture = models.ForeignKey(Lecture,on_delete = models.CASCADE,related_name = 'detail')

class Resource(models.Model):
    name = models.TextField()
    file = models.FileField(upload_to = 'file',null = True,blank = True)
    lecture = models.ForeignKey(Lecture,on_delete = models.CASCADE , related_name = "resource")

