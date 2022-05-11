from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import sys
sys.path.append("...")
from api.serializers.user import UserSerializer, User
@api_view (['GET'])
def ListUser(request):
    if request.method == "GET":
        users  = User.objects.all()
        serializer = UserSerializer(users,many= True)
        return Response(serializer.data )

@api_view (['POST','GET'])
def CreateUser(request):
    if request.method == "POST":
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetails(APIView):
    def get_data(self,pk,format = None):
        try:
            return User.objects.get(pk = pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def delete(self,request,pk,format = None):
        model = self.get_data(pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        model = self.get_data(pk)
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request,pk, format = None):
        model = self.get_data(pk)
        serializer = UserSerializer(model)
        return Response(serializer.data)
