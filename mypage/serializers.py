from rest_framework import serializers
from .models import User, Test
from main.models import Challenge
from django.utils import timezone
from datetime import timedelta


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile']

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id','user','question1', 'question2', 'question3', 'question4', 'question5']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','nickname','profile','balls']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'profile', 'nickname']

class AllProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','nickname','balls']



class AProfileSerializer(serializers.ModelSerializer):
    real_balls = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'profile', 'balls','real_balls']

    def get_real_balls(self, user):
        # 사용자의 최신 Ball 객체를 검색합니다.
        latest_ball = user.user_balls.order_by('-updated_at').first()

        if ((timezone.now() - latest_ball.updated_at).days >= 7) and (latest_ball.count == 0):
            latest_ball.count += 1


        elif ((timezone.now() - latest_ball.updated_at).days >= 7) and (latest_ball.count == 1):
            latest_ball.count += 0

        return latest_ball.count
