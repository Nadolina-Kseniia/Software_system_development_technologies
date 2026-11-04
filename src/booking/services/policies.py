from datetime import time, timedelta

from booking.domain.models import SeatKind
from booking.domain.rules import WorkingHours


class BookingPolicy:
    def __init__(
        self,
        working_hours: WorkingHours,
        max_duration: timedelta,
        min_advance: timedelta = timedelta(0),
    ):
        self.working_hours = working_hours
        self.max_duration = max_duration
        self.min_advance = min_advance


DESK_POLICY = BookingPolicy(WorkingHours(), timedelta(hours=8))
MEETING_ROOM_POLICY = BookingPolicy(
    WorkingHours(time(9), time(20)), timedelta(hours=3), timedelta(hours=1)
)

_POLICY_BY_KIND = {
    SeatKind.DESK: DESK_POLICY,
    SeatKind.MEETING_ROOM: MEETING_ROOM_POLICY,
}


def policy_for(kind: SeatKind) -> BookingPolicy:
    return _POLICY_BY_KIND[kind]
