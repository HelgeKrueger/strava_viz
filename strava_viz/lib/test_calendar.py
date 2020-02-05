from datetime import datetime
from .calendar import transform_month


def test_transform_month_handles_empty_data():
    assert len(transform_month([])) == 0


def test_transform_month():
    data = [
        {
            'datetime': datetime(2020, 1, 5),
            'activity_type': 'run',
            'moving_time': 0.5,
            'distance_km': 5
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
