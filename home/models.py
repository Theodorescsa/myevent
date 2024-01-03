from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class EventModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null = True)
    leader = models.CharField(max_length = 50,null = True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField(null = True)
    time = models.TimeField()
    
    deadlinedate = models.DateField(null = True)
    deadlinetime = models.TimeField(null = True)
    address = models.CharField(max_length = 1000)
    topic = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/",null = True)
    is_completed = models.BooleanField(default = False, null = True)
    def __str__(self):
        return self.name