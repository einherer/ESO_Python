"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django_app import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('admin/', admin.site.urls, name='maintainance'),
    path('upload/', views.upload_file, name='upload_file'),
    path('upload-form/', views.file_upload_form, name='file_upload_form'),
    path('accounts/', views.account_list, name='account_list'),
    path('account/<account_name>/', views.account_detail, name='account_detail'),
    path('character/<character_id>/', views.character_detail, name='character_detail'),
]
