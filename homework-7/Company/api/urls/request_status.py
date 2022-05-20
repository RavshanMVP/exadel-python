from django.urls import path, include
from api.view import RequestStatusDetails

urlpatterns = [
    path("<pk>", RequestStatusDetails.as_view({'get':'retrieve'})),
    path("list/", RequestStatusDetails.as_view({'get' :'list'})),
]
