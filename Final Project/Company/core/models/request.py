from django.db import models

from . import user, service, request_status


class Request(models.Model):
    country = models.CharField("Country", null=False, default="", max_length=50)
    city = models.CharField("City", null=False, default="", max_length=50)
    address = models.TextField("Full address", null=False, default="")
    created_at = models.DateTimeField("Time of the service", null=True)
    area = models.PositiveIntegerField("Area of cleaning", default=0.0, null=False)
    cost_total = models.FloatField("Total cost of the service", null=False, default=0.0)
    status = models.ForeignKey(request_status.RequestStatus, on_delete=models.CASCADE)
    user = models.ForeignKey(user.User, on_delete=models.CASCADE)
    minutes = models.PositiveSmallIntegerField("period of cleaning", default=60, null=False)
    final_service = models.ForeignKey(service.Service, on_delete=models.CASCADE, null=True)
    service_list = models.ManyToManyField(service.Service, related_name="service_list")
    def __str__(self):
        return self.user.fullname + str(self.created_at)

    REQUIRED_FIELDS = ['address', 'user', 'service', 'area',  'status']


