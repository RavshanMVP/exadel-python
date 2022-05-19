from django.urls import path, include
from api.view import ServiceDetails

urlpatterns = [
    path("<pk>", ServiceDetails.as_view({"get":'retrieve','delete':'delete','put':'put'})),
    path("list/", ServiceDetails.as_view({'get':'list'})),
    path("create/", ServiceDetails.as_view({'post': 'post',"get":'retrieve'}))
]
