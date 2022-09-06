from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user_id = instance
        Profile.objects.create(
            user_id=user_id,
        )
    print('User has been created')
# @receiver(post_save, sender=User)
