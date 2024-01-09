from django.shortcuts import render

from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework import views, generics
from rest_framework.status import *
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly

from main.models import *
from .serializers import *
from django.http import Http404
from datetime import date
#from .permissions import IsAuthorOrReadOnly
from urllib.parse import unquote
from django.db import transaction


from django.http import JsonResponse
from datetime import timedelta
from .models import Challenge, Achieve
from django.utils import timezone







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

    def post(self, request, pk, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, challenge_id=pk)
            return Response({'message': '댓글 작성 성공', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': '댓글 작성 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CommentRView(views.APIView):
    serializer_class = CommentsSerializer

    def get_object(self, comment_pk):
        return get_object_or_404(Comments, pk=comment_pk)

    def patch(self, request, pk, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = self.serializer_class(instance=comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '댓글 수정 성공', 'data': serializer.data})
        return Response({'message': '댓글 수정 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, comment_pk):
        comment = self.get_object(comment_pk)
        comment.delete()
        return Response({'message': '댓글 삭제 성공'}, status=status.HTTP_204_NO_CONTENT)

class RecommentView(views.APIView):
    serializer_class = RecommentsSerializer 

    def post(self, request, comment_pk):
        comment = get_object_or_404(Comments,pk=comment_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, comment=comment)
            return Response({'message': '대댓글 작성 성공', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': '대댓글 작성 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class DeleteGoalView(views.APIView): 
    serializer_class = GoalsSerializer  

    def get_object(self, goal_pk):
        goal = get_object_or_404(Goals, pk=goal_pk)
        self.check_object_permissions(self.request, goal)
        return goal

    def patch(self, request, goal_pk):
        goal =Goals.objects.get( pk=goal_pk)
        goal.activate = not goal.activate  # 반전
        goal.save()

        goal_serializer = GoalsSerializer(goal)

        return Response({'message' : '활성화 여부 변경 성공', 'data' : goal_serializer.data})


    
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
    def get_queryset(self):
        user = self.request.user
        return user.challenge_set.all()

    def get(self, request):
        challenges = self.get_queryset()
        serializer = GoalChallengeSerializer(challenges, many=True)

        if challenges.exists():
            return Response({'message': '챌린지 & 목표 목록 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '내가 만든 챌린지가 없습니다.'})

class ChallengeAddView(views.APIView):
    serializer_class = ChallengeSerializer

    def post(self, request):
        existing_challenges = Challenge.objects.filter(user=self.request.user)
        current_time = timezone.now().date()

        for challenge in existing_challenges:
            created_at = challenge.created_at
            period = challenge.period
            end_date = created_at + timezone.timedelta(days=period)

            if end_date > current_time:
                return Response({'message': '이전에 생성된 챌린지가 아직 끝나지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        challenge_serializer = self.serializer_class(data=request.data)
        if challenge_serializer.is_valid(raise_exception=True):
            new_challenge=challenge_serializer.save(user=request.user)
            Ball.objects.create(user=request.user, challenge=new_challenge)
            return Response({'message': '챌린지 작성 성공', 'data': challenge_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '챌린지 작성 실패', 'data': challenge_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class GoalAddView(views.APIView):
    serializer_class = GoalsSerializer

    def get(self, request, challenge_pk):
        challenge = get_object_or_404(Challenge, pk=challenge_pk)
        goal = Goals.objects.filter(challenge=challenge)
        serializer = self.serializer_class(goal, many=True)

        combined_data = {
            'challenge' : challenge.name,
            'goal':serializer.data
        }
        return Response({'message': '목표 목록 조회 성공', 'data': combined_data})

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
            combined_data = {
            'challenge' : challenge.name,
            'goal':serializer.data
            }
            return Response({'message': '목표 생성 성공', 'data': combined_data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '목표 생성 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
'''
class AchievementView(views.APIView):
    serializer_class = AchieveSerializer
    permission_classes = [IsAuthorOrReadOnly]

    
    def get(self, request, goal_pk):
        goal = get_object_or_404(Goals, pk=goal_pk)
        achieve = get_object_or_404(Achieve, goal=goal, today=True)
        self.check_object_permissions(request, achieve)

        # 이 부분에서 원하는 로직을 추가하거나 필요하면 데이터를 직접 반환
        achieve_serializer = AchieveSerializer(achieve)
        return Response({'message': '오늘 목표 조회 성공', 'data': achieve_serializer.data})

    def patch(self, request, goal_pk):
        achieve = get_object_or_404(Achieve, goal__pk=goal_pk, today=True)
        achieve.is_done = not achieve.is_done  # 반대로 변경
        achieve.save()
        achieve_serializer = AchieveSerializer(achieve)

        return Response({'message': '목표 달성 여부 변경 성공', 'data': achieve_serializer.data})
'''
class ReactionView(views.APIView):
    EMOTION_TYPES = ['good', 'question', 'fighting', 'fire', 'mark', 'heart']

    def get_emotion_counts(self, challenge, emotion_type):
        if emotion_type not in self.EMOTION_TYPES:
            return {}

        emotion_field = getattr(challenge, emotion_type)
        count = emotion_field.count()

        return {f'{emotion_type}_count': count}

    def post(self, request, challenge_id, emotion_type):
        try:
            challenge = Challenge.objects.get(pk=challenge_id)
        except Challenge.DoesNotExist:
            return Response({'error': 'Challenge not found'}, status=status.HTTP_404_NOT_FOUND)

        if emotion_type not in self.EMOTION_TYPES:
            return Response({'error': 'Invalid emotion type'}, status=status.HTTP_400_BAD_REQUEST)

        emotion_field = getattr(challenge, emotion_type)

        if emotion_field.filter(id=request.user.id).exists():
            emotion_field.remove(request.user)
            is_selected = False
        else:
            emotion_field.add(request.user)
            is_selected = True

        # 감정 개수도 반환
        emotion_counts = self.get_emotion_counts(challenge, emotion_type)

        response_data = {
            'message': f'{emotion_type} 리액션 변경 성공',
            'data': {
                'challenge_id': challenge_id,
                'emotion_type': emotion_type,
                'is_selected': is_selected,
                **emotion_counts,
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ReactionCountView(views.APIView):
    EMOTION_TYPES = ['good', 'question', 'fighting', 'fire', 'mark', 'heart']

    def get_emotion_counts(self, challenge, user):
        emotion_counts = {}
        for emotion_type in self.EMOTION_TYPES:
            emotion_field = getattr(challenge, emotion_type)
            count = emotion_field.count()
            is_clicked = user in emotion_field.all()
            emotion_counts[f'{emotion_type}_count'] = count
            emotion_counts[f'{emotion_type}_clicked'] = is_clicked

        return emotion_counts

    def get(self, request, challenge_id):
        try:
            challenge = Challenge.objects.get(pk=challenge_id)
        except Challenge.DoesNotExist:
            return Response({'error': 'Challenge not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user  # 현재 사용자

        emotion_counts = self.get_emotion_counts(challenge, user)

        response_data = {
            'message': '리액션 갯수 및 클릭 여부 조회 성공',
            'data': {
                'challenge_id': challenge_id,
                **emotion_counts,
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

'''
class ReactionCountView(views.APIView):
    EMOTION_TYPES = ['good', 'question', 'fighting', 'fire', 'mark', 'heart']

    def get_emotion_counts(self, challenge, user):
        emotion_counts = {}
        for emotion_type in self.EMOTION_TYPES:
            emotion_field = getattr(challenge, emotion_type)
            count = emotion_field.count()
            is_clicked = user in emotion_field.all()
            emotion_counts[f'{emotion_type}_count'] = count
            emotion_counts[f'{emotion_type}_clicked'] = is_clicked

        return emotion_counts

    def get(self, request, user_pk):
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get the most recent challenge for the user
        recent_challenge = Challenge.objects.filter(user=user).order_by('-created_at').first()

        if not recent_challenge:
            return Response({'error': '유저의 챌린지가 아직 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        emotion_counts = self.get_emotion_counts(recent_challenge, user)

        response_data = {
            'message': '리액션 갯수 및 클릭 여부 조회 성공',
            'data': {
                'challenge_id': recent_challenge.id,
                **emotion_counts,
            }
        }

'''
class AchievementRate(views.APIView):
    # @login_required
    def get(self, request):
        user = request.user

        # 현재 사용자가 작성한 챌린지만 가져오기
        user_challenges = Challenge.objects.filter(user=user)

        result = []

        for challenge in user_challenges:
            challenge_serializer = ChallengeSerializer(challenge)
            goals = challenge.goals.all()
            total_rate = 0
            total_achieves = Achieve.objects.filter(goal__challenge=challenge)
            completed_achieves = total_achieves.filter(is_done=True)

            result.append({
                'challenge': challenge_serializer.data
            })

            for goal in goals:
                goal_serializer = GoalsSerializer(goal)
                achieves = goal.achieves.all()
                done_count = achieves.filter(is_done=True).count()
                total_count = achieves.count()

                achievement_rate = (done_count / total_count) * 100 if total_count > 0 else 0
                achievement_rate = round(achievement_rate, 1)

                result.append({
                    'goal': goal_serializer.data,
                    'goal_rate': achievement_rate
                })
                total_rate += achievement_rate

            challenge_rate = (completed_achieves.count() / total_achieves.count()) * 100 if total_achieves.count() > 0 else 0
            challenge_rate = round(challenge_rate, 1)

            result.append({
                'challenge_rate': challenge_rate
            })

        return Response({
            'message': '달성률 조회 성공',
            'data': {
                'AchievementRate': result,
            }
        })
'''
class CalendarView(views.APIView):
    def get(self, request):
        raw_date_str = request.GET.get('date', None)

        if not raw_date_str:
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # 슬래시 제거
        date_str = unquote(raw_date_str.rstrip('/'))

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        achieves = Achieve.objects.filter(date=date)

        data = []
        for achieve in achieves:
            goal_content = achieve.goal.content
            goal_id = achieve.goal.id
            challenge_name = achieve.goal.challenge.name
            is_done = achieve.is_done

            data.append({
                'goal_content': goal_content,
                'goal_id':goal_id,
                'challenge_name': challenge_name,
                'is_done': is_done
            })

        return Response({'date': date_str, 'data': data}, status=status.HTTP_200_OK)

'''

class CalendarView(views.APIView):
    def get(self, request):
        user = request.user

        raw_date_str = request.GET.get('date', None)

        if not raw_date_str:
            return Response({'error': 'Date parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        # 슬래시 제거
        date_str = unquote(raw_date_str.rstrip('/'))

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        achieves = Achieve.objects.filter(date=date, goal__challenge__user=user)

        data = []
        for achieve in achieves:
            goal_content = achieve.goal.content
            goal_id:goal_id
            challenge_name = achieve.goal.challenge.name
            is_done = achieve.is_done

            data.append({
                'goal_content': goal_content,
                'goal_id':goal_id,
                'challenge_name': challenge_name,
                'is_done': is_done
            })

        return Response({'date': date_str, 'data': data}, status=status.HTTP_200_OK)
    

class BallView(views.APIView):
    permission_classes = [IsAuthorOrReadOnly]

    def patch(self, request, goal_pk, *args, **kwargs):
        date_param = self.request.query_params.get('date', None)
        if not date_param:
            return Response({"error": "Date parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
        date_str = unquote(date_param.rstrip('/'))

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        goal = get_object_or_404(Goals, pk=goal_pk)

        # 원자적인 트랜잭션을 시작합니다.
        with transaction.atomic():
            # 가져오기 조건에 맞는 Achieve 필터링
            achieves = Achieve.objects.filter(goal=goal, date=date, is_done=False)

            if not achieves.exists():
                return Response({"message": "No matching Achieves found"}, status=status.HTTP_404_NOT_FOUND)

            ball = get_object_or_404(Ball, user=request.user)
            if ball.count == 1:
                # Achieve 업데이트
                for achieve in achieves:
                    # Ensure that the user owns the Achieve before updating
                    if achieve.goal.challenge.user != request.user:
                        return Response({"error": "You don't have permission to update this Achieve"}, status=status.HTTP_403_FORBIDDEN)

                    achieve.is_done = True
                    achieve.save()

                # Ball 업데이트
                ball.count = 0
                ball.time = 1
                ball.save()
            else:
                return Response({"error": "You don't have ball to update this Achieve"}, status=status.HTTP_403_FORBIDDEN)

        achieve = Achieve.objects.filter(goal=goal, date=date)
        data = AchieveSerializer(achieve,many=True)

        return Response({"message": "Achieves and Ball updated successfully", "data": data.data}, status=status.HTTP_200_OK)
    
class AchievementView(views.APIView):
    permission_classes = [IsAuthorOrReadOnly]

    def patch(self, request, goal_pk, *args, **kwargs):
        date_param = self.request.query_params.get('date', None)
        if not date_param:
            return Response({"error": "Date parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
        date_str = unquote(date_param.rstrip('/'))

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        
        if date != timezone.localtime(timezone.now()).date() :
            return Response({"error": "오늘 날짜가 아닙니다"}, status=status.HTTP_404_NOT_FOUND)

        goal = get_object_or_404(Goals, pk=goal_pk, challenge__user=request.user)

        # 원자적인 트랜잭션을 시작합니다.
        with transaction.atomic():
            # 가져오기 조건에 맞는 Achieve 필터링
            achieves = Achieve.objects.filter(goal=goal, date=date)

            if not achieves.exists():
                return Response({"message": "No matching Achieves found"}, status=status.HTTP_404_NOT_FOUND)
            
            for achieve in achieves:
                if achieve.goal.challenge.user != request.user:
                    return Response({"error": "You don't have permission to update this Achieve"}, status=status.HTTP_403_FORBIDDEN)
            
                achieve.is_done= not achieve.is_done
                achieve.save()
                achieve_serializer=AchieveSerializer(achieve)
                return Response({'message': '목표 달성 여부 변경 성공', 'data': achieve_serializer.data}, status=status.HTTP_200_OK)



class AllCalendarView(views.APIView):
    def get(self, request, user_pk):
        # 사용자 가져오기
        user = get_object_or_404(User, pk=user_pk)
        
        # 날짜 매개 변수 가져오기
        date_param = request.GET.get('date')

        if not date_param:
            return Response({'error': 'Invalid date parameter'}, status=status.HTTP_400_BAD_REQUEST)
            
        date_str = unquote(date_param.rstrip('/'))
        try:
            selected_date = timezone.datetime.strptime(date_str, '%Y-%m')
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        # MM의 첫째 날짜 및 마지막 날짜 계산
        start_date = (selected_date.replace(day=1) - timedelta(days=6)).date()
        end_date = ((selected_date.replace(day=1) + timedelta(days=31)).replace(day=1) + timedelta(days=6) - timedelta(days=1)).date()

        result = []

        # 사용자에게 연결된 가장 최근의 챌린지 가져오기
        recent_challenge = Challenge.objects.filter(user=user).order_by('-created_at').first()

        if not recent_challenge:
            return Response({'error': 'No challenge found for the user'}, status=status.HTTP_400_BAD_REQUEST)

        # 챌린지의 모든 목표 가져오기
        goals = Goals.objects.filter(challenge=recent_challenge)

        # 각 목표에 대해 성취 조회
        for goal in goals:
            achieves = Achieve.objects.filter(goal=goal)

            for current_date in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
                # 현재 날짜에 해당하는 성취 찾기
                achieve = achieves.filter(date=current_date).first()

                if achieve:
                    result.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'goal': achieve.goal.content,
                        'is_done': achieve.is_done,
                    })
                else:
                    result.append({
                        'date': current_date.strftime('%Y-%m-%d'),
                        'goal': None,
                        'is_done': None,
                    })

        return Response({'data': result}, status=status.HTTP_200_OK)