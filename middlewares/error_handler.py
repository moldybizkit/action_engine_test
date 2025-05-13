import traceback
from aiohttp import ClientError
from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger

from errors.service_errors import (
    CityNotFoundError,
    ServiceError,
    UnexpectedError,
)


def service_error_handler(_request: Request, exc: ServiceError) -> JSONResponse:
    if isinstance(exc, CityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=exc.to_dict(),
        )
    if isinstance(exc, ClientError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=exc.to_dict(),
        )
    elif isinstance(exc, UnexpectedError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=exc.to_dict()
        )


def default_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    error_message = str(exc)
    formatted_traceback = traceback.format_exc()
    logger.error(f"{error_message}\n{formatted_traceback}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Unexpected error occurred"},
    )