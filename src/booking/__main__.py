"""Entry point: python -m booking."""

import uvicorn

from booking.config import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "booking.app:create_app",
        factory=True,
        host="0.0.0.0",
        port=settings.port,
        log_config=None,
    )


if __name__ == "__main__":
    main()
