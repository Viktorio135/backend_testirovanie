import datetime

from celery import shared_task
from django.utils import timezone

from .models import Schedule, Cure


@shared_task
def delete_old_reminders():
    """
    Запускатеся раз в 5 минут с помощью celery-beat

    Удаление неактульных записей в бд
    """
    Schedule.objects.filter(reminder_time__lt=timezone.now()).delete()


@shared_task
def extend_endless_cure():
    """
    Запускается раз в 2 часа

    автоматическое продление расписания для бесконечных приемов
    """
    cures = Cure.objects.filter(duration__isnull=True)
    
    for cure in cures:
        # получаем последнее запланированное напоминание
        last_schedule = Schedule.objects.filter(cure=cure).order_by('-reminder_time').first()
        
        if not last_schedule:
            continue
            

        time_until_last = last_schedule.reminder_time - timezone.now()
        
        if time_until_last.days <= 3: #если до последнего приема меньше 3 дней, добавляем новые расписания
            current_time = last_schedule.reminder_time
            end_time = current_time + datetime.timedelta(days=7)
            
            schedulers = []
            # аналогично созданию из модели Cure
            while current_time <= end_time:
                schedule_time = current_time
                minutes = schedule_time.minute
                if minutes % 15 != 0:
                    round_minutes = 15 - minutes % 15
                    schedule_time += datetime.timedelta(minutes=round_minutes)
                
                if 8 <= schedule_time.hour < 22:
                    schedulers.append(Schedule(cure=cure, reminder_time=schedule_time))
                
                current_time += datetime.timedelta(hours=cure.frequency)
            
            Schedule.objects.bulk_create(schedulers)