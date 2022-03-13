from django.contrib import admin
from .models import Schedule, ScheduleType

# Register your models here.
admin.site.register(ScheduleType)
admin.site.register(Schedule)