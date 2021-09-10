from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AlertModel(models.Model):
    user = models.ForeignKey(User, related_name='user_alert', on_delete=models.CASCADE)
    
