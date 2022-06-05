from django.db import models
from . import Request
class Response(models.Model):
    request = models.ForeignKey(Request,on_delete= models.CASCADE)
    is_accepted = models.BooleanField("Accepted or cancelled", default= True)
