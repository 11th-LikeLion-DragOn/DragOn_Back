from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    #path('logout/',LogoutView.as_view()),
    path('changenickname/', NicknameUpdateView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('delete/', DeleteView.as_view()),

]