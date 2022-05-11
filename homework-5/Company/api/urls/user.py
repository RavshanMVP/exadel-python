from django.urls import path, include
import sys
sys.path.append("....")
from api.view.user import CreateUser,ListUser,UserDetails

urlpatterns = [
    path("list/",ListUser),
    path("create/", CreateUser),
    path("<pk>", UserDetails.as_view())
]
