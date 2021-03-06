from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('strava', views.connect_to_strava, name='connect_to_strava'),
    path('strava_reply', views.strava_reply, name='strava_reply'),
    path('update_data', views.update_data, name="update_data"),
    path('delete_all', views.delete_all, name="delete_all"),
    path('api/monthly_data', views.monthly_data, name='stats_monthly_data'),
    path('api/activities', views.activities, name='api_activties'),
    path('api/polylines', views.polylines, name='api_polylines'),
    path('api/current_and_last_month', views.current_and_last_month, name='current_and_last_month'),
    path('api/activity/<int:id>', views.activity, name='api_activity')
]
