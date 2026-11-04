from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from booking.adapters.in_memory_repository import InMemoryBookingRepository
from booking.adapters.logging_notifier import LoggingNotifier
from booking.adapters.system_clock import SystemClock, UuidIdGenerator
from booking.config import Settings, get_settings
from booking.services.booking_service import BookingService
from booking.services.policies import policy_for


@lru_cache
def _repository() -> InMemoryBookingRepository:
    return InMemoryBookingRepository()


def get_booking_service(settings: Annotated[Settings, Depends(get_settings)]) -> BookingService:
    return BookingService(
        repository=_repository(),
        clock=SystemClock(),
        ids=UuidIdGenerator(),
        notifier=LoggingNotifier(),
        policy_for=policy_for,
    )
