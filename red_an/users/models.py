from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django_countries.fields import CountryField
import uuid
from PIL import Image
from ribbon.utils import square_crop


def defaultImage(imageType):
    if imageType == 'profile':
        return 'user/profile/default.png'
    else:
        return 'user/banner/default.png'


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=200, blank=True)
    country = CountryField(blank=True)
    drf_token = models.CharField(max_length=50, blank=True, null=True)
    rating = models.IntegerField(default=0)
    profile_image = models.ImageField(upload_to='user/profile/', blank=True, default=defaultImage('profile'))
    banner_image = models.ImageField(upload_to='user/banner/', blank=True, default=defaultImage('banner'))

    def __str__(self):
        return str(self.user_id)

    def save(self, **kwargs):
        super().save()

        if self.drf_token is None:
            self.drf_token = Token.objects.get(user=self.user_id).key
            self.save()

        if self.profile_image:
            square_crop(self.profile_image.path)

        else:
            self.profile_image = defaultImage('profile')
            self.save()

        if self.banner_image:
            banner = Image.open(self.banner_image.path)

            if banner.height > 360 or banner.width > 1200:
                output_size = (1200, 360)
                banner.thumbnail(output_size)
                banner.save(self.banner_image.path)
            banner.close()

        else:
            self.banner_image = defaultImage('banner')
            self.save()

    def update_token(self):
        self.drf_token = Token.objects.get(user=self.user_id).key
        self.save()

    def update_rating(self):
        posts = self.sectionpost_set.all()
        comments = self.comment_set.all()
        true_rating = 0

        rating_posts = posts.aggregate(Sum('rating'))['rating__sum']
        if rating_posts is not None:
            true_rating += rating_posts
        rating_comments = comments.aggregate(Sum('rating'))['rating__sum']
        if rating_comments is not None:
            true_rating += rating_comments
        self.rating = true_rating
        self.save()
