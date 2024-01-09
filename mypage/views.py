from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, login
from rest_framework import views
from rest_framework.status import *

from .serializers import *


from main.models import Achieve

from datetime import datetime
from django.shortcuts import get_object_or_404
from django.utils.http import unquote


from rest_framework import status, views
from rest_framework.response import Response
from main.models import Challenge, Achieve
from main.serializers import ChallengeSerializer, GoalsSerializer, NicknameUpdateSerializer


class TestAddView(views.APIView):
    serializer_class = TestSerializer

    def post(self, request, format=None):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            # 테스트 결과에 따라 프로필 변경
            profile_result = self.update_user_profile(serializer.data)
            return Response({'message': '테스트 완료', 'data': serializer.data, 'profile_result': profile_result})
        return Response(serializer.errors)

    def update_user_profile(self, test_data):
        # 테스트 결과에 따라 프로필 변경 로직
        result = [test_data.get(f'question{i}', False) for i in range(1, 6)]

        user = self.request.user

        print(f"Test Data: {test_data}")
        print(f"Result: {result}")

        if all(result[0:4]) or result == [False, True, True, True, True]:
            user.profile = 'red'
            profile_message = "공격형 이무기"
        elif all(result[0:3]) or result == [False, False, False, True, True]:
            user.profile = 'yellow'
            profile_message = "차분형 이무기"
        elif all(result[3:]) or result == [True, True, True, False, False]:
            user.profile = 'gray'
            profile_message = "근성형 이무기"
        elif result == [False, False, False, False, True] or result == [True, False, True, False, True]:
            user.profile = 'pink'
            profile_message = "시너지형 이무기"
        elif any(result) and not all(result):
            user.profile = 'green'
            profile_message = "도약형 이무기"

        user.save()  # Save the updated profile information to the user model

        return user.profile, profile_message


class TestView(views.APIView):
    def get(self, request):
        user = self.request.user
        latest_test = Test.objects.filter(user=user).order_by('-created_at').first()

        if latest_test:
            # 테스트 결과에 따라 프로필 변경
            test_add_view = TestAddView(request=self.request)
            profile_result = test_add_view.update_user_profile(TestSerializer(latest_test).data)
            
            # 해당 테스트 결과 및 프로필 결과를 응답으로 반환
            return Response({'message': '나의 테스트 결과 확인하기', 'data': TestSerializer(latest_test).data, 'profile_result': profile_result}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "아직 수행한 테스트가 없습니다. "}, status=status.HTTP_404_NOT_FOUND)


class ProfileView(views.APIView):
    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(request.user) 
        return Response({'message': '프로필 확인하기', 'data': serializer.data}, status=HTTP_200_OK)

class FollowView(views.APIView): 
    def post(self, request, user_id):

        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me in you.followers.all(): # users/models.py의 related_name=followers
            you.followers.remove(me) # (request.user)
            return Response({'message': '친구 삭제 완료'}, status=HTTP_200_OK)
        else:
            you.followers.add(me) # 너의 팔로워에 나를 더해라
            return Response({'message': '친구 추가 완료'}, status=HTTP_200_OK)
        
class FollowingListView(views.APIView):
    def get(self, request, format=None):
        following_list = request.user.following.all()
        serializer = FollowSerializer(following_list, many=True)
        return Response({'following_list': serializer.data}, status=status.HTTP_200_OK)


class UserSearchView(views.APIView):
    def get(self, request, user_nickname):
        try:
            # 현재 사용자가 팔로우한 사용자의 ID 리스트를 가져옵니다.
            following_ids = request.user.following.values_list('id', flat=True)

            # 팔로우한 사용자를 제외하고 검색합니다.
            user = User.objects.exclude(id__in=following_ids).get(nickname=user_nickname)

            user_data = {
                'id': user.id,
                'nickname': user.nickname,
                'profile': user.profile,
            }

            return Response({'message': '사용자를 찾았습니다.', 'user_data': user_data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': '해당 닉네임의 사용자가 없거나 팔로우한 사용자입니다.'}, status=status.HTTP_404_NOT_FOUND)
        

class UserAchievementRateView(views.APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        challenges = Challenge.objects.filter(user=user)
        result = []

        for challenge in challenges:
            challenge_serializer = ChallengeSerializer(challenge)
            goals = challenge.goals.all()
            total_rate = 0
            result.append({
                'challenge': challenge_serializer.data
            })

            for goal in goals:
                goal_serializer = GoalsSerializer(goal)
                achieves = goal.achieves.all()
                done_count = achieves.filter(is_done=True).count()
                total_count = achieves.count()

                achievement_rate = (done_count / total_count) * 100 if total_count > 0 else 0
                achievement_rate = round(achievement_rate, 1)

                result.append({
                    'goal': goal_serializer.data,
                    'goal_rate': achievement_rate
                })
                total_rate += achievement_rate

            challenge_rate = (total_rate / goals.count()) if goals.count() > 0 else 0
            challenge_rate = round(challenge_rate, 1)
            result.append({
                'challenge_rate': challenge_rate
            })

        return Response({
            'message': f'Achievement rate for user {user.username}',
            'data': {
                'Achievement Rate': result,
            }
        })



class CalendarView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id', None)
        raw_date_str = request.GET.get('date', None)

        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not raw_date_str:
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # 슬래시 제거
        date_str = unquote(raw_date_str.rstrip('/'))

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = int(user_id)
        except ValueError:
            return Response({'error': 'Invalid user ID format'}, status=status.HTTP_400_BAD_REQUEST)

        achieves = Achieve.objects.filter(goal__challenge__user__id=user_id, date=date)

        data = []
        for achieve in achieves:
            goal_content = achieve.goal.content
            goal_id = achieve.goal.id
            challenge_name = achieve.goal.challenge.name
            is_done = achieve.is_done

            data.append({
                'goal_content': goal_content,
                'goal_id': goal_id,
                'challenge_name': challenge_name,
                'is_done': is_done
            })

        return Response({'user_id': user_id, 'date': date_str, 'data': data}, status=status.HTTP_200_OK)





class Friend_ProfileView(views.APIView):
    def get(self, request, user_pk):
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        # 사용자의 닉네임 정보 가져오기
        serializer = NicknameUpdateSerializer(user)

        # 해당 사용자의 가장 최근에 만든 챌린지 가져오기
        try:
            latest_challenge = Challenge.objects.filter(user=user).latest('created_at')
        except Challenge.DoesNotExist:
            latest_challenge = None

        # 챌린지 정보도 시리얼라이즈
        challenge_serializer = ChallengeSerializer(latest_challenge) if latest_challenge else None

        # 응답 데이터 구성
        response_data = {
            'user_info': serializer.data,
            'latest_challenge': challenge_serializer.data if challenge_serializer else None
        }

        return Response(response_data)