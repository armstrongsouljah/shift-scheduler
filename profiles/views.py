from django.shortcuts import get_object_or_404, render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, UpdateAPIView
from .serializers import ProfileSerializer, ProfileUpdateSerializer
from .models import Profile

# Create your views here.
class UserProfileListView(ListAPIView):
    """ List User profiles on the platform """
    permission_classes = (IsAuthenticated, )
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserProfileUpdateView(UpdateAPIView):
    """ Updates profile details """
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

