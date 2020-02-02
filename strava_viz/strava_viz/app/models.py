from django.db import models
from django.contrib.auth.models import User


class StravaConnectionInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=100)
