from django.urls import reverse
from django.test import TestCase


class ConnectToStravaTests(TestCase):
    def test_contains_url(self):
        response = self.client.get(reverse('connect_to_strava'))

        self.assertContains(response, 'https://www.strava.com/')
