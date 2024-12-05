"""
This program is free software: you can redistribute it under the terms
of the GNU General Public License, v. 3.0. If a copy of the GNU General
Public License was not distributed with this file, see <https://www.gnu.org/licenses/>.
"""

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api_v1 import router as api_v1_router
from logutils import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="RelaySMS Telemetry API",
    description=(
        "Collects, analyzes, and exposes RelaySMS "
        "usage data for transparent telemetry insights."
    ),
    redoc_url=None,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


@app.exception_handler(HTTPException)
def http_exception_handler(_, exc: HTTPException):
    logger.error(exc.detail)
    return JSONResponse(exc.detail, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(_, exc: RequestValidationError):
    first_error = exc.errors()[0]
    field = " ".join(str(loc) for loc in first_error["loc"])
    message = first_error.get("msg", "Invalid input")
    error_message = f"{field}, {message}"

    logger.error(error_message)
    return JSONResponse({"error": error_message}, status_code=400)


@app.exception_handler(Exception)
def internal_exception_handler(_, exc: Exception):
    logger.exception(exc)
    return JSONResponse(
        {"error": "Oops! Something went wrong. Please try again later."},
        status_code=500,
    )


app.include_router(api_v1_router)
