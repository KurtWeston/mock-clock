"""Monkey-patching logic for system time functions."""

import datetime as dt_module
import time as time_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mock_clock.core import MockClock


class TimePatcher:
    """Handles patching and unpatching of time functions."""

    def __init__(self, clock: "MockClock"):
        self.clock = clock
        self._original_datetime_now = dt_module.datetime.now
        self._original_datetime_utcnow = dt_module.datetime.utcnow
        self._original_time = time_module.time
        self._original_monotonic = time_module.monotonic
        self._monotonic_start = time_module.monotonic()
        self._patched = False

    def start(self):
        """Apply patches to system time functions."""
        if self._patched:
            return

        dt_module.datetime.now = self._mock_datetime_now
        dt_module.datetime.utcnow = self._mock_datetime_utcnow
        time_module.time = self._mock_time
        time_module.monotonic = self._mock_monotonic
        self._patched = True

    def stop(self):
        """Restore original time functions."""
        if not self._patched:
            return

        dt_module.datetime.now = self._original_datetime_now
        dt_module.datetime.utcnow = self._original_datetime_utcnow
        time_module.time = self._original_time
        time_module.monotonic = self._original_monotonic
        self._patched = False

    def real_time(self) -> float:
        """Get real system time."""
        return self._original_time()

    def _mock_datetime_now(self, tz=None):
        """Mocked datetime.now()."""
        return self.clock.get_datetime(tz=tz)

    def _mock_datetime_utcnow(self):
        """Mocked datetime.utcnow()."""
        return self.clock.get_datetime(tz=dt_module.timezone.utc).replace(tzinfo=None)

    def _mock_time(self):
        """Mocked time.time()."""
        return self.clock.get_time()

    def _mock_monotonic(self):
        """Mocked time.monotonic()."""
        elapsed = self._original_monotonic() - self._monotonic_start
        return self.clock.get_time() - self._original_time() + elapsed
