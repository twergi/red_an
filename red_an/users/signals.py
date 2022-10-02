from django.contrib.auth.models import User
from .models import Profile
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user_id = instance
        Profile.objects.create(
            user_id=user_id,
        )


@receiver(post_save, sender=User)
def createToken(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(pre_delete, sender=User)
def deleteProfile(sender, instance, **kwargs):
    profile = Profile.objects.get(user_id=instance)
    profile.delete()


@receiver(pre_delete, sender=User)
def deleteToken(sender, instance, **kwargs):
    token = Token.objects.get(user_id=instance)
    token.delete()
