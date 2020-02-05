from datetime import datetime

from django.urls import reverse
from django.test import TestCase

from django.contrib.auth.models import User

from strava_viz.app.models import StravaConnectionInformation, StravaActivity, ActivityType


class MonthlyDataTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='fred')
        self.test_user.save()
        StravaConnectionInformation.objects.get_or_create(user=self.test_user)
        self.test_user.stravaconnectioninformation.save()

        self.client.force_login(self.test_user)

        self.activity_id = 1

    def test_current_and_last_month_basic_call(self):
        response = self.client.get(reverse('current_and_last_month'))

        assert response.status_code == 200

        data = response.json()

        assert 'current_month' in data
        assert 'last_month' in data

    def create_activity(self, my_datetime=None, moving_time=12, distance_meter=1000, activity_type=ActivityType.RUN):
        if my_datetime is None:
            my_datetime = datetime.now()

        activity = StravaActivity.objects.create(
            user=self.test_user,
            datetime=my_datetime,
            activity_id=self.activity_id,
            moving_time=moving_time,
            distance_meter=distance_meter,
            activity_type=activity_type)

        self.activity_id += 1
        activity.save()

    def test_current_and_last_month_with_data(self):
        first_day_of_month = datetime.now().replace(day=1)
        self.create_activity(my_datetime=first_day_of_month, moving_time=3600, activity_type=ActivityType.RUN)

        response = self.client.get(reverse('current_and_last_month'))

        assert response.status_code == 200

        data = response.json()

        assert 'current_month' in data
        assert 'last_month' in data
