from datetime import date, datetime, timedelta
from django.urls import reverse

from strava_viz.app.tests import ActivityTestCase


class MonthlyDataTests(ActivityTestCase):
    def test_gets_empty_response(self):
        response = self.client.get(reverse('stats_monthly_data'))

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['currentMonth'][-1], {
            'day': date.today().day,
            'total_distance': 0,
            'total_time': 0,
            'ride_distance': 0,
            'ride_time': 0,
            'run_distance': 0,
            'run_time': 0
        })

    def test_gets_response(self):
        self.create_activity(moving_time=12*3600)

        response = self.client.get(reverse('stats_monthly_data'))

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['currentMonth'][-1]['total_time'], 12)

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
        self.assertEqual(last_month[1], {
            'day': 1,
            'total_distance': 2,
            'total_time': 1,
            'ride_distance': 0,
            'ride_time': 0,
            'run_distance': 2,
            'run_time': 1
        })
        self.assertEqual(last_month[-1], {
            'day': 31,
            'total_distance': 2,
            'total_time': 1,
            'ride_distance': 0,
            'ride_time': 0,
            'run_distance': 2,
            'run_time': 1
        })
