from . import user, service,request
from django.db import models

class Review(models.Model):
    rating = models.IntegerField("Star rating of the service",null= False, default= 0)
    feedback = models.TextField("Comment of the service", null= False, default= "")
    created_at = models.DateTimeField("Time of the comment",  null= True)
    service = models.ForeignKey(service.Service, on_delete= models.CASCADE)
    user = models.ForeignKey(user.User, on_delete= models.CASCADE)
    request = models.ForeignKey(request.Request, on_delete= models.CASCADE)

    def __str__(self):
        return self.feedback
