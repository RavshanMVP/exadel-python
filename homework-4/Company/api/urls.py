
from django.urls import path, include
from .view import user_views
from .view.user_views import CreateUser,UpdateUser, DeleteUser,ListOfUsers, ReadDetails
urlpatterns = [
path('<int:pk>/read/', user_views.ReadOneUser),
    path('create/', CreateUser.as_view()),
    path('<int:pk>/update/', UpdateUser.as_view()),
    path('<int:pk>/delete/', DeleteUser.as_view()),
    path('all/', ListOfUsers.as_view()),
    path('<int:pk>/detail/', ReadDetails.as_view()),
]
