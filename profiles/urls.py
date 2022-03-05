from django.urls import path
from .views import (
    UserProfileListView,
    UserProfileUpdateView
)

urlpatterns = [
    path('', UserProfileListView.as_view(), name='profiles'),
    path('update', UserProfileUpdateView.as_view(), name='update-view')
]