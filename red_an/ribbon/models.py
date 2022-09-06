from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
import uuid
from PIL import Image


def section_path(instance, filename):
    return f'section/{instance.id}/{filename}'


class Section(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to=section_path)
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
    return f'post/{instance.id}/{filename}'


class SectionPost(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to=sectionpost_path, null=True, blank=True)
    content = models.TextField(max_length=2000, blank=True)
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
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id.username} on {self.section_post_id.title}'
