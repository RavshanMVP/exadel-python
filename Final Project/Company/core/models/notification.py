from django.db import models

class Notification(models.Model):

    subject = models.CharField("Subject of the email",max_length= 100, null= False)
    message = models.TextField("Message of the email", null= False)
    sender = models.CharField("Name of the sender", max_length= 50, null=False)
    recipient = models.EmailField("Name of the receiver", null= False)
