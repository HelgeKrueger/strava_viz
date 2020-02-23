# Visualization of strava statistics

Retrieves data from strava and stores it locally, by default in an sqlite3 database. Then offers various graphs displaying the data.

A sample production deployment is available at https://strava-viz.herokuapp.com/

## Development

Set the environment variables

```
STRAVA_CLIENT_ID=${YOUR_STRAVA_CLIENT_ID}
STRAVA_CLIENT_SECRET=${YOUR_STRAVA_CLIENT_SECRET}
ENVIRONMENT=dev
```

These can be obtained on https://www.strava.com/settings/api

Then run

```
./dev
```
