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
        queryset = Request.objects.all()
        requests = get_object_or_404(queryset, pk=pk)
        requests.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        data = request.data
        request_list = Service.objects.all()
        request_ = get_object_or_404(request_list, pk=pk)
        request_.address = data['address']
        request_.created_at = data['created_at']
        request_.are = data['area']
        request_.user = User.objects.get(id=data['user'])
        request_.service = Service.objects.get(id=data['service'])
        request_.status = RequestStatus.objects.get(id=data['status'])
        request_.save()

        serializer = RequestSerializer(request_)
        return Response(serializer.data)

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
