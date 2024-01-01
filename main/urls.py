from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    #path("challenge/", .as_view()),
    path("challengeadd/<int:user_pk>/", ChallengeAddView.as_view()), #챌린지 생성하기
    path("challengeList/<int:user_pk>/", ChallengeListView.as_view()), #챌린지 목록 조회
    path("challenge/<int:pk>/edit/<int:challenge_pk>/",ChallengeEditView.as_view()), #챌린지 수정하기
    path("goaladd/<int:challenge_pk>/", GoalAddView.as_view()), #목표 생성하기
    path("challengeCheck/<int:challenge_pk>/<int:goal_pk>/", CheckAchievement.as_view()), #목표 달성 후 체크
    #path("goal/", .as_view()),
    #path("<int:challenge_pk>/?type=int/", .as_view()),
    path("challenge/<int:pk>/commentList/", CommentListView.as_view()), #챌린지 댓글 모아보기
    path("challenge/<int:pk>/comment/", CommentView.as_view()), #챌린지 댓글 작성하기
    path("challenge/<int:pk>/comments/<int:comment_pk>/", CommentRView.as_view()), #챌린지 댓글 수정, 삭제
    path("comment/<int:comment_pk>/recomment/", RecommentView.as_view()), #챌린지 대댓글
    path("comment/<int:comment_pk>/recomment/<int:recomment_pk>/", RecommentRView.as_view()), #챌린지 대댓글 수정, 삭제
    path("challenge/<int:challenge_pk>/", DeleteChallengeView.as_view()), #챌린지 그만두기
    path("goal/<int:goal_pk>/", DeleteGoalView.as_view()), #목표 삭제하기


]