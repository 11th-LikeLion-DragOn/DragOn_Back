from django.urls import path
from .views import *

app_name = 'mypage'

urlpatterns = [
    #path('update-profile/', ProfileUpdateView.as_view()),
    path('test/', TestAddView.as_view()),
    path('mytest/', TestView.as_view()),
    path('profile/',ProfileView.as_view()),
    path('follow/<int:user_id>/', FollowView.as_view()),
    path('following-list/', FollowingListView.as_view()),
    path('search/<str:user_nickname>/', UserSearchView.as_view()),
    path('friend/<int:user_id>/', UserAchievementRateView.as_view()),
    path('fricalendar/', CalendarView.as_view(),),
    path('fri_profile/<int:user_pk>/', Friend_ProfileView.as_view()),

]