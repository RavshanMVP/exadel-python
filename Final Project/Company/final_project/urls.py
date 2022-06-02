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
from django.urls import path, include, re_path
from api.view import RequestDetails, ServiceDetails, UserDetails, RoleDetails, ReviewDetails, RequestStatusDetails, CategoryDetails
from djoser import urls
from djoser.urls import jwt
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [

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

    # category urls
    path("category/<pk>", CategoryDetails.as_view({'get':'retrieve','delete':'delete','put':'put'})),
    path("categories/list/", CategoryDetails.as_view({'get':'list'})),
    path("categories/create/", CategoryDetails.as_view({'post': 'post'})),

    #user urls
    path("user/<pk>", UserDetails.as_view({'get':'retrieve','delete':'delete','put':'put',})),
    path("users/list/", UserDetails.as_view({'get':'list'})),
    path("users/create/", UserDetails.as_view({ 'post': 'post'})),

    #for authorization
    path(r'auth/', include(urls)),
    path(r'auth/', include(jwt)),

    path('__debug__/', include('debug_toolbar.urls')),

    # swagger
   re_path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),



]









