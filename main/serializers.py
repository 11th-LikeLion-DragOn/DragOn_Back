
from rest_framework import serializers
from main.models import *
from accounts.serializers import *

class GoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Goals
        fields=['challenge', 'content', 'activate']
        many = True

class ChallengeSerializer(serializers.ModelSerializer):
    goal=GoalsSerializer(many=True, read_only=True)
    #period=serializers.SerializerMethodField()
    class Meta:
        model=Challenge
        fields=['user', 'name', 'period', 'time', 'reaction','created_at', 'goal', 'id' ,'ended_at'] #, 'ended_at'
    #def get_period(self, obj):
        # obj.ended_at과 obj.created_at의 차이를 계산하여 반환
        #period_delta = obj.ended_at - obj.created_at
        #return period_delta.total_seconds()  # 초 단위로 반환하거나 필요에 따라 다른 형태로 변환


        
class AchieveSerializer(serializers.ModelSerializer):
    #is_today = serializers.SerializerMethodField()
    class Meta:
        model=Achieve
        fields=['goal', 'is_done', 'today', 'date', 'period'] 

    #def get_is_today(self, obj): #오늘인지 확인
        #is_today=date.today()
        #return obj.plan_date == is_today
        #

class CommentsSerializer(serializers.ModelSerializer):
    #nickname = UserSerializer(many=True, read_only=True)
    class Meta:
        model=Comments
        fields='__all__'

        
class RecommentsSerializer(serializers.ModelSerializer):
    #comments = CommentsSerializer(many=True)
    class Meta:
        model=Recomments
        fields='__all__'

class BallsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ball
        fields='__all__'

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reaction
        fields='__all__'