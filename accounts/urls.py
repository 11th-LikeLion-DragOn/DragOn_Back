from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('duplicate/username',DuplicateIDView.as_view()),
    path('duplicate/nickname',DuplicateNickView.as_view()),
    path('changenickname/', NicknameUpdateView.as_view()),
    path('password_reset/', ChangePasswordView.as_view()),
    path('delete/', DeleteView.as_view()),
    #path('kakao/login/', KakaoLoginView.as_view()),
    #path('kakao/callback/', KakaoCallbackView.as_view()),
]