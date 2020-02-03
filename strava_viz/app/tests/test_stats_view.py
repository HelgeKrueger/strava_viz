from datetime import date, datetime, timedelta
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from strava_viz.app.models import StravaConnectionInformation, StravaActivity


class MonthlyDataTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='fred')
        self.test_user.save()
        StravaConnectionInformation.objects.get_or_create(user=self.test_user)
        self.test_user.stravaconnectioninformation.save()

        self.client.force_login(self.test_user)

        self.activity_id = 1

    def create_activity(self, my_datetime=None, moving_time=12, distance_meter=1000):
        if my_datetime is None:
            my_datetime = datetime.now()

        activity = StravaActivity.objects.create(
            user=self.test_user,
            datetime=my_datetime,
            activity_id=self.activity_id,
            moving_time=moving_time,
            distance_meter=distance_meter)

        self.activity_id += 1
        activity.save()

    def test_gets_empty_response(self):
        response = self.client.get(reverse('stats_monthly_data'))

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['currentMonth'][-1], [date.today().day, 0, 0])

    def test_gets_response(self):
        self.create_activity(moving_time=12*3600)

        response = self.client.get(reverse('stats_monthly_data'))

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['currentMonth'][-1][2], 12)

    def test_gets_last_month(self):
        now = datetime.now()
        start_of_month = now.replace(day=1)
        start_of_last_month = (start_of_month - timedelta(days=20)).replace(day=1)

        self.create_activity(my_datetime=start_of_last_month, moving_time=3600, distance_meter=2000)

        response = self.client.get(reverse('stats_monthly_data'))

        self.assertEqual(response.status_code, 200)

        data = response.json()

        last_month = data['lastYear'][0]
        self.assertEqual(len(last_month), 32)
        self.assertEquals(last_month[1], [1, 2, 1])
        self.assertEquals(last_month[-1], [31, 2, 1])
