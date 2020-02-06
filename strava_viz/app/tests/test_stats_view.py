from datetime import date, datetime, timedelta
from django.urls import reverse

from strava_viz.app.tests import ActivityTestCase


class MonthlyDataTests(ActivityTestCase):
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
