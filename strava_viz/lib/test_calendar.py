from datetime import datetime
from .calendar import transform_month, aggregate_month


def test_transform_month_handles_empty_data():
    assert len(transform_month([])) == 0


def test_transform_month():
    data = [
        {
            'datetime': datetime(2020, 1, 5),
            'activity_type': 'run',
            'moving_time': 0.5,
            'distance_km': 5,
            'activity_id': 12
        }
    ]

    result = transform_month(data)

    assert len(result) == 31
    assert result[4]['weekday'] == 6
    assert result[4]['week'] == 0
    assert result[4]['run_time'] == 0.5

    for j in range(31):
        assert 'run_time' in result[j]
        assert 'run_distance' in result[j]
        assert 'ride_time' in result[j]
        assert 'ride_distance' in result[j]


def test_aggregate_month_empty_dataset():
    result = aggregate_month([])
    result_10 = aggregate_month([], end_day=10)

    assert len(result) == 32
    assert len(result_10) == 11


def test_aggregate_month_one_ride_one_run():
    data = [
        {
            'datetime': datetime(2020, 1, 5),
            'activity_type': 'run',
            'moving_time': 0.5,
            'distance_km': 5
        },
        {
            'datetime': datetime(2020, 1, 10),
            'activity_type': 'ride',
            'moving_time': 2,
            'distance_km': 50
        }
    ]
    result = aggregate_month(data)
    assert result[-1] == {
        'day': 31,
        'total_distance': 55,
        'total_time': 2.5,
        'ride_distance': 50,
        'ride_time': 2,
        'run_distance': 5,
        'run_time': 0.5
    }
