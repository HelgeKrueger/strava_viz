from datetime import datetime, timezone

from django.test import TestCase
from django.contrib.auth.models import User
from strava_viz.app.models import StravaConnectionInformation, StravaActivity, ActivityType


class ActivityTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='fred')
        self.test_user.save()
        StravaConnectionInformation.objects.get_or_create(user=self.test_user)
        self.test_user.stravaconnectioninformation.save()

        self.client.force_login(self.test_user)

        self.activity_id = 1

    def create_activity(self, my_datetime=None, moving_time=12, distance_meter=1000, activity_type=ActivityType.RUN):
        if my_datetime is None:
            my_datetime = datetime.now(tz=timezone.utc)

        activity = StravaActivity.objects.create(
            user=self.test_user,
            datetime=my_datetime,
            activity_id=self.activity_id,
            moving_time=moving_time,
            distance_meter=distance_meter,
            activity_type=activity_type)

        self.activity_id += 1
        activity.save()
