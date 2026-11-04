from typing import Protocol

from booking.domain.models import BookingId, UserId


class Notifier(Protocol):
    def booking_created(self, user_id: UserId, booking_id: BookingId) -> None: ...
