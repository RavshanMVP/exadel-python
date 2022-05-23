from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from api.serializers.user import UserSerializer
from core.models import User, Role
class UserDetails(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    def retrieve(self, request, pk=None):

        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


    def delete(self,request,pk,format = None):
        user = get_object_or_404(self.queryset, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):

        data = request.data
        user = get_object_or_404(self.queryset, pk=pk)
        user.fullname = data['fullname']
        user.email = data['email']
        user.phone_number = data['phone_number']
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def list(self, request):
        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def post(self,request):

        data = request.data
        role = Role.objects.get(id=data['role'])
        model = User(fullname = data['fullname'], phone_number = data['phone_number'], email = data ['email'], role = role, password = data['password'])
        model.save()
        serializer = UserSerializer(model)
        return Response(serializer.data)
