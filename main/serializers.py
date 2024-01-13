
from rest_framework import serializers
from main.models import *
from accounts.serializers import *

class GoalsSerializer(serializers.ModelSerializer):
    activate = serializers.BooleanField(default=True)
    #reaction = ReactionSerializer(many=True, read_only=True)
    class Meta:
        model=Goals
        fields=['id','challenge', 'content', 'activate']

class ChallengeSerializer(serializers.ModelSerializer):
    ended_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField(method_name='get_created_at')

    class Meta:
        model = Challenge
        fields = ['user', 'id', 'name', 'period', 'created_at', 'ended_at']
        read_only_fields = ['user']

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d') if obj.created_at else None

    def get_ended_at(self, obj):
        created_at = obj.created_at
        period = obj.period-1

        if created_at is not None and period is not None:
            ended_at = created_at + timezone.timedelta(days=period)
            return ended_at.strftime('%Y-%m-%d')  # 원하는 형식으로 포맷
        else:
            return None

class GoalChallengeSerializer(serializers.ModelSerializer):
    ended_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField(method_name='get_created_at')
    goals = GoalsSerializer(many=True, read_only=True)

    class Meta:
        model = Challenge
        fields = ['user', 'id', 'name', 'period', 'created_at', 'ended_at', 'goals']

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d') if obj.created_at else None

    def get_ended_at(self, obj):
        created_at = obj.created_at
        period = obj.period

        if created_at is not None and period is not None:
            ended_at = created_at + timezone.timedelta(days=period)
            return ended_at.strftime('%Y-%m-%d')  # 원하는 형식으로 포맷
        else:
            return None

class AchieveSerializer(serializers.ModelSerializer):
    #is_today = serializers.SerializerMethodField()
    date = serializers.DateField(read_only=True)
    class Meta:
        model=Achieve
        fields=['goal', 'is_done', 'date'] 



class ComUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['id','nickname','profile']


class RecommentsSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField(method_name='get_updated_at')
    created_at = serializers.SerializerMethodField(method_name='get_created_at')
    user = ComUserSerializer(read_only=True)
    class Meta:
        model=Recomments
        fields=['id', 'user', 'content', 'created_at', 'updated_at']

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M') if obj.created_at else None

    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M') if obj.updated_at else None

class CommentsSerializer(serializers.ModelSerializer):
    user = ComUserSerializer(read_only=True)
    recomment = RecommentsSerializer(many=True, read_only=True)
    created_at = serializers.SerializerMethodField(method_name='get_created_at')
    updated_at = serializers.SerializerMethodField(method_name='get_updated_at')
    class Meta:
        model=Comments
        fields=['id', 'user', 'content', 'created_at', 'updated_at','recomment']

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M') if obj.created_at else None
    
    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M') if obj.updated_at else None

class BallsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ball
        fields='__all__'

