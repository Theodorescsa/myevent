from django.db import models
from django.contrib.auth.models import User
from home.models import EventModel
# Create your models here.
class ChatbotModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ManyToManyField(EventModel)
    question = models.CharField(max_length = 2000)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null = True)
    
    def __str__(self):
        return self.question
    
class ChatbotItemModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(EventModel,on_delete = models.PROTECT,null = True)
    question = models.CharField(max_length = 2000)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null = True)
    
    def __str__(self):
        return self.question
    