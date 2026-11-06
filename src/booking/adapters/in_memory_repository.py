from booking.domain.models import Booking, SeatId, TimeRange


class InMemoryBookingRepository:
    def __init__(self) -> None:
        self._bookings: list[Booking] = []

    def add(self, booking: Booking) -> None:
        self._bookings.append(booking)

    def find_overlapping(self, seat_id: SeatId, period: TimeRange) -> list[Booking]:
        return [
            existing
            for existing in self._bookings
            if existing.seat_id == seat_id and existing.period.overlaps(period)
        ]
