from django.urls import path, include
from api.view import RoleDetails

urlpatterns = [
    path("<pk>", RoleDetails.as_view({'get':'retrieve'})),
    path("list/", RoleDetails.as_view({'get':'list'})),
]
