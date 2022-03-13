from rest_framework import serializers
from .models import Schedule, ScheduleType
from profiles.serializers import ProfileSerializer


class ScheduleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleType
        fields = ['name', 'start_time', 'end_time']


class ScheduleSerializer(serializers.ModelSerializer):
    sched_type = ScheduleTypeSerializer(read_only=True)
    employee = ProfileSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = ('sched_type', 'employee', 'is_active')