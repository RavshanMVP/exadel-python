from django.db import models

class Role(models.Model):
    role = models.CharField("User or Company", max_length=7)

    def __str__(self):
        return self.role
