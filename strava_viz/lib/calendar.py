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
        rides = [a for a in activities if a['activity_type'] == 'ride']

        item = {
            'weekday': isoday-1,
            'week': isoweek-firstweek,
            'run_time': sum(a['moving_time'] for a in runs),
            'run_distance': sum(a['distance_km'] for a in runs),
            'ride_time': sum(a['moving_time'] for a in rides),
            'ride_distance': sum(a['distance_km'] for a in rides),
            'ids': [a['activity_id'] for a in activities]
        }

        result.append(item)

    return result


def aggregate_month(activities, end_day=31):
    total_distance = 0
    total_time = 0
    ride_distance = 0
    ride_time = 0
    run_distance = 0
    run_time = 0

    result = [{
        'day': 0,
        'total_distance': total_distance,
        'total_time': total_time,
        'ride_distance': ride_distance,
        'ride_time': ride_time,
        'run_distance': run_distance,
        'run_time': run_time
    }]

    for j in range(1, end_day+1):
        for a in activities:
            if a['datetime'].day == j:
                total_distance += a['distance_km']
                total_time += a['moving_time']

                if a['activity_type'] == 'run':
                    run_distance += a['distance_km']
                    run_time += a['moving_time']

                if a['activity_type'] == 'ride':
                    ride_distance += a['distance_km']
                    ride_time += a['moving_time']

        result.append({
            'day': j,
            'total_distance': total_distance,
            'total_time': total_time,
            'ride_distance': ride_distance,
            'ride_time': ride_time,
            'run_distance': run_distance,
            'run_time': run_time
        })

    return result
