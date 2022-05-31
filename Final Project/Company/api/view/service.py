
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from api.serializers.service import ServiceSerializer, CategorySerializer
from core.models import Service, User, Category


class ServiceDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.select_related('category','company').order_by("-cost")
    serializer_class = ServiceSerializer

    def retrieve(self, request, pk=None):
        service = get_object_or_404(self.queryset, pk=pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)


    def delete(self,request,pk,format = None):
        service = get_object_or_404(self.queryset, pk=pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        data = request.data
        service = get_object_or_404(self.queryset, pk=pk)
        service.name = data['name']
        service.cost = int(data['cost'])
        service.company = User.objects.get(fullname=data['company'])
        service.category = Category.objects.get(category = data['category'])
        service.save()

        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def list(self, request):
        serializer = ServiceSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        company = User.objects.get(fullname=data['company'])
        category = Category.objects.get(category=data['category'])
        model = Service(name = data['name'], cost = data['cost'], company = company, category = category)
        model.save()
        serializer = ServiceSerializer(model)
        return Response(serializer.data)


class CategoryDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all().order_by("category")
    serializer_class = CategorySerializer

    def retrieve(self, request, pk=None):
        category = get_object_or_404(self.queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


    def delete(self,request,pk,format = None):
        category = get_object_or_404(self.queryset, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        data = request.data
        category = get_object_or_404(self.queryset, pk=pk)
        category.category = data['category']

        category.save()

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data

        model = Category(category = data['category'])
        model.save()
        serializer = CategorySerializer(model)
        return Response(serializer.data)
