from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    time = models.TimeField(auto_now_add=False)
    task = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.task)

class Remainder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=False)
    time = models.DateTimeField(auto_now_add=False)
    text = models.TextField()
    mail = models.CharField(max_length=50, blank=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + str(self.time)