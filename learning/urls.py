from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("login/",views.login),
    path("",views.page),
    path("load/<int:id>/",views.load),
    path("chat/<int:id>/",views.chat),
    path('load_msg/<int:id>/',views.load_msg),
    path('picture/<int:id>/',views.picture),
    path('search/',views.search)
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

