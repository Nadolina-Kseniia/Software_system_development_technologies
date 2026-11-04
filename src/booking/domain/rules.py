from dataclasses import dataclass
from datetime import datetime, time, timedelta

from booking.domain.errors import BookingTooLong, InvalidPeriod, OutsideWorkingHours
from booking.domain.models import BookingRequest

DEFAULT_OPENS_AT = time(8, 0)
DEFAULT_CLOSES_AT = time(22, 0)
DEFAULT_MAX_DURATION = timedelta(hours=8)
DEFAULT_MIN_DURATION = timedelta(minutes=30)


@dataclass(frozen=True, slots=True)
class WorkingHours:
    opens_at: time = DEFAULT_OPENS_AT
    closes_at: time = DEFAULT_CLOSES_AT

    def contains(self, moment: datetime) -> bool:
        return self.opens_at <= moment.timetz().replace(tzinfo=None) <= self.closes_at


def require_valid_period(request: BookingRequest) -> None:
    if request.period.duration < DEFAULT_MIN_DURATION:
        raise InvalidPeriod("booking is shorter than the minimum slot")


def require_within_working_hours(request: BookingRequest, hours: WorkingHours) -> None:
    if not hours.contains(request.period.starts_at) or not hours.contains(request.period.ends_at):
        raise OutsideWorkingHours("outside working hours")


def require_duration_at_most(request: BookingRequest, limit: timedelta) -> None:
    if request.period.duration > limit:
        raise BookingTooLong(f"duration exceeds {limit}")


def require_not_in_past(request: BookingRequest, now: datetime) -> None:
    if request.period.starts_at < now:
        raise InvalidPeriod("booking starts in the past")


def require_advance_notice(request: BookingRequest, now: datetime, notice: timedelta) -> None:
    if request.period.starts_at - now < notice:
        raise InvalidPeriod(f"booking must be made at least {notice} in advance")
