from enum import Enum

from django.db import models
from django_enum_choices.fields import EnumChoiceField


class ActivityType(Enum):
    RUN = 'run'
    RIDE = 'ride'


class StravaActivity(models.Model):
    distance_meter = models.FloatField()
    datetime = models.DateTimeField()
    activity_type = EnumChoiceField(ActivityType, default=ActivityType.RUN)
