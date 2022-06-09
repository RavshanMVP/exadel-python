from django.db import models
from django.utils import timezone
from . import user, service, request_status


class Request(models.Model):
    country = models.CharField("Country", null=False, default="", max_length=50)
    city = models.CharField("City", null=False, default="", max_length=50)
    address = models.TextField("Full address", null=False, default="")
    created_at = models.DateTimeField("Time of the service", default=timezone.now)
    area = models.PositiveIntegerField("Area of cleaning", default=0.0, null=False)
    cost_total = models.FloatField("Total cost of the service", null=False, default=0.0)
    minutes = models.PositiveSmallIntegerField("period of cleaning", default=60, null=False)

    service_list = models.ManyToManyField(service.Service, related_name="service_list", default=[])
    final_service = models.ForeignKey(service.Service, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(request_status.RequestStatus, on_delete=models.CASCADE)
    user = models.ForeignKey(user.User, on_delete=models.CASCADE)
    accepted_list = models.ManyToManyField(service.Service, related_name="accepted_list", default=[],
                                           verbose_name="List of services who accepted user's order")

    is_filtered = models.BooleanField("Do you want to use filters?", default=False)
    min_rating = models.FloatField("Rating for filters", default=3)
    max_cost = models.FloatField("Cost for filters", default=100)
    search_category = models.CharField("Category for filters", max_length=50, default="Vacuuming")

    def __str__(self):
        return self.user.fullname + str(self.created_at)

    REQUIRED_FIELDS = ['address', 'user', 'service', 'area',  'status']
