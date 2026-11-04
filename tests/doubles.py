from datetime import datetime

from booking.domain.models import BookingId, UserId


class FixedClock:
    def __init__(self, moment: datetime) -> None:
        self._moment = moment

    def now(self) -> datetime:
        return self._moment


class SequentialIds:
    def __init__(self) -> None:
        self._counter = 0

    def next_id(self) -> BookingId:
        self._counter += 1
        return BookingId(f"b-{self._counter}")


class SpyNotifier:
    def __init__(self) -> None:
        self.notified: list[tuple[UserId, BookingId]] = []

    def booking_created(self, user_id: UserId, booking_id: BookingId) -> None:
        self.notified.append((user_id, booking_id))
