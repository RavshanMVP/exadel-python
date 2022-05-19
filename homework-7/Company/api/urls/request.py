from django.urls import path

from api.view import RequestDetails

urlpatterns = [
    path("<pk>", RequestDetails.as_view({"get":'retrieve','delete':'delete','put':'put','post':'post'})),
        path("list/", RequestDetails.as_view({'get':'list'})),
]
