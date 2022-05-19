from . import user
from django.db import models

class Service(models.Model):
    name = models.CharField("Name of the service", max_length= 50, null= False)
    cost = models.FloatField("price of one service", default= 0.0 , null= False)
    company = models.ForeignKey(user.User, on_delete= models.CASCADE)

    def __str__(self):
        return self.name
