from django.contrib.auth.models import User
from ribbon.models import PostReview, CommentReview
from .models import Profile
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user_id = instance
        Token.objects.create(user=user_id)
        Profile.objects.create(
            user_id=user_id,
        )


@receiver(pre_delete, sender=User)
def deleteProfile(sender, instance, **kwargs):
    profile = Profile.objects.get(user_id=instance)
    profile.delete()


@receiver(pre_delete, sender=User)
def deleteToken(sender, instance, **kwargs):
    token = Token.objects.get(user_id=instance)
    token.delete()


@receiver(pre_delete, sender=User)
def deleteVotes(sender, instance, **kwargs):
    comment_reviews = CommentReview.objects.filter(owner=instance)
    if comment_reviews is not None:
        for comment_review in comment_reviews:
            comment = comment_review.comment
            comment_review.delete()
            comment.update_rating()

    post_reviews = PostReview.objects.filter(owner=instance)
    if post_reviews is not None:
        for post_review in post_reviews:
            post = post_review.post
            post_review.delete()
            post.update_rating()
