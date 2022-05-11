from django.urls import path, include
import sys
sys.path.append("....")
from api.view.user import UserDetails

urlpatterns = [

    path("<pk>", UserDetails.as_view({"get":'retrieve','delete':'delete','put':'put','post':'post'})),
    path("list/", UserDetails.as_view({'get':'list'})),
]
