import json
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
from django.contrib.auth import authenticate, login, logout
#from dragon.settings import KAKAO_REST_API_KEY, KAKAO_REDIRECT_URI, KAKAO_CLIENT_SECRET_KEY
from .models import *
from .serializers import *

import dragon
import allauth

from urllib.parse import urlencode
from urllib.request import urlopen, Request
from django.http import JsonResponse
#from dragon.settings import KAKAO_CLIENT_ID, REDIRECT_URI
import requests
# Create your views here.


#from rest_auth.registration.views import SocialLoginView                   
from allauth.socialaccount.providers.kakao import views as kakao_views     
from allauth.socialaccount.providers.oauth2.client import OAuth2Client  
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter


BASE_URL = 'http://drag-on.shop'

KAKAO_CONFIG = {
    "KAKAO_REST_API_KEY":getattr(dragon.settings.base, 'KAKAO_REST_API_KEY', None),
    #"KAKAO_REDIRECT_URI": f"http://drag-on.shop/accounts/kakao/callback",
    "KAKAO_REDIRECT_URI": "http://localhost:3000/accounts/kakao/callback/",
    "KAKAO_CLIENT_SECRET_KEY": getattr(dragon.settings.base, 'KAKAO_CLIENT_SECRET_KEY', None), 
    "KAKAO_PW":getattr(dragon.settings.base, 'KAKAO_PW', None),
}


kakao_login_uri = "https://kauth.kakao.com/oauth/authorize"
kakao_token_uri = "https://kauth.kakao.com/oauth/token"
kakao_profile_uri = "https://kapi.kakao.com/v2/user/me"


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





class KakaoLoginView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        client_id = KAKAO_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = KAKAO_CONFIG['KAKAO_REDIRECT_URI']

        uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        
        res = redirect(uri)
        # res = requests.get(uri)
        print(res.get("access_tocken"))
        return res
    

class KakaoCallbackView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request):  
        data = request.query_params.copy()

        code = data.get('code')
        if not code:
            return Response(status=HTTP_400_BAD_REQUEST)

        request_data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_CONFIG['KAKAO_REST_API_KEY'],
            'redirect_uri': KAKAO_CONFIG['KAKAO_REDIRECT_URI'],
            'client_secret': KAKAO_CONFIG['KAKAO_CLIENT_SECRET_KEY'],
            'code': code,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_res = requests.post(kakao_token_uri, data=request_data, headers=token_headers)

        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response(status=HTTP_400_BAD_REQUEST)
        access_token = f"Bearer {access_token}" \

        # kakao 회원정보 요청
        auth_headers = {
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.get(kakao_profile_uri, headers=auth_headers)
        user_info_json = user_info_res.json()

        social_type = 'kakao'
        social_id = f"{social_type}_{user_info_json.get('id')}"

        properties = user_info_json.get('properties',{})
        nickname=properties.get('nickname','')
        profile=properties.get('thumbnail_image_url','')
        print(user_info_json)

        # 회원가입 및 로그인 처리 
        try:   
            user_in_db = User.objects.get(username=social_id) 
            # kakao계정 아이디가 이미 가입한거라면 
            # 서비스에 rest-auth 로그인
            data={'username':social_id,'password':social_id}
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                return Response({'message': "카카오 로그인 성공", 'data': serializer.validated_data}, status=HTTP_200_OK)
            return Response({'message': "카카오 로그인 실패", 'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:   
            # 회원 정보 없으면 회원가입 후 로그인
            # def post(self,request):
            print("회원가입")
            data={'username':social_id,'password':social_id,'nickname':nickname,'profile':profile}
            serializer=KSignUpSerializer(data=data)  
            if serializer.is_valid():
                serializer.save()                          # 회원가입
                data1={'username':social_id,'password':social_id}
                serializer1 = LoginSerializer(data=data1)
                if serializer1.is_valid():
                    return Response({'message':'카카오 회원가입 성공','data':serializer1.validated_data}, status=HTTP_201_CREATED)
            return Response({'message':'카카오 회원가입 실패','error':serializer.errors},status=HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    def post(self, request):
        # 로그아웃 처리
        logout(request)
        return Response({'detail': '로그아웃되었습니다.'}, status=HTTP_200_OK)

class DuplicateIDView(views.APIView):
    def post(self, request):
        username = request.data.get('username')

        if User.objects.filter(username=username).exists():
            response_data = {'duplicate':True}
        else:
            response_data = {'duplicate':False}
        
        return Response(response_data, status=HTTP_200_OK)
    

class DuplicateNickView(views.APIView):
    def post(self, request):
        nickname = request.data.get('nickname')

        if User.objects.filter(nickname__iexact=nickname).exists():
            response_data = {'duplicate': True}
        else:
            response_data = {'duplicate': False}

        return Response(response_data, status=HTTP_200_OK)
    
