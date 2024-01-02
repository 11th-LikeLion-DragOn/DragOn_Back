
from django.db import models
from accounts.models import *
from datetime import datetime, timedelta
from django.utils import timezone

class Reaction(models.Model):
    #challenge = models.ForeignKey('Challenge', on_delete=models.CASCADE, related_name='reactions')
    emgoji = models.IntegerField()
    check = models.BooleanField(default=False)

class Challenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(null=False)
    period = models.IntegerField() #기간, 며칠동안
    time = models.IntegerField() #여의주 충전 7일 관련.. 사용자 직접 입력 x 
    reaction = models.ManyToManyField(Reaction, related_name='challenges', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=False, default=timezone.now) #period 더하면 ended_at 

class Goals(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='goals')
    content = models.TextField(blank=True)
    activate = models.BooleanField(default=True)

class Achieve(models.Model):
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE)
    period = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    today = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Recomments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ball(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_balls')
    count = models.IntegerField()