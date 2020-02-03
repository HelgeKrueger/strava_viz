from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import StravaConnectionInformation, StravaActivity


class ConnectToStravaTests(TestCase):
    def test_contains_url(self):
        response = self.client.get(reverse('connect_to_strava'))

        self.assertContains(response, 'https://www.strava.com/')


def create_activity(id='1234'):
    return {
        'id': id,
        'name': 'test_activity',
        'type': 'ride',
        'start_date': '2020-02-03 14:13:30Z',
        'distance': 1,
        'moving_time': 2,
        'average_heartrate': 3,
        'average_speed': 4,
        'map': {
                'summary_polyline': 'abc'
        }
    }


class UpdateDataTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='fred')
        self.test_user.save()
        StravaConnectionInformation.objects.get_or_create(user=self.test_user)
        self.test_user.stravaconnectioninformation.save()

        self.client.force_login(self.test_user)

    @patch('strava_viz.lib.Strava.get_activities', return_value=[])
    def test_insert_nothing_to_insert(self, getActivitiesMock):
        response = self.client.get(reverse('update_data'))

        self.assertEqual(response.json()['insert_count'], 0)

    @patch('strava_viz.lib.Strava.get_activities')
    def test_insert_insert_one_entry(self, getActivitiesMock):
        getActivitiesMock.return_value = [
            create_activity()
        ]

        response = self.client.get(reverse('update_data'))

        self.assertEqual(response.json()['insert_count'], 1)

    @patch('strava_viz.lib.Strava.get_activities')
    def test_insert_insert_one_entry_already_exists(self, getActivitiesMock):
        activity_id = 1235
        getActivitiesMock.return_value = [
            create_activity(activity_id)
        ]

        StravaActivity.objects.create(activity_id=activity_id, user=self.test_user).save()

        response = self.client.get(reverse('update_data'))

        self.assertEqual(response.json()['insert_count'], 0)
