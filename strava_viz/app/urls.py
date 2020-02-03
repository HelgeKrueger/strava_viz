from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('strava', views.connect_to_strava, name='connect_to_strava'),
    path('strava_reply', views.strava_reply, name='strava_reply'),
    path('update_data', views.update_data, name="update_data")
]
