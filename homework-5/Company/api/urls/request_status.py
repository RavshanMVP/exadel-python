from django.urls import path, include
import sys
sys.path.append("....")
from api.view.request_status import RequestStatusList,RequestStatusDetails

urlpatterns = [
    path("list/",RequestStatusList),
    path("<pk>", RequestStatusDetails.as_view())
]
