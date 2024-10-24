# models.py
from django.db import models
from django.contrib.auth.models import User

class SavedTimetable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # To identify different timetables
    batch = models.CharField(max_length=20)  # Morning/Afternoon
    timetable_data = models.JSONField()  # Store the timetable as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s timetable - {self.name}"