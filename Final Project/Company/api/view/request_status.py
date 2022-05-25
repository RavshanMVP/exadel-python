from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from api.serializers import RequestStatusSerializer
from core.models import RequestStatus

class RequestStatusDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = RequestStatus.objects.all()
    serializer_class = RequestStatusSerializer
    def retrieve(self, request, pk=None):

        status = get_object_or_404(self.queryset, pk=pk)
        serializer = RequestStatusSerializer(status)
        return Response(serializer.data)

    def list(self, request):

        serializer = RequestStatusSerializer(self.queryset, many=True)
        return Response(serializer.data)

