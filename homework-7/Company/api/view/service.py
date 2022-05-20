
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from api.serializers.service import ServiceSerializer
from core.models import Service


class ServiceDetails(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def retrieve(self, request, pk=None):
        queryset = Service.objects.all()
        service = get_object_or_404(queryset, pk=pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)


    def delete(self,request,pk,format = None):
        model = self.get_data(pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        model = self.get_data(pk)
        serializer = ServiceSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        permission_classes = [AllowAny]
        queryset = Service.objects.all()
        serializer = ServiceSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self,request):
        permission_classes = [AllowAny]
        data = request.data
        model = Service(name = data['name'], cost = data['cost'], company = data['company'])
        model.save()
        serializer = ServiceSerializer(model)
        return Response(serializer.data)
