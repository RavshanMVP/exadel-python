from django.urls import path, include
import sys
sys.path.append("....")
from api.view.service import ServiceDetails

urlpatterns = [
    path("<pk>", ServiceDetails.as_view({"get":'retrieve','delete':'delete','put':'put','list':'list','post':'post'})),
            path("list/", ServiceDetails.as_view({'get':'list'})),
]
