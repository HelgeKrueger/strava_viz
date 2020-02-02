from django.test import TestCase
from django.urls import reverse


class ConnectToStravaTests(TestCase):
    def test_contains_url(self):
        response = self.client.get(reverse('connect_to_strava'))

        self.assertContains(response, 'https://www.strava.com/')
