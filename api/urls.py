from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'api'

urlpatterns = [
    path('schedule/', CreateOrGetScheduleView.as_view()),
    path("schedules/", UserScheduleView.as_view()),
    path("next_taking/", NextTakkingView.as_view()),
]
