"""
This program is free software: you can redistribute it under the terms
of the GNU General Public License, v. 3.0. If a copy of the GNU General
Public License was not distributed with this file, see <https://www.gnu.org/licenses/>.
"""

import datetime
import requests
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from data_retriever import get_summary
from response_models import SummaryResponse, ErrorResponse

router = APIRouter(prefix="/v1", tags=["API V1"])


def parse_date(date_str: str = None, default_days: int = 0) -> datetime.datetime:
    """
    Parse and validate the date string.
    """
    if not date_str:
        default_date = datetime.datetime.now() + datetime.timedelta(days=default_days)
        return default_date.strftime("%Y-%m-%d")

    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Date must be in the format 'YYYY-MM-DD', but got {date_str}"
            },
        ) from e


def get_security_headers() -> dict:
    """
    Return a dictionary of security headers.
    """
    return {
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "no-referrer-when-downgrade",
        "Content-Security-Policy": "default-src 'self';",
        "Permissions-Policy": "geolocation=(self)",
    }


@router.get(
    "/summary",
    response_model=SummaryResponse,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
def summary(
    start_date: str,
    end_date: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=10),
):
    """
    Fetch metrics summary.

    Args:
        page (int): Pagination page number.
        page_size (int): Number of items per page.
        start_date (datetime): Start date for filtering.
        end_date (datetime): End date for filtering.

    Returns:
        dict: Summary of metrics.
    """
    start_date = parse_date(start_date, default_days=0)
    end_date = parse_date(end_date, default_days=30)

    try:
        params = {
            "page": page,
            "page_size": page_size,
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
        }

        summary_data = get_summary(params)

        return JSONResponse(
            content=summary_data,
            headers=get_security_headers(),
        )
    except requests.HTTPError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e
