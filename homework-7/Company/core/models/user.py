from . import role
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):  # model, which extends capabilities of basic abstract user
    fullname = models.CharField("Full name of the user", max_length= 50, null= False, unique=True)
    email = models.EmailField("Email of the user", max_length=254, null= False)
    phone_number = models.CharField("Number", max_length=15, null=False, default="+123456789")
    role = models.ForeignKey(role.Role, on_delete= models.CASCADE)
    password = models.CharField("Password", null=False, max_length=256)
    def __str__(self):
        return self.fullname


    USERNAME_FIELD = 'fullname'
    REQUIRED_FIELDS = []

