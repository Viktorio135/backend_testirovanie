from rest_framework import serializers

from .models import Cure, CustomUser, Schedule

class CureSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True, write_only=True) #поле для получения юзера

    class Meta:
        model = Cure
        fields = [
            "name",
            "user_id",
            "frequency",
            "duration"
        ]


    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        # получаем либо создаем пользователя
        user, created = CustomUser.objects.get_or_create(
            user_id=user_id,
            defaults={'user_id': user_id}
        )
        cure = Cure.objects.create(user=user, **validated_data)
        return cure

    
class ScheduleSerializer(serializers.ModelSerializer):
    reminder_time = serializers.DateTimeField(format="%d %B %Y %H:%M") #меняем формат времени для более удобного вида
    class Meta:
        model = Schedule
        fields = '__all__'
