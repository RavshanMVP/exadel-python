from . import user,service,request_status
from django.db import models

class Request(models.Model):
    address = models.TextField("Full address")
    created_at = models.DateTimeField("Time of the service", null=True, blank= True)
    area = models.FloatField("Area of cleaning", default= 0)
    cost_total = models.FloatField("Total cost of the service")
    status_id = models.ForeignKey(request_status.RequestStatus,on_delete= models.CASCADE)
    user_id = models.ForeignKey(user.User,on_delete= models.CASCADE)
    service_id = models.ForeignKey(service.Service,on_delete= models.CASCADE)

    def __str__(self):
        return self.address + self.created_at
