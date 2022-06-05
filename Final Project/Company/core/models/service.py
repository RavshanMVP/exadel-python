from . import user
from django.db import models

class Category(models.Model):
    category = models.CharField("Category of the service", max_length=50, null=False)

    REQUIRED_FIELDS = ['category']
    def __str__(self):
        return self.category

class Service(models.Model):
    name = models.CharField("Name of the service", max_length= 50, null= False)
    cost = models.PositiveIntegerField("price of one service", default= 0.0 , null= False)
    company = models.ForeignKey(user.User, on_delete= models.CASCADE)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)

    def __str__(self):
        return self.name

    REQUIRED_FIELDS = ['category','name','cost']
