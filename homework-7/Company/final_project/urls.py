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
from api.view import RequestDetails, ServiceDetails, UserDetails, RoleDetails, ReviewDetails, RequestStatusDetails
from djoser import urls
from djoser.urls import jwt

urlpatterns = [
    path('admin/', admin.site.urls),

    # request urls
    path("request/<pk>", RequestDetails.as_view({'get':'retrieve','delete':'delete','put':'put'})),
    path("requests/list/", RequestDetails.as_view({'get':'list'})),
    path("requests/create/", RequestDetails.as_view({'post':'post'})),

# request status urls
    path("status/<pk>", RequestStatusDetails.as_view({'get':'retrieve'})),
    path("statuses/list/", RequestStatusDetails.as_view({'get' :'list'})),

# review urls
    path("review/<pk>", ReviewDetails.as_view({'get':'retrieve','delete':'delete','put':'put'})),
    path("reviews/list/", ReviewDetails.as_view({'get':'list'})),
    path("reviews/create/", ReviewDetails.as_view({'post': 'post'})),

    # role urls
    path("role/<pk>", RoleDetails.as_view({'get':'retrieve'})),
    path("roles/list/", RoleDetails.as_view({'get':'list'})),

    # service urls
    path("service/<pk>", ServiceDetails.as_view({'get':'retrieve','delete':'delete','put':'put'})),
    path("services/list/", ServiceDetails.as_view({'get':'list'})),
    path("services/create/", ServiceDetails.as_view({'post': 'post'})),

    #user urls
    path("user/<pk>", UserDetails.as_view({'get':'retrieve','delete':'delete','put':'put',})),
    path("users/list/", UserDetails.as_view({'get':'list'})),
    path("users/create/", UserDetails.as_view({ 'post': 'post'})),

    path(r'auth/', include(urls)),
    path(r'auth/', include(jwt)),


]
