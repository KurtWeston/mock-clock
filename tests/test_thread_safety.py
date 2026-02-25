"""Tests for thread-safe time manipulation."""

import threading
import time
from datetime import datetime, timezone

from mock_clock import MockClock


class TestThreadSafety:
    """Test concurrent access to MockClock."""

    def test_concurrent_advance(self):
        clock = MockClock()
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock.freeze(frozen_dt)
        
        results = []
        
        def advance_time():
            for _ in range(10):
                clock.advance(seconds=1)
                results.append(clock.get_time())
        
        threads = [threading.Thread(target=advance_time) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(results) == 30
        clock.reset()

    def test_concurrent_freeze_and_read(self):
        clock = MockClock()
        errors = []
        
        def freeze_and_read():
            try:
                clock.freeze(datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc))
                time.sleep(0.001)
                _ = clock.get_time()
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=freeze_and_read) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0
        clock.reset()

    def test_lock_prevents_race_conditions(self):
        clock = MockClock()
        frozen_dt = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock.freeze(frozen_dt)
        
        timestamps = []
        
        def read_time():
            for _ in range(100):
                timestamps.append(clock.get_time())
        
        threads = [threading.Thread(target=read_time) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert all(isinstance(ts, float) for ts in timestamps)
        clock.reset()
