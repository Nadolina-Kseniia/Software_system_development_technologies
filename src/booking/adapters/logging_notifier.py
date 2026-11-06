import structlog

from booking.domain.models import BookingId, UserId


class LoggingNotifier:
    def booking_created(self, user_id: UserId, booking_id: BookingId) -> None:
        structlog.get_logger().info(
            "booking_created_notified", user_id=user_id, booking_id=booking_id
        )
