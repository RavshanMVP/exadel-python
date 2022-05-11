from django.urls import path, include
import sys
sys.path.append("....")
from api.view.role import RoleList,RoleDetails

urlpatterns = [
    path("list/",RoleList),
    path("<pk>", RoleDetails.as_view())
]
