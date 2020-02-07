from django.urls import reverse
from unittest.mock import patch

from strava_viz.app.tests import ActivityTestCase
# from strava_viz.app.models import StravaActivity


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


class StravaViewTests(ActivityTestCase):
    def test_delete_all(self):
        response = self.client.get(reverse('delete_all'))

        assert response.status_code == 200

    @patch('strava_viz.lib.Strava.get_activities', return_value=[])
    def test_insert_nothing_to_insert(self, getActivitiesMock):
        response = self.client.get(reverse('update_data'))
        assert response.status_code == 200
#
#  TODO: Migrate to background task
#
    # @patch('strava_viz.lib.Strava.get_activities')
    # def test_insert_insert_one_entry(self, getActivitiesMock):
    #     getActivitiesMock.return_value = [
    #         create_activity()
    #     ]

    #     response = self.client.get(reverse('update_data'))

    #     self.assertEqual(response.json()['insert_count'], 1)

    # @patch('strava_viz.lib.Strava.get_activities')
    # def test_insert_insert_one_entry_already_exists(self, getActivitiesMock):
    #     activity_id = 1235
    #     getActivitiesMock.return_value = [
    #         create_activity(activity_id)
    #     ]

    #     StravaActivity.objects.create(activity_id=activity_id, user=self.test_user).save()

    #     response = self.client.get(reverse('update_data'))

    #     self.assertEqual(response.json()['insert_count'], 0)
