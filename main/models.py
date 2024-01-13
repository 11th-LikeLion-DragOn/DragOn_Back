
from django.db import models
from accounts.models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models.signals import pre_save


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

    def __str__(self):
        return f'{self.id} - {self.user}'
    

'''
@receiver(post_save, sender=Challenge)
def create_ball(sender, instance, created, **kwargs):
    if created:
        ball = Ball.objects.create(user=instance.user, challenge=instance)
        # user 필드에 instance.user 할당
        ball.user = instance.user
        ball.save()
'''
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
            Achieve.objects.create(goal=instance, date=start_date)
            start_date += timedelta(days=1)


class Achieve(models.Model):
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE, related_name='achieves')
    is_done = models.BooleanField(default=False)
    #today = models.BooleanField(default=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.goal} - {self.date}'



class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.user}'

class Recomments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='recomment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.user}'

class Ball(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_balls')
    challenge=models.ForeignKey(Challenge, on_delete=models.CASCADE, null=True) #챌린지 한 개당 여의주 한개 
    #time = models.IntegerField(default=1)
    count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.user}'
'''
@receiver(post_save, sender=Challenge)
def create_ball(sender, instance, created, **kwargs):
    if created:
        Ball.objects.create(user=instance.user, challenge=instance)

@receiver(post_save, sender=Ball)
def update_user_balls(sender, instance, created, **kwargs):
    if created:
        user_recent_ball = Ball.objects.filter(user=instance.user).order_by('-updated_at').first()
        if user_recent_ball:
            instance.user.balls = user_recent_ball.count
            instance.user.save()
            '''

@receiver(post_save, sender=Challenge)
def create_ball(sender, instance, created, **kwargs):
    if created:
        # User 모델의 balls 필드를 연결된 Ball 객체 중 최근에 생성된 객체의 count 값으로 업데이트
        latest_ball = instance.user.user_balls.order_by('-updated_at').first()
        if latest_ball:
            instance.user.balls = latest_ball.count
        else:
            instance.user.balls = 0  # 연결된 Ball 객체가 없을 경우
        instance.user.save()

        # Ball 모델에 새로운 Ball 객체 생성
        Ball.objects.create(user=instance.user, challenge=instance)