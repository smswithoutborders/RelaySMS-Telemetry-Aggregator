"""
This program is free software: you can redistribute it under the terms
of the GNU General Public License, v. 3.0. If a copy of the GNU General
Public License was not distributed with this file, see <https://www.gnu.org/licenses/>.
"""

from typing import Annotated

import requests
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from api_data_schemas import (
    ErrorResponse,
    MetricsParams,
    PublicationsParams,
    PublicationsResponse,
    RetainedResponse,
    SignupResponse,
    SummaryParams,
    SummaryResponse,
)
from data_retriever import get_publications, get_retained, get_signup, get_summary

router = APIRouter(prefix="/v1", tags=["API V1"])


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
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
    }


@router.get(
    "/summary",
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    response_model=SummaryResponse,
)
def summary(query: Annotated[SummaryParams, Query()]) -> SummaryResponse:
    """Fetch metrics summary."""

    try:
        params = {
            "start_date": query.start_date,
            "end_date": query.end_date,
            "country_code": query.country_code,
            "type": query.type,
            "origin": query.origin,
        }

        summary_data = get_summary(params)

        response_data = {"summary": summary_data}

        return JSONResponse(content=response_data, headers=get_security_headers())
    except requests.HTTPError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.get(
    "/signup",
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    response_model=SignupResponse,
)
def signup(query: Annotated[MetricsParams, Query()]) -> SignupResponse:
    """Fetch signup users metrics."""

    try:
        params = {
            "start_date": query.start_date,
            "end_date": query.end_date,
            "country_code": query.country_code,
            "granularity": query.granularity,
            "group_by": query.group_by,
            "top": query.top,
            "page": query.page,
            "page_size": query.page_size,
            "type": query.type,
            "origin": query.origin,
        }

        signup_data = get_signup(params)

        response_data = {"signup": signup_data}

        return JSONResponse(content=response_data, headers=get_security_headers())
    except requests.HTTPError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.get(
    "/retained",
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    response_model=RetainedResponse,
)
def retained(query: Annotated[MetricsParams, Query()]) -> RetainedResponse:
    """Fetch retained users metrics."""

    try:
        params = {
            "start_date": query.start_date,
            "end_date": query.end_date,
            "country_code": query.country_code,
            "granularity": query.granularity,
            "group_by": query.group_by,
            "top": query.top,
            "page": query.page,
            "page_size": query.page_size,
            "type": query.type,
            "origin": query.origin,
        }

        retained_data = get_retained(params)

        response_data = {"retained": retained_data}

        return JSONResponse(content=response_data, headers=get_security_headers())
    except requests.HTTPError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e


@router.get(
    "/publications",
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    response_model=PublicationsResponse,
)
def publications(query: Annotated[PublicationsParams, Query()]):
    """Fetch publication metrics."""

    try:
        params = {
            "start_date": query.start_date,
            "end_date": query.end_date,
            "country_code": query.country_code,
            "platform_name": query.platform_name,
            "source": query.source,
            "status": query.status,
            "gateway_client": query.gateway_client,
            "page": query.page,
            "page_size": query.page_size,
        }

        publications_data = get_publications(params)

        response_data = {"publications": publications_data}

        return JSONResponse(content=response_data, headers=get_security_headers())
    except requests.HTTPError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=e.response.json()
        ) from e

