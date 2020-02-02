from unittest.mock import patch

from . import Strava


def test_build_authorize_url():
    strava = Strava()

    url = strava.build_authorize_url('redirect_here')

    assert 'redirect_here' in url


@patch('requests.post')
def test_initial_authorization(mockClass):
    strava = Strava()

    strava.initial_authorization(123)

    assert mockClass.call_count == 1
    assert mockClass.call_args[1]['data']['code'] == 123
