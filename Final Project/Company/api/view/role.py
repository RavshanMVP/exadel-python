from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.serializers.role import RoleSerializer
from core.models import Role


class RoleDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    def retrieve(self, request, pk=None):
        role = get_object_or_404(self.queryset, pk=pk)
        serializer = RoleSerializer(role)
        return Response(serializer.data)

    def list(self, request):
        serializer = RoleSerializer(self.queryset, many=True)
        return Response(serializer.data)
