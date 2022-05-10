from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic import ListView, DetailView
import sys
sys.path.append("...")
from core.models.user import User
def ReadOneUser(request, pk):
    models = User.objects.filter(id = pk)

    for model in models:
        final = model.fullname
        final += "\n" + model.email
        final += "\n" + model.phone_number

    return HttpResponse(final)

class CreateUser(CreateView):
    users = User.objects.all()
    id_counter=1
    for user in users:
        id_counter+=1
    model = User
    fields = ['fullname','phone_number','email','role_id']
    template_name = "create.html"

    success_url = '/views/'+str(id_counter)+'/read'


class UpdateUser(UpdateView):
    id_update =1

    model = User
    fields = ['fullname','phone_number','email','role_id']
    template_name = "update.html"

    success_url = '/views/all'


class DeleteUser(DeleteView):

    model = User
    template_name = "delete.html"
    success_url = '/views/all'

class ListOfUsers(ListView):

    model = User
    template_name = 'list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ReadDetails(DetailView):
    model =  User
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
