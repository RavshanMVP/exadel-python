
from django.db import models

class RequestStatus(models.Model):
    status = models.CharField("Pending, Canceled, Completed", max_length=10)

    def __str__(self):
        return self.status

