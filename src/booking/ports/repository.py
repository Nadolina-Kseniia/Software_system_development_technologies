from typing import Protocol

from booking.domain.models import Booking, SeatId, TimeRange


class BookingRepository(Protocol):
    def add(self, booking: Booking) -> None: ...
    def find_overlapping(self, seat_id: SeatId, period: TimeRange) -> list[Booking]: ...
