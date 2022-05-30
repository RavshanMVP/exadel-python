from . import role
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):

    def create_user(self, fullname, email, phone_number, role, password, **extra_fields):
        user = self.model(fullname=fullname, email=email, role = role, phone_number = phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):  # model, which extends capabilities of basic abstract user
    fullname = models.CharField("Full name of the user", max_length= 50, null= False, )
    email = models.EmailField("Email of the user", max_length=254, null= False, unique=True)
    phone_number = models.CharField("Number", max_length=15, null=False, default="+123456789")
    role = models.ForeignKey(role.Role, on_delete= models.CASCADE)
    password = models.CharField("Password", null=False, max_length=256)

    def __str__(self):
        return self.fullname
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'phone_number','role','password']


