from django.urls import path, include
from api.view import ReviewDetails

urlpatterns = [
    path("<pk>", ReviewDetails.as_view({"get":'retrieve','delete':'delete','put':'put'})),
            path("list/", ReviewDetails.as_view({'get':'list'})),
    path("create/", ReviewDetails.as_view({'get': 'retrieve', 'post': 'post'}))
]
