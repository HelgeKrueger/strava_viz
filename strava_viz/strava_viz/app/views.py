from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from strava_viz.app.models import StravaConnectionInformation
from strava_viz.lib import Strava

import requests


@login_required
def index(request):
    return render(request, 'index.html')


def connect_to_strava(request):
    strava = Strava()
    context = {
        'strava_link': strava.build_authorize_url('http://localhost:8000/app/strava_reply')
    }
    return render(request, 'strava.html', context=context)


def strava_reply(request):
    code = request.GET['code']
    payload = {
        'client_id':  '4469',
        'client_secret': 'eb04c03b67cf447e1919fb833410133a8442c76b',
        'code': code,
        'grant_type': 'authorization_code'
    }

    response = requests.post('https://www.strava.com/api/v3/oauth/token', data=payload)

    parsed_response = response.json()
    athlete_id = parsed_response['athlete']['id']

    username = f'__strava__{athlete_id}'

    user, _ = User.objects.get_or_create(username=username)

    StravaConnectionInformation.objects.get_or_create(user=user)
    user.stravaconnectioninformation.access_token = parsed_response['access_token']
    user.stravaconnectioninformation.refresh_token = parsed_response['refresh_token']
    user.stravaconnectioninformation.save()

    login(request, user)

    return redirect('/app')
