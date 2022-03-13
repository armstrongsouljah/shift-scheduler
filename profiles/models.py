from django.db import models
from authentication.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='user_profile')

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'


@receiver(post_save, sender=User)
def user_signup_receiver(instance, created, *args, **kwargs):
    """
    Automatically creates a profile instance for each user that signs up.
    """
    if created:
        Profile.objects.get_or_create(user=instance)
