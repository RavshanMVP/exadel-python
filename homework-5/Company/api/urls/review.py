from django.urls import path, include
import sys
sys.path.append("....")
from api.view.review import CreateReview,ReviewDetails

urlpatterns = [
    path("create/",CreateReview),
    path("<pk>", ReviewDetails.as_view({"get":'retrieve','delete':'delete','put':'put'}))
]
