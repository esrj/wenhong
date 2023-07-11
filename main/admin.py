from django.contrib import admin
from .models import Profile,Contact,Course,Student,Document,Lecture,Resource

admin.site.register(Contact)
# 學員專區
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Document)
# 公開資源
admin.site.register(Lecture)
admin.site.register(Resource)
