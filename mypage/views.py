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
class TestView(APIView):
    serializer_class = TestSerializer
    def post(self, request):
        # 유저 확인 및 테스트 응답 생성
        user = request.user
        try:
            test_instance = Test.objects.get(user=user)
        except Test.DoesNotExist:
            test_instance = Test(user=user)

        serializer = TestSerializer(test_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

class TestAddView(views.APIView):
    serializer_class = TestSerializer

    def post(self, request, format=None):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': '테스트 완료', 'data': serializer.data})
        return Response(serializer.errors) 

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