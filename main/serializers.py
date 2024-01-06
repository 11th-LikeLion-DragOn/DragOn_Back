
from rest_framework import serializers
from main.models import *
from accounts.serializers import *

'''
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reaction
        fields=['good','question','fighting','fire','Mark','heart']
'''
class GoalsSerializer(serializers.ModelSerializer):
    activate = serializers.BooleanField(default=True)
    #reaction = ReactionSerializer(many=True, read_only=True)
    class Meta:
        model=Goals
        fields=['id','challenge', 'content', 'activate']



class ChallengeSerializer(serializers.ModelSerializer):
    ended_at = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ['user', 'id', 'name', 'period', 'created_at', 'ended_at']

    def get_ended_at(self, obj):
        created_at = obj.created_at
        period = obj.period

        if created_at is not None and period is not None:
            # ended_at을 년-월-일 형식으로 포맷
            ended_at = created_at + timezone.timedelta(days=period)
            return ended_at.strftime('%Y-%m-%d')
        else:
            return None

class GoalChallengeSerializer(serializers.ModelSerializer):
    ended_at = serializers.SerializerMethodField()
    goals=GoalsSerializer(many=True, read_only=True)
    class Meta:
        model=Challenge
        fields=['user', 'id', 'name', 'period', 'created_at', 'ended_at', 'goals']

    def get_ended_at(self, obj):
        created_at = obj.created_at
        period = obj.period

        if created_at is not None and period is not None:
            # ended_at을 년-월-일 형식으로 포맷
            ended_at = created_at + timezone.timedelta(days=period)
            return ended_at.strftime('%Y-%m-%d')
        else:
            return None


class AchieveSerializer(serializers.ModelSerializer):
    #is_today = serializers.SerializerMethodField()
    date = serializers.DateField(read_only=True)
    class Meta:
        model=Achieve
        fields=['goal', 'is_done', 'today', 'date'] 

class CommentsSerializer(serializers.ModelSerializer):
    user = NicknameUpdateSerializer(many=True, read_only=True)
    class Meta:
        model=Comments
        fields=['id', 'user', 'content', 'created_at', 'updated_at']

        
class RecommentsSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True)
    class Meta:
        model=Recomments
        fields='__all__'

class BallsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ball
        fields='__all__'

class ChallengegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'
