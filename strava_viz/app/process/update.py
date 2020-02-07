from django.contrib.auth.models import User
from multiprocessing import Process

from strava_viz.lib import Strava
from strava_viz.app.models import StravaActivity, ActivityType


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


def get_strava_activities_async(user_id):
    process = Process(target=get_strava_activities, args=(user_id,))
    process.start()


def get_strava_activities(user_id):
    current_user = User.objects.get(pk=user_id)
    print("Starting background task")

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

    current_page = 0

    while len(result) > 0:
        print(f"Processing page {current_page}")
        for activity in result:
            if not insert_strava_activity(current_user, activity):
                return

        current_page += 1
        result = strava.get_activities(page=current_page)
