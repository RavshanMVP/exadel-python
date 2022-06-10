from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.serializers.service import ServiceSerializer, CategorySerializer
from core.models import Service, User, Category
from core.utility import ServiceFilter


class ServiceDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Service.objects.select_related('category', 'company').order_by("-cost")
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend,)
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def retrieve(self, request, pk=None):
        service = get_object_or_404(self.queryset, pk=pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        service = get_object_or_404(self.queryset, pk=pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        data = request.data
        service = get_object_or_404(self.queryset, pk=pk)
        service.name = data['name']
        service.cost = int(data['cost'])
        service.save()

        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def list(self, request):
        serializer = ServiceSerializer(self.filter_queryset(self.queryset), many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        company = User.objects.get(fullname=data['company'])
        if company.role.role == "Comp":
            category = Category.objects.get(category=data['category'])
            model = Service(name=data['name'], cost=data['cost'], company=company,
                            id=data['id'], category=category)
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

    def delete(self, request, pk, format=None):
        category = get_object_or_404(self.queryset, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        data = request.data
        category = get_object_or_404(self.queryset, pk=pk)
        category.category = data['category']

        category.save()

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def list(self, request):
        serializer = CategorySerializer(self.filter_queryset(self.queryset), many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        model = Category(category=data['category'])
        model.save()
        serializer = CategorySerializer(model)
        return Response(serializer.data)
