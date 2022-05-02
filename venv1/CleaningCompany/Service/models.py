from django.db import models

# Create your models here.
class Service(models.Model):
    service_name = models.TextField("Name of the service")