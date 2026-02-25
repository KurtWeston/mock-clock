"""Tests for MockClock core functionality."""

import time
from datetime import datetime, timedelta, timezone

import pytest

from mock_clock import MockClock, freeze_time


class TestMockClockFreeze:
    """Test freezing time at specific points."""

    def test_freeze_with_datetime(self):
        clock = MockClock()
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock.freeze(frozen_dt)
        
        assert datetime.now() == frozen_dt
        time.sleep(0.01)
        assert datetime.now() == frozen_dt
        clock.reset()

    def test_freeze_with_timestamp(self):
        clock = MockClock()
        timestamp = 1705320000.0
        clock.freeze(timestamp)
        
        assert abs(time.time() - timestamp) < 0.001
        clock.reset()

    def test_freeze_with_iso_string(self):
        clock = MockClock()
        clock.freeze("2024-01-15T12:00:00+00:00")
        
        result = datetime.now()
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15
        clock.reset()


class TestMockClockAdvance:
    """Test advancing time forward."""

    def test_advance_seconds(self):
        clock = MockClock()
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock.freeze(frozen_dt)
        
        clock.advance(seconds=30)
        expected = frozen_dt + timedelta(seconds=30)
        assert datetime.now() == expected
        clock.reset()

    def test_advance_multiple_units(self):
        clock = MockClock()
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock.freeze(frozen_dt)
        
        clock.advance(days=1, hours=2, minutes=30, seconds=45)
        expected = frozen_dt + timedelta(days=1, hours=2, minutes=30, seconds=45)
        assert datetime.now() == expected
        clock.reset()

    def test_advance_chainable(self):
        clock = MockClock()
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        result = clock.freeze(frozen_dt).advance(hours=1).advance(minutes=30)
        
        assert result is clock
        expected = frozen_dt + timedelta(hours=1, minutes=30)
        assert datetime.now() == expected
        clock.reset()


class TestMockClockRewind:
    """Test rewinding time backward."""

    def test_rewind_seconds(self):
        clock = MockClock()
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock.freeze(frozen_dt)
        
        clock.rewind(seconds=30)
        expected = frozen_dt - timedelta(seconds=30)
        assert datetime.now() == expected
        clock.reset()

    def test_rewind_days(self):
        clock = MockClock()
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock.freeze(frozen_dt)
        
        clock.rewind(days=5)
        expected = frozen_dt - timedelta(days=5)
        assert datetime.now() == expected
        clock.reset()


class TestMockClockReset:
    """Test resetting to real time."""

    def test_reset_restores_real_time(self):
        clock = MockClock()
        clock.freeze(datetime(2020, 1, 1, tzinfo=timezone.utc))
        
        before_reset = time.time()
        clock.reset()
        after_reset = time.time()
        
        assert after_reset > 1700000000
        assert after_reset >= before_reset

    def test_reset_is_chainable(self):
        clock = MockClock()
        result = clock.freeze(datetime(2020, 1, 1, tzinfo=timezone.utc)).reset()
        assert result is clock


class TestFreezeTimeContext:
    """Test freeze_time context manager."""

    def test_context_manager_freezes_time(self):
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        
        with freeze_time(frozen_dt) as clock:
            assert datetime.now() == frozen_dt
            clock.advance(hours=1)
            assert datetime.now() == frozen_dt + timedelta(hours=1)
        
        assert datetime.now().year >= 2024

    def test_context_manager_restores_on_exception(self):
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        
        with pytest.raises(ValueError):
            with freeze_time(frozen_dt):
                raise ValueError("test error")
        
        assert datetime.now().year >= 2024


class TestTimePatching:
    """Test that all time functions are patched."""

    def test_datetime_now_patched(self):
        clock = MockClock()
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock.freeze(frozen_dt)
        
        assert datetime.now() == frozen_dt
        clock.reset()

    def test_datetime_utcnow_patched(self):
        clock = MockClock()
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock.freeze(frozen_dt)
        
        result = datetime.utcnow()
        assert result.year == 2024
        assert result.tzinfo is None
        clock.reset()

    def test_time_time_patched(self):
        clock = MockClock()
        timestamp = 1705320000.0
        clock.freeze(timestamp)
        
        assert abs(time.time() - timestamp) < 0.001
        clock.reset()

    def test_time_monotonic_patched(self):
        clock = MockClock()
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock.freeze(frozen_dt)
        
        mono1 = time.monotonic()
        clock.advance(seconds=5)
        mono2 = time.monotonic()
        
        assert mono2 > mono1
        clock.reset()
