# Generated by Django 4.1 on 2022-09-06 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ribbon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('text', models.TextField(max_length=500)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('section_post_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ribbon.sectionpost')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
