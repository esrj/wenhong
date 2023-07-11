from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("login/",views.adminlogin),
    path('logout/',views.logout),

    path("", views.adminpage),
    path('contact/<int:id>/',views.contact),
    path('sign/<int:id>/',views.sign),
    path('single/<int:id>/',views.single),
    path("delete/<int:id>/",views.delete),

    path("info/",views.info),
    path("create/",views.create),
    path("post/",views.post),
    path('upload/',views.upload),
    path('document/',views.document),
    path('load_document/<int:id>/',views.load_document),
    path('delete_/<int:id>/',views.delete_),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
