from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Blog(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cont = models.TextField()
    updated_at = models.DateTimeField(auto_now=True) 


