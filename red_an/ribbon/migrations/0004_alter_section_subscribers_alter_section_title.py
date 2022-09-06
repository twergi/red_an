# Generated by Django 4.1 on 2022-09-06 09:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ribbon', '0003_section_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='subscribers',
            field=models.ManyToManyField(editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='section',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
