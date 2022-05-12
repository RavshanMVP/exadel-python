from django.urls import path, include
from api.view.role import RoleDetails

urlpatterns = [
    path("<pk>", RoleDetails.as_view({"get":'retrieve','delete':'delete','put':'put','post':'post'})),
    path("list/", RoleDetails.as_view({'get':'list'})),
]
