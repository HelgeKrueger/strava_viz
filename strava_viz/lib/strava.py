import os
from urllib.parse import urlencode


class Strava:
    def __init__(self):
        self.client_id = os.environ['STRAVA_CLIENT_ID']

    def build_authorize_url(self, redirect_url):
        strava_base_url = ' https://www.strava.com/oauth/authorize?'
        strava_params = {
            'client_id': '4469',
            'redirect_uri': redirect_url,
            'response_type': 'code',
            'approval_prompt': 'auto',
            'scope': 'read'
        }

        return strava_base_url + urlencode(strava_params)
