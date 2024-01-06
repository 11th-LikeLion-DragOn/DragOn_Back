from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    nickname=models.CharField(max_length=200)
    profile_choices = [
        ("red","red"),
        ("yellow","yellow"),
        ("gray","gray"),
        ("pink","pink"),
        ("white","white"),
        ("0","0")
    ]
    profile=models.CharField(max_length=10, choices=profile_choices, default='0')
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    balls=models.IntegerField(default=0)

    def __str__(self):
        return f'{self.username}'
