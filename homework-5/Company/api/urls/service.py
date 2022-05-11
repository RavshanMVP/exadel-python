from django.urls import path, include
import sys
sys.path.append("....")
from api.view.service import CreateService,ServiceDetails

urlpatterns = [
    path("create/",CreateService),
    path("<pk>", ServiceDetails.as_view({"get":'retrieve','delete':'delete','put':'put'}))
]
