from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from .serializers import ScheduleSerializer, ScheduleTypeSerializer
from .models import Schedule, ScheduleType

# Create your views here.

class ScheduleList(ListAPIView):
    queryset = Schedule.objects.filter(is_active=True)
    permission_classes = []
    serializer_class = ScheduleSerializer

class ScheduleAddView(CreateAPIView):
    queryset = Schedule.objects.filter(is_active=True)
    serializer_class = ScheduleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class ScheduleUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Schedule.objects.filter(is_active=True)
    serializer_class = ScheduleSerializer


class SchedTypeView(CreateAPIView):
    queryset = ScheduleType.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = ScheduleTypeSerializer
