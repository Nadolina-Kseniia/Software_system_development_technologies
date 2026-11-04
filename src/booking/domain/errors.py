class DomainError(Exception):
    """Base class for rule violations."""


class InvalidPeriod(DomainError):
    """The requested interval is not valid."""


class OutsideWorkingHours(DomainError):
    """The interval falls outside the hours."""


class BookingTooLong(DomainError):
    """The interval exceeds the allowed duration."""


class SeatAlreadyBooked(DomainError):
    """Another booking occupies the seat."""
