from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .strava import connect_to_strava, strava_reply, update_data
from .stats import monthly_data, activities, polylines, current_and_last_month


@login_required
def index(request):
    return render(request, 'index.html')
