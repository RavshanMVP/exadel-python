from django.db import models


class RequestStatus(models.Model):

    PENDING = 'Pending'
    CANCELED = 'Cancelled'
    COMPLETED = 'Completed'
    ACCEPTED = 'Accepted'
    IN_PROCESS = 'In process'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CANCELED, 'Canceled'),
        (COMPLETED, 'Completed'),
        (ACCEPTED, 'Accepted'),
        (IN_PROCESS, 'In process')
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING, null=False)

    def __str__(self):
        return self.status
