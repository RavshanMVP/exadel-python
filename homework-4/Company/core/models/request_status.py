
from django.db import models

class RequestStatus(models.Model):

    PENDING = 'Pend'
    CANCELED = 'Canc'
    COMPLETED = 'Comp'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CANCELED, 'Canceled'),
        (COMPLETED, 'Completed'),
    ]

    status = models.CharField(max_length=4, choices= STATUS_CHOICES, default=PENDING, null=False)

    def __str__(self):
        return self.status

