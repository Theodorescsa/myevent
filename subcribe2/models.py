from django.db import models
from django.contrib.auth.models import User
from home.models import EventModel
# Create your models here.
class SubcribeModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(EventModel,on_delete = models.PROTECT,null=True)
    status = models.BooleanField(default = False)
    
    def __str__(self):
        return self.event 