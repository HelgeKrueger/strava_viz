import os

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from strava_viz.app.models import StravaConnectionInformation, StravaActivity
from strava_viz.lib import Strava
from strava_viz.app.process import get_strava_activities_async


def connect_to_strava(request):
    redirect_uri = 'https://strava-viz.herokuapp.com/strava_reply'

    if os.environ['ENVIRONMENT'] == 'dev':
        redirect_uri = 'http://localhost:8000/strava_reply'

    strava = Strava()
    context = {
        'strava_link': strava.build_authorize_url(redirect_uri)
    }
    return render(request, 'strava.html', context=context)


def strava_reply(request):
    code = request.GET['code']

    strava = Strava()
    parsed_response = strava.initial_authorization(code)

    athlete_id = parsed_response['athlete']['id']

    username = f'__strava__{athlete_id}'

    user, _ = User.objects.get_or_create(username=username)

    StravaConnectionInformation.objects.get_or_create(user=user)
    user.stravaconnectioninformation.access_token = parsed_response['access_token']
    user.stravaconnectioninformation.refresh_token = parsed_response['refresh_token']
    user.stravaconnectioninformation.save()

    login(request, user)

    return redirect('/')


@login_required
def update_data(request):
    get_strava_activities_async(request.user.id)

    return JsonResponse({
        'scheduled': True
    })


@login_required
def delete_all(request):
    StravaActivity.objects.filter(user=request.user).delete()

    return JsonResponse({})
