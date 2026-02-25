"""Core time manipulation functionality."""

import threading
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from typing import Optional, Union

from mock_clock.patches import TimePatcher


class MockClock:
    """Controls time for testing by intercepting system calls."""

    def __init__(self):
        self._frozen_time: Optional[datetime] = None
        self._offset: float = 0.0
        self._lock = threading.RLock()
        self._patcher = TimePatcher(self)
        self._active = False

    def freeze(self, dt: Union[datetime, float, str]) -> "MockClock":
        """Freeze time at specific datetime or timestamp."""
        with self._lock:
            if isinstance(dt, str):
                dt = datetime.fromisoformat(dt)
            elif isinstance(dt, (int, float)):
                dt = datetime.fromtimestamp(dt, tz=timezone.utc)

            self._frozen_time = dt
            if not self._active:
                self._patcher.start()
                self._active = True
            return self

    def advance(self, seconds: float = 0, minutes: float = 0, hours: float = 0, days: float = 0) -> "MockClock":
        """Move time forward."""
        total_seconds = seconds + (minutes * 60) + (hours * 3600) + (days * 86400)
        with self._lock:
            if self._frozen_time:
                self._frozen_time += timedelta(seconds=total_seconds)
            else:
                self._offset += total_seconds
            return self

    def rewind(self, seconds: float = 0, minutes: float = 0, hours: float = 0, days: float = 0) -> "MockClock":
        """Move time backward."""
        total_seconds = seconds + (minutes * 60) + (hours * 3600) + (days * 86400)
        return self.advance(seconds=-total_seconds)

    def reset(self) -> "MockClock":
        """Restore real system time."""
        with self._lock:
            self._frozen_time = None
            self._offset = 0.0
            if self._active:
                self._patcher.stop()
                self._active = False
            return self

    def get_time(self) -> float:
        """Get current mocked timestamp."""
        with self._lock:
            if self._frozen_time:
                return self._frozen_time.timestamp()
            return self._patcher.real_time() + self._offset

    def get_datetime(self, tz=None) -> datetime:
        """Get current mocked datetime."""
        with self._lock:
            if self._frozen_time:
                if tz and self._frozen_time.tzinfo:
                    return self._frozen_time.astimezone(tz)
                return self._frozen_time
            return datetime.fromtimestamp(self.get_time(), tz=tz)


@contextmanager
def freeze_time(dt: Union[datetime, float, str]):
    """Context manager for temporary time control."""
    clock = MockClock()
    clock.freeze(dt)
    try:
        yield clock
    finally:
        clock.reset()
