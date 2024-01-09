from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    #path("challenge/", .as_view()),
    path("challengeadd/", ChallengeAddView.as_view()), #챌린지 생성하기
    path("challengelist/", ChallengeListView.as_view()), #챌린지 목록 조회 (관련 목표들도 같이)
    path("goaladd/<int:challenge_pk>/", GoalAddView.as_view()), #목표 생성하기
    path("goal/<int:goal_pk>/", AchievementView.as_view()), #목표 달성 후 체크
    #path("challenge/reaction/<int:challenge_id>/",  ReactionView.as_view()), #챌린지 반응 달기
    path("challenge/<int:pk>/commentlist/", CommentListView.as_view()), #챌린지 댓글 모아보기
    path("challenge/<int:pk>/comment/", CommentView.as_view()), #챌린지 댓글 작성하기
    path("challenge/<int:pk>/comment/<int:comment_pk>/", CommentRView.as_view()), #챌린지 댓글 수정, 삭제
    path("comment/<int:comment_pk>/recomment/", RecommentView.as_view()), #챌린지 대댓글
    path("challenge/<int:challenge_pk>/", DeleteChallengeView.as_view()), #챌린지 그만두기
    path("goaldelete/<int:goal_pk>/", DeleteGoalView.as_view()), #목표 삭제하기
    path('reactions/<int:challenge_id>/<str:emotion_type>/', ReactionView.as_view()),
    path("achieverate/", AchievementRate.as_view()), #달성률 확인하기
    path("calendar/", CalendarView.as_view()),#달력 열어서 달성 여부 확인하기
    path("ball/<int:goal_pk>/", BallView.as_view()), #여의주 사용하기
    # path("allcalendar/<int:user_id>/<str:year_month>/", AllCalendarView.as_view())
    path("reaction-count/<int:user_pk>/",ReactionCountView.as_view()),
    #path("allcalendar/<int:user_pk>/",AllCalendarView.as_view()),

]