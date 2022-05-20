from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from api.serializers import RequestSerializer
from core.models import Request, User, Service, RequestStatus
from rest_framework.permissions import IsAuthenticated, AllowAny

class RequestDetails(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def retrieve(self, request, pk=None):
        queryset = Request.objects.all()
        request = get_object_or_404(queryset, pk=pk)
        serializer = RequestSerializer(request)
        return Response(serializer.data)


    def delete(self,request,pk,format = None):
        model = self.get_data(pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        serializer = RequestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = Request.objects.all()
        serializer = RequestSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        user = User.objects.get(id=data['user'])
        service = Service.objects.get(id=data['service'])
        status = RequestStatus.objects.get(id=data['status'])
        model = Request(address = data['address'], created_at = data['created_at'], area = data ['area'], cost_total = data['cost_total'], status = status, service = service, user = user)
        model.save()
        serializer = RequestSerializer(model)
        return Response(serializer.data)
