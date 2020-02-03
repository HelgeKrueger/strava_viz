from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import StravaConnectionInformation, StravaActivity, ActivityType
from strava_viz.lib import Strava


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

    return redirect('/app')


@login_required
def update_data(request):
    current_user = request.user
    sci = current_user.stravaconnectioninformation

    strava = Strava()
    strava.set_tokens(sci.access_token, sci.refresh_token)

    try:
        result = strava.get_activities()
    except Exception:
        strava.request_new_access_token()
        current_user.stravaconnectioninformation.refresh_token = strava.refresh_token
        current_user.stravaconnectioninformation.save()

        result = strava.get_activities()

    insert_count = 0
    current_page = 0

    while len(result) > 0:
        for activity in result:
            if insert_strava_activity(current_user, activity):
                insert_count += 1
            else:
                return JsonResponse({
                    'insert_count': insert_count
                })

        current_page += 1
        result = strava.get_activities(page=current_page)

    return JsonResponse({
        'insert_count': insert_count
    })


def insert_strava_activity(user, activity):
    activity_id = activity['id']

    if StravaActivity.objects.filter(activity_id=activity_id):
        return False

    activity_type = ActivityType(activity['type'].lower())

    polyline = activity['map']['summary_polyline']
    if not polyline:
        polyline = ""

    activity = StravaActivity.objects.create(
        user=user,
        name=activity['name'],
        datetime=activity['start_date'],
        activity_type=activity_type,
        activity_id=activity_id,
        distance_meter=activity['distance'],
        moving_time=activity['moving_time'],
        average_heartrate=activity.get('average_heartrate', 0),
        average_speed=activity.get('average_speed', 0),
        polyline=polyline
    )
    activity.save()

    return True
