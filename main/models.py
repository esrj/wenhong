from django.db import models
from django.contrib.auth.models import User
import os

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
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

# 學生
class Student(models.Model):
    course = models.ForeignKey(Course,on_delete = models.CASCADE,related_name = 'mystudent')
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE,related_name = 'mycourse')
# 公開資源
class Document(models.Model):
    title = models.TextField()
    upload = models.FileField(upload_to = 'file',null = True,blank = True)
    date = models.DateField(auto_now_add =True)
    course = models.ForeignKey(Course,on_delete =models.CASCADE,null = True,blank=True,related_name = 'document')

# 訊息
class Msg(models.Model):
    date = models.DateTimeField(auto_now_add = True)
    msg = models.TextField(blank = True , null = True)
    photo = models.ImageField(upload_to='msg', height_field=None, width_field=None, max_length=100,null=True,blank=True)
    auth = models.ForeignKey(Course,on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE)

#公開資源(課程)講師
class Lecturer(models.Model):
    name = models.TextField()
    subject = models.TextField()
    info = models.TextField()
    email = models.TextField()

#公開資源(課程)資訊
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

# 公開資源(課程)細節
class Detail(models.Model):
    text = models.TextField()
    lecture = models.ForeignKey(Lecture,on_delete = models.CASCADE,related_name = 'detail')

# 公開資源(課程)文件
class Resource(models.Model):
    name = models.TextField()
    file = models.FileField(upload_to = 'file',null = True,blank = True)
    lecture = models.ForeignKey(Lecture,on_delete = models.CASCADE , related_name = "resource")

#小考系統
#考試
class Quiz(models.Model):
    data = models.DateTimeField(auto_now_add = True)

#小考系統
class Quiz_member(models.Model):
    member = models.ForeignKey(Profile,on_delete = models.CASCADE)
    quiz = models.ForeignKey(Quiz,on_delete = models.CASCADE)
    complete = models.BooleanField(default = True)
    total_score = models.IntegerField(default = -1)

    def score(self):
        self.quiz


#小考系統
#題目
class Question(models.Model):
    no =models.IntegerField(default = 1)
    q = models.TextField()
    A = models.TextField()
    B = models.TextField()
    C = models.TextField()
    D = models.TextField()
    ans = models.CharField(max_length = 1)
    quiz = models.ForeignKey(Quiz,on_delete = models.CASCADE,related_name = 'question')
    proportion = models.IntegerField(default = 2)


# 儲存學生作答結果
class Answer(models.Model):
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # 先找到是哪一次小考
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    # 那次小考的第幾題
    no = models.IntegerField()
    my_ans = models.CharField(max_length=1)
    complete = models.BooleanField(default = False)
    right = models.BooleanField(default = True)
    proportion = models.IntegerField(default = 2)

    def __init__(self):
        self.proportion = self.quiz.question.objects.filter(no=self.no).first().no
        self.save()

    def is_right(self):
        ques = self.quiz.question.objects.filter(no = self.no).first()
        if ques.ans == self.my_ans:
            self.right = True
            self.complete = True
            self.save()
        else:
            self.right = False
            self.complete = True
            self.save()

