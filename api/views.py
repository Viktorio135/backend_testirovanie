import datetime

from django.utils import timezone


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import Cure, CustomUser, Schedule
from .serializers import CureSerializer, ScheduleSerializer

class CreateOrGetScheduleView(APIView):
    """Представление для создания и чтения расписания"""
    def post(self, request):
        """Создание расписания приемов на день."""
        data = request.data
        serializer = CureSerializer(data=data)
        if serializer.is_valid():
            cure = serializer.save()
            return Response(
                data=cure.id, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'errors': serializer.errors,},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def get(self, request):
        """
        Возвращает данные о выбранном расписании с рассчитанным
        графиком приёмов на день
        """
        user_id = request.GET.get('user_id')
        schedule_id = request.GET.get('schedule_id')
        user = get_object_or_404(CustomUser, user_id=user_id)
        cure = get_object_or_404(Cure, id=schedule_id)
        if cure.user == user:
            schedule = Schedule.objects.filter(cure=cure, reminder_time__lt=timezone.now()+datetime.timedelta(days=1))
            serializer = ScheduleSerializer(schedule, many=True)
            data = serializer.data
            return Response(data)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
class UserScheduleView(APIView):
    """
    Возвращает список идентификаторов существующих
    расписаний для указанного пользователя
    """
    def get(self, request):
        user_id = request.GET.get('user_id')
        user = get_object_or_404(CustomUser, user_id=user_id)
        cure = Cure.objects.filter(user=user)
        serializer_date = CureSerializer(cure, many=True)
        return Response(data=serializer_date.data, status=status.HTTP_200_OK)


class NextTakkingView(APIView):
    """
    Возвращает данные о таблетках, которые необходимо принять
    в ближайший час. Период времени задается через 
    параметры конфигурации сервиса
    """
    def get(self, request):
        user_id = request.GET.get('user_id')
        user = get_object_or_404(CustomUser, user_id=user_id)
        time_now = timezone.now()
        schedules = Schedule.objects.select_related('cure').filter(
            cure__user=user, 
            reminder_time__gte=time_now,
            reminder_time__lte=time_now+datetime.timedelta(hours=settings.NEXT_TAKKING_HOURS)
        )
        serializers_data = ScheduleSerializer(schedules, many=True)
        return Response(data=serializers_data.data, status=status.HTTP_200_OK)

    


