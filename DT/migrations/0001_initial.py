# Generated by Django 5.1.1 on 2024-10-14 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch', models.CharField(max_length=100)),
                ('day', models.CharField(max_length=10)),
                ('time_slot', models.CharField(max_length=20)),
                ('lecture_or_practical', models.CharField(max_length=200)),
            ],
        ),
    ]
