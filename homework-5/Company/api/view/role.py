from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status

from api.serializers.role import RoleSerializer, Role

class RoleDetails(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Role.objects.all()
        role = get_object_or_404(queryset, pk=pk)
        serializer = RoleSerializer(role)
        return Response(serializer.data)


    def delete(self,request,pk,format = None):
        model = self.get_data(pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        model = self.get_data(pk)
        serializer = RoleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Role.objects.all()
        serializer = RoleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        model = Role(fullname = data['fullname'], phone_number = data['phone_number'], email = data ['email'], role_id = data['role_id'])
        model.save()
        serializer = RoleSerializer(model)
        return Response(serializer.data)
