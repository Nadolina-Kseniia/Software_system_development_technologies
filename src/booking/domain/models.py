from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from typing import NewType

from booking.domain.errors import InvalidPeriod

BookingId = NewType("BookingId", str)
SeatId = NewType("SeatId", str)
UserId = NewType("UserId", str)


class SeatKind(StrEnum):
    DESK = "desk"
    MEETING_ROOM = "meeting_room"


def seat_kind_of(seat_id: SeatId) -> SeatKind:
    return SeatKind.MEETING_ROOM if seat_id.startswith("room") else SeatKind.DESK


@dataclass(frozen=True, slots=True)
class TimeRange:
    """A half-open interval [starts_at, ends_at)."""

    starts_at: datetime
    ends_at: datetime

    def __post_init__(self) -> None:
        if self.ends_at <= self.starts_at:
            raise InvalidPeriod("end must be after start")

    @property
    def duration(self) -> timedelta:
        return self.ends_at - self.starts_at

    def overlaps(self, other: "TimeRange") -> bool:
        return self.starts_at < other.ends_at and other.starts_at < self.ends_at


@dataclass(frozen=True, slots=True)
class BookingRequest:
    seat_id: SeatId
    user_id: UserId
    period: TimeRange


@dataclass(frozen=True, slots=True)
class Booking:
    id: BookingId
    seat_id: SeatId
    user_id: UserId
    period: TimeRange

    def conflicts_with(self, other: "Booking") -> bool:
        return self.seat_id == other.seat_id and self.period.overlaps(other.period)
