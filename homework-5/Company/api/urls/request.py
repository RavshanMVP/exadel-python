from django.urls import path, include
import sys
sys.path.append("....")
from api.view.request import CreateRequest,ListRequest,RequestDetails

urlpatterns = [
    path("list/",ListRequest),
    path("create/", CreateRequest),
    path("<pk>", RequestDetails.as_view())
]
