from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from booking.api.dependencies import get_booking_service
from booking.domain.errors import (
    BookingTooLong,
    InvalidPeriod,
    OutsideWorkingHours,
    SeatAlreadyBooked,
)
from booking.domain.models import BookingRequest, SeatId, TimeRange, UserId
from booking.services.booking_service import BookingService

router = APIRouter(tags=["bookings"])

_STATUS_BY_ERROR = {
    InvalidPeriod: 422,
    OutsideWorkingHours: 422,
    BookingTooLong: 422,
    SeatAlreadyBooked: 409,
}


class CreateBookingRequest(BaseModel):
    seat_id: str = Field(min_length=1, max_length=64)
    user_id: str = Field(min_length=1, max_length=64)
    starts_at: datetime
    ends_at: datetime


class BookingResponse(BaseModel):
    id: str
    seat_id: str
    user_id: str
    starts_at: datetime
    ends_at: datetime


@router.post("/bookings", status_code=201, response_model=BookingResponse)
async def create_booking(
    payload: CreateBookingRequest,
    service: Annotated[BookingService, Depends(get_booking_service)],
) -> BookingResponse:
    try:
        request = BookingRequest(
            seat_id=SeatId(payload.seat_id),
            user_id=UserId(payload.user_id),
            period=TimeRange(payload.starts_at, payload.ends_at),
        )
        booking = service.create(request)
    except tuple(_STATUS_BY_ERROR) as error:
        raise HTTPException(status_code=_STATUS_BY_ERROR[type(error)], detail=str(error)) from error

    return BookingResponse(
        id=booking.id,
        seat_id=booking.seat_id,
        user_id=booking.user_id,
        starts_at=booking.period.starts_at,
        ends_at=booking.period.ends_at,
    )
