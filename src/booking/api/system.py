"""System endpoints: liveness and version."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from booking.config import Settings, get_settings

router = APIRouter(tags=["system"])


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


class VersionResponse(BaseModel):
    version: str = Field(examples=["1.2.3"])
    environment: str = Field(examples=["production"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse()


@router.get("/version", response_model=VersionResponse)
async def version(
    settings: Annotated[Settings, Depends(get_settings)],
) -> VersionResponse:
    return VersionResponse(version=settings.app_version, environment=settings.environment)
