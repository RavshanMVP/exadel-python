from . import role
from django.db import models

class User(models.Model):
    fullname = models.CharField("Full name of the user", max_length= 50, null= False)
    email = models.EmailField("Email of the user", max_length=254, null= False)
    phone_number = models.CharField("Number", max_length=15, null=False, default="+123456789")
    role = models.ForeignKey(role.Role, on_delete= models.CASCADE)

    def __str__(self):
        return self.fullname
