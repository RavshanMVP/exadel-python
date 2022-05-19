from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status

from api.serializers import RequestStatusSerializer
from core.models import RequestStatus

class RequestStatusDetails(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = RequestStatus.objects.all()
        status = get_object_or_404(queryset, pk=pk)
        serializer = RequestStatusSerializer(status)
        return Response(serializer.data)

    def list(self, request):
        queryset = RequestStatus.objects.all()
        serializer = RequestStatusSerializer(queryset, many=True)
        return Response(serializer.data)

