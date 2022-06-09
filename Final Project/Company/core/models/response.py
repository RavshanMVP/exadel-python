from django.db import models
from . import Request, Service


class Response(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    is_accepted = models.BooleanField("Accepted or cancelled", default=True)
    is_completed = models.BooleanField("Completed or in process", default=False)

