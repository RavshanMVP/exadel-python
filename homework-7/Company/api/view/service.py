
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from api.serializers.service import ServiceSerializer
from core.models import Service, User


class ServiceDetails(viewsets.ViewSet):
    permission_classes = [AllowAny]



    def retrieve(self, request, pk=None):
        queryset = Service.objects.all()
        service = get_object_or_404(queryset, pk=pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)


    def delete(self,request,pk,format = None):
        queryset = Service.objects.all()
        service = get_object_or_404(queryset, pk=pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        data = request.data
        service_list = Service.objects.all()
        service = get_object_or_404(service_list, pk=pk)
        service.name = data['name']
        service.cost = int(data['cost'])
        service.company = User.objects.get(id=data['company'])
        service.save()

        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def list(self, request):
        queryset = Service.objects.all()
        serializer = ServiceSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        company = User.objects.get(id=data['company'])
        model = Service(name = data['name'], cost = data['cost'], company = company)
        model.save()
        serializer = ServiceSerializer(model)
        return Response(serializer.data)
