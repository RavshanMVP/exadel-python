from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.serializers.user import UserSerializer_
from core.models import User, Role
from core.utility import UserFilter
import json


class UserDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.select_related('role').order_by("fullname")
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    serializer_class = UserSerializer_

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend,)
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.filter_queryset(self.queryset), pk=pk)
        serializer = UserSerializer_(user)
        if user.role.role == "user":
            serializer.fields.pop("company_rating")
            serializer.fields.pop("ratings_count")

        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        user = get_object_or_404(self.queryset, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):

        data = request.data
        user = get_object_or_404(self.queryset, pk=pk)
        user.fullname = data['fullname']
        user.email = data['email']
        user.phone_number = data['phone_number']
        user.address = data['address']
        user.city = data['city']
        user.country = data["country"]
        user.save()

        serializer = UserSerializer_(user)
        if user.role.role == "user":
            serializer.fields.pop("company_rating")
            serializer.fields.pop("ratings_count")

        return Response(serializer.data)

    def list(self, request):
        lst = []
        users = self.filter_queryset(self.queryset)
        for user in users:
            serializer = UserSerializer_(user)
            if user.role.role == "user":
                serializer.fields.pop("company_rating")
                serializer.fields.pop("ratings_count")
            lst.append(serializer.data)
        return Response(lst)

    def post(self, request):

        data = request.data
        role = Role.objects.get(role=data['role'])
        model = User(fullname=data['fullname'], phone_number=data['phone_number'], email=data['email'],
                     role=role, password=data['password'], address=data['address'], city=data['city'],
                     country=data['country'])
        model.save()
        serializer = UserSerializer_(model)
        if model.role.role == "user":
            serializer.fields.pop("company_rating")
            serializer.fields.pop("ratings_count")
        return Response(serializer.data)
