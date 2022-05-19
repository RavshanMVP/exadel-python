from django.urls import path, include
from api.view import UserDetails

urlpatterns = [

    path("<pk>", UserDetails.as_view({"get":'retrieve','delete':'delete','put':'put'})),
    path("list/", UserDetails.as_view({'get':'list'})),
    path("create/", UserDetails.as_view({ 'post': 'post'}))
]
