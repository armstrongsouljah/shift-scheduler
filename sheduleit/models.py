from django.db import models
from django.contrib.auth import get_user_model

from profiles.models import Profile

User = get_user_model()

SCHEDULE_TYPES = (
    ('EARLY_RISER', 'EARLY_RISER'),
    ('REGULAR', 'REGULAR'),
    ('LATE_NIGHT', 'LATE_NIGHT')
)

SCHEDULE_TIMES = (
    ('EARLY_START', '00:00:00'),
    ('EARLY_END', '08:00:00'),
    ('REGULAR_START', '08:00:00'),
    ('REGULAR_END', '16:00:00'),
    ('LATE_START', '16:00:00'),
    ('LATE_END', '23:59:00')
)

# Create your models here.
class ScheduleType(models.Model):
    """Desclares the type of the schedule an employee belongs too"""

    name = models.CharField(max_length=255,
           choices=SCHEDULE_TYPES, default=SCHEDULE_TYPES[0])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    start_time = models.TimeField(choices=SCHEDULE_TIMES)
    end_time = models.TimeField(choices=SCHEDULE_TIMES)

    def __str__(self):
        return F'{self.name}'


class Schedule(models.Model):
    """Holds details about a particular schedule and who belongs to it!"""
    sched_type = models.ForeignKey(ScheduleType,
                 on_delete=models.CASCADE,
                 related_name='employee_schedules')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return F"{self.employee.first_name} {self.employee.last_name} Schedule."