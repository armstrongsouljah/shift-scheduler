from django.urls import path
from .views import *

urlpatterns = [
    path('', ScheduleList.as_view(), name='schedule-list'),
    path('new/', ScheduleAddView.as_view(), name='add-schedule'),
    path('<pk>/udate', ScheduleUpdateView.as_view(), name='change-it'),
    path('new/sched-type/', SchedTypeView.as_view(), name='add-sched-type')
]