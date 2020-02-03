import os
from urllib.parse import urlencode
import requests


class Strava:
    def __init__(self):
        self.client_id = os.environ['STRAVA_CLIENT_ID']
        self.client_secret = os.environ['STRAVA_CLIENT_SECRET']

        self.access_token = None
        self.refresh_token = None

    def build_authorize_url(self, redirect_url):
        strava_base_url = ' https://www.strava.com/oauth/authorize?'
        strava_params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_url,
            'response_type': 'code',
            'approval_prompt': 'auto',
            'scope': 'read'
        }

        return strava_base_url + urlencode(strava_params)

    def initial_authorization(self, code):
        payload = {
            'client_id':  self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code'
        }

        response = requests.post('https://www.strava.com/api/v3/oauth/token', data=payload)

        return response.json()

    def set_tokens(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token

    def request_new_access_token(self):
        payload = {
            'client_id':  self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        response = requests.post('https://www.strava.com/api/v3/oauth/token', data=payload)

        self.access_token = response.json()['access_token']

    def get_athlete(self):
        response = requests.get("https://www.strava.com/api/v3/athlete", headers=self.get_headers())

        if response.status_code != 200:
            raise Exception("Need to update token")

        return response.json()

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}'
        }
