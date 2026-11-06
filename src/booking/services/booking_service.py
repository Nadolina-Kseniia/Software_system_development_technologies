from collections.abc import Callable

import structlog

from booking.domain import rules
from booking.domain.errors import SeatAlreadyBooked
from booking.domain.models import Booking, BookingRequest, SeatKind, seat_kind_of
from booking.ports.clock import Clock, IdGenerator
from booking.ports.notifier import Notifier
from booking.ports.repository import BookingRepository
from booking.services.policies import BookingPolicy

PolicyFor = Callable[[SeatKind], BookingPolicy]


class BookingService:
    def __init__(
        self,
        repository: BookingRepository,
        clock: Clock,
        ids: IdGenerator,
        notifier: Notifier,
        policy_for: PolicyFor,
    ):
        self._repository = repository
        self._clock = clock
        self._ids = ids
        self._notifier = notifier
        self._policy_for = policy_for

    def create(self, request: BookingRequest) -> Booking:
        policy = self._policy_for(seat_kind_of(request.seat_id))
        now = self._clock.now()

        rules.require_valid_period(request)
        rules.require_within_working_hours(request, policy.working_hours)
        rules.require_duration_at_most(request, policy.max_duration)
        rules.require_not_in_past(request, now)
        rules.require_advance_notice(request, now, policy.min_advance)

        conflicts = self._repository.find_overlapping(request.seat_id, request.period)
        if conflicts:
            raise SeatAlreadyBooked(f"seat {request.seat_id} is taken")

        booking = Booking(
            id=self._ids.next_id(),
            seat_id=request.seat_id,
            user_id=request.user_id,
            period=request.period,
        )
        self._repository.add(booking)
        self._notifier.booking_created(booking.user_id, booking.id)

        structlog.get_logger().info("booking_created", booking_id=booking.id)
        return booking
