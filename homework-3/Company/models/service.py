from . import user
from django.db import models

class Service(models.Model):
    name = models.CharField("Name of the service", max_length= 50)
    cost = models.FloatField("price of one service", default= 0.0 )
    company_id = models.ForeignKey(user.User,on_delete= models.CASCADE)

    def __str__(self):
        return self.name
