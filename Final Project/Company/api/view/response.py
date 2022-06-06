from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import ResponseSerializer
from core.models import Request, Response as Resp, Service
from final_project.tasks.tasks import respond, respond_negative


class ResponseDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Resp.objects.select_related('request')
    serializer_class = ResponseSerializer

    def retrieve(self, request, pk=None):
        response = get_object_or_404(self.queryset, pk=pk)
        serializer = ResponseSerializer(response)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        response = get_object_or_404(self.queryset, pk=pk)
        response.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        data = request.data
        response = get_object_or_404(self.queryset, pk=pk)
        response.is_accepted = (data["is_accepted"])
        request_ = Request.objects.get(id=data['request'])
        service = Service.objects.get(name=data['service'])

        if request_.status.status != "Accepted":

            if data["is_accepted"] == "True":
                request_.status.status = "Accepted"
                respond.delay(verdict=data["is_accepted"], company_name=service.company.fullname,
                              email=request_.user.email,
                              user_name=request_.user.fullname, service_name=service.name,)
            else:
                request_.status.status = "Canceled"
                respond_negative.delay(company_name=service.company.fullname, email=request_.user.email,
                                       user_name=request_.user.fullname, service_name=service.name)

            request_.status.save()
            request_.save()
            model = Resp(is_accepted=data["is_accepted"], request=request_, service=service)
            model.save()
            serializer = ResponseSerializer(model)

            return Response(serializer.data)
        else:
            model = Resp(is_accepted="False", request=request_, service=service)
            model.save()
            serializer = ResponseSerializer(model)
            return Response(serializer.data)

    def list(self, request):
        serializer = ResponseSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        request_ = Request.objects.get(id=data['request'])
        service = Service.objects.get(name=data['service'])

        if request_.status.status != "Accepted":

            if data["is_accepted"] == "True":
                request_.status.status = "Accepted"
                respond.delay(verdict=data["is_accepted"], company_name=service.company.fullname,
                              email=request_.user.email,
                              user_name=request_.user.fullname, service_name=service.name,)
            else:
                request_.status.status = "Canceled"
                respond_negative.delay(company_name=service.company.fullname, email=request_.user.email,
                                       user_name=request_.user.fullname, service_name=service.name)

            request_.status.save()
            request_.save()
            model = Resp(is_accepted=data["is_accepted"], request=request_, service=service)
            model.save()
            serializer = ResponseSerializer(model)

            return Response(serializer.data)
        else:
            model = Resp(is_accepted="False", request=request_, service=service)
            model.save()
            serializer = ResponseSerializer(model)
            return Response(serializer.data)
