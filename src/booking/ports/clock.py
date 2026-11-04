from datetime import datetime
from typing import Protocol

from booking.domain.models import BookingId


class Clock(Protocol):
    def now(self) -> datetime: ...


class IdGenerator(Protocol):
    def next_id(self) -> BookingId: ...
