"""Company URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from api.urls import request, user, role, review, request_status, service
from djoser import urls
from djoser.urls import jwt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('request/', include(request)),
    path('users/', include(user)),
    path('role/', include(role)),
    path('status/', include(request_status)),
    path('service/', include(service)),
    path('review/', include(review)),

    path(r'auth/', include(urls)),
    path(r'auth/', include(jwt)),


]
