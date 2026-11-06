"""Request-scoped logging context."""

import time
import uuid
from collections.abc import Awaitable, Callable

import structlog
from fastapi import Request, Response

REQUEST_ID_HEADER = "X-Request-Id"


async def request_context(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
    request.state.request_id = request_id

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
    )

    logger = structlog.get_logger()
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("request_failed", duration_ms=int((time.perf_counter() - started) * 1000))
        raise

    logger.info(
        "request_handled",
        status_code=response.status_code,
        duration_ms=int((time.perf_counter() - started) * 1000),
    )
    response.headers[REQUEST_ID_HEADER] = request_id
    return response
