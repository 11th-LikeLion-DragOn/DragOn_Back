from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, login
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from django.conf import settings

#from dragon.settings import KAKAO_REST_API_KEY, KAKAO_REDIRECT_URI, KAKAO_CLIENT_SECRET_KEY
from .models import *
from .serializers import *


# Create your views here.
class SignUpView(views.APIView):
    serializer_class = SignUpSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공', 'data': serializer.data}, status=HTTP_201_CREATED)
        return Response({'message': '회원가입 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({'message': "로그인 성공", 'data': serializer.validated_data}, status=HTTP_200_OK)
        return Response({'message': "로그인 실패", 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class NicknameUpdateView(views.APIView):
    serializer_class = NicknameUpdateSerializer
    
    def get(self, request, format=None):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    
    def patch(self, request, format=None):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '닉네임이 성공적으로 변경되었습니다.', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message': '닉네임 변경 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
class ChangePasswordView(views.APIView):
    serializer_class =ChangePasswordSerializer
    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']
            confirm_new_password = serializer.validated_data['confirm_new_password']

            # 현재 비밀번호 확인
            if not user.check_password(current_password):
                return Response({'message': '현재 비밀번호가 옳지 않습니다.'}, status=HTTP_400_BAD_REQUEST)

            # 새로운 비밀번호 확인
            if new_password != confirm_new_password:
                return Response({'message': '새로운 비밀번호와 확인 비밀번호가 일치하지 않습니다.'}, status=HTTP_400_BAD_REQUEST)

            # 새로운 비밀번호 설정
            user.set_password(new_password)
            user.save()

            return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'}, status=HTTP_200_OK)
        else:
            return Response({'message': '올바르지 않은 데이터입니다.'}, status=HTTP_400_BAD_REQUEST)
        
class DeleteView(views.APIView):
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'message': '계정 삭제 성공'}, status=HTTP_204_NO_CONTENT)
