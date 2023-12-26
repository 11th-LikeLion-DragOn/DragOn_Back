from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    nickname=models.CharField(max_length=15)
    profile_choices = [
        ("빨간색","빨간색"),
        ("노란색","노란색"),
        ("회색","회색"),
        ("핑크색","핑크색"),
        ("하얀색","하얀색"),
    ]
    profile=models.CharField(max_length=10, choices=profile_choices, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')