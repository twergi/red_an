# Generated by Django 4.1 on 2022-09-06 10:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ribbon', '0004_alter_section_subscribers_alter_section_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sectionpost',
            options={'ordering': ['-rating']},
        ),
        migrations.AddField(
            model_name='sectionpost',
            name='date_published',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sectionpost',
            name='content',
            field=models.TextField(blank=True, max_length=2000),
        ),
    ]