from calendar import monthrange


def transform_month(data):
    if len(data) == 0:
        return []

    first_day = data[0]['datetime'].date().replace(day=1)
    _, firstweek, _ = first_day.isocalendar()
    days_in_month = monthrange(first_day.year, first_day.month)[1]

    result = []
    for j in range(1, days_in_month+1):
        current_day = first_day.replace(day=j)
        isoyear, isoweek, isoday = current_day.isocalendar()

        activities = [d for d in data if d['datetime'].date() == current_day]
        runs = [a for a in activities if a['activity_type'] == 'run']
        rides = [a for a in activities if a['activity_type'] == 'rides']

        item = {
            'weekday': isoday-1,
            'week': isoweek-firstweek,
            'run_time': sum(a['moving_time'] for a in runs),
            'run_distance': sum(a['distance_km'] for a in runs),
            'ride_time': sum(a['moving_time'] for a in rides),
            'ride_distance': sum(a['distance_km'] for a in rides),
        }

        result.append(item)

    return result
