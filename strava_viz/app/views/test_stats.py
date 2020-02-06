from datetime import datetime
from django.urls import reverse

from strava_viz.app.models import ActivityType
from strava_viz.app.tests import ActivityTestCase


class MonthlyDataTests(ActivityTestCase):
    def test_current_and_last_month_basic_call(self):
        response = self.client.get(reverse('current_and_last_month'))

        assert response.status_code == 200

        data = response.json()

        assert 'current_month' in data
        assert 'last_month' in data

    def test_current_and_last_month_with_data(self):
        first_day_of_month = datetime.utcnow().replace(day=1)
        self.create_activity(my_datetime=first_day_of_month, moving_time=3600, activity_type=ActivityType.RUN)

        response = self.client.get(reverse('current_and_last_month'))

        assert response.status_code == 200

        data = response.json()

        assert 'current_month' in data
        assert 'last_month' in data

        assert len(data['current_month']) == datetime.now().day
