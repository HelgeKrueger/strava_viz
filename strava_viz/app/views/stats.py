from datetime import date
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from strava_viz.app.models import StravaActivity


def strava_activity_to_dict(strava_activity):
    return {
        'activity_id': strava_activity.activity_id,
        'datetime': strava_activity.datetime,
        'moving_time': strava_activity.moving_time,
        'distance_km': strava_activity.distance_meter / 1000
    }


def year_month_string(my_date):
    return f'{my_date.year}-{my_date.month}'


def build_month_list():
    today = date.today()

    year = today.year
    month = today.month

    result = [f"{year}-{month}"]

    for j in range(1, 12):
        month -= 1
        if month == 0:
            year -= 1
            month = 12
        result.append(f"{year}-{month}")

    return result


def transform_month(activities, end_day=31):
    total_distance = 0
    total_time = 0
    result = [[0, 0, 0]]

    for j in range(1, end_day+1):
        for a in activities:
            if a['datetime'].day == j:
                total_distance += a['distance_km']
                total_time += a['moving_time']

        result.append([j, total_distance, total_time])

    return result


@login_required
def monthly_data(request):
    activities = StravaActivity.objects.filter(user=request.user)
    activities = map(strava_activity_to_dict, activities)

    activities_by_month = defaultdict(list)

    for activity in activities:
        key = year_month_string(activity['datetime'])
        activities_by_month[key].append(activity)

    month_list = build_month_list()
    current_month = activities_by_month[month_list[0]]

    return JsonResponse({
        'current_month': transform_month(current_month, end_day=date.today().day),
        'last_year': [transform_month(activities_by_month[m]) for m in month_list[1:]]
    })
