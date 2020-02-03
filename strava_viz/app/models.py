from enum import Enum

from django.db import models
from django.contrib.auth.models import User
from django_enum_choices.fields import EnumChoiceField


class StravaConnectionInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=100)


class ActivityType(Enum):
    RUN = 'run'
    RIDE = 'ride'


class StravaActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    distance_meter = models.FloatField()
    moving_time = models.FloatField()
    activity_id = models.BigIntegerField()
    datetime = models.DateTimeField()
    activity_type = EnumChoiceField(ActivityType, default=ActivityType.RUN)
