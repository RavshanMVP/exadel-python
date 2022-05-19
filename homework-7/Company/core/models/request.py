from . import user,service,request_status
from django.db import models

class Request(models.Model):
    address = models.TextField("Full address", null = False, default="")
    created_at = models.DateTimeField("Time of the service", null=True)
    area = models.FloatField("Area of cleaning", default= 0.0, null = False)
    cost_total = models.FloatField("Total cost of the service", null = False, default=0.0)
    status = models.ForeignKey(request_status.RequestStatus, on_delete= models.CASCADE)
    user = models.ForeignKey(user.User, on_delete= models.CASCADE)
    service = models.ForeignKey(service.Service, on_delete= models.CASCADE)

    def __str__(self):
        return self.address + self.created_at