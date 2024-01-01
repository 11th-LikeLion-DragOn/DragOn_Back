from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response

from main.models import *
from .serializers import *
from django.http import Http404
from datetime import date
#from .permissions import IsAuthorOrReadOnly


class CommentListView(views.APIView): #챌린지에 달린 댓글 보기
    serializer_class = CommentsSerializer

    def get(self, request, pk):
        comment = Comments.objects.filter(challenge=pk)
        
        if comment.exists():
            serializer = self.serializer_class(comment, many=True, context={'request': request})
            return Response({'message': '댓글 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            raise Http404("찾을 수 없습니다.")
        

# Create your views here.
class CommentView(views.APIView): 
    serializer_class = CommentsSerializer
    #permission_classes = [IsAuthorOrReadOnly]
    def post(self, request, pk):
        challenge = get_object_or_404(Challenge, pk=pk)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save( challenge=challenge)
            return Response({'message': '댓글 작성 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '댓글 작성 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CommentRView(views.APIView): 
    serializer_class=CommentsSerializer 

    def get_object(self, pk):
        challenge = get_object_or_404(Challenge, pk=pk)
        self.check_object_permissions(self.request, challenge)
        return challenge
    
    def patch(self, request, pk, comment_pk):
        challenge = self.get_object(pk=pk)
        comment = get_object_or_404(Comments, challenge=challenge, pk=comment_pk)
        serializer = self.serializer_class(instance=comment, data=request.data, partial=True,
                                    context={'request': request})
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': '댓글 수정 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '댓글 수정 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, comment_pk):
        challenge = self.get_object(pk=pk)
        comment = get_object_or_404(Comments, challenge=challenge, pk=comment_pk)
        comment.delete()
        
        return Response({'message': '댓글 삭제 성공'}, status=status.HTTP_200_OK)


class RecommentView(views.APIView): 
    serializer_class = RecommentsSerializer 
    #permission_classes = [IsAuthorOrReadOnly]
    def post(self, request, comment_pk):
        comment = get_object_or_404(Comments, pk=comment_pk)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(comment=comment)
            return Response({'message': '대댓글 작성 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '대댓글 작성 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class RecommentRView(views.APIView): 
    serializer_class=RecommentsSerializer 

    def get_object(self, comment_pk, recomment_pk):
        comment = get_object_or_404(Comments, pk=comment_pk)
        recomment = get_object_or_404(Recomments, comment=comment, pk=recomment_pk)
        self.check_object_permissions(self.request, recomment)
        return recomment
    
    def patch(self, request, comment_pk, recomment_pk):
        recomment = self.get_object(comment_pk, recomment_pk)
        serializer = self.serializer_class(instance=recomment, data=request.data, partial=True,
                                        context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': '대댓글 수정 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '대댓글 수정 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_pk, recomment_pk):
        recomment = self.get_object(comment_pk, recomment_pk)
        recomment.delete()

        return Response({'message': '대댓글 삭제 성공'}, status=status.HTTP_200_OK)

class DeleteGoalView(views.APIView): 
    serializer_class = GoalsSerializer 

    def get_object(self, pk):
        goal = get_object_or_404(Goals, pk=pk)
        self.check_object_permissions(self.request, goal)
        return goal

    def put(self, request, pk, goal_pk):
        goal = self.get_object(pk=goal_pk)

        # goal에 연결된 Challenge의 Serializer 초기화
        challenge_serializer = ChallengeSerializer(goal.challenge, data={'activate': False}, partial=True)

        if challenge_serializer.is_valid():
            # Challenge의 activate 필드를 False로 업데이트
            challenge_serializer.save()

            # Goals의 Serializer를 통해 activate가 False로 업데이트된 목표 정보 응답
            goal_serializer = GoalsSerializer(goal, data={'activate': False}, partial=True)
            if goal_serializer.is_valid():
                goal_serializer.save()
                return Response({'message': '활성화 여부 변경 성공', 'data': goal_serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': '활성화 여부 변경 실패.', 'data': goal_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': '도전을 비활성화할 수 없습니다.', 'data': challenge_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
class  DeleteChallengeView(views.APIView): 
    serializer_class = ChallengeSerializer

    def get_object(self, challenge_pk):
        challenge = get_object_or_404(Challenge, pk=challenge_pk)
        self.check_object_permissions(self.request, challenge)
        return challenge
    
    def delete(self, request, challenge_pk):
        challenge = self.get_object(challenge_pk)
        challenge.delete()
        
        return Response({'message': '챌린지 그만두기 성공'}, status=status.HTTP_200_OK)

class ChallengeListView(views.APIView):
    def get(self, request, user_pk):
        challenges = Challenge.objects.filter(user__pk=user_pk).order_by('-created_at')
        serializer=ChallengeSerializer(challenges, many=True)
        return Response({'message': '챌린지 목록 조회 성공', 'data': serializer.data})

class ChallengeAddView(views.APIView):
    serializer_class = ChallengeSerializer
    def post(self, request, user_pk):
        user=get_object_or_404(User, pk=user_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            challenges = Challenge.objects.filter(user=user).order_by('-created_at')
            serializer = self.serializer_class(challenges, many=True)
            return Response({'message': '챌린지 생성 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '챌린지 생성 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

class ChallengeEditView(views.APIView):
    serializer_class = ChallengeSerializer
    
    def get_object(self, pk):
        challenge = get_object_or_404(Challenge, pk=pk)
        self.check_object_permissions(self.request, challenge)
        return challenge

    def get(self, request, pk, challenge_pk):
        challenge = self.get_object(pk=pk)
        serializer = self.serializer_class(challenge)
        return Response({'message': '챌린지 조회 성공', 'data': serializer.data})

    def put(self, request, pk, challenge_pk):
        challenge = self.get_object(pk=pk)
        serializer = self.serializer_class(data=request.data, instance=challenge)

        if serializer.is_valid():
            serializer.save()
            return Response({'message' : '챌린지 수정 성공', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message': '챌린지 수정 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
class GoalAddView(views.APIView):
    serializer_class = GoalsSerializer

    def get(self, request, challenge_pk):
        challenge = get_object_or_404(Challenge, pk=challenge_pk)
        goal = Goals.objects.filter(challenge=challenge)
        serializer = self.serializer_class(goal, many=True)
        return Response({'message': '목표 목록 조회 성공', 'data': serializer.data})

    def post(self, request, challenge_pk):
        challenge=get_object_or_404(Challenge, pk=challenge_pk)
        #현재 목표의 수 확인
        current_goal_count=Goals.objects.filter(challenge=challenge).count()
        #목표가 3개 이상이면 에러 응답
        if current_goal_count >= 3:
            return Response({'message': '최대 3개의 목표까지만 작성할 수 있습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(challenge=challenge)
            goals = Goals.objects.filter(challenge=challenge)
            serializer = self.serializer_class(goals, many=True)
            return Response({'message': '목표 생성 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '목표 생성 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

class CheckAchievement(views.APIView):
    #serializer_class = AchieveSerializer

    def get(self, request, challenge_pk, goal_pk):
        try:
            challenge=get_object_or_404(Challenge, pk=challenge_pk)
            goal=get_object_or_404(Goals, challenge=challenge, pk=goal_pk)
            achieve=Achieve.objects.filter(goal=goal, many=True)
        except Achieve.DoesNotExist:
            return Response({'error': 'Achieve not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer=AchieveSerializer(achieve)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, challenge_pk, goal_pk):
        try:
            challenge = Challenge.objects.get(id=challenge_pk)
            goal = Goals.objects.get(id=goal_pk, challenge=challenge)
        except (Challenge.DoesNotExist, Goals.DoesNotExist):
            return Response({'error': 'Challenge or Goal not found'}, status=status.HTTP_404_NOT_FOUND)

        today = date.today()

        try:
            achieve = Achieve.objects.get(goal=goal, period=challenge, today=True)
            achieve.is_done = not achieve.is_done
            achieve.save()
        except Achieve.DoesNotExist:
            Achieve.objects.create(goal=goal, period=challenge, is_done=True, today=True)

        return Response({'success': True}, status=status.HTTP_200_OK)
