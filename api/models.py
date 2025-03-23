import datetime

from django.db import models


class CustomUser(models.Model):
    """Модель для пользователей, она не прикреплена к User, так как нет необходимости в авторизации"""
    user_id = models.PositiveIntegerField(verbose_name='user id', primary_key=True)

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user_id
    

class Cure(models.Model):
    """
    Модель для лекарств.
    Так же можно убрать привязку к пользователю, но нормализации таблеток нет.
    """
    name = models.CharField(verbose_name='Лекарство', max_length=100)
    user = models.ForeignKey(
        CustomUser, 
        verbose_name='Пользователь', 
        on_delete=models.CASCADE, 
        related_name='cure'
    )
    start_time = models.DateTimeField(verbose_name='Вреям начала приема', auto_now_add=True)
    frequency = models.PositiveIntegerField(verbose_name='Периодичность приема', null=False,) # в часах
    duration = models.PositiveIntegerField(verbose_name='Продолжительность', null=True, blank=True) # в днях

    @property
    def end_time(self):
        """Окончание"""
        if self.duration:
            return self.start_time + datetime.timedelta(days=self.duration)
        return None

    
    def save(self, *args, **kwargs):
        """Переопределение метода для того чтобы расписание создавалось автоматически"""
        super().save(*args, **kwargs) # сохраняем объект
        end_time = self.end_time if self.duration else self.start_time + datetime.timedelta(days=7)
        schedulers = []
        current_time = self.start_time

        while current_time <= end_time:
            schedule_time = current_time
            minutes = schedule_time.minute
            if minutes % 15 != 0:
                # окргуляем до 15 минут
                round_minutes = 15 - minutes % 15
                schedule_time = schedule_time + datetime.timedelta(minutes=round_minutes) # прибавляем остаток от делений
            if 8 <= schedule_time.hour < 22:
                schedule = Schedule(
                    cure=self,
                    reminder_time=schedule_time
                )
                schedulers.append(schedule)
            current_time += datetime.timedelta(hours=self.frequency)
        
        Schedule.objects.bulk_create(schedulers) #создаем все объекты разом 


    class Meta:
        verbose_name = 'Лекарство'
        verbose_name_plural = 'Лекарства'

    def __str__(self):
        return f"{self.user} - {self.name}"
    

class Schedule(models.Model):
    """Расписание приемов"""
    cure = models.ForeignKey(
        Cure, 
        verbose_name='Лекарство',
        on_delete=models.CASCADE,
        related_name='schedule'
    )
    reminder_time = models.DateTimeField(verbose_name='Дата и время приема')
    # тут например можно реализовать флаг актуальности, но в этом нет необходиости, так как нет эндпоинта истории приемов

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'
        ordering = ['reminder_time']
    
    def __str__(self):
        return f"{self.cure} - {self.reminder_time}"
    



    







