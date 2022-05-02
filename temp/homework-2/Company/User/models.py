from django.db import models

# Create your models here.

class Admin(models.Model):
    user_name =  models.CharField("Name of the user", max_length= 30)
    password = models.CharField("Password", max_length= 50)
    def __str__(self) -> str:
        return self.user_name

class User(models.Model):
    user_name =  models.CharField("Name of the user", max_length= 30)
    password = models.CharField("Password", max_length= 50)
    phone_number = models.CharField("Phone number", max_length= 15)
    def __str__(self) -> str:
        return self.user_name
