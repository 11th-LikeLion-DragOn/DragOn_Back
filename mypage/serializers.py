from rest_framework import serializers
from .models import User, Test
from main.models import Challenge

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
        model = User  # Replace 'User' with the actual name of your User model
        fields = ['id', 'username', 'profile', 'nickname']

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['pk']  # 여기에 챌린지 모델의 다른 필드들을 추가해도 됩니다.

class UserProfileWithLatestChallengeSerializer(serializers.ModelSerializer):
    latest_challenge = ChallengeSerializer()

    class Meta:
        model = User
        fields = ['id', 'nickname', 'profile', 'latest_challenge']