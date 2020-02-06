from datetime import date, datetime, time, timedelta, timezone
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from strava_viz.app.models import StravaActivity
from strava_viz.lib import transform_month, aggregate_month


def strava_activity_to_dict(strava_activity):
    return {
        'activity_id': strava_activity.activity_id,
        'datetime': strava_activity.datetime,
        'moving_time': strava_activity.moving_time / 3600,
        'distance_km': strava_activity.distance_meter / 1000,
        'activity_type': strava_activity.activity_type.value
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

    transformed = [aggregate_month(current_month, end_day=date.today().day)]
    transformed += [aggregate_month(activities_by_month[m]) for m in month_list[1:]]

    return JsonResponse({
        'currentMonth': transformed[0],
        'lastYear': transformed[1:]
    })


@login_required
def activities(request):
    activities = StravaActivity.objects.filter(user=request.user)
    activities = map(strava_activity_to_dict, activities)

    return JsonResponse(list(activities), safe=False)


@login_required
def polylines(request):
    activities = StravaActivity.objects.filter(user=request.user)
    today = date.today()
    this_year = [{
        'polyline': a.polyline,
        'activity_type': a.activity_type.value
    } for a in activities if a.datetime.year == today.year]

    return JsonResponse({
        'thisYear': this_year
    })


def date_to_utc_midnight(my_date):
    return datetime.combine(my_date, time(), tzinfo=timezone.utc)


@login_required
def current_and_last_month(request):
    print(timezone.utc)
    activities = StravaActivity.objects.filter(user=request.user)
    activities = list(map(strava_activity_to_dict, activities))

    first_month = date_to_utc_midnight(date.today().replace(day=1))
    first_last_month = date_to_utc_midnight((first_month - timedelta(days=5)).replace(day=1))

    current_month = [
        a for a in activities
        if a['datetime'] >= first_month]
    activities_last_month = [
        a for a in activities
        if a['datetime'] >= first_last_month and a['datetime'] < first_month]

    transformed_last_month = transform_month(activities_last_month)
    transformed_current_month = transform_month(current_month)
    transformed_current_month = transformed_current_month[:(datetime.now().day)]

    return JsonResponse({
        'current_month': transformed_current_month,
        'last_month': transformed_last_month
    })
