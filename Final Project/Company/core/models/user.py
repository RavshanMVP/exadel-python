from . import role
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):

    def create_user(self, fullname, email, phone_number, role, password, **extra_fields):
        user = self.model(fullname=fullname, email=email, role=role, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, fullname, email, phone_number, role, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(fullname, email, phone_number, role, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):  # model, which extends capabilities of basic abstract user
    fullname = models.CharField("Full name of the user", max_length=50, null=False,)
    email = models.EmailField("Email of the user", max_length=254, null=False, unique=True)
    phone_number = models.CharField("Number", max_length=15, null=False, default="+123456789")
    role = models.ForeignKey(role.Role, on_delete=models.CASCADE)
    password = models.CharField("Password", null=False, max_length=256)
    country = models.CharField("Country", null=False, default="", max_length=50)
    city = models.CharField("City", null=False, default="", max_length=50)
    address = models.TextField("Full address", null=False, default="")

    company_rating = models.FloatField("Average star rating for company", default=0)
    ratings_count = models.PositiveSmallIntegerField("Number of reviews", default=0)

    def __str__(self):
        return self.fullname
    objects = CustomUserManager()

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'phone_number', 'role', 'password']
