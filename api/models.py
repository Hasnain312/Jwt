from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100)
    age= models.IntegerField()
    title=models.CharField(max_length=100)

    def __str__(self):
        return self.title

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    refresh_token = models.TextField(default="Default refresh text")
    access=models.TextField(default="Default access text")

    def __str__(self):
        return f"{self.user.username}'s token"

