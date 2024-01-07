from rest_framework import serializers
from .models import User, Test

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