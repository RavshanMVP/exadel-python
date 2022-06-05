from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from api.serializers import RequestSerializer
from core.models import Request, User, Service, RequestStatus, Notification
from rest_framework.permissions import IsAuthenticated, AllowAny
from final_project.tasks.tasks import send_notification

class RequestDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Request.objects.select_related('user','service','status').order_by("-created_at")
    serializer_class = RequestSerializer
    def retrieve(self, request, pk=None):

        request = get_object_or_404(self.queryset, pk=pk)
        serializer = RequestSerializer(request)
        return Response(serializer.data)


    def delete(self,request,pk,format = None):
        requests = get_object_or_404(self.queryset, pk=pk)
        requests.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format = None):
        data = request.data
        user = User.objects.get(fullname=data['user'])
        service = Service.objects.get(name=data['service'])

        request_ = get_object_or_404(self.queryset, pk=pk)
        request_.address = data['address']
        request_.country = data['country']
        request_.city = data['city']
        request_.created_at = data['created_at']
        request_.area = data['area']
        request_.minutes = data['minutes'],
        request_.status = RequestStatus.objects.get(status=data['status'])
        request_.save()

        serializer = RequestSerializer(request_)
        send_notification(service_name = service.name, recipient = service.company.email,
                          address= user.country+ " " + user.city + " " + user.address,
                          company_name= service.company.fullname, user_name= user.fullname,
                          category= str(service.category.category),
                          cost_total= (float(data["area"]) * float(service.cost)),
                          phone = user.phone_number, email= user.email )

        return Response(serializer.data)

    def list(self, request):
        serializer = RequestSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def post(self,request):
        data = request.data
        user = User.objects.get(fullname=data['user'])
        service = Service.objects.get(name=data['service'])
        status = RequestStatus.objects.get(status=data['status'])


        model = Request(address = data['address'], created_at = data['created_at'], minutes = data['minutes'],
                        area = data ['area'], city = data['city'], country = data['country'],
                        cost_total = data['cost_total'], status = status, service = service, user = user)
        model.save()


        send_notification.delay(service_name = service.name, recipient = service.company.email,
                          address= user.country+ " " + user.city + " " + user.address,
                          company_name= service.company.fullname, user_name= user.fullname,
                          category= str(service.category.category),
                          cost_total= (float(data["area"]) * float(service.cost)),
                          phone = user.phone_number, email= user.email )
        serializer = RequestSerializer(model)
        return Response(serializer.data)
