from . import Strava


def test_build_authorize_url():
    strava = Strava()

    url = strava.build_authorize_url('redirect_here')

    assert 'redirect_here' in url
