from datetime import UTC, datetime
from uuid import uuid4

from booking.domain.models import BookingId


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


class UuidIdGenerator:
    def next_id(self) -> BookingId:
        return BookingId(str(uuid4()))
