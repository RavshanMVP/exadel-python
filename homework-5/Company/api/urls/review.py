from django.urls import path, include
from api.view import ReviewDetails

urlpatterns = [
    path("<pk>", ReviewDetails.as_view({"get":'retrieve','delete':'delete','put':'put','post':'post'})),
            path("list/", ReviewDetails.as_view({'get':'list'})),
]
