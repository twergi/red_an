from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
import uuid
from colorfield.fields import ColorField
from PIL import Image


def section_image_path(instance, filename):
    return f'section/{instance.title}/image/{filename}'


def section_banner_path(instance, filename):
    return f'section/{instance.title}/banner/{filename}'


class Section(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=50, unique=True)
    short_description = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to=section_image_path)
    banner = models.ImageField(upload_to=section_banner_path, blank=True)
    banner_color = ColorField()
    subscribers = models.ManyToManyField(User, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        img.close()


def sectionpost_path(instance, filename):
    return f'section/{instance.section_id.title}/{instance.id}/{filename}'


class SectionPost(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to=sectionpost_path, null=True, blank=True)
    content = models.TextField(max_length=4000, blank=True)
    date_published = models.DateField(auto_now_add=True)

    class Meta():
        ordering = ['-rating']

    def __str__(self):
        return str(self.title)


class SectionStaff(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    section_id = models.OneToOneField(Section, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    moderators = models.ManyToManyField(User)

    def __str__(self):
        return str(self.section_id.title)


class Comments(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    section_post_id = models.ForeignKey(SectionPost, null=True, on_delete=models.SET_NULL)
    text = models.TextField(max_length=500)
    rating = models.IntegerField(default=0, editable=False)
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id.username} on {self.section_post_id.title}'
