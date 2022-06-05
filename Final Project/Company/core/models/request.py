from . import user,service,request_status
from django.db import models
from django.http import HttpResponse

class Request(models.Model):
    country = models.CharField("Country", null= False, default="", max_length=50)
    city = models.CharField("City",null=False, default="", max_length=50)
    address = models.TextField("Full address", null = False, default="")
    created_at = models.DateTimeField("Time of the service", null=True)
    area = models.PositiveIntegerField("Area of cleaning", default= 0.0, null = False)
    cost_total = models.FloatField("Total cost of the service", null = False, default=0.0)
    status = models.ForeignKey(request_status.RequestStatus, on_delete= models.CASCADE)
    user = models.ForeignKey(user.User, on_delete= models.CASCADE)
    minutes = models.PositiveSmallIntegerField("period of cleaning", default=60,null= False)
    service = models.ForeignKey(service.Service, on_delete= models.CASCADE)

    def __str__(self):
        return self.user.fullname + str(self.created_at)


    REQUIRED_FIELDS = ['address','user','service','area','status']

    def save(self, *args, **kwargs):
        if (int(self.area) < 0):
            raise ValueError("Area cannot be negative")
        else:
            self.cost_total = float(self.area) * self.service.cost
            super().save(*args,**kwargs)
