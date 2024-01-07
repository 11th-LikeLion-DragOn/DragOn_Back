
from django.db import models
from accounts.models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Challenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(null=False) 
    period = models.IntegerField(blank=False, null=False) #기간, 며칠동안
    #time = models.IntegerField(default=7, editable=False) #여의주 충전 7일 관련.. 사용자 직접 입력 x 
    created_at = models.DateTimeField(auto_now_add=True)
    #ended_at = models.DateTimeField(null=True, blank=True)
    good=models.ManyToManyField(User, related_name="challgege_good")
    question=models.ManyToManyField(User, related_name="challgege_question")
    fighting=models.ManyToManyField(User, related_name="challgege_fighting")
    fire=models.ManyToManyField(User, related_name="challgege_fire")
    mark=models.ManyToManyField(User, related_name="challgege_mark")
    heart=models.ManyToManyField(User, related_name="challgege_heart")


class Goals(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='goals')
    content = models.TextField(blank=True)
    activate = models.BooleanField(default=True)

@receiver(post_save, sender=Goals)
def create_achieves(sender, instance, created, **kwargs):
    if created:
        period = instance.challenge.period
        start_date = timezone.localtime(instance.challenge.created_at).date()

        for _ in range(period):
            Achieve.objects.create(goal=instance, today=(start_date == timezone.localtime(timezone.now()).date()), date=start_date)
            start_date += timedelta(days=1)


class Achieve(models.Model):
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE, related_name='achieves')
    is_done = models.BooleanField(default=False)
    today = models.BooleanField(default=True)
    date = models.DateField(null=True, blank=True)



class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Recomments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='recomment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Ball(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_balls')
    challenge=models.ForeignKey(Challenge, on_delete=models.CASCADE, null=True) #챌린지 한 개당 여의주 한개 
    time = models.IntegerField(default=1)
    count = models.IntegerField(default=0)
    is_use=models.BooleanField(default=False)
