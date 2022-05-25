from django.db import models

class Role(models.Model):

    USER = 'user'
    COMPANY = 'Comp'

    ROLE_CHOICES = [
        (USER, 'User'),
        (COMPANY, 'Company'),
    ]

    role = models.CharField(max_length=4, choices= ROLE_CHOICES, default=USER, null=False)

    def __str__(self):
        return self.role
