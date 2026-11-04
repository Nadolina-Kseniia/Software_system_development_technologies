"""Structured logging setup."""

import logging
import sys

import structlog

from booking.config import Environment, LogLevel

_LEVELS: dict[LogLevel, int] = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}


def configure_logging(level: LogLevel, environment: Environment) -> None:
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=_LEVELS[level])

    processors: list[structlog.typing.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if environment == "development":
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    else:
        processors.append(structlog.processors.JSONRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(_LEVELS[level]),
        logger_factory=structlog.PrintLoggerFactory(sys.stdout),
        cache_logger_on_first_use=True,
    )
