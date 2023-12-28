from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, login
from rest_framework import views
from rest_framework.status import *

from .serializers import *

'''
class TestAddView(views.APIView):
    serializer_class = TestSerializer

    def post(self, request, format=None):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': '테스트 완료', 'data': serializer.data})
        return Response(serializer.errors) 

'''

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
        elif all(result[0:3]) or result == [False, False, False, True, True]:
            user.profile = 'yellow'
        elif all(result[3:]) or result == [True, True, True, False, False]:
            user.profile = 'gray'
        elif result == [False, False, False, False, True] or result == [True, False, True, False, True]:
            user.profile = 'pink'
        elif any(result) and not all(result):
            user.profile = 'white'

        user.save()

        return f"프로필이 {user.profile}로 변경되었습니다."

class TestView(views.APIView):
    def get(self, request):
        user = self.request.user
        latest_test = Test.objects.filter(user=user).order_by('-created_at').first()

        if latest_test:
            serializer = TestSerializer(latest_test)
            return Response({'message': '나의 테스트 결과 확인하기', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({"message": "아직 수행한 테스트가 없습니다. "}, status=404)


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
        following_usernames = [user.username for user in following_list]
        return Response({'following_list': following_usernames}, status=status.HTTP_200_OK)
    
class UserSearchView(views.APIView):
    def get(self, request, user_nickname):
        try:
            user = User.objects.get(nickname=user_nickname)

            return Response({'message': '사용자를 찾았습니다.', 'user_data': {'id': user.id, 'nickname': user.nickname}}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': '해당 닉네임의 사용자가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)