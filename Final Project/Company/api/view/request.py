from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.serializers import RequestSerializer
from core.models import Request, User, Service, RequestStatus
from core.utility import RequestFilter
from final_project.tasks.tasks import send_notification


class RequestDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Request.objects.select_related('user', 'final_service', 'status').order_by("-created_at")
    serializer_class = RequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RequestFilter

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend, )
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def retrieve(self, request, pk=None):
        request = get_object_or_404(self.queryset, pk=pk)
        serializer = RequestSerializer(request)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        requests = get_object_or_404(self.queryset, pk=pk)
        requests.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        data = request.data
        user = User.objects.get(fullname=data['user'])

        request_ = get_object_or_404(self.queryset, pk=pk)
        request_.address = data['address']
        request_.country = data['country']
        request_.city = data['city']
        request_.created_at = data['created_at']
        request_.area = data['area']
        request_.minutes = data['minutes']
        request_.save()

        for service in data["service_list"]:
            service_obj = Service.objects.get(name=service["name"])
            request_.service_list.add(service_obj)
        send_notification(service_name=service.name, recipient=service.company.email,
                          address=user.country + " " + user.city + " " + user.address,
                          company_name=service.company.fullname, user_name=user.fullname,
                          category=str(service.category.category),
                          cost_total=(float(data["area"]) * float(service.cost)),
                          phone=user.phone_number, email=user.email)

        serializer = RequestSerializer(request_)


        return Response(serializer.data)

    def list(self, request):
        serializer = RequestSerializer(self.filter_queryset(self.queryset), many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = User.objects.get(fullname=data['user'])
        status = RequestStatus.objects.get(status=data['status'])

        model = Request(address=data['address'], created_at=data['created_at'], minutes=data['minutes'],
                        area=data['area'], city=data['city'], country=data['country'],
                        cost_total=data['cost_total'], user=user)
        model.save()

        for service in data["service_list"]:
            service_obj = Service.objects.get(name=service["name"])
            model.service_list.add(service_obj)

            send_notification.delay(service_name=service_obj.name, recipient=service_obj.company.email,
                                address=user.country + " " + user.city + " " + user.address,
                                company_name=service_obj.company.fullname, user_name=user.fullname,
                                category=str(service_obj.category.category),
                                cost_total=(float(data["area"]) * float(service_obj.cost)),
                                phone=user.phone_number, email=user.email)
        serializer = RequestSerializer(model)
        return Response(serializer.data)
