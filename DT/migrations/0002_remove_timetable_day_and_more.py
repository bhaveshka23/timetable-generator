# Generated by Django 5.1.1 on 2024-10-16 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DT', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetable',
            name='day',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='lecture_or_practical',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='time_slot',
        ),
        migrations.AddField(
            model_name='timetable',
            name='timetable_data',
            field=models.JSONField(default={}),
        ),
    ]
