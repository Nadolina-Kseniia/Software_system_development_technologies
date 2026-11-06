from datetime import UTC, datetime, timedelta

import pytest

from booking.adapters.in_memory_repository import InMemoryBookingRepository
from booking.domain.errors import SeatAlreadyBooked
from booking.domain.models import BookingRequest, SeatId, TimeRange, UserId
from booking.services.booking_service import BookingService
from booking.services.policies import policy_for
from tests.doubles import FixedClock, SequentialIds, SpyNotifier

NOW = datetime(2030, 10, 14, 8, 0, tzinfo=UTC)


def _request(hour: int = 9, hours: int = 3) -> BookingRequest:
    start = NOW.replace(hour=hour)
    return BookingRequest(
        SeatId("desk-1"), UserId("u-1"), TimeRange(start, start + timedelta(hours=hours))
    )


@pytest.fixture
def service():
    notifier = SpyNotifier()
    return (
        BookingService(
            repository=InMemoryBookingRepository(),
            clock=FixedClock(NOW),
            ids=SequentialIds(),
            notifier=notifier,
            policy_for=policy_for,
        ),
        notifier,
    )


def test_booking_gets_a_generated_id(service) -> None:
    svc, _ = service
    assert svc.create(_request()).id == "b-1"


def test_second_booking_on_the_same_seat_is_rejected(service) -> None:
    svc, _ = service
    svc.create(_request(hour=9, hours=3))
    with pytest.raises(SeatAlreadyBooked):
        svc.create(_request(hour=10, hours=1))


def test_user_is_notified(service) -> None:
    svc, notifier = service
    booking = svc.create(_request())
    assert notifier.notified == [(booking.user_id, booking.id)]
