from lib import Strava
import requests
import sys

from datetime import datetime
from dateutil.parser import parse


strava = Strava()
api_url = "http://localhost:8000/strava-activity/"

response = requests.get(api_url).json()
last_activity_date = parse(response[0]['datetime'])

print("Last activity date", last_activity_date)

for page in range(1, 100):
    activities = strava.retrieve_activities(page=page)

    if len(activities) == 0:
        print(f"Ending on page {page}")
        break

    for activity in activities:
        activity_date = parse(activity['start_date_local'])

        if activity_date <= last_activity_date:
            print("Old activity")
            sys.exit(0)

        payload = {
            'activity_type': activity['type'].lower(),
            'distance_meter': activity["distance"],
            'datetime': activity['start_date_local'],
        }

        response = requests.post(api_url, data=payload)
        print(payload['datetime'], response.status_code)
