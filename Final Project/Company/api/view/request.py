from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.http import HttpResponse
from django.utils import timezone

from api.serializers import RequestSerializer
from core.models import Request, User, Service, RequestStatus
from core.utility import RequestFilter
from final_project.tasks.tasks import send_notification, confirm


class RequestDetails(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Request.objects.select_related('user', 'final_service', 'status') \
        .prefetch_related('accepted_list__category', 'service_list__category',
                          'accepted_list__company', 'service_list__company').order_by("-created_at")
    serializer_class = RequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RequestFilter

    def filter_queryset(self, queryset):
        filter_backends = (DjangoFilterBackend,)
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset

    def retrieve(self, request, pk=None):
        request = get_object_or_404(self.filter_queryset(self.queryset), pk=pk)
        serializer = RequestSerializer(request)

        serializer = RequestSerializer(request)
        serializer.fields.pop("is_filtered")
        serializer.fields.pop("search_category")
        serializer.fields.pop("min_rating")
        serializer.fields.pop("max_cost")

        if request.status.status == "Pending":
            serializer.fields.pop("final_service")
            serializer.fields.pop("cost_total")

        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        requests = get_object_or_404(self.queryset, pk=pk)
        requests.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        data = request.data
        request_ = get_object_or_404(self.queryset, pk=pk)
        request_.created_at = timezone.now()
        if request_.status.status == "Pending":

            request_.address = data['address']
            request_.country = data['country']
            request_.city = data['city']

            request_.area = data['area']
            request_.minutes = data['minutes']
            request_.save()

            if data["is_filtered"] == str(True) or True:
                services = Service.objects.filter(company__role__role="Comp",
                                                  category__category=data["search_category"],
                                                  cost__lte=float(request_.max_cost),
                                                  company__company_rating__gte=request_.min_rating,
                                                  company__city=data["city"], company__country=data["country"])
                for service in services:
                    request_.service_list.add(service)
            else:
                for service in data["service_list"]:
                    service_obj = Service.objects.get(name=service["name"])
                    request_.service_list.add(service_obj)
                    send_notification.delay(service_name=service_obj.name, recipient=service_obj.company.email,
                                            address=request_.user.country + " " + request_.user.city
                                            + " " + request_.user.address, company_name=service_obj.company.fullname,
                                            user_name=request_.user.fullname, category=str(service_obj.category.category),
                                            cost_total=(float(data["area"]) * float(service_obj.cost)),
                                            phone=request_.user.phone_number, email=request_.user.email)

        elif request_.status.status == "Accepted":
            request_.final_service = Service.objects.get(name=data['final_service'])
            if request_.final_service in request_.accepted_list.all():
                request_.status = RequestStatus.objects.get(status="In process")
                request_.cost_total = float(request_.final_service.cost) * float(request_.area)
                request_.save()

                confirm.delay(company_name=request_.final_service.company.fullname,
                              service_name=request_.final_service.name,
                              user_name=request_.user.fullname, email=request_.final_service.company.email)
            else:
                return HttpResponse("The company of the service hasn't responded yet or denied your offer")

        elif request_.status.status == "Cancelled":
            return HttpResponse("Sorry, but all the companies denied your offer")

        else:
            return HttpResponse("The request is in the process or finished")

        serializer = RequestSerializer(request_)
        serializer.fields.pop("is_filtered")
        serializer.fields.pop("search_category")
        serializer.fields.pop("min_rating")
        serializer.fields.pop("max_cost")

        if request_.status.status == "Pending":
            serializer.fields.pop("final_service")
            serializer.fields.pop("cost_total")
        else:
            serializer.fields.pop("service_list")
            serializer.fields.pop("accepted_list")

        return Response(serializer.data)

    def list(self, request):
        lst = []
        requests = Request.objects.select_related('user', 'final_service', 'status').order_by("created_at")
        requests = self.filter_queryset(requests)
        for request in requests:
            serializer = RequestSerializer(request)
            serializer.fields.pop("is_filtered")
            serializer.fields.pop("search_category")
            serializer.fields.pop("min_rating")
            serializer.fields.pop("max_cost")

            serializer.fields.pop("service_list")
            serializer.fields.pop("accepted_list")

            if request.status.status == "Pending":
                serializer.fields.pop("final_service")
                serializer.fields.pop("cost_total")

            lst.append(serializer.data)
        return Response(lst)

    def post(self, request):
        data = request.data
        user = User.objects.get(fullname=data['user'],)
        filter = data["is_filtered"]

        model = Request(address=data['address'], minutes=data['minutes'], created_at=timezone.now(),
                        area=data['area'], city=data['city'], country=data['country'],
                        user=user, is_filtered=filter, status=RequestStatus.objects.get(status="Pending"))
        model.save()

        if filter == str(True):
            services = Service.objects.filter(company__role__role="Comp", category__category=data["search_category"],
                                              cost__lte=float(data["max_cost"]),
                                              company__company_rating__gte=data["min_rating"],
                                              company__city=data["city"], company__country=data["country"])
            for service in services:
                model.service_list.add(service)
                send_notification.delay(service_name=service.name, recipient=service.company.email,
                                        address=user.country + " " + user.city + " " + user.address,
                                        company_name=service.company.fullname, user_name=user.fullname,
                                        category=str(service.category.category),
                                        cost_total=(float(data["area"]) * float(service.cost)),
                                        phone=user.phone_number, email=user.email)
        else:
            for service in data["service_list"]:
                print(service)
                service_obj = Service.objects.get(name=service["name"])
                model.service_list.add(service_obj)

                send_notification.delay(service_name=service_obj.name, recipient=service_obj.company.email,
                                        address=user.country + " " + user.city + " " + user.address,
                                        company_name=service_obj.company.fullname, user_name=user.fullname,
                                        category=str(service_obj.category.category),
                                        cost_total=(float(data["area"]) * float(service_obj.cost)),
                                        phone=user.phone_number, email=user.email)
        serializer = RequestSerializer(model)
        serializer.fields.pop("accepted_list")
        serializer.fields.pop("search_category")
        serializer.fields.pop("min_rating")
        serializer.fields.pop("max_cost")
        serializer.fields.pop("cost_total")
        serializer.fields.pop("final_service")
        return Response(serializer.data)
