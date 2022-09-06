from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import uuid
from PIL import Image


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=200, blank=True)
    country = CountryField(blank=True)
    rating = models.IntegerField(default=0)
    profile_image = models.ImageField(upload_to='profile/', blank=True, default='profile/default.png')
    banner_image = models.ImageField(upload_to='banner/', blank=True, default='banner/default.png')

    def __str__(self):
        return str(self.user_id)

    def save(self, **kwargs):
        super().save()

        if self.profile_image:
            img = Image.open(self.profile_image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)
            img.close()

        else:
            self.profile_image = 'profile/default.png'
            self.save()

        if self.banner_image:
            banner = Image.open(self.banner_image.path)

            if banner.height > 360 or banner.width > 1200:
                output_size = (1200, 360)
                banner.thumbnail(output_size)
                banner.save(self.banner_image.path)
            banner.close()

        else:
            self.banner_image = 'banner/default.png'
            self.save()


# class Comments(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
#     user_id = models.OneToOneField(User, on_delete=models.CASCADE)
