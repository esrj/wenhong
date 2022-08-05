from django.contrib import admin
from .models import Profile,Contact,Course,Student,Document,Msg

admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Document)
admin.site.register(Msg)