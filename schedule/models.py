from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
  TYPES = (
      (0, 'rehearsal'),
      (1, 'gig'),
  )

  name = models.CharField(max_length=255, blank=True, null=True)
  event_type = models.IntegerField(choices=TYPES)
  location = models.TextField(blank=True, null=True)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField(blank=True, null=True)

class Attendance(models.Model):
  user = models.ForeignKey(User)
  event = models.ForeignKey(Event)
  can_attend = models.BooleanField()

