from rest_framework import serializers
from authentication.serializers import UserSerializer
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'user',)
        read_only_fields = ('user',)
