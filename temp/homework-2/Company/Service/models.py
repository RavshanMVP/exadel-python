from django.db import models

# Create your models here.
class Service(models.Model):
    service_name = models.CharField("Name of the service", max_length= 30)
    service_price = models.FloatField("Price of the service", default= 0)
    service_date = models.DateTimeField("Date of the service", blank= True, null= True)

    def __str__(self) -> str:
        return self.service_name

class Review(models.Model):
    name = models.ForeignKey(Service, on_delete= models.CASCADE)
    comment = models.TextField("Feedback")
    star_rating = models.IntegerField("Rating of the service", default= 5)

    def __str__(self) -> str:
        return self.comment