"""Tests for timezone-aware datetime handling."""

from datetime import datetime, timezone, timedelta

from mock_clock import MockClock


class TestTimezoneSupport:
    """Test timezone-aware datetime objects."""

    def test_freeze_with_utc_timezone(self):
        clock = MockClock()
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock.freeze(frozen_dt)
        
        result = datetime.now(tz=timezone.utc)
        assert result == frozen_dt
        assert result.tzinfo == timezone.utc
        clock.reset()

    def test_freeze_with_custom_timezone(self):
        clock = MockClock()
        est = timezone(timedelta(hours=-5))
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=est)
        clock.freeze(frozen_dt)
        
        result = datetime.now(tz=est)
        assert result.hour == 12
        assert result.tzinfo == est
        clock.reset()

    def test_get_datetime_with_timezone_conversion(self):
        clock = MockClock()
        utc_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock.freeze(utc_dt)
        
        est = timezone(timedelta(hours=-5))
        result = clock.get_datetime(tz=est)
        
        assert result.hour == 7
        assert result.tzinfo == est
        clock.reset()

    def test_naive_datetime_handling(self):
        clock = MockClock()
        naive_dt = datetime(2024, 1, 15, 12, 0, 0)
        clock.freeze(naive_dt)
        
        result = datetime.now()
        assert result.year == 2024
        clock.reset()
